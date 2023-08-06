# -*- coding: utf8 -*-
class MLDataGenerator(object):
    def __init__(self, volume_id, query, data_callback, cache_directory=None, batch_size=32, use_threads=None, processes=-1, shuffle=True, cache_limit=None):
        self.__volume_id = volume_id
        self.__query = query
        self.__data_callback = data_callback
        self.__batch_size = batch_size
        self.__use_threads = use_threads
        self.__processes = processes
        self.__shuffle = shuffle
        self.__cache_directory = cache_directory
        self.__cache_limit = cache_limit

    def __yield_single_query(self):
        yield self.__query

    @classmethod
    def __yield_phase_queries(cls, tree, split_visitor):
        from missinglink.legit.scam import AddPhaseFunction
        from missinglink.legit.scam import resolve_tree

        def wrap():
            for phase in ['train', 'test', 'validation']:
                if not split_visitor.has_phase(phase):
                    continue

                resolved_tree = resolve_tree(tree, AddPhaseFunction(phase))

                yield str(resolved_tree)

        return wrap

    def flow(self):
        from missinglink.legit.scam import QueryParser, visit_query
        from .query_data_generator import QueryDataGeneratorFactory
        from missinglink.legit.scam import SplitVisitor, SeedVisitor

        tree = QueryParser().parse_query(self.__query)

        split_visitor = visit_query(SplitVisitor, tree)
        seed_visitor = visit_query(SeedVisitor, tree)

        factory = QueryDataGeneratorFactory(
            self.__processes, self.__use_threads,
            self.__cache_directory, self.__cache_limit, self.__data_callback,
            self.__volume_id, self.__batch_size, self.__shuffle, seed_visitor.seed)

        query_gen = self.__yield_phase_queries(tree, split_visitor) if getattr(split_visitor, 'has_split', True) else self.__yield_single_query

        iters = []
        for query in query_gen():
            query_iter = factory.create(query)

            iters.append(query_iter)

        return iters if len(iters) > 1 else iters[0]
