from Mechanic import *


class Platform(Sprite):
    def __init__(self, width, height, pl_image):
        Sprite.__init__(self)
        self.hp = 10
        self.image = pl_image
        self.rect = self.image.get_rect()
        self.rect.x = width
        self.rect.y = height