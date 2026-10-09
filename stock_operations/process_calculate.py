from multiprocessing import Process, Value, Lock, Barrier
import time


class MyBarrier3(Process):
    def __init__(self, data: Value, lock: Lock, barrier: Barrier):
        super().__init__()
        # Store references to shared IPC objects
        self.data = data
        self.lock = lock
        self.barrier = barrier

    def calculate(self):
        local = 0
        for _ in range(50000000):
            local += 1

        # Safely update shared memory across processes
        with self.lock:
            self.data.value += local

    def run(self):
        self.calculate()
        # Use an IPC Barrier instead of busy-waiting on class variables
        self.barrier.wait()



if __name__ == "__main__":
    num_workers = 2
    # 1. Instantiate IPC synchronization and shared state
    shared_data = Value('i', 0)
    shared_lock = Lock()
    shared_barrier = Barrier(num_workers)

    workers = [MyBarrier3(shared_data, shared_lock, shared_barrier) for _ in range(num_workers)]

    sta = time.time()

    for w in workers:
        w.start()
    for w in workers:
        w.join()

    end = time.time()

    print(f"Final Shared Data: {shared_data.value}")
    print(f"Total Time: {end - sta:.6f} seconds")