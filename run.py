import multiprocessing

def startJarvis():
    #code for process 1
    print("process 1 is running...")
    from main import start
    start()

#to run hotword
def listenHotWord():
    #code for process 2
    print("process 2 is running...")
    from engine.features import hotword
    hotword()

#start both processsec
if __name__ == '__main__':
    p1 = multiprocessing.Process(target = startJarvis)
    p2 = multiprocessing.Process(target = listenHotWord)
    p1.start()
    p2.start()
    p1.join()

    if p2.is_alive():
        p2.terminate()
        p2.join()

    print("JARVIS STOP")
