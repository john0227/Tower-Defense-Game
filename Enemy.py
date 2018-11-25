
class Enemy:
    
    E_TYPE = {1: ( 100,   4,  10, 20, (255, 255, 255)), 
              2: (  50,   7,  20, 15, (255, 165,   0)),
              3: ( 150,   3,  50, 22, (255, 255,  80)),
              4: ( 300,   2, 100, 24, (170, 170, 170)),
              5: ( 500, 1.5, 150, 26, (250, 130, 200)),
              6: (1000, 1.2, 200, 30, (230,  80, 170)),
              7: (1500,   1, 300, 50, (  0, 220, 250)),
              8: (3000, 0.8, 700, 75, (180,  50, 200))}
    difficulty_scale = 1
    
    def __init__(self, id):
        self.id = id
        self.x = random(4.3, 5.6) * 50
        self.y = 225
        self.radius = self.E_TYPE[id][3]
        self.speed = self.E_TYPE[id][1]
        self.coloring = self.E_TYPE[id][4]
        self.totalHP = int(self.E_TYPE[id][0] * self.difficulty_scale)
        self.hp = int(self.E_TYPE[id][0] * self.difficulty_scale)
        self.loot = self.E_TYPE[id][2] / 2
        self.visible = True
    
    def __move(self, vx, vy):
        self.x += self.speed * vx
        self.y += self.speed * vy
        
    def move_and_display(self, vx, vy):
        self.__move(vx, vy)
        # Display the enemy
        fill(self.coloring[0], self.coloring[1], self.coloring[2])
        ellipse(self.x, self.y, 2 * self.radius, 2 * self.radius)
        # Display the health bar
        fill(255, 0, 0)
        rect(self.x - self.radius, self.y - self.radius - 20, 2 * self.radius, 10)
        fill(0, 150, 0)
        rect(self.x - self.radius, self.y - self.radius - 20, 2 * self.radius * self.hp / self.totalHP, 10)

    def is_defeated(self):
        return self.hp <= 0
