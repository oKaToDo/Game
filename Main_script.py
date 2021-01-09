import pygame
import math


# Классы игровых объектов


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # начальное положение игрока
        self.speed = 150  # скорость пискелей в секунду

        self.image = pygame.image.load('Sprites/Ресурс 1.png')
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.center = (640, 960)
        self.lastRect_x = self.rect.x
        self.lastRect_y = self.rect.y

        self.lastKey = ''
        self.image.set_colorkey((255, 255, 255))

        self.hp = 10  # хп танка (уничтожение от 2 попаданий, урон снарядом противника - 5 хп)

    def update(self):
        # изменение координат игрока в зависимости от кнопки
        key = pygame.key.get_pressed()
        sp = self.speed // 60
        if key[pygame.K_w]:
            self.rect.y -= sp
            self.image = pygame.image.load('Sprites/Ресурс 1.png')
            self.lastKey = 'w'
        elif key[pygame.K_s]:
            self.rect.y += sp
            self.image = pygame.image.load('Sprites/Ресурс 3.png')
            self.lastKey = 's'
        elif key[pygame.K_d]:
            self.rect.x += sp
            self.image = pygame.image.load('Sprites/Ресурс 2.png')
            self.lastKey = 'd'
        elif key[pygame.K_a]:
            self.rect.x -= sp
            self.image = pygame.image.load('Sprites/Ресурс 4.png')
            self.lastKey = 'a'

        self.lastRect_x = self.rect.x
        self.lastRect_y = self.rect.y
        self.image = pygame.transform.scale(self.image, (60, 60))
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
        global player, landscape
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

        self.hp = 10

    def update(self):
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        distance = math.hypot(dx, dy)
        print(distance)
        if distance > 350:
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
        elif distance <= 350:
            if self.rect.x > player.rect.x:
                self.image = pygame.image.load('Sprites/Ресурс 4.png')
                self.rect.x -= self.sp
                self.lastdir = 'a'
            elif self.rect.x < player.rect.x:
                self.image = pygame.image.load('Sprites/Ресурс 2.png')
                self.rect.x += self.sp
                self.lastdir = 'd'
            self.image = pygame.image.load('Sprites/Ресурс 3.png')
            self.image = pygame.transform.scale(self.image, (60, 60))
        self.check_collide()


    def shoot(self):
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


    def check_collide(self):
        if pygame.sprite.spritecollide(self, landscape, False, False):
            self.sp = 0
            if not self.cooldown:
                self.shoot()
                self.cooldown = 50
            else:
                self.cooldown -= 1
        else:
            self.sp = self.speed // 60



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
    global running, player, enemy
    # проверки на попадания пуль и на столкновения с объектами
    if pygame.sprite.groupcollide(enemies, player_bullets, False, True):
        enemy.hp -= 5
        if enemy.hp == 0:
            enemy.kill()

    if pygame.sprite.groupcollide(landscape, enemy_bulltes, False, True) or\
            pygame.sprite.groupcollide(landscape, player_bullets, False, True):
        wall.hp -= 5

    if pygame.sprite.spritecollide(player, enemy_bulltes, True):
        player.hp -= 5
        if player.hp == 0:
            running = False

    if pygame.sprite.spritecollide(player, landscape, False):
        player.check_border(is_collided=True)


if __name__ == '__main__':
    pygame.init()
    running = True
    cooldown_player = 0
    fps = 60
    size = width, height = 1280, 1000
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)

    player = Player()
    enemy = Enemy()
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

    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        all_sprites.update()
        check_collide()

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()