
# from threading import Thread
import threading
from time import sleep

import json
from typing import Iterable, Mapping

TARGET = "target"
ACTION = "action"
VALUE = "value"
SPEED = "speed"

class TaskMaster():
    class TaskTicker(threading.Thread):
        def __init__(self):
            self.active = threading.Event()
            self.active.set()
            self.interval = 1
            self.callback = lambda : None
            super().__init__()

        def run(self):
            while self.active.is_set():
                # print("callback!")
                self.callback()
                sleep(self.interval)
        
        def start(self):
            super().start()

        def stop(self):
            self.active.clear()
    


    def __init__(self):
        self.hardware = HardWare()
        self.ticker = TaskMaster.TaskTicker()
        # pass

    def action_servo_absolute(self, index, value,speed):
        print(f'{index} {value}: {speed}')
        pass
    
    def start(self):
        self.hardware.start()
        self.ticker.callback = self.hardware.update
        self.ticker.interval = 1
        self.ticker.start()


    def stop(self):
        self.ticker.stop()

    def add_task(self, data):
        print(data)

        if data[TARGET] == "Servo_1":
            index = 1
            value = data[VALUE]
            speed = data[SPEED]
            self.action_servo_absolute(index,value,speed)
        else:
            print("wrong json command")
            pass
    
    def interped_command(self,msg):
        pass
    
class Channel():
    def write(self):
        pass
    
    def read(self):
        pass
    
    

class HardWare():
    # 16 channels
    def __init__(self) -> None:
        pass

    def update(self):
        print("update!")
        # pass

    def start(self):
        pass

    def set(self):
        pass

if __name__ == "__main__":
    taskMaster = TaskMaster()
    taskMaster.start()
    sleep(10)
    taskMaster.stop()
    print("done!")