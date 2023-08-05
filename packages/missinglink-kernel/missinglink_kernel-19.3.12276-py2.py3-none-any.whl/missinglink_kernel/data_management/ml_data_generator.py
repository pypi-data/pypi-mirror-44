# -*- coding: utf8 -*-
import os


class MLDataGenerator(object):
    def __init__(self, volume_id, query, data_callback, cache_directory=None, batch_size=32, use_threads=None, processes=-1, shuffle=True, cache_limit=None):
        self.__volume_id = volume_id
        self.__query = query
        self.__data_callback = data_callback
        self.__batch_size = batch_size
        self.__use_threads = use_threads
        self.__processes = processes
        self.__storage = self.__create_cache_storage(cache_directory, cache_limit)
        self.__shuffle = shuffle

    @classmethod
    def __create_cache_storage(cls, cache_directory, cache_limit):
        from .cache_storage import CacheStorage

        cache_directory = cache_directory or os.environ.get('ML_CACHE_FOLDER', './ml_cache')

        return CacheStorage(cache_directory, cache_limit)

    def flow(self):
        from missinglink.legit.scam import QueryParser, visit_query, resolve_tree
        from missinglink.core.multi_process_control import get_multi_process_control
        from .query_data_generator import QueryDataGeneratorFactory
        from missinglink.legit.scam import SplitVisitor, SeedVisitor, AddPhaseFunction

        tree = QueryParser().parse_query(self.__query)

        split_visitor = visit_query(SplitVisitor, tree)
        seed_visitor = visit_query(SeedVisitor, tree)

        multi_process_control = get_multi_process_control(self.__processes, use_threads=self.__use_threads)

        factory = QueryDataGeneratorFactory(
            multi_process_control, self.__storage, self.__data_callback,
            self.__volume_id, self.__batch_size, self.__shuffle, seed_visitor.seed)

        iters = []
        ctx = None
        for phase in ['train', 'test', 'validation']:
            if not split_visitor.has_phase(phase):
                continue

            resolved_tree = resolve_tree(tree, AddPhaseFunction(phase))

            query = str(resolved_tree)

            query_iter = factory.create(query, ctx=ctx)

            iters.append(query_iter)

            ctx = query_iter.ctx

        return iters if len(iters) > 1 else iters[0]
