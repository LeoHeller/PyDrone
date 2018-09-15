import threading

class myThread (threading.Thread):
    def __init__(self, arg1, arg2):
        threading.Thread.__init__(self)
        self.arg1 = arg1
        self.arg2 = arg2

    def run(self):
        while True:
            self.do_something()
        
    def do_something(self):
        print(self.arg1)

t = myThread("1", "2").start()