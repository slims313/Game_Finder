from Globals import *

window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Testing')
screen = pygame.Surface(SCREEN_SIZE)


imag = pygame.image.load('images/hero.png').convert_alpha()
imag = pygame.transform.scale(imag, (50, 50))

Wall_image = pygame.image.load('images/wall.png').convert_alpha()
Wall_image = pygame.transform.scale(Wall_image, (BLOCK_SIZE, BLOCK_SIZE))

select_surf = pygame.image.load('images/selection.png').convert_alpha()
select_surf = pygame.transform.scale(select_surf, (50, 50))