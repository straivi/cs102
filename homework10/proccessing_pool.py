import multiprocessing
import random
import time
import numpy
import psutil


def heavy_computation(data_chunk):
    # Matrix calculation
    M = 1100
    a = numpy.array([[random.randint(M * (-data_chunk), M * data_chunk)
                      for _ in range(M)] for _ in range(M)])
    b = numpy.array([[random.randint(M * (-data_chunk), M * data_chunk)
                      for _ in range(M)] for _ in range(M)])
    c = numpy.array([[random.randint(M * (-data_chunk), M * data_chunk)
                      for _ in range(M)] for _ in range(M)])
    x = a * b * c
    return x

class ProcessPool:
    def __init__(self, min_workers=2, max_workers=50, memory_usage='1GB'):
        self.memory_usage = memory_to_int(memory_usage)
        self.fact_memory_usage = 0
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.avg_workers = 0
        self.memory_queue = multiprocessing.Queue()

    def map(self, computations, data):
        t_p = multiprocessing.Process(target=computations, name='test process', args=(data.get(),))
        t_p.start()

        t_m = multiprocessing.Process(target=self.memory_test, name='test memory', args=(t_p.pid,))
        t_m.start()

        t_p.join()
        t_m.join()
        mem_list = []

        while not self.memory_queue.empty():
            m = self.memory_queue.get()
            mem_list.append(m)
        self.fact_memory_usage = max(mem_list)

        print(f'Max memory used in tests:    {self.fact_memory_usage * 1024}MB')
        print(f'Memory avaliable for pools:  {self.memory_usage * 1024}MB')

        if self.fact_memory_usage > self.memory_usage:
            raise Warning('Memory level is too low even for one process!')
        else:
            print('> Memory usage test verdict: OK')

        self.avg_workers = int(self.memory_usage // self.fact_memory_usage)
        if self.avg_workers > self.max_workers:
            self.avg_workers = self.max_workers
        elif self.avg_workers < self.min_workers:
            raise Warning('Memory level is too low even for minimum workers number!')
        else:
            self.avg_workers = int(self.memory_usage // self.fact_memory_usage)
        process_list = []
        for process_number in range(self.avg_workers):
            if not data.empty():
                process = multiprocessing.Process(target=computations, args=(data.get(),))
                process.start()
                process_list.append(process)
            else:
                for pp in process_list:
                    pp.join()
                return self.avg_workers, self.fact_memory_usage

        while True:
            for process in process_list:
                process.join(0.001)
                if not process.is_alive():
                    process.terminate()
                    if not data.empty():
                        process_list.remove(process)
                        pp = multiprocessing.Process(target=computations,
                                                     args=(data.get(),))
                        pp.start()
                        process_list.append(pp)
                    else:
                        for pp in process_list:
                            pp.join()
                        return self.avg_workers, self.fact_memory_usage

    def memory_test(self, pid):
        p_mem = psutil.Process(pid)
        while psutil.pid_exists(pid):
            try:
                self.memory_queue.put(p_mem.memory_info().rss // 1000000 / 1000)
            except:
                pass
            time.sleep(0.01)

def memory_to_int(memory_usage):
    m = memory_usage.upper()
    try:
        size = int(m)
        return size
    except Exception:
        if not m[-2:-1].isdigit():
            size = int(m[:-2])
            units = m[-2:]
            units_dict = {
                'GB': 1,
                'MB': 1024,
                'KB': 1024 * 1024,
            }
            size = size / units_dict[units]
        else:
            size = int(m[:-1]) / 1024 ** 3
        return round(size, 3)

if __name__ == '__main__':
    queue = multiprocessing.Queue()
    for i in range(10):
        queue.put(i * 100)

    pool = ProcessPool()
    print(pool.map(heavy_computation, queue))
