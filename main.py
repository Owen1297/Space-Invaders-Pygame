import pygame
import random
import tkinter as tk
from tkinter import messagebox

def gameover():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Game over!", "Press OK to restart")
    root.destroy()

# laziness
true = True
false = False

# setup
pygame.init()
sx = 640
sy = sx
screen = pygame.display.set_mode((sx, sy))
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(pygame.image.load("player.png"))

# classes
class Player:
    def __init__(me, x, y, speed):
        me.posX = x
        me.posY = y
        me.speed = speed
        me.t = "player.png"
        me.img = pygame.image.load(me.t)
        me.sz = 16
        me.img = pygame.transform.scale(me.img, (me.sz, me.sz))
        me.rect = me.img.get_rect()
    def update(me):
        if me.posX <= 0:
            me.posX = 0
        elif me.posX >= sx:
            me.posX = sx
    def die(me):
        gameover()
        global level, bullets, ens
        me.posX = 50
        me.posY = 620
        level = 0
        bullets.clear()
        ens.clear()
        newEnemy(3, false, level, true)
    def check(me, ob):
        # Update rect position before checking collision
        me.rect.topleft = (me.posX/2, me.posY/2)
        ob.rect.topleft = (ob.posX/2, ob.posY/2)

        if me.rect.colliderect(ob.rect):
            if not ob.ps:
                me.die()
                if ob in bullets:
                    bullets.remove(ob)  # Remove the bullet that hit the enemy
                else:
                    print(f"Warning - bullet #{id(ob)} does not exist")
class Bullet:
    def __init__(me, x, y, speed, shotByPlayer):
        me.posX = x
        me.posY = y
        me.speed = speed
        me.t = "bullet.png"
        me.img = pygame.image.load(me.t)
        me.sz = 8
        me.img = pygame.transform.scale(me.img, (me.sz, me.sz))
        me.rect = me.img.get_rect()
        me.ps = shotByPlayer
    def update(me):
        me.posY += me.speed
        if me.posX >= sx or me.posX <= 0 or me.posY >= sy or me.posY <= 0:
            bullets.remove(me)
            print(f"Debug - bullet #{id(me)} deleted")
class Star:
    def __init__(me, x, y):
        me.x = x
        me.y = y
class Enemy:
    def __init__(me, x, y, sd):
        me.posX = x
        me.posY = y
        me.dir = 1
        me.cd = sd
        me.speed = 1
        me.t = "enemy.png"
        me.img = pygame.image.load(me.t)
        me.sz = 16
        me.img = pygame.transform.scale(me.img, (me.sz, me.sz))
        me.rect = me.img.get_rect()
        me.tus = random.randrange(70, 100)
    def update(me):
        me.posX += me.cd * me.speed
        if me.posX >= sx or me.posX <= 0:
            me.cd = 0-me.cd
        if me.tus == 0:
            bullets.append(Bullet(me.posX, me.posY+32, 10, False))
            me.tus = random.randrange(50, 70)
        me.tus -= 1
    def die(me):
        ens.remove(me)
    def check(me, ob):
        # Update rect position before checking collision
        me.rect.topleft = (me.posX/2, me.posY/2)
        ob.rect.topleft = (ob.posX/2, ob.posY/2)

        if me.rect.colliderect(ob.rect):
            if ob.ps:
                me.die()
                bullets.remove(ob)  # Remove the bullet that hit the enemy

# functions
def rect(color, x, y, width, height):
    left = x-(width/2)
    top = y-(height/2)
    pygame.draw.rect(screen, color,(left, top, width, height))
def img(path, x, y, scale):
    screen.blit(pygame.transform.scale(pygame.image.load(path), (scale, scale)), (x-(scale/2), y-(scale/2)))
def imgS(image, x, y, scale):
    screen.blit(image, (x-(scale/2), y-(scale/2)))
def newEnemy(count, rand, m, um):
        if rand:
            enemyCount = random.randrange(1, 4)
        else:
            enemyCount = count
        if um:
            enemyCount *= m
        while not enemyCount == 0:
            xx = random.randrange(16, sx)
            yy = random.randrange(16, round(sy/3))
            sd = random.randrange(1, 4)
            if sd >= 3:
                sd = 1
            else:
                sd = -1
            ens.append(Enemy(xx, yy, sd))
            enemyCount -= 1

# variables
running = true
clock = pygame.time.Clock()
p = Player(50, 620, 5)
white = (255, 255, 255)
black = (0, 0, 0)
bg = black
level = 0
bullets = []
stars = []
ens = []

# star - init
starMaster = 50
starCount = starMaster
while not starCount == 0:
    stx = random.randrange(0, sx)
    sty = random.randrange(0, sy)
    stars.append(Star(stx, sty))
    starCount -= 1

# main loop
while running:
    screen.fill(bg)
    keys = pygame.key.get_pressed()

    # player logic
    imgS(p.img, p.posX, p.posY, p.sz)
    p.update()
    for b in bullets[:]:
        p.check(b)

    # star - draw
    for s in stars[:]:
        img("star.png",s.x, s.y, 16)

    # controls
    if keys[pygame.K_LEFT]:
        p.posX -= p.speed
    if keys[pygame.K_RIGHT]:
        p.posX += p.speed

    # bullet logic
    for b in bullets[:]:
        imgS(b.img, b.posX, b.posY, b.sz)
        b.update()
    
    # enemy logic
    for e in ens[:]:
        imgS(e.img, e.posX, e.posY, e.sz)
        e.update()
        for b in bullets:
            e.check(b)
    
    # stages
    if len(ens) == 0:
        level += 1
        newEnemy(3, false, level, true)
    
    # win logic
    if level >= 10:
        print("Won!!")
        running = false

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = false
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(Bullet(p.posX, p.posY, -10, True))
            if event.key == pygame.K_d:
                print(bullets)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
