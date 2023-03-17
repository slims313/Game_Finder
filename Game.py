from Levels import *
import sys
from os import path
mech = Mechanics()

class Game:
    def __init__(self):
        self.timer = pygame.time.Clock()
        self.running = True
        self.__init_window__()
        self.main_loop()

    def __init_window__(self):
        pygame.init()
        self.dt = self.timer.tick(FPS) / 1000.0

    def quit(self):
        pygame.quit()
        sys.exit()

    def key_press(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.quit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    mpos = vec(pygame.mouse.get_pos())
                    for i in UnitsGroup:
                        i.target = mpos

    def draw_grid(self):  # СЕТКА
        for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
            pygame.draw.line(screen, LIGHTGRAY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
            pygame.draw.line(screen, LIGHTGRAY, (0, y), (SCREEN_WIDTH, y))

    def update(self):
        self.key_press()

        for i in UnitsGroup:
            i.update(self.dt)

        self.render()

    def render(self):
        window.blit(screen, (0, 0))
        screen.fill((0, 0, 0))
        self.draw_grid()

        for i in UnitsGroup:
            screen.blit(i.image, (i.rect.x, i.rect.y))


        pygame.display.flip()

    def main_loop(self):
        while self.running:
            self.update()
            self.timer.tick(FPS)

