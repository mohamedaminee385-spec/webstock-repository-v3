from threading import Thread, Lock
import time
import os

class MyBarrier2(Thread):
    counter = 1
    data = 0
    B = True
    lock = Lock()
    b = True
    sta = 0.0
    end = 0.0

    def __init__(self):
        super().__init__()

    def calculate(self):
        local = 0
        for i in range(2000000):
            local += 1
            #with MyBarrier2.lock:
        with MyBarrier2.lock:
            MyBarrier2.data += local
        MyBarrier2.counter -= 1

    def run(self):
        self.calculate()
        while MyBarrier2.counter != 0:
            pass
        if MyBarrier2.B:
            MyBarrier2.B = False
            print(MyBarrier2.data)
            MyBarrier2.end = time.time()
            print(MyBarrier2.end - MyBarrier2.sta)

# 9.608694076538086

if __name__ == "__main__":
    threads = [MyBarrier2() for i in range(1)]
    MyBarrier2.sta = time.time()
    for t in threads:
        t.start()
    #MyBarrier2.end = time.time()

