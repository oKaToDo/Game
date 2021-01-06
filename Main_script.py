import pygame

#Классы игровых объектов


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #начальное положение игрока
        self.pos_x = 100
        self.pos_y = 100
        self.last_posx = 100
        self.last_posy = 100
        self.speed = 150  # скорость пискелей в секунду

        self.image = pygame.image.load('Sprites/Ресурс 1.png')
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

        self.rect = self.image.get_rect()
        self.lastKey = ''
        self.image.set_colorkey((255, 255, 255))

    def update(self):
        #изменение координат игрока в зависимости от кнопки
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.rect.y -= self.speed // 60
            self.image = pygame.image.load('Sprites/Ресурс 1.png')
            self.lastKey = 'w'
        if key[pygame.K_s]:
            self.rect.y += self.speed // 60
            self.image = pygame.image.load('Sprites/Ресурс 3.png')
            self.lastKey = 's'
        if key[pygame.K_d]:
            self.rect.x += self.speed // 60
            self.image = pygame.image.load('Sprites/Ресурс 2.png')
            self.lastKey = 'd'
        if key[pygame.K_a]:
            self.rect.x -= self.speed // 60
            self.image = pygame.image.load('Sprites/Ресурс 4.png')
            self.lastKey = 'a'

        self.image = pygame.transform.scale(self.image, (60, 60))
        print(self.pos_x, self.pos_y, self.rect.x, self.rect.y)
        print(self.rect)

    def shoot(self):
        if self.lastKey == 'w':
            bullet = Bullet(self.rect.centerx, self.rect.top, self.lastKey)
        elif self.lastKey == 's':
            bullet = Bullet(self.rect.centerx, self.rect.bottom, self.lastKey)
        elif self.lastKey == 'a':
            bullet = Bullet(self.rect.centerx - 30, self.rect.y + 30, self.lastKey, notSide=False)
        elif self.lastKey == 'd':
            bullet = Bullet(self.rect.centerx + 30, self.rect.y + 30, self.lastKey, notSide=False)
        sprites.add(bullet)
        bullets.add(bullet)


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
        self.speed = 10

    def update(self):
        if self.dir == 'w':
            self.rect.y -= self.speed
        elif self.dir == 's':
            self.rect.y += self.speed
        elif self.dir == 'a':
            self.rect.x -= self.speed
        elif self.dir == 'd':
            self.rect.x += self.speed



class Enemy:
    pass


class Bush:
    pass


class Wall:
    pass


if __name__ == '__main__':
    pygame.init()
    running = True
    fps = 60
    size = width, height = 1280, 1000
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    player = Player()
    sprites = pygame.sprite.Group()
    sprites.add(player)
    bullets = pygame.sprite.Group()
    sprites.add(player)
    key_pressed = None
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    player.shoot()
        sprites.update()

        screen.fill((0, 0, 0))
        sprites.draw(screen)
        pygame.display.flip()
pygame.quit()