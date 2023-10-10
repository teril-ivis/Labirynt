import pygame
import os
pygame.init()

def file_path(file_name):
    folder = os.path.abspath(__file__+ "/..")
    path = os.path.join(folder, file_name)
    return path
#setting and start
WIN_WIDTH = 900
WIN_HEIGHT = 600
FPS = 40

FUCHSIA = (255,222,173)
AMET = (176,196,222)
ORHI = (188,143,143)
FIOL = (147, 112, 219)
BLACK = (0, 0, 0)
WHITE2 = (255, 255, 255)
#color/s

fon = pygame.image.load(file_path(r"images\fone1.jpg"))
fon = pygame.transform.scale(fon,(WIN_WIDTH, WIN_HEIGHT))

image_win = pygame.image.load(file_path(r"images\wiin.jpg"))
image_win = pygame.transform.scale(image_win,(WIN_WIDTH, WIN_HEIGHT))

image_lose = pygame.image.load(file_path(r"images\defeat.jpg"))
image_lose = pygame.transform.scale(image_lose,(WIN_WIDTH, WIN_HEIGHT))

image_menu = pygame.image.load(file_path(r"images\menuu.jpg"))
image_menu = pygame.transform.scale(image_menu,(WIN_WIDTH, WIN_HEIGHT))
#fon/s

music_shot = pygame.mixer.Sound(file_path(r"music\lazernyim-orujiem.ogg"))
music_shot.set_volume(0.2)

pygame.mixer.music.load(file_path(r"music\audio.mp3"))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play()
#music

game_name = pygame.font.SysFont("Comic Sans MS", 40, 1).render("Mini Genshin Labyrint", True, FUCHSIA)
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()
#regular settings

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
            bullet = Bullet(self.rect.right, self.rect.centery, 10, 10, r"images\magical.png", 5)
        
        elif self.direction == "left":
            bullet = Bullet(self.rect.left -10, self.rect.centery, 10, 10, r"images\magical.png", -5)
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

class Button():
    def __init__ (self, x, y, width, height, color_btn, color_collide, color_txt, text, text_size, px, py):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_btn = color_btn
        self.color_collide = color_collide
        self.color = color_btn
        font = pygame.font.SysFont("French Script MT", text_size)
        self.text = font.render(text, True, color_txt)
        self.px = px
        self.py = py

    def show(self):
        pygame.draw.rect(window, self.color, self.rect)
        window.blit(self.text, (self.rect.x + self.px, self.rect.y + self.py))
#class
        
btn_start = Button(330, 220, 200, 50, AMET, ORHI, WHITE2, "go", 20, 10, 5)
btn_esc = Button(350, 320, 150, 55, AMET, ORHI, WHITE2, "exit", 22, 10, 5)

bullets = pygame.sprite.Group()

player = Player(65, 90, 25,25, r"images\play.png", 0, 0)
target = GameSprite(740, 540, 40, 40, r"images\target.png")
#player, target, btn

enemys = pygame.sprite.Group()
enemy = Enemy(604, 390, 40, 30, r"images\enemys.png", 175, 316, "up", 3)
enemy2 = Enemy(106, 90, 60, 70, r"images\enem.png", 185, 550, "up", 3)
enemy3 = Enemy (267, 180, 30, 50, r"images\ene.png", 200, 360, "up", 2)
enemy4 = Enemy(400, 291, 80, 65, r"images\boss enemy.png", 0, 1, "up", 0)
enemy5 = Enemy(330, 290, 40, 35, r"images\Enemy_.png", 200, 360, "up", 2)
enemy6 = Enemy(390, 75, 40, 35, r"images\emyyy.png", 77, 210, "up", 2)
enemy7 = Enemy(677, 437, 40, 35, r"images\eeenemy.png", 320, 527, "up", 3)
#enemy7 = Enemy(673, 500, 40, 35, r"images\eeenemy.png", 510, 670, "up", 3)

enemys.add(enemy, enemy2, enemy3, enemy4, enemy5, enemy6, enemy7)
#enemy/s

walls = pygame.sprite.Group()
wall_0 = GameSprite(86, 67, 720, 10, r"images\wall2.jpg")
walls.add(wall_0)
wall_1 = GameSprite(100, 200, 70, 10, r"images\wall2.jpg")
walls.add(wall_1)
wall_2 = GameSprite(85, 110, 15, 430, r"images\wall2.jpg")
walls.add(wall_2)
wall_3 = GameSprite(100, 530, 638, 10, r"images\wall2.jpg")
walls.add(wall_3)
wall_4 = GameSprite(800, 67, 10, 540, r"images\wall2.jpg")
walls.add(wall_4)
wall_5 = GameSprite(660, 307, 140, 10, r"images\wall2.jpg")
walls.add(wall_5)
wall_6 = GameSprite(517, 111, 203, 10, r"images\wall2.jpg")
walls.add(wall_6)
wall_7 = GameSprite(450, 77, 10, 137, r"images\wall2.jpg")
walls.add(wall_7)
wall_8 = GameSprite(165, 111, 220, 10, r"images\wall2.jpg")
walls.add(wall_8)
wall_9 = GameSprite(716, 111, 10, 161, r"images\wall2.jpg")
walls.add(wall_9)
wall_10 = GameSprite(164, 477, 197, 10, r"images\wall2.jpg")
walls.add(wall_10)
wall_11 = GameSprite(165, 121, 10, 240, r"images\wall2.jpg")
walls.add(wall_11)
wall_12 = GameSprite(239, 153, 10, 157, r"images\wall2.jpg")
walls.add(wall_12)
wall_13 = GameSprite(300, 156, 87, 10, r"images\wall2.jpg")
walls.add(wall_13)
wall_14 = GameSprite(375, 121, 10, 36, r"images\wall2.jpg")
walls.add(wall_14)
wall_15 = GameSprite(590, 163, 82, 10, r"images\wall2.jpg")
walls.add(wall_15)
wall_16 = GameSprite(660, 173, 10, 320, r"images\wall2.jpg")
walls.add(wall_16)
wall_17 = GameSprite(229, 430, 378, 10, r"images\wall2.jpg")
walls.add(wall_17)
wall_18 = GameSprite(726, 350, 10, 250, r"images\wall2.jpg")
walls.add(wall_18)
wall_19 = GameSprite(162, 390, 318, 10, r"images\wall2.jpg")
walls.add(wall_19)
wall_20 = GameSprite(300, 210, 10, 100, r"images\wall2.jpg")
walls.add(wall_20)
wall_21 = GameSprite(375, 248, 10, 100, r"images\wall2.jpg")
walls.add(wall_21)
wall_22 = GameSprite(474, 477, 185, 10, r"images\wall2.jpg")
walls.add(wall_22)
wall_23 = GameSprite(512, 307, 150, 10, r"images\wall2.jpg")
walls.add(wall_23)
wall_24 = GameSprite(583, 248, 10, 110, r"images\wall2.jpg")
walls.add(wall_24)
wall_25 = GameSprite(517, 204, 92, 10, r"images\wall2.jpg")
walls.add(wall_25)
wall_26 = GameSprite(240, 200, 215, 10, r"images\wall2.jpg")
walls.add(wall_26)
wall_27 = GameSprite(517, 120, 10, 160, r"images\wall2.jpg")
walls.add(wall_27)
wall_28 = GameSprite(410, 440, 10, 92, r"images\wall2.jpg")
walls.add(wall_28)
wall_29 = GameSprite(374, 250, 152, 10, r"images\wall2.jpg")
walls.add(wall_29)
wall_30 = GameSprite(515, 315, 10, 44, r"images\wall2.jpg")
walls.add(wall_30)
wall_31 = GameSprite(175, 350, 230, 10, r"images\wall2.jpg")
walls.add(wall_31)
wall_32 = GameSprite(470, 350, 47, 10, r"images\wall2.jpg")
walls.add(wall_32)
wall_33 = GameSprite(528, 387, 78, 10, r"images\wall2.jpg")
walls.add(wall_33)
wall_34 = GameSprite(595, 395, 10, 44, r"images\wall2.jpg")
walls.add(wall_34)
wall_35 = GameSprite(470, 350, 10, 41, r"images\wall2.jpg")
walls.add(wall_35)
wall_36 = GameSprite(165, 400, 10, 85, r"images\wall2.jpg")
walls.add(wall_36)
#wall/s

timer = 60
font_time = pygame.font.SysFont("Comic Sans", 35)
txt_time = font_time.render("Time: " + str(timer), True, WHITE2)

start_time = pygame.time.get_ticks()

#window.blit(timer, (150, 6)

level = 0
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

        elif level == 0:
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if btn_start.rect.collidepoint(x, y):
                    btn_start.color = btn_start.color_collide
                elif btn_esc.rect.collidepoint(x, y):
                    btn_esc.color = btn_esc.color_collide 
                else:
                    btn_start.color = btn_start.color_btn
                    btn_esc.color = btn_esc.color_btn

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if btn_start.rect.collidepoint(x, y):
                    level = 1
                    pygame.mixer.music.load(file_path(r"music\main music.wav"))
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play()   
                elif btn_esc.rect.collidepoint(x, y):
                    game = False

           
    if level == 1:
        window.blit(fon, (0, 0))
        new_time = pygame.time.get_ticks()

        if (new_time - start_time) / 1000 > 1:
            timer -= 1
            txt_time = font_time.render("Time: " + str(timer), True, WHITE2)
            start_time = new_time
        window.blit(txt_time, (680, 20))   
             
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

        if pygame.sprite.spritecollide(player, enemys, False) or timer <= 0:
            level = 11
            pygame.mixer.music.load(file_path(r"music\failsound.mp3"))
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.3)
        pygame.sprite.groupcollide(bullets, walls, True, False)

        iii_collide = pygame.sprite.groupcollide(bullets, enemys, True, True)
        if iii_collide:
            timer += 5 
            txt_time = font_time.render("Time:" + str(timer), True, WHITE2)
    
    elif level == 0:
        window.blit(image_menu, (0, 0))
        window.blit(game_name, (300, 100))
        btn_start.show()
        btn_esc.show()

    elif level == 10:
        window.blit(image_win,(0, 0))
    elif level == 11:
        window.blit(image_lose,(0,0))

    clock.tick(FPS)
    pygame.display.update()