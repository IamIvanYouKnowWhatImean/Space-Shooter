#   Импорт
from pygame import *
from random import randint



#   Окно приложения:
window = display.set_mode((700, 500))
display.set_caption('Space Shooter')

background = transform.scale(image.load('galaxy.jpg'),(700, 500))

window.blit(background, (0, 0))

#   Фоновая музыка:
mixer.init()

mixer.music.load('space.ogg')
mixer.music.play()



#   Частота кадров:
clock = time.Clock()
FPS = 60



#   Спрайты:
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_lenght, player_width):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(player_lenght, player_width))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

ammo = sprite.Group()
class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_lenght, player_width):
        super().__init__(player_image, player_x, player_y, player_speed, player_lenght, player_width)
    def key_movement(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 1:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 630:
            self.rect.x += self.speed
        if keys_pressed[K_LEFT] and self.rect.x > 1:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10, 10, 15)
        ammo.add(bullet)

misses = 0
class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_lenght, player_width):
        super().__init__(player_image, player_x, player_y, player_speed, player_lenght, player_width)
    def update(self):
        global misses
        if self.rect.y < 501:
            self.rect.y += self.speed
            misses += 1
        else:
            self.rect.y = -70
            self.rect.x = randint(0, 630)

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_lenght, player_width):
        super().__init__(player_image, player_x, player_y, player_speed, player_lenght, player_width)
    def update(self):
        self.rect.y -= self.speed




rocket = Player('rocket.png', 310, 428, 7, 70, 70)

aliens = sprite.Group()
for i in range(5):
    alien = Enemy('ufo.png', randint(0, 630), randint(-500, -300), randint(3, 6), 70, 70)
    aliens.add(alien)



#   Игровой цикл:
shot = mixer.Sound('fire.ogg')

game_loop = True
while game_loop:
    window.blit(background, (0, 0))
    rocket.reset()
    rocket.key_movement()

    keys_pressed = key.get_pressed()
    if keys_pressed[K_SPACE]:
        shot.play()
        rocket.fire()
    ammo.update()

    aliens.draw(window)
    ammo.draw(window)
    aliens.update()
    for e in event.get():
        if e.type == QUIT:
            game_loop = False

    clock.tick(FPS)

    display.update()