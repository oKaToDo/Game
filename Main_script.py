import pygame

#Классы игровых объектов


class Player(pygame.sprite.Sprite):
    def __init__(self, fps):
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

        self.pressedKeys = {pygame.K_w: False, pygame.K_s: False,
                            pygame.K_a: False, pygame.K_d: False, pygame.K_SPACE: False}
        self.lastKey = ''
        self.fps = fps
        self.image.set_colorkey((255, 255, 255))

    def actions(self, key):
        #изменение координат игрока в зависимости от кнопки
        if key != None and self.pressedKeys[key]:
            if key == pygame.K_w:
                self.pos_y -= self.speed // self.fps
                self.rect.y -= self.speed // self.fps
                self.image = pygame.image.load('Sprites/Ресурс 1.png')
                self.lastKey = key
            if key == pygame.K_s:
                self.pos_y += self.speed // self.fps
                self.rect.y += self.speed // self.fps
                self.image = pygame.image.load('Sprites/Ресурс 3.png')
                self.lastKey = key
            if key == pygame.K_d:
                self.pos_x += self.speed // self.fps
                self.rect.x += self.speed // self.fps
                self.image = pygame.image.load('Sprites/Ресурс 2.png')
                self.lastKey = key
            if key == pygame.K_a:
                self.pos_x -= self.speed // self.fps
                self.rect.x -= self.speed // self.fps
                self.image = pygame.image.load('Sprites/Ресурс 4.png')
                self.lastKey = key

        self.image = pygame.transform.scale(self.image, (60, 60))
        self.last_posx = self.pos_x
        self.last_posy = self.pos_y
        print(self.pos_x, self.pos_y, self.rect.x, self.rect.y)

    def shoot(self):
        if self.lastKey == pygame.K_w:
            bullet = Bullet(self.rect.centerx, self.rect.top, self.lastKey)
        elif self.lastKey == pygame.K_s:
            bullet = Bullet(self.rect.centerx, self.rect.bottom, self.lastKey)
        elif self.lastKey == pygame.K_a:
            bullet = Bullet(self.rect.centerx, self.rect.left, self.lastKey, notSide=False)
        elif self.lastKey == pygame.K_d:
            bullet = Bullet(self.rect.centerx, self.rect.right, self.lastKey, notSide=False)
        sprites.add(bullet)
        bullets.add(bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, notSide=True):
        pygame.sprite.Sprite.__init__(self)
        self.pos_x = x
        self.pox_y = y
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
        if self.dir == pygame.K_w:
            self.rect.y -= self.speed
        elif self.dir == pygame.K_s:
            self.rect.y += self.speed
        elif self.dir == pygame.K_a:
            self.rect.x -= self.speed
        elif self.dir == pygame.K_d:
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
    player = Player(fps)
    sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    key_pressed = None
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                key_pressed = event.key
                value = True
            if event.type == pygame.KEYUP:
                value = False
                if event.key == pygame.K_SPACE:
                    player.shoot()
        if key_pressed in player.pressedKeys.keys():
            player.pressedKeys[key_pressed] = value
            player.actions(key_pressed)
        screen.blit(player.image, player.rect)
        sprites.update()
        sprites.draw(screen)
        pygame.display.flip()
        clock.tick(fps)