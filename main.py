import pygame
import os
pygame.init()

def file_path(file_name):
    folder = os.path.abspath(__file__+ "/..")
    path = os.path.join(folder, file_name)
    return path

WIN_WIDTH = 900
WIN_HEIGHT = 600
FPS = 40

fon = pygame.image.load(file_path(r"images\fone1.jpg"))
fon = pygame.transform.scale(fon,(WIN_WIDTH, WIN_HEIGHT))
image_win = pygame.image.load(file_path(r"images\wiin.jpg"))
image_win = pygame.transform.scale(image_win,(WIN_WIDTH, WIN_HEIGHT))
image_lose = pygame.image.load(file_path(r"images\defeat.jpg"))
image_lose = pygame.transform.scale(image_lose,(WIN_WIDTH, WIN_HEIGHT))
#fon



pygame.mixer.music.load(file_path(r"music\main music.wav"))
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()
music_shot = pygame.mixer.Sound(file_path(r"music\lazernyim-orujiem.ogg"))
music_shot.set_volume(0.3)
#music

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

class GameSprite(pygame.sprite.Sprite):
    def __init__ (self, x, y, widht, height, image):
        super().__init__()
        self.rect = pygame.Rect(x, y, widht, height)
        self.image = pygame.image.load(file_path(image))
        self.image = pygame.transform.scale(self.image, (widht, height))
    
    def show(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, x, y, widht, height, image, speed_x, speed_y):
        super().__init__(x, y, widht, height, image)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.direction = "left"
        self.image_l = self.image
        self.image_r = pygame.transform.flip(self.image, True, False)

    def update(self):
        if self.speed_x < 0 and self.rect.left > 0 or self.speed_x > 0 and self.rect.right < WIN_WIDTH:
            self.rect.x += self.speed_x 
        walls_touched = pygame.sprite.spritecollide(self, walls, False)
        if self.speed_x < 0:
            for wall in walls_touched:
                self.rect.left = max(self.rect.left, wall.rect.right)
        elif self.speed_x > 0:
            for wall in walls_touched:
                self.rect.right = min(self.rect.right, wall.rect.left)
        if self.speed_y < 0 and self.rect.top > 0 or self.speed_y > 0 and self.rect.bottom < WIN_HEIGHT:
            self.rect.y += self.speed_y
        walls_touched = pygame.sprite.spritecollide(self, walls, False)
        if  self.speed_y < 0:
            for wall in walls_touched:
                self.rect.top = max(self.rect.top, wall.rect.bottom)
        elif  self.speed_y > 0:
            for wall in walls_touched:
                self.rect.bottom = min(self.rect.bottom, wall.rect.top)

    def shot(self):
        if self.direction == "right":
            bullet = Bullet(self.rect.right, self.rect.centery, 10, 10, r"images\magical.png", 3)
        elif self.direction == "left":
            bullet = Bullet(self.rect.left -10, self.rect.centery, 10, 10, r"images\magical.png", -3)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, x, y, width, height, image, min_cord, max_cord, direction, speed):
        super().__init__(x, y, width, height, image)
        self.min_cord = min_cord
        self.max_cord = max_cord
        self.speed = speed
        self.direction = direction
        
    def update(self):
        if self.direction == "left" or self.direction == "right":
            if self.direction == "left":
                self.rect.x -= self.speed
            elif self.direction == "right":
                self.rect.x += self.speed
            
            if self.rect.right >= self.max_cord:
                self.direction = "left"
            elif self.rect.left <= self.min_cord:
                self.direction = "right"

        elif self.direction == "up" or self.direction == "down":
            if self.direction == "up":
                self.rect.y -= self.speed
            elif self.direction == "down":
                self.rect.y += self.speed

            if self.rect.bottom >= self.max_cord:
                self.direction = "up"
            elif self.rect.top <= self.min_cord:
                self.direction = "down"

class Bullet(GameSprite):
    def __init__ (self, x, y, width, height, image, speed):
        super().__init__(x, y, width, height, image)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.left >= WIN_WIDTH or self.rect.right <= 0:
            self.kill()

bullets = pygame.sprite.Group()

player = Player(290, 0, 25, 20, r"images\play.png", 0, 0)
target = GameSprite(630, 540, 40, 40, r"images\target.png")
#player, target

enemys = pygame.sprite.Group()
enemy = Enemy(600, 390, 40, 30, r"images\enemys.png", 180, 420, "up", 2)
enemy2 = Enemy(125, 90, 60, 70, r"images\enem.png", 90, 520, "up", 3)
enemy3 = Enemy (270, 180, 30, 50, r"images\ene.png", 165, 340, "up", 2)
"""enemy4 = Enemy ()"""
enemys.add(enemy, enemy2, enemy3)
#enemy/s

walls = pygame.sprite.Group()
wall_1 = GameSprite(115, 77, 170, 15, r"images\wall2.jpg")
walls.add(wall_1)
wall_2 = GameSprite(115, 90, 15, 435, r"images\wall2.jpg")
walls.add(wall_2)
wall_3 = GameSprite(130, 515, 490, 10, r"images\wall2.jpg")
walls.add(wall_3)
wall_4 = GameSprite(775, 80, 10, 446, r"images\wall2.jpg")
walls.add(wall_4)
wall_5 = GameSprite(680, 515, 105, 10, r"images\wall2.jpg")
walls.add(wall_5)
wall_6 = GameSprite(345, 77, 440, 10, r"images\wall2.jpg")
walls.add(wall_6)
wall_7 = GameSprite(345, 77, 15, 50, r"images\wall2.jpg")
walls.add(wall_7)
wall_8 = GameSprite(345, 120, 380, 10, r"images\wall2.jpg")
walls.add(wall_8)
wall_9 = GameSprite(710, 130, 15, 355, r"images\wall2.jpg")
walls.add(wall_9)
wall_10 = GameSprite(178, 475, 532, 10, r"images\wall2.jpg")
walls.add(wall_10)
wall_11 = GameSprite(178, 308, 15, 177, r"images\wall2.jpg")
walls.add(wall_11)
wall_12 = GameSprite(178, 120, 15, 147, r"images\wall2.jpg")
walls.add(wall_12)
wall_13 = GameSprite(178, 120, 100, 10, r"images\wall2.jpg")
walls.add(wall_13)
wall_14 = GameSprite(273, 80, 15, 95, r"images\wall2.jpg")
walls.add(wall_14)
wall_15 = GameSprite(247, 163, 408, 15, r"images\wall2.jpg")
walls.add(wall_15)
wall_16 = GameSprite(640, 163, 15, 272, r"images\wall2.jpg")
walls.add(wall_16)
wall_17 = GameSprite(247, 428, 406, 10, r"images\wall2.jpg")
walls.add(wall_17)
wall_18 = GameSprite(247, 380, 15, 49, r"images\wall2.jpg")
walls.add(wall_18)
wall_19 = GameSprite(178, 330, 152, 10, r"images\wall2.jpg")
walls.add(wall_19)
wall_20 = GameSprite(247, 218, 15, 123, r"images\wall2.jpg")
walls.add(wall_20)
wall_21 = GameSprite(320, 300, 15, 90, r"images\wall2.jpg")
walls.add(wall_21)
wall_22 = GameSprite(335, 380, 250, 10, r"images\wall2.jpg")
walls.add(wall_22)
wall_23 = GameSprite(335, 300, 50, 10, r"images\wall2.jpg")
walls.add(wall_23)
wall_24 = GameSprite(571, 214, 15, 170, r"images\wall2.jpg")
walls.add(wall_24)
wall_25 = GameSprite(470, 212, 100, 10, r"images\wall2.jpg")
walls.add(wall_25)
wall_26 = GameSprite(320, 212, 100, 10, r"images\wall2.jpg")
walls.add(wall_26)
wall_27 = GameSprite(318, 212, 15, 48, r"images\wall2.jpg")
walls.add(wall_27)
wall_28 = GameSprite(410, 179, 10, 80, r"images\wall2.jpg")
walls.add(wall_28)
wall_29 = GameSprite(374, 250, 152, 10, r"images\wall2.jpg")
walls.add(wall_29)
wall_30 = GameSprite(515, 250, 10, 103, r"images\wall2.jpg")
walls.add(wall_30)
wall_31 = GameSprite(374, 341, 144, 10, r"images\wall2.jpg")
walls.add(wall_31)
#wall/s

level = 1
game = True

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if level == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    player.speed_x = 3
                    player.direction = "right"
                    player.image = player.image_r
                if event.key == pygame.K_a:
                    player.direction = "left"
                    player.image = player.image_l
                    player.speed_x = -3
                if event.key == pygame.K_w:
                    player.speed_y = -3
                if event.key == pygame.K_s:
                    player.speed_y = 3
                if event.key == pygame.K_SPACE:
                    player.shot()
                    music_shot.play()
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    player.speed_x = 0
                if event.key == pygame.K_a:
                    player.speed_x = 0
                if event.key == pygame.K_w:
                    player.speed_y = 0
                if event.key == pygame.K_s:
                    player.speed_y = 0

    if level == 1:
        window.blit(fon, (0, 0))
        player.show()
        player.update()
        enemys.draw(window)
        enemys.update()
        target.show()
        walls.draw(window)
        bullets.draw(window)
        bullets.update()

        if pygame.sprite.collide_rect(player, target):
            level = 10
            pygame.mixer.music.load(file_path(r"music\welcome.wav"))
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play()

        
        if pygame.sprite.spritecollide(player, enemys, False):
            level = 11
            pygame.mixer.music.load(file_path(r"music\failsound.mp3"))
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.3)
        pygame.sprite.groupcollide(bullets, walls, True, False)
        pygame.sprite.groupcollide(bullets, enemys, True, True)
        
    elif level == 10:
        window.blit(image_win,(0, 0))
    elif level == 11:
        window.blit(image_lose,(0,0))


    clock.tick(FPS)
    pygame.display.update()