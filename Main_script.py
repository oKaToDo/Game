import pygame

#Классы игровых объектов


class Player:
    def __init__(self, fps):
        #начальное положение игрока
        self.pos_x = 100
        self.pos_y = 100
        self.speed = 80 #скорость пискелей в секунду

        self.pressedKeys = {pygame.K_w: False, pygame.K_s: False,
                            pygame.K_a: False, pygame.K_d: False}
        self.fps = fps

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



class Enemy:
    pass


class Bush:
    pass


class Wall:
    pass


def Game():
    running = True
    fps = 60
    size = width, height = 800, 600
    player = Player(fps)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    key_pressed = None
    while running:
        pygame.display.update()
        screen.fill((0, 0, 0))
        #пока что вместо спрайта танка просто кружок)
        pygame.draw.circle(screen, (0, 0, 255), (player.pos_x, player.pos_y), 20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                key_pressed = event.key
                player.pressedKeys[event.key] = True
            if event.type == pygame.KEYUP:
                player.pressedKeys[event.key] = False
                print(player.pressedKeys)
        player.move(key_pressed)

        clock.tick(fps)


if __name__ == '__main__':
    pygame.init()
    Game()
