from settings import *
from typing import Callable

class Timer: #? Type annotations so I don't accidentally mess shit up 
    def __init__(self, duration, func: Callable = None, repeat: bool = None, autostart: bool = False):
        self.duration = duration
        self.start_time = 0
        self.active = False
        self.func = func
        self.repeat = repeat

        if autostart:
            self.activate()

    def __bool__(self): #? runs if timer is put in an if statement
        return self.active


    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0
        if self.repeat:
            self.activate() #? Never deactivates

    def update(self):
        if pygame.time.get_ticks() - self.start_time >= self.duration:
            if self.func and self.start_time != 0:
                self.func()
            self.deactivate()