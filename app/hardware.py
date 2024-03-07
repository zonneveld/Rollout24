
# from threading import Thread
import threading
from time import sleep

verbose = True

def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

import sys
if sys.platform == 'win32':
    def write_to_channel(index,value,scale_range):
        _min,_max = scale_range
        scale = int(map_range(value,_min,_max,0,0xffff))
        if verbose:
            print(f'{index}->{value}({hex(scale)})')
else:
    from board import SCL, SDA
    import busio
    # Import the PCA9685 module.
    from adafruit_pca9685 import PCA9685
    i2c_bus = busio.I2C(SCL, SDA)
    pca = PCA9685(i2c_bus)
    pca.frequency = 60
    def write_to_channel(index,value,scale_range):
        _min,_max = scale_range
        scale = int(map_range(value,_min,_max,0,0xffff))
        pca[index].duty_cycle = scale
    # pca.channels[0].duty_cycle = 0x7FFF



# from typing import Iterable, Mapping



TARGET = "target"
ACTION = "action"
VALUE = "value"
SPEED = "speed"
CHANNEL= "channel"

SERVO = (0,180)
MOTOR = (0.0,1.0)

UPDATE_INTERFALL = 0.01

class TaskMaster():
    class TaskTicker(threading.Thread):
        def __init__(self):
            self.active = threading.Event()
            self.active.set()
            self.interval = UPDATE_INTERFALL
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
        self.ticker = TaskMaster.TaskTicker()
        self.ticker.callback = self.update_channels
        self.channels = {}
        self.channels['servo_1'] = Channel(0,SERVO)
        self.channels['servo_2'] = Channel(1,SERVO)
        
        # pass

    def update_channels(self):
        # print("update channels!")
        for channel_handles in self.channels:
            # print(channel_handles)
            self.channels[channel_handles].update()

    def start(self):
        # self.ticker.interval = 0.1
        self.ticker.start()


    def stop(self):
        self.ticker.stop()

    def add_task(self, data):
        print(data)

        # if data[TARGET] == "servo_1":
        #     index = 1
        #     value = data[VALUE]
        #     speed = data[SPEED]
        #     self.action_servo_absolute(index,value,speed)
        if data[ACTION] == 'move_servo_absolute':
            channel = data[CHANNEL]
            target = data[TARGET]
            speed  = data[SPEED]
            if channel in self.channels:
                self.move_serv_absolute(channel,target,speed)
        elif data[ACTION] == 'move_servo_relative':
            channel = data[CHANNEL]
            target = data[TARGET]
            speed  = data[SPEED]
            if channel in self.channels:
                self.move_serv_relative(channel,target,speed)

        else:
            print("wrong json command")
            pass
    
    def move_serv_absolute(self,channel,target,speed):
        _min, _max = SERVO
        
        target = target if target >= _min else _min
        target = target if target <= _max else _max

        self.channels[channel].target = target
        self.channels[channel].speed = speed
    
    def move_serv_relative(self,channel,target,speed):
        _min, _max = SERVO
        
        target += self.channels[channel].target

        target = target if target >= _min else _min
        target = target if target <= _max else _max

        self.channels[channel].target = target
        self.channels[channel].speed = speed
    
    def move_serv_now(self,channel,target):
        pass

class Channel():
    def __init__(self,index,scale_range) -> None:
        self.index = index
        self.postition = 0
        self.speed = 1
        self.target = 0
        self.scale_range = scale_range

    def update(self):
        # print(self.index)
        distance = abs(self.postition - self.target)
        if self.postition == self.target:
            return True
        
        elif self.postition > self.target:
            self.postition -= (self.speed if distance >= self.speed  else distance )
            
        elif self.postition < self.target:
            self.postition += (self.speed if distance >= self.speed  else distance )
        
        self.write()
        # print(self.postition)
        return False
    
    def travel(self):
        self.postition = self.target

    def write(self):
        write_to_channel(self.index,self.postition,self.scale_range)
    
    def read(self):
        return self.postition
    


if __name__ == "__main__":
    # channel = Channel()
    taskMaster = TaskMaster()
    taskMaster.start()
    command = input()
    while command != "exit":
        try:
            taskMaster.channels['servo_1'].target = int(command)
            # pass
            # print(5 + int(command))
        except:
            pass
        command = input()
    taskMaster.stop()
    # taskMaster = TaskMaster()
    # taskMaster.start()
    # sleep(10)
    # taskMaster.stop()
    # print("done!")