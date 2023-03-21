from PathFinder import *


class Unit(pygame.sprite.Sprite):
    def __init__(self, imag, x_pos, y_pos):

        # basic
        super().__init__()
        self.image = imag
        self.rect = imag.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.detect_radius = 1
        self.target = None
        self.current = []

        # path
        self.path = []
        self.collision_rects = []


class Player(Unit):
    def __init__(self, imag, x_pos, y_pos):
        super().__init__(imag, x_pos, y_pos)

        self.speed = 2
        self.vel = vec(0, 0)
        self.pos = vec(x_pos, y_pos)
        self.rot = 0
        self.rot_speed = 0
        self.direction = pygame.math.Vector2(0, 0)
        self.pf = Pathfinder(matrix)

    def empty_path(self):
        self.path = []

    def get_coord(self):
        col = self.rect.centerx // BLOCK_SIZE
        row = self.rect.centery // BLOCK_SIZE
        return (col, row)

    def create_path(self):
        # start
        self.pf.grid = Grid(matrix=matrix)
        start_x, start_y = self.get_coord()
        start = self.pf.grid.node(start_x, start_y)

        # end
        end_x, end_y = self.target[0] // BLOCK_SIZE, self.target[1] // BLOCK_SIZE
        end = self.pf.grid.node(end_x, end_y)

        # path
        finder = AStarFinder(diagonal_movement=DiagonalMovement.if_at_most_one_obstacle)
        self.path, _ = finder.find_path(start, end, self.pf.grid)
        self.pf.grid.cleanup()
        self.set_path(self.path)

    def set_path(self, path):
        self.path = path
        try:
            self.current = [self.path[1][0] * BLOCK_SIZE + BLOCK_SIZE // 2,
                    self.path[1][1] * BLOCK_SIZE + BLOCK_SIZE // 2]
            # print(self.current)
        except:
            pass
        self.create_collision_rects()

    def create_collision_rects(self):
        if self.path:  # !! empty path
            self.collision_rects = []
            for point in self.path:
                x = (point[0] * BLOCK_SIZE) + BLOCK_SIZE // 2
                y = (point[1] * BLOCK_SIZE) + BLOCK_SIZE // 2
                rect = pygame.Rect((x - 2, y - 2), (4, 4))
                self.collision_rects.append(rect)

    def check_collisions(self):
        if self.collision_rects:
            # print("Workspace: check_collision")
            for rect in self.collision_rects:
                if rect.collidepoint(self.pos):
                    self.empty_path()
                    self.create_path()
                    del self.collision_rects[0]
        else:
            self.empty_path()

    def automove_to_target(self, dt):
        if self.target:
            # print("Workspace: automove_to_target")
            target_dist = self.current - self.pos
            if target_dist.length_squared() > self.speed*10:
                self.movement(dt, target_dist, self.speed)
            elif self.speed*10 > target_dist.length_squared() > 1:
                self.movement(dt, target_dist, 1)
            else:
                self.target = None

    def draw_path(self):
        if self.path:
            # print("Workspace: draw_path")
            points = []
            for point in self.path:
                x = (point[0] * BLOCK_SIZE) + BLOCK_SIZE//2
                y = (point[1] * BLOCK_SIZE) + BLOCK_SIZE//2
                points.append((x, y))
            try:
                pygame.draw.lines(screen, '#00d6ff', False, points, 3)
            except:
                pass

    def movement(self, dt, target_dist, speed):
        self.rot = target_dist.angle_to(vec(1, 0))
        self.image = pygame.transform.rotate(imag, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.acc = vec(1, 0).rotate(-self.rot)

        try:
            self.acc.scale_to_length(speed)
        except:
            pass
        self.acc += self.vel * -1
        self.vel += self.acc * dt
        self.pos += self.vel * dt + 0.5 * self.acc * dt ** 2
    def stop(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)

    def update(self, dt):
        self.draw_path()
        self.automove_to_target(dt)
        self.check_collisions()


