import pygame
import math


# Классы игровых объектов

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # начальное положение игрока
        self.speed = 150  # скорость пискелей в секунду

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
        sp = self.speed // 60
        if key[pygame.K_w]:
            self.rect.y -= sp
            self.image = self.player_anim_forward[self.last_anim]
            self.check_anim()
            self.lastKey = 'w'
        elif key[pygame.K_s]:
            self.rect.y += sp
            self.image = self.player_anim_back[self.last_anim]
            self.check_anim()
            self.lastKey = 's'
        elif key[pygame.K_d]:
            self.rect.x += sp
            self.image = self.player_anim_right[self.last_anim]
            self.check_anim()
            self.lastKey = 'd'
        elif key[pygame.K_a]:
            self.rect.x -= sp
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
        sp = self.speed // 60
        if is_collided is False:
            if self.rect.left + sp < 0:
                self.rect.left = 0
            if self.rect.right + sp > 1280:
                self.rect.right = 1280
            if self.rect.top + sp < 0:
                self.rect.top = 0
            if self.rect.bottom + sp > 1000:
                self.rect.bottom = 1000
        else:
            #игрок не движется при столкновении с препятствием так как из его координат вычитается скорость
            if self.lastKey == 'w':
                self.rect.y = self.rect.y + sp
            elif self.lastKey == 's':
                self.rect.y = self.rect.y - sp
            elif self.lastKey == 'a':
                self.rect.x = self.rect.x + sp
            elif self.lastKey == 'd':
                self.rect.x = self.rect.x - sp



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
        global player_base, landscape, player
        pygame.sprite.Sprite.__init__(self)
        self.speed = 150  # скорость пискелей в секунду
        self.is_ready_to_shoot = False
        self.cooldown = 0
        self.sp = self.speed // 60
        self.lastdir = 's'

        self.image = pygame.image.load('Sprites/Ресурс 3.png')
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.center = (640, 40)

        self.image.set_colorkey((255, 255, 255))

        self.hp = 15

    def update(self):
        # рассчет дистанции до базы игрока и до самого игрока

        base_x, base_y = player_base.rect.x - self.rect.x, player_base.rect.y - self.rect.y
        player_x, player_y = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        distance = math.hypot(base_x, base_y)
        distance_to_player = math.hypot(player_x, player_y)

        # главная задача ИИ - уничтожить базу игрока, поэтому они движутся в сторону базы, а если встретят игрока,
        # то сначала уничтожают его

        if distance_to_player > 300:
            # движение к базе
            if distance > 150:
                if self.rect.x > player_base.rect.x:
                    self.image = pygame.image.load('Sprites/Ресурс 4.png')
                    self.rect.x -= self.sp
                    self.lastdir = 'a'
                elif self.rect.x < player_base.rect.x:
                    self.image = pygame.image.load('Sprites/Ресурс 2.png')
                    self.rect.x += self.sp
                    self.lastdir = 'd'
                elif self.rect.y < player_base.rect.y:
                    self.image = pygame.image.load('Sprites/Ресурс 3.png')
                    self.rect.y += self.sp
                    self.lastdir = 's'
                elif self.rect.y > player_base.rect.y:
                    self.image = pygame.image.load('Sprites/Ресурс 1.png')
                    self.rect.y -= self.sp
                    self.lastdir = 'w'
                self.image = pygame.transform.scale(self.image, (60, 60))
            else:
                self.shoot()
        else:
            # движение за игроком
            if distance_to_player > 250:
                if self.rect.x > player.rect.x:
                    self.image = pygame.image.load('Sprites/Ресурс 4.png')
                    self.rect.x -= self.sp
                    self.lastdir = 'a'
                elif self.rect.x < player.rect.x:
                    self.image = pygame.image.load('Sprites/Ресурс 2.png')
                    self.rect.x += self.sp
                    self.lastdir = 'd'
                elif self.rect.y < player.rect.y:
                    self.image = pygame.image.load('Sprites/Ресурс 3.png')
                    self.rect.y += self.sp
                    self.lastdir = 's'
                elif self.rect.y > player.rect.y:
                    self.image = pygame.image.load('Sprites/Ресурс 1.png')
                    self.rect.y -= self.sp
                    self.lastdir = 'w'
                self.image = pygame.transform.scale(self.image, (60, 60))
            else:
                self.shoot()
        self.check_collide()


    def shoot(self):
        if not self.cooldown:
            if self.lastdir == 'w':
                bullet = Bullet(self.rect.centerx, self.rect.top, self.lastdir)
            elif self.lastdir == 's':
                bullet = Bullet(self.rect.centerx, self.rect.bottom, self.lastdir)
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
        if pygame.sprite.spritecollide(self, landscape, False, False):
            self.sp = 0
            self.shoot()
        else:
            self.sp = self.speed // 60

class Player_base(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.hp = 15

        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (640, 960)

    def update(self):
        pass




class Bush(pygame.sprite.Sprite):
    pass


class Wall(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('Sprites/brick.png')
        self.rect = self.image.get_rect()
        self.rect.center = (start_x, start_y)
        self.image.set_colorkey((255, 255, 255))
        self.hp = 20

    def update(self):
        if self.hp == 15:
            pass
        elif self.hp == 10:
            pass
        elif self.hp == 5:
            pass
        elif self.hp == 0:
            self.kill()

def check_collide():
    global running, player, enemy, player_base, explosion
    # проверки на попадания пуль и на столкновения с объектами
    if pygame.sprite.groupcollide(enemies, player_bullets, False, True):
        enemy.hp -= 5
        if enemy.hp == 0:
            enemy.kill()
            enemies.remove(enemy)
            all_sprites.remove(enemy)

    if pygame.sprite.spritecollide(player_base, enemy_bulltes, True):
        player_base.hp -= 5
        if player_base.hp == 0:
            for i in range(3):
                player_base.image = explosion[i]
            running = False

    if pygame.sprite.groupcollide(landscape, enemy_bulltes, False, True) or\
            pygame.sprite.groupcollide(landscape, player_bullets, False, True):
        wall.hp -= 5

    if pygame.sprite.spritecollide(player, enemy_bulltes, True):
        player.hp -= 5
        if player.hp == 0:
            for i in range(3):
                player.image = explosion[i]
            running = False

    if pygame.sprite.spritecollide(player, landscape, False):
        player.check_border(is_collided=True)


if __name__ == '__main__':
    pygame.init()
    running = True
    fps = 60
    size = width, height = 1280, 1000
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    waves = 5
    player_cooldown = pygame.USEREVENT + 2
    cooldown_shoot = False

    player = Player()
    enemy = Enemy()
    player_base = Player_base()
    all_sprites = pygame.sprite.Group()
    landscape = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    enemy_bulltes = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    enemies.add(enemy)

    all_sprites.add(player)
    all_sprites.add(enemy)
    for _ in range(1):
        wall = Wall(640, 500)
        landscape.add(wall)
        all_sprites.add(wall)
    landscape.add(player_base)
    all_sprites.add(player_base)
    explosion = []
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
            enemy = Enemy()
            enemies.add(enemy)
            all_sprites.add(enemy)
            waves -= 1
        check_collide()

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()