import pygame


class Ship(pygame.sprite.Sprite):
    def __init__(self, name, length, image, x=0, y=0, column=0, row=0, horizontal=True):
        super().__init__()
        self.horizontal = horizontal
        self.row = row
        self.column = column
        self.length = length
        self.name = name
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.centery = y + 20

    def rotate(self, x, y):
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.horizontal = not self.horizontal
