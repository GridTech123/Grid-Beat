import pygame 
from pygame import *
from pygame.locals import *

def play(path):
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(0, 0.0)

def pause():
    pygame.mixer.music.pause()

def unpause():
    pygame.mixer.music.unpause()

def stop():
    pygame.mixer.music.stop()      