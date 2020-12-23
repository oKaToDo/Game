import pygame

#Классы игровых объектов


class Player(pygame.sprite.Sprite):
    def __init__(self, fps, screen):
        pygame.sprite.Sprite.__init__(self)
        #начальное положение игрока
        self.pos_x = 100
        self.pos_y = 100
        self.speed = 90  # скорость пискелей в секунду

        self.image = pygame.image.load('Sprites/Ресурс 1.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

        self.pressedKeys = {pygame.K_w: False, pygame.K_s: False,
                            pygame.K_a: False, pygame.K_d: False}
        self.fps = fps
        self.sprite = pygame.image.load('Sprites/Player.png')
        self.sprite.set_colorkey((255, 255, 255))

    def move(self, key):
        #изменение координат игрока в зависимости от кнопки
        print(self.pressedKeys)
        if key != None and self.pressedKeys[key]:
            if key == pygame.K_w:
                self.pos_y -= self.speed / self.fps
            if key == pygame.K_s:
                self.pos_y += self.speed / self.fps
            if key == pygame.K_d:
                self.pos_x += self.speed / self.fps
            if key == pygame.K_a:
                self.pos_x -= self.speed / self.fps
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))



class Enemy:
    pass


class Bush:
    pass


class Wall:
    pass


def Game():
    running = True
    fps = 60
    size = width, height = 1280, 1000
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    player = Player(fps, screen)
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
                print(player.pressedKeys)
        if key_pressed in player.pressedKeys.keys():
            player.pressedKeys[key_pressed] = value
            player.move(key_pressed)
        screen.blit(player.image, player.rect)
        pygame.display.update()
        clock.tick(fps)


if __name__ == '__main__':
    pygame.init()
    Game()
