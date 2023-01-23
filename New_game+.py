import sys
import time
import pygame
import loader_game_sprites as LGS
from random import randint
from pygame.locals import *

all_sprites = pygame.sprite.Group()
player = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__(all_sprites)

        self.player = LGS._main_sprite("boss_body.png")[0]
        self.player_x = x
        self.player_y = y 

        self.rect_x = pygame.Rect(self.player_x, self.player_y, 200, 150)
        pygame.draw.rect(self.player, (self.rect_x, 3, 3))
        self.add(player)
    
    def update(self, *args):
        if args:
            x = args[0][0]
            while self.player_x < x and x <= 1600:
                self.player_x += 3
                self.rect_x = self.rect_x.move(3, 0)
            while self.player_x > x and x <= 1600:
                self.player_x += 3
                self.rect_x = self.rect_x.move(-3, 0)
            
            y = args[0][0]
            while self.player_y < y and y <= 1000:
                self.player_y += 3
                self.rect_x = self.rect_x.move(0, 3)
            while self.player_y > y and y <= 1000:
                self.player_y -= 3
                self.rect_x = self.rect_x.move(0, -3)
            return self.player_x, self.player_y



class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)

        self.enemy = LGS._main_sprite("ring.png")
        self.enemy_x = randint(0, 900)
        self.enemy_y = randint(0, 600)

        self.rect_x = pygame.Rect(self.enemy_x, self.enemy_y, 200, 200)
        pygame.draw.rect(self.enemy, self.rect, 3)
        self.add(Player)
    
    def update(self):
        global player_hp
        while self.enemy_x and self.enemy_y < Player.update():
            self.enemy_x += 2
            self.rect_x.move(2, 2)

        while self.enemy_x and self.enemy_y > Player.update():
            self.enemy_x -= 2
            self.rect_x.move(-2, -2)
        if pygame.sprite.spritecollideany(self, player):
            player_hp -= 10

def start(screen):
    font = pygame.font.Font(None, 39)
    text1 = font.render(f"lifes: {player_hp}", True, (120, 255, 120))
    screen.blit(text1, (10, 2))
    pygame.draw.rect(screen, (120, 255, 120), (0, 0, 600, 50), 2)

def defeat(screen):
    for s in all_sprites:
        s.kill()
    screen.fill((224, 32, 11))
    font = pygame.font.Font(None, 30)
    text0 = font.render("  ВЫ ПРОИГРАЛИ", True, 'white')
    screen.blit(text0, (0, 100))



if __name__ == "__main__":
    pygame.init()
    size = 1600, 1000
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Game")
    screen.blit(LGS._background("Venator.jpg"), (1600, 1000))
    fps = 30
    clock = pygame.time.Clock()
    
    player = Player(100, 100)
    player_hp = 100
    _enemy = False
    final = None
    start_sc = True
    running = True

    while running:
        screen.blit(LGS._background("Venator.jpg"), (1600, 1000))
        while start_sc:
            pygame.mouse.set_visible(True)
            start(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start_sc = False
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pygame.mouse.set_visible(False)
                        start_sc = False
            pygame.display.flip()
        all_sprites.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                player.update(event.pos)
        start(screen)
        if player_hp == 0:
            final = True
        if final:
            pygame.mouse.set_visible(True)
            defeat(screen)
        if not _enemy:
            Enemy()
            _enemy = True
        all_sprites.update()
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
    sys.exit()