from threading import Thread
import time

class PrintA(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True

    def run(self):
        while self.running:
            print('A')
            time.sleep(1)
    def stop(self):
        self.running = False

class PrintB(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
    def run(self):
        while self.running:
            print('B')
            time.sleep(2)
    def stop(self):
        self.running = False

a = PrintA()
b = PrintB()

a.start()
b.start()

time.sleep(10)
a.stop()
time.sleep(10)
b.stop()