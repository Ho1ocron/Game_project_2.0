'''есть баг с прохождением падающего квадрата через правую часть платформы, пока не могу придумать как исправить'''
'''если попытаться поймать падающий квадрат правым краем платформы, он просто пройдет сквозь платформу'''

import sys
import pygame
import random

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group() # группа для платформы (в ней будет один элемент - основная платформа)
borders = pygame.sprite.Group() # группа для границ (в ней будет нижняя граница поля)


class Platform(pygame.sprite.Sprite): # платформа, управляемая игроком с помощью перемещения мыши
    def __init__(self, x: int):
        super().__init__(all_sprites)
        self.image = pygame.Surface((80, 20))
        self.color = pygame.Color('grey')
        self.image.fill(self.color)
        self.x = x
        self.rect = pygame.Rect(self.x, 500, 50, 10)
        pygame.draw.rect(self.image, self.color, self.rect, 3)
        self.add(platforms)

    def update(self, *args): # перемещение платформы
        if args:
            x = args[0][0] # координата по горизонтали, к которой нужно переместиться
            while self.x < x and x <= 520:
                self.x += 1
                self.rect = self.rect.move(1, 0)
            while self.x > x and x <= 520:
                self.x -= 1
                self.rect = self.rect.move(-1, 0)


class Note(pygame.sprite.Sprite): # падающий объект
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.Surface((20, 20))
        self.color = pygame.Color('blue')
        self.image.fill(self.color)
        self.rect = pygame.Rect(random.randint(0, 580), 45, 20, 20)
        pygame.draw.rect(self.image, self.color, self.rect, 3)

    def update(self):
        global ep, HP, SCORE, COMBO, max_combo #ep - проверяем если мы что-то сделали с нотой (поймали/не поймали)
        if pygame.sprite.spritecollideany(self, platforms): # если поймали
            ep = True
            SCORE += 1
            COMBO += 1
            if COMBO % 10 == 0:
                HP += 1
            max_combo = max(max_combo, COMBO)
            self.kill() # убиваем, чтобы потом создать новую
        elif pygame.sprite.spritecollideany(self, borders): # если не поймали
            ep = True
            HP -= 1
            COMBO = 0
            self.kill() # убиваем, чтобы потом создать новую
        else:
            self.rect = self.rect.move(0, 10) # иначе продолжает падать


class Border(pygame.sprite.Sprite): # граница поля
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.Surface((600, 10))
        self.color = pygame.Color('black')
        self.image.fill(self.color)
        self.rect = pygame.Rect(0, 590, 600, 10)
        pygame.draw.rect(self.image, self.color, self.rect, 3)
        self.add(borders)


def set_stat(screen): # отображение на экране количества баллов и хп
    font = pygame.font.Font(None, 39)
    text1 = font.render(f"lifes: {HP}", True, (120, 255, 120))
    text2 = font.render(f"score: {SCORE}", True, (120, 255, 120))
    text3 = font.render(f"combo: {COMBO}", True, (120, 255, 120))
    screen.blit(text1, (10, 2))
    screen.blit(text2, (200, 0))
    screen.blit(text3, (400, 0))
    pygame.draw.rect(screen, (120, 255, 120), (0, 0, 600, 50), 2)


def set_start_screen(screen): # стартовый экран
    screen.fill((76, 141, 38))
    intro_text = [" ПРАВИЛА ИГРЫ", "",
                  " Ловите синие квадраты с помощью платформы",
                  " Управляйте платформой движением мыши",
                  " Если вы пропустите квадрат, вычтется жизнь",
                  " В начале у вас пять жизней",
                  " Если комбо кратно 10, восстанавливается жизнь ",
                  " Чтобы продолжить, нажмите ЛКМ", "", "",
                  " игра находится в разработке, присутствуют баги", " tg: @Owlga6"]
    font = pygame.font.Font(None, 30)
    text_coord = 70
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 0
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def set_final_screen(screen): # финальный экран
    for s in all_sprites:
        s.kill()
    screen.fill((224, 32, 11))
    font = pygame.font.Font(None, 30)
    text0 = font.render("  ВЫ ПРОИГРАЛИ", True, 'white')
    text1 = font.render(f"  вы набрали столько баллов: {SCORE}", True, 'white')
    text2 = font.render(f"  максимальное комбо: {max_combo}", True, 'white')
    screen.blit(text0, (0, 100))
    screen.blit(text1, (0, 200))
    screen.blit(text2, (0, 200 + text1.get_size()[1]))


if __name__ == '__main__':
    pygame.init()
    size = 600, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('note game')
    screen.fill('black')

    fps = 30
    clock = pygame.time.Clock()

    player = Platform(210) # создаем платформу
    Border() # ставим границу
    note_on = False # есть ли сейчас нота на поле
    ep = False # надо ли добавлять ноту
    HP = 5
    SCORE = 0
    COMBO = 0
    max_combo = 0
    final = None # нужен ли финальный экран
    start = True # нужен ли стартовый экран

    running = True
    while running:
        screen.fill('black')
        while start: # стартовый экран, в это время все остальные функции не работают
            pygame.mouse.set_visible(True)
            set_start_screen(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start = False
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pygame.mouse.set_visible(False)
                        start = False
            pygame.display.flip()
        all_sprites.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.MOUSEMOTION: # двигаем мышь - двигаем платформу
                player.update(event.pos)
        set_stat(screen) # выводим на экран счет и хп
        if HP == 0:
            final = True
        if final: # финальный экран
            pygame.mouse.set_visible(True)
            set_final_screen(screen)
        if not note_on: # если на поле нет ноты, создаем ноту
            Note()
            note_on = True # теперь на поле есть нота
        if ep: # если мы что-то сделали с нотой (поймали/не поймали)
            note_on = False # то на поле больше нет ноты
            ep = False
        all_sprites.update()
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
    sys.exit()
