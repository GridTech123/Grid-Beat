import pygame 
from pygame import *
from pygame.locals import *
import random
import sys
import pickle
import time
import os
import pyError
import hovering
import player
from Tkinter import *
from tkFileDialog import*
import ntpath

#colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
blue2 = (44, 157, 201)
blue3 = (8, 140, 196)
blue4 = (40, 181, 166)
blue5 = (1, 142, 203)
red = (255, 0, 0)
green = (0, 255, 0)
green2 = (0, 153, 0)
green3 = (0,100,0)
gray = (158, 156, 166)
gray2 = (69, 67, 68)

#images
os.chdir('images')
musicImg = pygame.image.load('music.png')
musicHoverImg = pygame.image.load('musicHover.png')
newSongImg = pygame.image.load('newSong.png')
newSongHoverImg = pygame.image.load('newSongHover.png')
noPicImg = pygame.image.load('noPic.png')
searchImg = pygame.image.load('search.png')
searchHoverImg = pygame.image.load('searchHover.png')
errorImg = pygame.image.load('error.png')
helpImg = pygame.image.load('help.png')
helpHoverImg = pygame.image.load('helpHover.png')
playImg = pygame.image.load('play.png')
playHoverImg = pygame.image.load('playHover.png')
pauseImg = pygame.image.load('pause.png')
pauseHoverImg = pygame.image.load('pauseHover.png')
upImg = pygame.image.load('^.png')
upHoverImg = pygame.image.load('^Hover.png')
upNImg = pygame.image.load('^N.png')
downImg = pygame.image.load('^2.png')
downHoverImg = pygame.image.load('^2Hover.png')
downNImg = pygame.image.load('^2N.png')
os.chdir('..')

#vars
colorSetting = 1
panelMode = 'myMusic'
render = False
renderX = 0
renderY = 0
renderObj = []
renderNames = []
renderPaths = []
renderClock = 0
newSong = ''
newPic = ''
playingName = 'no song'
playingPlPa = True
playingCover = os.path.dirname(__file__) + '\images/noPic.png'
scrollPage = 0
scrollPages = 0
scrollY = 0

try:
    pickle_in = open('firstStart.data', 'r')
    firstStart = pickle.load(pickle_in)
    pickle_in = open('songCovers.data', 'r')
    renderObj = pickle.load(pickle_in)
    pickle_in = open('songPaths.data', 'r')
    renderPaths = pickle.load(pickle_in)
    pickle_in = open('songNames.data', 'r')
    renderNames = pickle.load(pickle_in)
except:
    firstStart = True
    pickle_out = open('firstStart.data', 'w')
    pickle.dump(firstStart, pickle_out)
    pickle_out.close()
if firstStart == True:
    panelMode = 'firstStart'


#setup
clock = pygame.time.Clock()

#pygame start
pygame.init()
screen_x = 1366
screen_y = 820
screen = pygame.display.set_mode([screen_x,screen_y], RESIZABLE)
middlex = screen_x/2
middley = screen_y/2
print middlex
print middley

#fonts
menu_font = pygame.font.SysFont('Calibri', 40)
hud_font = pygame.font.SysFont('Calibri', 40)
hud_font2 = pygame.font.SysFont('Calibri', 20)
big_font = pygame.font.SysFont('Calibri', 80)
mid_font = pygame.font.SysFont('Calibri', 70)

try:
    from win32api import GetSystemMetrics
    import win32gui
except:
     root = Tk()
     root.title("Boot error")
     root["padx"] = 20
     root["pady"] = 20

     tkinterLabel = Label(root)
     tkinterLabel["text"] = "There was an error on startup!"
     tkinterLabel.pack()
     tkinterLabel2 = Label(root)
     tkinterLabel2["text"] = "Please install win32api(pywin32)"
     tkinterLabel2.pack()

     root.mainloop()

try:  
    print "Width =", GetSystemMetrics(0)
    print "Height =", GetSystemMetrics(1)
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ( GetSystemMetrics(0) / 4, 1)
    pygame.init()
    screen_x = GetSystemMetrics(0)
    screen_y = GetSystemMetrics(1)

    #fonts
    big_font = pygame.font.SysFont('Calibri', 80)
    menu_font = pygame.font.SysFont('Calibri', 30)
    app_bar_font = pygame.font.SysFont('Calibri', 25)   

except:
     root = Tk()
     root.title("Boot error")
     root["padx"] = 20
     root["pady"] = 20

     tkinterLabel = Label(root)
     tkinterLabel["text"] = "an unkown error occured on startup!"
     tkinterLabel.pack()
     tkinterLabel2 = Label(root)
     tkinterLabel2["text"] = "Please be sure to use python 2.7"
     tkinterLabel2.pack()

#songs

#window settings
pygame.display.set_icon(musicImg)
pygame.display.set_caption("Grid Beat")

#program
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==VIDEORESIZE:
            screen=pygame.display.set_mode(event.dict['size'], RESIZABLE)

    #settings
    if colorSetting == 1:
        color1 = gray2
        color2 = gray
        color3 = white

    if colorSetting == 2:
        color1 = white
        color2 = gray
        color3 = black

    screen.fill(color1)
    clock.tick(200)
    mx, my = pygame.mouse.get_pos()

    fps_text = menu_font.render('FPS:' +str (clock.get_fps()), True, white)
    sx, sy = screen.get_size()

    pygame.draw.rect(screen, color2, [0, 0 , 60, sy])
    if mx > 0 and mx < 60 and my > 0 and my < 60:
        screen.blit(musicHoverImg, (0,0))
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            panelMode = 'myMusic'
    else:
        screen.blit(musicImg, (0,0))    
    if mx > 0 and mx < 60 and my > 65 and my < 125:
        screen.blit(helpHoverImg, (0,65))
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            panelMode = 'help'
    else:
        screen.blit(helpImg, (0,65))    

    if panelMode == 'firstStart':
        pygame.draw.rect(screen, color2, [60, 0, sx, 100])
        screen.blit(big_font.render('HELLO!', True, color3), (65, 10))
        screen.blit(mid_font.render('It seems like you are new, Lets get you started', True, color3), (65, 110))
        pygame.draw.rect(screen, color2, [75, 190, sx - 85, 2])
        screen.blit(menu_font.render('Adding a song is simple, go to your music(by clicking the music icon on the side of the screen), click the +,', True, color3), (65, 195))
        screen.blit(menu_font.render('and just fill out the forms and hit the add button! To play a song go to your music and click the song you want!', True, color3), (65, 220))
        screen.blit(mid_font.render('Need more help?', True, color3), (65, 300))
        pygame.draw.rect(screen, color2, [75, 380, sx - 85, 2])
        screen.blit(menu_font.render('Just click the question mark on the side of the screen!', True, color3), (65, 385))
        firstStart = False
        pickle_out = open('firstStart.data', 'w')
        pickle.dump(firstStart, pickle_out)
        pickle_out.close()
    if panelMode == 'myMusic':
        if mx > sx - 80 and mx < sx - 10 and my > 10 and my < 80:
            screen.blit(newSongHoverImg, (sx - 80, 10))
            hovering.hover(screen, 'Add a new song      ', color1, color2, mx, my, menu_font, sx)
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                panelMode = 'newMusic'   
                newPic = os.path.dirname(__file__) + '\images/noPic.png'
                newSongName = ''
                newSong = ''
                backup = True
        else:
            screen.blit(newSongImg, (sx - 80, 10))
        #renderer
        render = True
        renderClock = 0
        renderX = 65
        renderY = 105 + scrollY
        scrollPages = 0
        while render == True:
            try:
                if mx > renderX and mx < renderX + 300 and my > renderY and my < renderY + 330:
                    pygame.draw.rect(screen, blue5, [renderX, renderY, 300, 350])
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:   
                        playingName = renderNames[renderClock]
                        playingCover = renderObj[renderClock]
                        playingPlPa = False
                        player.play(renderPaths[renderClock])
                picture = pygame.image.load(renderObj[renderClock])
                picture = pygame.transform.scale(picture, (300, 300))
                screen.blit(picture, (renderX, renderY))
                screen.blit(menu_font.render(renderNames[renderClock], True, color2), (renderX, renderY + 310))
                if renderClock == len(renderObj) - 1:
                    break
                renderClock = renderClock + 1
                renderX = renderX + 320
                if renderX + 310> sx - 55:
                    renderX = 65
                    renderY = renderY + 370   
                    scrollPages = scrollPages + 1  
            except:
                render = False

        #print scrollPage,' ', scrollPages 
        if scrollPage < scrollPages:
            if mx > sx - 50 and mx < sx and my > sy / 2 + 25 and my < sy / 2 + 75:
                screen.blit(downHoverImg, (sx - 50, sy / 2 + 25))
                if event.type == MOUSEBUTTONDOWN and event.button == 1:   
                    scrollY = scrollY - 370
                    scrollPage = scrollPage + 1
                    pygame.display.update()
                    pygame.time.delay(100)
            else:
                screen.blit(downImg, (sx - 50, sy / 2 + 25))
        else:
            screen.blit(downNImg, (sx - 50, sy / 2 + 25))

        if not scrollPage == 0:
            if mx > sx - 50 and mx < sx and my > sy / 2 - 25  and my < sy / 2 + 25:
                screen.blit(upHoverImg, (sx - 50, sy / 2 - 25))
                if event.type == MOUSEBUTTONDOWN and event.button == 1:   
                    scrollY = scrollY + 370
                    scrollPage = scrollPage - 1
                    pygame.display.update()
                    pygame.time.delay(100)
            else:
                screen.blit(upImg, (sx - 50, sy / 2 - 25))
        else:
            screen.blit(upNImg, (sx - 50, sy / 2 - 25))

        pygame.draw.rect(screen, color2, [60, 0, sx, 100])
        screen.blit(big_font.render('My Music', True, color3), (65, 10))

    if panelMode == 'newMusic':
        if backup == True:
            os.chdir('songs backup')
            pickle_out = open('songCovers.data', 'w')
            pickle.dump(renderObj, pickle_out)
            pickle_out.close()
            pickle_out = open('songNames.data', 'w')
            pickle.dump(renderNames, pickle_out)
            pickle_out.close()
            pickle_out = open('songPaths.data', 'w')
            pickle.dump(renderPaths, pickle_out)
            pickle_out.close()
            os.chdir('..')
            backup = False
        pygame.draw.rect(screen, color2, [60, 0, sx, 100])
        screen.blit(big_font.render('Add Music', True, color3), (65, 10))       
        screen.blit(menu_font.render('Song: ' +str(newSongName), True, color3), (65, 110))  
        screen.blit(menu_font.render('Image: ', True, color3), (65, 240))   
        try:
            newPic2 = pygame.image.load(newPic)
            newPic3 = pygame.transform.scale(newPic2, (100, 100))
        except:
            newPic = errorImg
        screen.blit(newPic3, (200, 190))
        if mx > sx - 80 and mx < sx - 10 and my > 190 and my < 260:
            screen.blit(searchHoverImg, (sx - 80, 190))
            hovering.hover(screen, 'Browse   ', color2, color1, mx, my, menu_font, sx)
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                try:
                    f = askopenfilename()
                    newPic = f
                except:
                    newPic = errorImg
        else:
            screen.blit(searchImg, (sx - 80, 190))
        if mx > sx - 80 and mx < sx - 10 and my > 110 and my < 170:
            screen.blit(searchHoverImg, (sx - 80, 110))
            hovering.hover(screen, 'Browse   ', color2, color1, mx, my, menu_font, sx)
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                try:
                    f = askopenfilename()
                    newSongName = ntpath.basename(f)[0:len(ntpath.basename(f)) - 4]
                    newSong = f
                except:
                    newSong = ''
        else:
            screen.blit(searchImg, (sx - 80, 110))
        if mx > 65 and mx < 135 and my > 350 and my < 420:
            screen.blit(newSongHoverImg, (65, 350))  
            if event.type == MOUSEBUTTONDOWN and event.button == 1: 
                try:
                    renderObj.append(newPic)
                    renderNames.append(newSongName)
                    renderPaths.append(newSong)
                    pickle_out = open('songCovers.data', 'w')
                    pickle.dump(renderObj, pickle_out)
                    pickle_out.close()
                    pickle_out = open('songNames.data', 'w')
                    pickle.dump(renderNames, pickle_out)
                    pickle_out.close()
                    pickle_out = open('songPaths.data', 'w')
                    pickle.dump(renderPaths, pickle_out)
                    pickle_out.close()
                    panelMode = 'myMusic'
                except:
                    pyError.newError('Grid Beat Error', 'ERROR', 'There was an error creating the song', 0, 0)
                    break
        else:
            pygame.draw.rect(screen, color2, [65, 350, 70, 70])
            screen.blit(newSongImg, (65, 350))   

    if panelMode == 'help':
        pygame.draw.rect(screen, color2, [60, 0, sx, 100])
        screen.blit(big_font.render('Help', True, color3), (65, 10))    
        screen.blit(mid_font.render('Recovering lost music', True, color3), (65, 110))
        pygame.draw.rect(screen, color2, [75, 190, sx - 85, 2])
        screen.blit(menu_font.render('Oh no! Did you lose all your songs? no worries you can almost always recover it! Step 1: Go to grid beat in', True, color3), (65, 195))
        screen.blit(menu_font.render('file explorer. Step 2: go to grid beat > grid beat > songs backup. Step 3: Copy all those files into', True, color3), (65, 220))
        screen.blit(menu_font.render('grid beat > grid beat. If it tells you it will replace files let it do it.', True, color3), (65, 245))

    pygame.draw.rect(screen, color1, [sx / 2 - 102, 8, 400, 84])    
    playingPicture = pygame.image.load(playingCover)
    playingPicture = pygame.transform.scale(playingPicture, (80, 80))
    screen.blit(playingPicture, (sx / 2 - 100, 10))
    screen.blit(menu_font.render(playingName, True, color2), (sx / 2 - 15, 10))
    if mx > sx / 2 - 17 and mx < sx / 2 + 31 and my > 40 and my < 90:
        if playingPlPa == True:            
            screen.blit(playHoverImg, (sx / 2 - 17, 40))
            if event.type == MOUSEBUTTONDOWN and event.button == 1: 
                playingPlPa = False
                player.unpause()
                pygame.time.delay(100)
        elif playingPlPa == False:            
            screen.blit(pauseHoverImg, (sx / 2 - 17, 40))
            if event.type == MOUSEBUTTONDOWN and event.button == 1: 
                playingPlPa = True
                player.pause()
                pygame.time.delay(100)
    else:
        if playingPlPa == True:            
            screen.blit(playImg, (sx / 2 - 17, 40))
        elif playingPlPa == False:            
            screen.blit(pauseImg, (sx / 2 - 17, 40))

    pygame.display.update()