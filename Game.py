from Levels import *
import sys
from os import path


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
                if e.key == pygame.K_g:
                    self.save_level()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    mpos = vec(pygame.mouse.get_pos()) // BLOCK_SIZE * BLOCK_SIZE
                    mpos_center = [int(mpos[0]+BLOCK_SIZE//2), int(mpos[1]+BLOCK_SIZE//2)]
                    for i in UnitsGroup:
                        i.target = mpos_center
                        i.create_path()

                if e.button == 2:
                    mpos = vec(pygame.mouse.get_pos()) // BLOCK_SIZE
                    try:
                        Wall_List.remove([pygame.mouse.get_pos()[0]//BLOCK_SIZE, pygame.mouse.get_pos()[1]//BLOCK_SIZE])
                    except:
                        pass
                    matrix[int(mpos[1])][int(mpos[0])] = 1

                if e.button == 3:
                    mpos = vec(pygame.mouse.get_pos()) // BLOCK_SIZE
                    if [pygame.mouse.get_pos()[0]//BLOCK_SIZE, pygame.mouse.get_pos()[1]//BLOCK_SIZE] not in Wall_List:
                        Wall_List.append([pygame.mouse.get_pos()[0]//BLOCK_SIZE, pygame.mouse.get_pos()[1]//BLOCK_SIZE])
                    matrix[int(mpos[1])][int(mpos[0])] = 0
                # print(matrix)
                print(Wall_List)

    def draw_grid(self):  # СЕТКА
        for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
            pygame.draw.line(screen, LIGHTGRAY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
            pygame.draw.line(screen, LIGHTGRAY, (0, y), (SCREEN_WIDTH, y))

    def draw_active_cell(self):
        mouse_pos = pygame.mouse.get_pos()
        row = mouse_pos[1] // BLOCK_SIZE
        col = mouse_pos[0] // BLOCK_SIZE
        rect = pygame.Rect((col * BLOCK_SIZE, row * BLOCK_SIZE), (BLOCK_SIZE, BLOCK_SIZE))
        screen.blit(select_surf, rect)

    def save_level(self):
        np.savetxt('matrix', matrix, fmt='%d')

    def update(self):
        self.key_press()

        for i in UnitsGroup:
            i.update(self.dt)

        self.render()

    def render(self):
        window.blit(screen, (0, 0))
        screen.fill((0, 0, 0))
        self.draw_grid()
        self.draw_active_cell()

        for i in Wall_List:
            screen.blit(Wall_image, (i[0]*BLOCK_SIZE, i[1]*BLOCK_SIZE))

        for i in UnitsGroup:
            screen.blit(i.image, (i.rect.x, i.rect.y))

        pygame.display.flip()

    def main_loop(self):
        while self.running:
            self.update()
            self.timer.tick(FPS)

