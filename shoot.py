import pygame


class Shoot(pygame.sprite.Sprite):
    def __init__(self, image, rect_center):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = (rect_center[0] +1, rect_center[1] +1)