
import math


class Fruit:
    def __init__(self, x, y, vx, vy, gravity, radius=28, kind="fruit"):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.gravity = gravity
        self.radius = radius
        self.kind = kind  # "fruit" or "bomb"
        self.sliced = False

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy

    def contains_point(self, x, y):
        """Check whether a point lies inside the fruit's circle."""
        return math.hypot(self.x - x, self.y - y) <= self.radius

    def intersects_segment(self, start_x, start_y, end_x, end_y):
        """Check whether a mouse swipe segment intersects the fruit."""
        dx = end_x - start_x
        dy = end_y - start_y

        length_squared = dx * dx + dy * dy

        if length_squared == 0:
            return self.contains_point(start_x, start_y)

        t = (
            (self.x - start_x) * dx
            + (self.y - start_y) * dy
        ) / length_squared

        t = max(0.0, min(1.0, t))

        closest_x = start_x + t * dx
        closest_y = start_y + t * dy

        distance = math.hypot(
            self.x - closest_x,
            self.y - closest_y
        )

        return distance <= self.radius

    def off_screen(self, height):
        return self.y - self.radius > height
