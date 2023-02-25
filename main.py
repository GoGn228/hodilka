import pygame
import os
import sys
import random

pygame.init()
current_path=os.path.dirname(__file__)
os.chdir(current_path)
WIDTH=600
HEIGHT=600
FPS=60
#pygame.mixer.music.load('sound/mario.mp3')
#pygame.mixer.music.play(-1)
sc=pygame.display.set_mode((WIDTH, HEIGHT))
clock=pygame.time.Clock()

from load import *

def game_lvl():
    sc.fill((0, 100, 0))
    block_group.update(0, 0)
    block_group.draw(sc)
    player_group.update()
    player_group.draw(sc)
    pygame.display.update()

def drawMaps(nameFile):
    maps=[]
    source="game_lvl/" + str(nameFile)
    with open(source, "r") as file:
        for i in range(0, 100):
            maps.append(file.readline().replace("\n", "").split(",")[0:-1])

    pos=[0, 0]
    for i in range(0, len(maps)):
        pos[1] = i *50
        for j in range(0, len(maps[0])):
           pos[0]=50 * j
           if maps[i][j]=="1":
              block=Block(block_image, pos)
              block_group.add(block)
              camera_group.add(block)
           if maps[i][j] == "2":
                player.rect.x = pos[0]
                player.rect.y = pos[1]


class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image[0]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.x = pos[1]
        self.speedx = 5
        self.speedy = 5
        self.dir = "right"
    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.rect.y -= self.speedy
            self.dir = "top"
            self.image = player_image[3]
            if self.rect.top < 100:
                self.rect.top = 100
                camera_group.update(0, self.speedy)
        elif key[pygame.K_d]:
            self.rect.x += self.speedx
            self.dir = "right"
            self.image = player_image[0]
            if self.rect.right > WIDTH - 100:
                self.rect.right = WIDTH - 100
                camera_group.update(-self.speedx,0)
        elif key[pygame.K_s]:
            self.rect.y += self.speedy
            self.dir = "bottom"
            self.image = player_image[1]
            if self.rect.bottom > HEIGHT - 100:
                self.rect.bottom = HEIGHT - 100
                camera_group.update(0, -self.speedy)
        elif key[pygame.K_a]:
            self.rect.x -= self.speedx
            self.dir = "left"
            self.image = player_image[2]
            if self.rect.left < 100:
                self.rect.left = 100
                camera_group.update( self.speedx, 0)
class Block(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, stepx, stepy):
        self.rect.x += stepx
        self.rect.y += stepy
        if pygame.sprite.spritecollide(self, player_group, False):
            if player.dir == "left":
                player.rect.left = self.rect.right
            elif player.dir == "right":
                player.rect.right = self.rect.left
            elif player.dir == "top":
                player.rect.top = self.rect.bottom
            elif player.dir == "bottom":
                player.rect.bottom = self.rect.top

def restart():
    global player_group, camera_group, block_group, player
    camera_group = pygame.sprite.Group()
    block_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    player = Player(player_image, (0, 0))
    player_group.add(player)

restart()
drawMaps('1.txt')
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    game_lvl()
    clock.tick(FPS)