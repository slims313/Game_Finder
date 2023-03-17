from Windows import *


class Unit:
    def __init__(self, imag, x_pos, y_pos):
        self.image = imag
        self.rect = imag.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.detect_radius = 3
        self.target = (400, 400,)


class Player(Unit):
    def __init__(self, imag, x_pos, y_pos):
        super().__init__(imag, x_pos, y_pos)
        self.speed = 3
        self.vel = vec(0, 0)
        self.pos = vec(x_pos, y_pos)
        self.rot = 0
        self.rot_speed = 0

    def automove_to_target(self, dt):
        target_dist = self.target - self.pos
        if target_dist.length_squared() > self.detect_radius:
            self.rot = target_dist.angle_to(vec(1, 0))
            self.image = pygame.transform.rotate(imag, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos

            self.acc = vec(1, 0).rotate(-self.rot)

            try:
                self.acc.scale_to_length(self.speed)
            except:
                pass
            self.acc += self.vel * -1
            self.vel += self.acc * dt
            self.pos += self.vel * dt + 0.5 * self.acc * dt ** 2

    def stop(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)

    def update(self, dt):
        self.automove_to_target(dt)
