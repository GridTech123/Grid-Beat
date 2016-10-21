import pygame 
from pygame import *
from pygame.locals import *

def hover(screen, text, color1, color2, x, y, font, sx):
    if x < sx / 2:
        pygame.draw.rect(screen, color1, [x, y, len(text) * 10, 40])
        screen.blit(font.render(text, True, color2), (x, y))
    else:
        pygame.draw.rect(screen, color1, [x - len(text) * 10, y, len(text) * 10, 40])
        screen.blit(font.render(text, True, color2), (x - len(text) * 10, y))