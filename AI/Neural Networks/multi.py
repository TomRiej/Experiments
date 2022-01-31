from multiprocessing import Pool


class ParallelEvaluator(object):
    def __init__(self, num_workers, eval_function, timeout=None):
        self.num_workers = num_workers
        self.eval_function = eval_function
        self.timeout = timeout
        self.pool = Pool(num_workers)

    def __del__(self):
        self.pool.close() # should this be terminate?
        self.pool.join()

    def evaluate(self, nets):
        jobs = []
        for net in nets:
            jobs.append(self.pool.apply_async(self.eval_function, nets))

        # assign the fitness back to each genome
        for job, net in zip(jobs, nets):
            net.score = job.get(timeout=self.timeout)