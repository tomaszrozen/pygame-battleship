import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, name, image, x, y):
        super().__init__()
        self.name = name
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.centery = y
