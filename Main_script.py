import pygame
import math
from random import random, choice


# Классы игровых объектов

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # начальное положение игрока
        self.speed = 120  # скорость пискелей в секунду

        self.image = pygame.image.load('Sprites/forward/forward7.PNG')
        self.image.set_colorkey((255, 255, 255))
        self.load_images()
        self.last_anim = 0

        self.rect = self.image.get_rect()
        self.rect.center = (640, 860)
        self.lastRect_x = self.rect.x
        self.lastRect_y = self.rect.y

        self.lastKey = ''

        self.hp = 20  # хп танка (уничтожение от 4 попаданий, урон снарядом противника - 5 хп)
        self.sp = self.speed // 60

    def load_images(self):
        self.player_anim_forward = []
        for i in range(1, 9):
            self.player_anim_forward.append(pygame.image.load('Sprites/forward/forward{id}.png'.format(id=str(i))))
        self.player_anim_forward.reverse()

        self.player_anim_back = []
        for i in range(1, 9):
            self.player_anim_back.append(pygame.image.load('Sprites/back/back{id}.png'.format(id=str(i))))

        self.player_anim_left = []
        for i in range(1, 9):
            self.player_anim_left.append(pygame.image.load('Sprites/left/left{id}.png'.format(id=str(i))))
        self.player_anim_left.reverse()

        self.player_anim_right = []
        for i in range(1, 9):
            self.player_anim_right.append(pygame.image.load('Sprites/right/right{id}.png'.format(id=str(i))))
        self.player_anim_right.reverse()

    def check_anim(self):
        self.last_anim += 1
        if self.last_anim == 8:
            self.last_anim = 0

    def update(self):
        # изменение координат игрока в зависимости от кнопки
        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            self.rect.y -= self.sp
            self.image = self.player_anim_forward[self.last_anim]
            self.check_anim()
            self.lastKey = 'w'
        elif key[pygame.K_s]:
            self.rect.y += self.sp
            self.image = self.player_anim_back[self.last_anim]
            self.check_anim()
            self.lastKey = 's'
        elif key[pygame.K_d]:
            self.rect.x += self.sp
            self.image = self.player_anim_right[self.last_anim]
            self.check_anim()
            self.lastKey = 'd'
        elif key[pygame.K_a]:
            self.rect.x -= self.sp
            self.image = self.player_anim_left[self.last_anim]
            self.check_anim()
            self.lastKey = 'a'

        self.lastRect_x = self.rect.x
        self.lastRect_y = self.rect.y
        self.check_border()

    def shoot(self):

        bullet = Bullet(self.rect.centerx, self.rect.top, 'w')
        if self.lastKey == 'w':
            bullet = Bullet(self.rect.centerx, self.rect.top, self.lastKey)
        elif self.lastKey == 's':
            bullet = Bullet(self.rect.centerx, self.rect.bottom, self.lastKey)
        elif self.lastKey == 'a':
            bullet = Bullet(self.rect.centerx - 30, self.rect.y + 30, self.lastKey, notSide=False)
        elif self.lastKey == 'd':
            bullet = Bullet(self.rect.centerx + 30, self.rect.y + 30, self.lastKey, notSide=False)
        all_sprites.add(bullet)
        player_bullets.add(bullet)

    def check_border(self, is_collided=False):
        if is_collided is False:
            if self.rect.left + self.sp < 260:
                self.rect.left = 260
            if self.rect.right + self.sp > 1040:
                self.rect.right = 1040
            if self.rect.top + self.sp < 0:
                self.rect.top = 0
            if self.rect.bottom + self.sp > 1000:
                self.rect.bottom = 1000

        if pygame.sprite.spritecollide(self, landscape, False) or \
                pygame.sprite.spritecollide(self, iron_landscape, False):
            # игрок не движется при столкновении с препятствием так как из его координат вычитается скорость
            if self.lastKey == 'w':
                self.rect.y = self.rect.y + self.sp
            elif self.lastKey == 's':
                self.rect.y = self.rect.y - self.sp
            elif self.lastKey == 'a':
                self.rect.x = self.rect.x + self.sp
            elif self.lastKey == 'd':
                self.rect.x = self.rect.x - self.sp


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, notSide=True):
        pygame.sprite.Sprite.__init__(self)
        self.dir = direction

        if notSide is False:
            self.image = pygame.Surface((15, 10))
        else:
            self.image = pygame.Surface((10, 20))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 20

    def update(self):
        if self.dir == 'w':
            self.rect.y -= self.speed
        elif self.dir == 's':
            self.rect.y += self.speed
        elif self.dir == 'a':
            self.rect.x -= self.speed
        elif self.dir == 'd':
            self.rect.x += self.speed

        if self.rect.left < 0 or self.rect.right > 1280 or \
                self.rect.top < 0 or self.rect.bottom > 1000:
            self.kill()


class Enemy(Player):
    def __init__(self):
        global player_base, landscape, player, way
        pygame.sprite.Sprite.__init__(self)
        self.speed = 110  # скорость пискелей в секунду
        self.is_ready_to_shoot = False
        self.cooldown = 0
        self.sp = self.speed // 60
        self.lastdir = 's'
        self.target_to_move = [640, 960]
        self.direction = choice(['r', 'l'])
        self.last_anim = 0
        self.alarm = False
        self.see_player = True

        self.load_images()
        self.image = pygame.image.load('Sprites/forward/forward7.PNG')
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.center = (630, 40)
        self.rect.inflate_ip(-20, 0)

        self.image.set_colorkey((255, 255, 255))

        self.hp = 15

    def load_images(self):
        self.player_anim_forward = []
        for i in range(1, 9):
            self.player_anim_forward.append(pygame.image.load('Sprites/forward/forward{id}.png'.format(id=str(i))))
        self.player_anim_forward.reverse()

        self.player_anim_back = []
        for i in range(1, 9):
            self.player_anim_back.append(pygame.image.load('Sprites/back/back{id}.png'.format(id=str(i))))

        self.player_anim_left = []
        for i in range(1, 9):
            self.player_anim_left.append(pygame.image.load('Sprites/left/left{id}.png'.format(id=str(i))))
        self.player_anim_left.reverse()

        self.player_anim_right = []
        for i in range(1, 9):
            self.player_anim_right.append(pygame.image.load('Sprites/right/right{id}.png'.format(id=str(i))))
        self.player_anim_right.reverse()

    def update(self):
        # рассчет дистанции до базы игрока и до самого игрока

        base_x, base_y = player_base.rect.x - self.rect.x, player_base.rect.y - self.rect.y
        player_x, player_y = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        distance = math.hypot(base_x, base_y)
        distance_to_player = math.hypot(player_x, player_y)

        self.mask = pygame.mask.from_surface(self.image)
        if distance_to_player > 300 and (self.rect.right != self.rect.centerx or \
                                         self.rect.centery != player.rect.centery):
            # движение к базе
            self.alarm = False
            if self.target_to_move[1] != self.rect.centery:
                if self.sp != 0:
                    print(self.target_to_move)
                    if self.rect.x > self.target_to_move[0]:
                        self.image = self.player_anim_left[self.last_anim]
                        self.check_anim()
                        self.rect.x -= self.sp
                        self.lastdir = 'a'
                    elif self.rect.x < self.target_to_move[0]:
                        self.image = self.player_anim_right[self.last_anim]
                        self.check_anim()
                        self.rect.x += self.sp
                        self.lastdir = 'd'
                    elif self.rect.y < self.target_to_move[1]:
                        self.image = self.player_anim_back[self.last_anim]
                        self.check_anim()
                        self.rect.y += self.sp
                        self.lastdir = 's'
                    elif self.rect.y > self.target_to_move[1]:
                        self.image = self.player_anim_forward[self.last_anim]
                        self.check_anim()
                        self.rect.y -= self.sp
                        self.lastdir = 'w'
                else:
                    pass
            else:
                self.target_to_move = player_base.rect.center
                if distance > 200:
                    if self.rect.x > self.target_to_move[0]:
                        self.image = self.player_anim_left[self.last_anim]
                        self.check_anim()
                        self.rect.x -= self.sp
                        self.lastdir = 'a'
                    elif self.rect.x < self.target_to_move[0]:
                        self.image = self.player_anim_right[self.last_anim]
                        self.check_anim()
                        self.rect.x += self.sp
                        self.lastdir = 'd'
                else:
                    self.shoot()
            self.check_collide()
        else:
            self.alarm = True
            if self.rect.x > player.rect.x:
                self.image = self.player_anim_left[self.last_anim]
                self.check_anim()
                self.rect.x -= self.sp
                self.lastdir = 'a'
            elif self.rect.x < player.rect.x:
                self.image = self.player_anim_right[self.last_anim]
                self.check_anim()
                self.rect.x += self.sp
                self.lastdir = 'd'
            self.shoot()
            self.check_collide()

    def shoot(self):
        if not self.cooldown:
            if self.lastdir == 'w':
                bullet = Bullet(self.rect.centerx - 7, self.rect.top, self.lastdir)
            elif self.lastdir == 's':
                bullet = Bullet(self.rect.centerx + 7, self.rect.bottom, self.lastdir)
            elif self.lastdir == 'a':
                bullet = Bullet(self.rect.centerx - 30, self.rect.y + 30, self.lastdir, notSide=False)
            elif self.lastdir == 'd':
                bullet = Bullet(self.rect.centerx + 30, self.rect.y + 30, self.lastdir, notSide=False)
            all_sprites.add(bullet)
            enemy_bulltes.add(bullet)
            self.cooldown = 50
        else:
            self.cooldown -= 1

    def check_collide(self):
        wall = pygame.sprite.spritecollide(self, landscape, False)
        iron = pygame.sprite.spritecollide(self, iron_landscape, False)

        if wall:
            print('wall')
            self.sp = 0
            if self.alarm:
                self.rect.y -= 10
                self.sp = self.speed // 60
                return
            self.shoot()
        else:
            self.sp = self.speed // 60
            self.alarm = False

        if iron:
            self.rect.y -= 15
            if self.direction == 'r':
                if self.target_to_move[0] + 30 < 1280:
                    self.target_to_move[0] += 30
            elif self.direction == 'l':
                if self.target_to_move[0] - 40 > 0:
                    self.target_to_move[0] -= 40
            print('iron')

        if pygame.sprite.spritecollide(player, bushes, False):
            self.see_player = False
        else:
            self.see_player = True

        if pygame.sprite.spritecollide(self, players, False):
            self.shoot()


class Player_base(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.hp = 15

        self.image = pygame.image.load('Sprites/base.PNG')
        self.rect = self.image.get_rect()
        self.rect.center = (642, 960)

    def update(self):
        global running
        if self.hp == 0:
            running = False
            game_menu()


class Iron(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('Sprites/железная стенка.png')
        self.rect = self.image.get_rect()
        self.rect.center = (start_x, start_y)
        self.image.set_colorkey((255, 255, 255))

    def update(self):
        if pygame.sprite.spritecollide(self, player_bullets, True) or \
                pygame.sprite.spritecollide(self, enemy_bulltes, True):
            pass


class Bush(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('Sprites/кустик.png')
        self.rect = self.image.get_rect()
        self.rect.center = (start_x, start_y)
        self.image.set_colorkey((255, 255, 255))


class Wall(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('Sprites/brick.png')
        self.rect = self.image.get_rect()
        self.rect.center = (start_x, start_y)
        self.image.set_colorkey((255, 255, 255))
        self.hp = 20

    def update(self):
        if pygame.sprite.spritecollide(self, enemy_bulltes, True) or \
                pygame.sprite.spritecollide(self, player_bullets, True):
            self.hp -= 5
        if self.hp == 15:
            self.image = pygame.image.load('Sprites/first.png')
        elif self.hp == 10:
            self.image = pygame.image.load('Sprites/second.png')
        elif self.hp == 5:
            self.image = pygame.image.load('Sprites/third_2.png')
        elif self.hp == 0:
            self.kill()


def check_collide():
    global running, player, enemy, player_base, explosion
    # проверки на попадания пуль и на столкновения с объектами
    if pygame.sprite.groupcollide(enemies, player_bullets, False, True):
        enemy.hp -= 5
        if enemy.hp == 0:
            for i in range(3):
                enemy.image = explosion[i]
            enemy.kill()
            enemies.remove(enemy)
            all_sprites.remove(enemy)

    if pygame.sprite.spritecollide(player_base, enemy_bulltes, True):
        player_base.hp -= 5
        if player_base.hp == 0:
            for i in range(3):
                player_base.image = explosion[i]
            all_sprites.remove(player_base)
            running = False

    if pygame.sprite.spritecollide(player, enemy_bulltes, True):
        player.hp -= 5
        if player.hp == 0:
            for i in range(3):
                player.image = explosion[i]
            running = False

    if pygame.sprite.groupcollide(player_bullets, iron_landscape, True, False) or \
            pygame.sprite.groupcollide(enemy_bulltes, iron_landscape, True, False):
        pass


def print_text(message, x, y, font_color=(0, 0, 0), font_size=30):
    font_type = pygame.font.SysFont('arial', font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


class Button():
    def __init__(self, width, height, message):
        self.message = message
        self.width = width
        self.height = height
        self.inactive_clr = (136, 69, 53)
        self.active_clr = (120, 50, 40)

    def draw(self, x, y, message, font_size=30, action=None, button_sound=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.active_clr, (x, y, self.width, self.height))

            if click[0] == 1:
                pygame.time.delay(300)
                if action is not None:
                    if action == quit:
                        pygame.quit()
                        quit()
                    else:
                        action()

        else:
            pygame.draw.rect(screen, self.inactive_clr, (x, y, self.width, self.height))

        print_text(message=self.message, x=x + 10, y=y + 10, font_size=font_size)


def game_menu():
    size = width, height = 600, 500
    screen = pygame.display.set_mode(size)
    menu = pygame.image.load('Sprites/логотип.png')
    menu = pygame.transform.scale(menu, (381, 241))
    menu.set_colorkey((255, 255, 255))

    button_for_start = Button(250, 70, 'Start')
    button_for_quit = Button(120, 70, 'Exit')

    show = True

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            screen.blit(menu, (150, 35))
            button_for_start.draw(170, 320, 'Начать игру', action=start_game)
            button_for_quit.draw(230, 400, 'Выйти из игры', action=quit)

            pygame.display.update()
            pygame.display.flip()
            clock.tick(60)


def load_map():
    global landscape, all_sprites, iron_poses
    landscape_pos = {
        0: [650, 500], 1: [590, 500], 2: [710, 500], 3: [770, 560], 4: [830, 560], 5: [890, 560], 6: [890, 500],
        7: [890, 440], 8: [830, 440], 9: [770, 440], 10: [290, 740], 11: [950, 500], 12: [1010, 500], 13: [1010, 560],
        14: [1010, 440], 15: [410, 560], 16: [530, 560],
        17: [470, 560], 18: [410, 560], 19: [470, 440], 20: [530, 440], 21: [410, 440], 22: [410, 500], 23: [350, 500],
        24: [290, 500], 25: [290, 440], 26: [290, 560],
        27: [290, 260], 28: [410, 260], 29: [530, 260], 30: [650, 260], 31: [770, 260], 32: [890, 260], 33: [1010, 260],
        34: [1010, 740], 35: [890, 740], 36: [770, 740],
        37: [650, 740], 38: [530, 740], 39: [410, 740]
    }
    bush_pos = {0: [290, 620], 1: [350, 620], 2: [350, 560], 3: [410, 620], 4: [470, 620], 5: [530, 620], 6: [590, 620],
                7: [650, 620], 8: [710, 620], 9: [770, 620],
                10: [830, 620], 11: [890, 620], 12: [950, 620], 13: [950, 560], 14: [1010, 620], 15: [290, 380],
                16: [350, 380],
                17: [350, 440], 18: [410, 380], 19: [470, 380], 20: [530, 380], 21: [590, 380],
                22: [650, 380], 23: [710, 380], 24: [770, 380], 25: [830, 380], 26: [890, 380],
                27: [950, 380], 28: [950, 440], 29: [1010, 380]
                }
    iron_pos = {0: [650, 560], 1: [710, 560], 2: [590, 560], 3: [650, 440], 4: [710, 440], 5: [590, 440], 6: [770, 500],
                7: [830, 500], 8: [530, 500], 9: [470, 500], 10: [350, 260],
                11: [470, 260], 12: [0, 0], 13: [0, 0], 14: [830, 260], 15: [950, 260],
                16: [350, 740], 17: [470, 740], 18: [590, 740], 19: [710, 740], 20: [830, 740],
                21: [950, 740]
                }

    for a in range(40):
        wall = Wall(landscape_pos[a][0], landscape_pos[a][1])
        landscape.add(wall)
        all_sprites.add(wall)
    for a in range(30):
        bush = Bush(bush_pos[a][0], bush_pos[a][1])
        bushes.add(bush)
        all_sprites.add(bush)
    for a in range(22):
        iron_wall = Iron(iron_pos[a][0], iron_pos[a][1])
        iron_landscape.add(iron_wall)
        all_sprites.add(iron_wall)


def start_game():
    global clock
    running = True
    fps = 60
    waves = 5
    size = width, height = 1280, 1000
    screen = pygame.display.set_mode(size)
    player_cooldown = pygame.USEREVENT + 2
    cooldown_shoot = False

    load_map()

    pygame.time.set_timer(player_cooldown, 1000)

    rect_color = (255, 0, 0)

    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_menu()

            if event.type == player_cooldown:
                cooldown_shoot = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and cooldown_shoot is False:
                    player.shoot()
                    pygame.time.set_timer(player_cooldown, 1000)
                    cooldown_shoot = True

                elif event.key == pygame.K_ESCAPE:
                    running = False
                    game_menu()

        all_sprites.update()
        if len(enemies) == 0 and waves != 0:
            enemy = Enemy()
            enemies.add(enemy)
            all_sprites.add(enemy)
            waves -= 1
        check_collide()

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        # pygame.draw.rect(screen, rect_color, enemy.rect)
        pygame.display.flip()

    for i in range(1, 4):
        explosion.append((pygame.image.load('Sprites/explosion/explosion{id}.png'.format(id=str(i)))))

    pygame.time.set_timer(player_cooldown, 1000)
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == player_cooldown:
                cooldown_shoot = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and cooldown_shoot is False:
                    player.shoot()
                    pygame.time.set_timer(player_cooldown, 1000)
                    cooldown_shoot = True

        all_sprites.update()
        if len(enemies) == 0 and waves != 0:
            if waves != 5:
                enemy = Enemy()
                enemies.add(enemy)
                all_sprites.add(enemy)
                waves -= 1
            else:
                print('BOOOOOOOOOOOOOSS!')
                enemy = Enemy()
                enemy.hp = 30
        check_collide()

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()


pygame.init()
running = True
fps = 60
size = width, height = 600, 800
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
waves = 5
all_sprites = pygame.sprite.Group()
landscape = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bulltes = pygame.sprite.Group()
enemies = pygame.sprite.Group()
players = pygame.sprite.Group()
iron_landscape = pygame.sprite.Group()
bushes = pygame.sprite.Group()

player = Player()
players.add(player)
enemy = Enemy()
player_base = Player_base()
enemies.add(enemy)

all_sprites.add(player)
all_sprites.add(enemy)
landscape.add(player_base)
all_sprites.add(player_base)
explosion = []

for i in range(1, 4):
    explosion.append((pygame.image.load('Sprites/explosion/explosion{id}.png'.format(id=str(i)))))

game_menu()
