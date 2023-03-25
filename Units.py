from PathFinder import *


a = (0, )


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

        self.speed = 15
        self.vel = vec(0, 0)
        self.pos = vec(x_pos, y_pos)
        self.rot = 0
        self.rot_speed = 0
        self.direction = pygame.math.Vector2(0, 0)
        self.pf = Pathfinder(matrix)

        self.radars = []
        self.collision_points = []

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

    def compute_radars(self, degree):
        length = 0
        x = int(self.pos[0] + math.cos(math.radians(360 - (self.rot + degree))) * length)
        y = int(self.pos[1] + math.sin(math.radians(360 - (self.rot + degree))) * length)
        try:
            while not screen.get_at((x, y)) == walls and length < 150:
                length = length + 1
                x = int(self.pos[0] + math.cos(math.radians(360 - (self.rot + degree))) * length)
                y = int(self.pos[1] + math.sin(math.radians(360 - (self.rot + degree))) * length)
        except:
            pass

        dist = int(math.sqrt(math.pow(x - self.pos[0], 2) + math.pow(y - self.pos[1], 2)))
        self.radars.append([(x, y), dist])

    def compute_collision_points(self):
        lw = BLOCK_SIZE - BLOCK_SIZE * 0.3
        lh = BLOCK_SIZE - BLOCK_SIZE * 0.3

        lt = [self.pos[0] + math.cos(math.radians(360 - (self.rot + 45))) * lw,
              self.pos[1] + math.sin(math.radians(360 - (self.rot + 45))) * lh]
        rt = [self.pos[0] + math.cos(math.radians(360 - (self.rot + 135))) * lw,
              self.pos[1] + math.sin(math.radians(360 - (self.rot + 135))) * lh]
        lb = [self.pos[0] + math.cos(math.radians(360 - (self.rot + 225))) * lw,
              self.pos[1] + math.sin(math.radians(360 - (self.rot + 225))) * lh]
        rb = [self.pos[0] + math.cos(math.radians(360 - (self.rot + 315))) * lw,
              self.pos[1] + math.sin(math.radians(360 - (self.rot + 315))) * lh]

        self.collision_points = [lt, rt, lb, rb]

    def draw_collision_points(self, screen):
        if self.collision_points:
            for p in self.collision_points:
                if (screen.get_at((int(p[0]), int(p[1]))) == walls):
                    pygame.draw.circle(screen, (255, 0, 0), (int(p[0]), int(p[1])), 5)
                else:
                    pygame.draw.circle(screen, (15, 192, 252), (int(p[0]), int(p[1])), 5)

    def draw_me(self, screen):
        self.draw_radars(screen)
        self.draw_center(screen)

    def draw_center(self, screen):
        pygame.draw.circle(screen, (0, 72, 186), (math.floor(self.pos[0]), math.floor(self.pos[1])), 5)

    def draw_radars(self, screen):
        for r in self.radars:
            p, d = r
            pygame.draw.line(screen, (183, 15, 70), self.pos, p, 1)
            pygame.draw.circle(screen, (183, 235, 70), p, 5)

    def update(self, dt):
        self.draw_path()
        self.automove_to_target(dt)
        self.check_collisions()

        # sensors
        self.compute_collision_points()
        self.draw_collision_points(screen)

        self.radars.clear()
        for i in range(-60, 80, 20):
            self.compute_radars(i)
        self.draw_me(screen)


