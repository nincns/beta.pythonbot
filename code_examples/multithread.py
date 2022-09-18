from multiprocessing import Process

def methodA():
    while TRUE:
        do something

def methodB():
    while TRUE:
        do something

p=Process(target=methodA())
p.start()
p1=Process(target=methodB())
p1.start()