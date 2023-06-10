import pygame
import os
pygame.init()

def file_path(file_name):
    folder = os.path.abspath(__file__+ "/..")
    path = os.path.join(folder, file_name)

WIN_WIDTH = 900
WIN_HEIGHT = 600
FPS = 40

fon = pygame.image.load(file_path(r"images\fone.jpg"))
fon = pygame.transform.scale(fon,(WIN_WIDTH, WIN_HEIGHT))

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

class GameSprite(pygame.sprine.Sprite):
    def __init__ (self, x, y, widht, height, image):
        self.rect = pygame.Rect(x, y, widht, height)
        self.image.load(file_path(image))
        self.image = pygame.transform.scale(self.image, (widht, height))
    def show(self):
        window.blit(self.image (self.rect.x, self.rect.y))

player = GameSprite(50, 55, 30, 33, r"images\me.jpg")

enemy = GameSprite(70, 333, 30, 33, r"images\enemy.jpg")

target = GameSprite(222, 100, 30, 33, r"images\target.jpg")



level = 1
game = True

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    if level == 1:
        window.blit(fon, (0, 0))
        player.show()
        enemy.show()
        target.show()

    clock.tick(FPS)
    pygame.display.update()


