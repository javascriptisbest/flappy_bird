import pygame
from pygame.locals import *
import os, sys, random
import math 

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pipe_gap = 160
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png').convert_alpha()
        
        self.rect = self.image.get_rect()

        #position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = (x, y - int(pipe_gap / 2)  )
        if position == -1:
            self.rect.topleft = (x, y + int(pipe_gap / 2) )
    def update(self):
        self.rect.x -= 4
        if self.rect.right < 0:
            self.kill()

class Game_over:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  
    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action
class Bird(pygame.sprite.Sprite):

    def __init__(self,x, y,screen_height = 800, flying = True, game_over = False):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.screen = pygame.display.get_surface()
        self.flying = flying
        self.game_over = game_over
        self.count = 0
        self.index = 0
        self.vel = 0
        
        for so in range(1, 4):
            img = pygame.image.load(f"img/bird{so}.png")
            self.images.append(img)
       
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
      #  self.rect.center = [50, 384]
    def update(self):
        if self.flying == True:
            
            if self.vel <= 10:
                self.vel += 0.5
            if self.rect.bottom < self.screen.get_height() - 125:
                self.rect.y += int(self.vel)
        if self.game_over == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.vel = -10
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            
            self.count += 1 
            flap_cooldown = 5
            if self.count > flap_cooldown:
                self.count = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
            
            self.image = pygame.transform.rotozoom(self.image, -self.vel * 1.25, 1)
        elif self.flying == True:
            self.image = self.images[self.index]
            self.image = pygame.transform.rotozoom(self.image, -90, 1)
        else:
            self.image = self.images[self.index]

class Main:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Minh dep trai vay')

        high = open('./hiscore.txt', 'r')
        self.highscore = high.read()
        
        high.close()
        

        self.clock = pygame.time.Clock()
        self.fps =60
        self.groundx = 0
        self.scroll_speed = 4
        self.starttime = pygame.time.get_ticks()
        self.pipe_frequency = 1300
        self.inpipe = False
        self.score = 0
        self.font = pygame.font.Font('./04B_19.TTF', 40)
        self.fontto = pygame.font.Font('./04B_19.TTF', 70)

        self.flying = False
        self.game_over = False

        self.bird_group = pygame.sprite.Group()
        self.flappy = Bird(130, self.screen_height//2, self.screen_height, self.flying, self.game_over)
        self.bird_group.add(self.flappy)

        self.pipe_group = pygame.sprite.Group()

        self.over = Game_over(self.screen_width//2, self.screen_height//2 - 80, pygame.transform.scale2x( pygame.image.load('./img/gold.png').convert_alpha()))
        self.incre = 0
        self.start = pygame.transform.scale2x( pygame.image.load('./img/message.png').convert_alpha())
        
    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))
    
    def draw_text2(self, text, font, text_col, x, y, screen = None):
        img = font.render(text, True, text_col)
        rect = img.get_rect()
        rect.center = (x, y)
        screen.blit(img, rect)




    def run(self):
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and self.flying == False and self.game_over == False:
                    self.flying = True
                    self.flappy.flying = True


            self.screen.blit(pygame.image.load('img/bg.png').convert_alpha(), (0,0))
            self.pipe_group.draw(self.screen)

            
            self.bird_group.draw(self.screen)
            self.bird_group.update()

            if self.flying == False and self.game_over == False:
                self.score = 0
                #self.draw_text('Click to start', self.font, (255, 255, 255), self.screen_width//2 - 100, self.screen_height//2 - 50)
                #self.draw_text('Flappy Bird', self.fontto, (255, 255, 255), self.screen_width//2 - 100, self.screen_height//2 - 150)
                self.screen.blit(self.start, (self.screen_width//2 -100, 100))
            if len(self.pipe_group) > 0:
                if self.bird_group.sprites()[0].rect.left > self.pipe_group.sprites()[0].rect.left and self.bird_group.sprites()[0].rect.right < self.pipe_group.sprites()[0].rect.right and self.inpipe == False:
                    self.inpipe = True
                if self.bird_group.sprites()[0].rect.left > self.pipe_group.sprites()[0].rect.right and self.inpipe == True:
                    self.score += 1
                    self.inpipe = False
        
            if pygame.sprite.groupcollide(self.bird_group, self.pipe_group, False, False) or self.flappy.rect.top < 0 or self.flappy.rect.bottom > self.screen_height - 125:
                self.game_over = True
                self.flappy.game_over = True
            if self.flappy.rect.bottom > self.screen_height - 125:
                self.flying = False
                self.flappy.flying = False
                self.game_over = True
                self.flappy.game_over = True
            
                

            if self.game_over == False and self.flying == True:

                    
                if pygame.time.get_ticks() - self.starttime > self.pipe_frequency:
                    self.starttime = pygame.time.get_ticks()
                    self.pipe_height = random.choice([-100 +20*i for i in range(int(200/20))])
                    btm =Pipe(self.screen_width, self.screen_height/2 +self.pipe_height, -1)
                    top = Pipe(self.screen_width, self.screen_height/2 + self.pipe_height, 1)
                    
                    self.pipe_group.add(btm)
                    self.pipe_group.add(top)
                self.groundx -= self.scroll_speed
                if self.groundx < -800:
                    self.groundx = 0
                
                self.pipe_group.update()
                
                self.draw_text(str(self.score), self.font, (255, 255, 255), self.screen_width//2, self.screen_height//10)





           

            self.screen.blit(pygame.image.load('img/ground.png').convert_alpha(), (self.groundx, self.screen_height - 125))
            self.screen.blit(pygame.image.load('img/ground.png').convert_alpha(), (self.groundx + 795, self.screen_height - 125))
            
            if self.game_over == True:
                if Button(self.screen_width/2, 600, pygame.image.load('img/restart.png')).draw(self.screen):
                    self.game_over = False
                    self.flappy.game_over = False
                    self.flying = False
                    self.flappy.flying = False
                    #self.score = 0
                    self.flappy.rect.center = (130, self.screen_height//2)
                    self.flappy.vel = 0
                    self.pipe_group.empty()
                    self.flappy.image = self.flappy.images[0]
                    
                self.over.draw(self.screen)
                if self.score > int(self.highscore):
                   high = open('./hiscore.txt', 'w')
                   high.write(str(self.score))
                   high.close()
                   self.highscore = self.score
                self.draw_text2(str(self.score), self.fontto, (255, 255, 255), self.screen_width/2 + 140 ,self.screen_height/2, self.screen)
                self.draw_text2(f'High Score : {self.highscore}', self.font, (0, 255, 255), self.screen_width/2,80, self.screen)
                
                        
            self.clock.tick(self.fps)
            pygame.display.update()

if __name__ == '__main__':
    main = Main()
    main.run()

