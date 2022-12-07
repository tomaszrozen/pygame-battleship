import pygame

class Text:
    def __init__(self, text, text_colour, pos_x_center, pos_y_center, font_type = None, size = 74):
        self.text = str(text)
        self.text_colour = text_colour
        self.font_type = font_type
        self.size = size
        self.font = pygame.font.SysFont(self.font_type, self.size)
        self.image = self.font.render(self.text, True, self.text_colour)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x_center, pos_y_center]

    def draw(self, surface):
        surface.blit(self.image, self.rect)