import pygame
from os import walk
from os.path import join
from pytmx.util_pygame import load_pygame

#* Constants fo da game
#* These type annotations are not needed but i did it anyways for fun
WINDOW_WIDTH: int; WINDOW_HEIGHT: int
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TILE_SIZE: int = 64 
FRAMERATE:int  = 60
BG_COLOR: hex = '#fcdfcd'