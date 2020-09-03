# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 09:03:27 2019

@author: Maki Yu
"""

# This game is based on pygame 1.9.1
import pygame
from pygame.locals import *
import random

# Settings
WIDTH = 1000
HEIGHT = 600
FPS = 30

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
PURPLE = (184, 175, 202)
DPURPLE = (124, 80, 157)
APURPLE = (208, 171, 191)

OBSTACLE = DPURPLE
BACKGROUND = PURPLE
GROUND = APURPLE

ACC = 1
FRI = 0.2
GRV = 0.7

INIT_OBSTACLE_NUM = 13

AXIE_L = pygame.transform.scale(pygame.image.load("axie_example_l.png"), (73, 53))
AXIE_R = pygame.transform.scale(pygame.image.load("axie_example_r.png"), (73, 53))
AXIE_K = pygame.transform.scale(pygame.image.load("axie_example_k.png"), (73, 53))

# Supplimental Classes
class Vec2():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.plain = (x,y)
    def __add__(self, another_Vec2):
        return Vec2(self.x + another_Vec2.x, self.y + another_Vec2.y)
    def __sub__(self, another_Vec2):
        return Vec2(self.x - another_Vec2.x, self.y - another_Vec2.y)
    def __mul__(self, scalar):
        return Vec2(self.x * scalar, self.y * scalar)
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) +")"
    
# Game Objects
class Axie(pygame.sprite.Sprite):
    def __init__(self):
        super(Axie,self).__init__()
        self.image = AXIE_L
        self.rect = self.image.get_rect()
        self.pos = Vec2(WIDTH / 2, HEIGHT - 60)
        self.rect.midbottom = self.pos.plain
        self.vel = Vec2(0,0)
        self.killed = False
        self.out = False
        
    def update(self):
        self.acc = Vec2(0, GRV)
        if not self.killed and not self.out:
            keys_down = pygame.key.get_pressed()
            if keys_down[K_UP] or keys_down[K_w]:
                self.acc.y -= ACC
            if keys_down[K_DOWN] or keys_down[K_s]:
                self.acc.y += ACC
            if keys_down[K_LEFT] or keys_down[K_a]:
                self.acc.x -= ACC
            if keys_down[K_RIGHT] or keys_down[K_d]:
                self.acc.x += ACC
        
        self.acc.x -= self.vel.x * FRI
        self.vel += self.acc
        self.pos += self.vel + self.acc * 0.5
        
        #Return Axie to the screen if moved out
        if self.pos.x < 0:
            self.pos.x = WIDTH
        elif self.pos.x > WIDTH:
            self.pos.x = 0
#        if self.pos.y <= 0:
#            self.pos.y = HEIGHT
#        elif self.pos.y >= HEIGHT:
#            self.pos.y = 0
        
        self.rect.midbottom = self.pos.plain
        
        # Animation
        if self.killed:
            self.image = AXIE_K
        elif self.vel.x > 0:
            self.image = AXIE_R
        elif self.vel.x < 0:
            self.image = AXIE_L
        
        
class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,wid,hit,color):
        super(Platform,self).__init__()
        self.image = pygame.Surface((wid,hit))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Game():
    
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.screen.fill(BACKGROUND)
        pygame.init()
        pygame.mixer.init()
        
        pygame.display.set_caption("Axie")
    
    # Supplimental Functions
    def draw_text(self, text, size, color, x, y):
        font_name = pygame.font.match_font('arial')
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
    
    def wait(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    waiting = False
                    pygame.quit()
                if event.type == KEYUP:
                    if event.key == K_SPACE:
                        waiting = False
            
    # Start and Finish
    def start(self):
        self.draw_text("Axie Flies Up", 50, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("(Don't Touch Me)", 22, DPURPLE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press Space to Continue", 22, WHITE, WIDTH / 2, HEIGHT * 3 /5 )
        pygame.display.flip()
        self.wait()
        
    def finish(self):
        self.draw_text("Game Over", 50, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.level), 22, DPURPLE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press Space to Continue", 22, WHITE, WIDTH / 2, HEIGHT * 3 /5 )
        pygame.display.flip()
        self.wait()
    
    # Main Game Logic
    def new_game(self):
        # Runtime Initialization
        
        all_sprites = pygame.sprite.Group()
        all_obstacles = pygame.sprite.Group()
        all_grounds = pygame.sprite.Group()
        
        axie = Axie()
        all_sprites.add(axie)
        
        ground = Platform(0, HEIGHT - 20, WIDTH, 500, GROUND)
        all_sprites.add(ground)
        all_grounds.add(ground)
        
        while len(all_obstacles) < INIT_OBSTACLE_NUM:
                width = random.randrange(50, 100)
                x = random.randrange(0, WIDTH -width)
                y = random.randrange(-200, HEIGHT - 200)
                obstacle = Platform(x, y, width, 20, OBSTACLE)
                if not pygame.sprite.spritecollide(obstacle, all_obstacles, False):
                    all_obstacles.add(obstacle)
                    all_sprites.add(obstacle)

        self.level = 0
        
        # Main loop
        while self.running:
            # Timing
            self.clock.tick(FPS)
            
            # Quit Scenario Examination
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
            
            # Objects Update
            self.screen.fill(PURPLE)
            all_sprites.update()
            self.draw_text(str(self.level), 22, WHITE, 20, 5)
            
            # Ground Control
            touchground = pygame.sprite.spritecollide(axie, all_grounds, False)
            if touchground and not axie.killed:
                axie.acc.y = 0
                axie.vel.y = 0
                axie.pos.y = touchground[0].rect.top
            
            # Game Over Control
            collision = pygame.sprite.spritecollide(axie, all_obstacles, False)
            if collision:
                axie.killed = True
            
            if axie.rect.bottom > HEIGHT:
                axie.out = True
                for sprite in all_sprites:
                    sprite.rect.y -= max(axie.vel.y, 10)
                    if sprite.rect.bottom < 0:
                        sprite.kill()
            if len(all_obstacles) == 0:
                break
            
            # Camera Control
            if axie.rect.top <= HEIGHT / 3:
                axie.pos.y += abs(axie.vel.y)
                ground.rect.y += abs(axie.vel.y)
                if ground.rect.top >= HEIGHT:
                    ground.kill()
                for obstacle in all_obstacles:
                    obstacle.rect.y += abs(axie.vel.y)
                    if obstacle.rect.top >= HEIGHT:
                        self.level += 1
                        obstacle.kill()
            while len(all_obstacles) < INIT_OBSTACLE_NUM:
                width = random.randrange(50 + self.level, 100 + self.level)
                x = random.randrange(0, WIDTH -width)
                y = random.randrange(-600, -20)
                obstacle = Platform(x, y, width, 20, OBSTACLE)
                if not pygame.sprite.spritecollide(obstacle, all_obstacles, False):
                    all_obstacles.add(obstacle)
                    all_sprites.add(obstacle)
            
            # Frame Update
            all_sprites.draw(self.screen)
            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.start()
    while game.running:
        game.new_game()
        game.finish()
    pygame.quit()