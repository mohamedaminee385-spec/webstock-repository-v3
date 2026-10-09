from threading import Thread, Barrier
from .models import Device


class Awaitable:

    def __init__(self):
        self.is_below = False
        self.laptop = False
        self.desktop = False
        self.printer = False
        self.scanner = False
        self.monitor = False
        self.msg = ""

    def waiter(self):
        while not self.is_below:
            if Device.objects.get(name="Laptop").stock_number <= 70:
                self.laptop = True
                #self.is_below = True
            if Device.objects.get(name="Desktop").stock_number <= 70:
                self.desktop = True
                #self.is_below = True
            if Device.objects.get(name="Printer").stock_number <= 100:
                self.printer = True
                #self.is_below = True
            if Device.objects.get(name="Scanner").stock_number <= 100:
                self.scanner = True
                #self.is_below = True
            if Device.objects.get(name="Monitor").stock_number <= 30:
                self.monitor = True
            if self.laptop == True or self.desktop == True or self.printer == True or self.scanner == True or self.monitor == True:
                self.is_below = True
                #self.is_below = True
        #return "The stock of Laptops is almost used"

        if self.laptop:
            self.msg = self.msg + "<strong>Warning:</strong> The stock of Laptops is almost used <br>"
        if self.desktop:
            self.msg = self.msg + "<strong>Warning:</strong> The stock of Desktops is almost used <br>"
        if self.printer:
            self.msg = self.msg + "<strong>Warning:</strong> The stock of Printers is almost used <br>"
        if self.scanner:
            self.msg = self.msg + "<strong>Warning:</strong> The stock of Scanners is almost used <br>"
        if self.monitor:
            self.msg = self.msg + "<strong>Warning:</strong> The stock of Monitors is almost used <br>"

        return self.msg


class MyBarrier(Thread):

    def __init__(self):
        super(Thread, self).__init__()
        self.counter = 3

    def task1(self):
        self.counter -= 1
        print("task1")

    def task2(self):
        self.counter -= 1
        print("task2")

    def task(self):
        self.counter -= 1
        print("task3")

    def run(self):
        while(self.counter != 0):
            pass
        self.task4()

    def task4(self):
        print("task4")


