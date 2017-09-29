import display
import pygame
import random

d = display.Display()
fnt_name = '/home/sementsov/proj/yac/DejaVuSansMono-Bold.ttf'
fnt = pygame.font.Font(fnt_name, 16)

while d.is_running:
    for i in range(30):
        txt = fnt.render('Hoolaaaa.... AAAAAaAAAaaaaaAAAAAAAAAAAaAaaAAAAAA', True, (255, random.randrange(255), random.randrange(255)))
        d.screen.blit(txt, (0, i * 20))
#        d.prn('Hoolaaaa.... AAAAAaAAAaaaaaAAAAAAAAAAAaAaaAAAAAA', 0, i, win=d.stdscr)

    key = d.input()

