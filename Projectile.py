
class Projectile:
    
    def __init__(self, x, y, x1, y1, x2, y2, coloring):
        self.x = x
        self.y = y
        self.starting = (x1, y1)
        self.ending = (x2, y2)
        self.spd = 80
        self.radius = 10
        self.coloring = coloring
    
    def move(self):
        # Normalize vector
        d = sqrt(pow(self.starting[0] - self.ending[0], 2) + pow(self.starting[1] - self.ending[1], 2))
        v = ((self.ending[0] - self.starting[0]) / d, (self.ending[1] - self.starting[1]) / d)
        # Set dx and dy
        dx = v[0] * self.spd
        dy = v[1] * self.spd
        d = self.distance(self.starting[0], self.starting[1], self.x + dx, self.y + dy)
        D = self.distance(self.starting[0], self.starting[1], self.ending[0], self.ending[1])
        if d > D:
            dx, dy = self.ending[0] - self.x, self.ending[1] - self.y
        # Move position
        self.x += dx
        self.y += dy
    def distance(self, x1, y1, x2, y2):
        return sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))
    def display(self):
        self.move()
        # Draw the projectile
        fill(self.coloring[0], self.coloring[1], self.coloring[2])
        ellipse(self.x, self.y, self.radius * 2, self.radius * 2)
