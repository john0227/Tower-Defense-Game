from Projectile import Projectile
from Timer import Timer

class Tower:
    
    T_TYPE = {"Blaster": {1: ( 10, 250,  15, 1.5, False,   0, "close", (255,  51,   0), (255, 153, 102)),
                          2: ( 20, 250,  23, 1.5, False,   0, "close", (204,   0,   0), (255, 153, 102)),
                          3: ( 35, 250,  35, 1.5, False,   0, "close", (153,   0,   0), (255, 153, 102))},
              "Blitz"  : {1: ( 15, 300,   5, 0.3, False,   0, "close", (255, 255, 153), (255, 255, 204)),
                          2: ( 25, 300,  10, 0.3, False,   0, "close", (255, 255, 102), (255, 255, 204)),
                          3: ( 40, 300,  15, 0.3, False,   0, "close", (255, 255,   0), (255, 255, 204))},
              "R. Hood": {1: ( 20, 500,  20, 1.2, False,   0,   "far", (  0, 204,   0), (204, 255,  51)),
                          2: ( 30, 550,  25, 1.2, False,   0,   "far", (  0, 153,  51), (204, 255,  51)),
                          3: ( 50, 600,  35, 1.2, False,   0,   "far", (  0, 102,   0), (204, 255,  51))},
              "Mortar" : {1: ( 60, 225,  40,   3,  True,  50, "close", (  0, 102, 204), (153, 153, 255)),
                          2: ( 80, 225,  60,   3,  True,  50, "close", (  0,   0, 153), (153, 153, 255)),
                          3: (120, 250, 120, 2.5,  True,  75, "close", (  0,   0, 103), (153, 153, 255))},
              "Bomber" : {1: ( 40, 275,  20,   2,  True,  75, "close", ( 89,  89,  89), ( 38,  38,  38)),
                          2: ( 50, 275,  50,   2,  True,  75, "close", ( 50,  50,  50), ( 38,  38,  38)),
                          3: ( 75, 300,  80,   2,  True, 100, "close", (  0,   0,   0), ( 38,  38,  38))}}
    projectiles = []
    
    def __init__(self, name, level, x, y):
        self.name = name
        self.level = level
        self.x = x
        self.y = y
        self.cost = self.T_TYPE[name][level][0]
        self.upgrade_cost = self.T_TYPE[name][self.level + 1][0] if self.level != 3 else "MAX LV"
        self.price = int(self.cost * 0.75)
        self.reach = self.T_TYPE[name][level][1]
        self.dmg = self.T_TYPE[name][level][2]
        self.shootspd = self.T_TYPE[name][level][3]
        self.is_splash = self.T_TYPE[name][level][4]
        self.radius = self.T_TYPE[name][level][5]
        self.targeting = self.T_TYPE[name][level][6]
        self.target = None
        self.coloring = self.T_TYPE[name][level][7]
        self.projectile_color = self.T_TYPE[name][level][8]
        self.timer = Timer()
        self.timer.start_timer()
    
    def shoot(self, x1, y1):
        self.projectiles.append(Projectile(self.x, self.y, self.x, self.y, x1, y1, self.projectile_color))
        self.timer.reset()
        self.timer.start_timer()
    def distance(self, x1, y1, x2, y2):
        return sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))
    
    def upgrade(self):
        self = self.__init__(self.name, self.level + 1, self.x, self.y)
    
    def show_info(self, x, y):
        # Change x, y position
        if y <= 475:
            y += 220
        elif y > 475:
            y -= 220
        if x <= 750:
            x += 150
        elif x > 750:
            x -= 150
        stroke(0)
        strokeCap(ROUND)
        strokeWeight(6)
        fill(230)
        rectMode(CENTER)
        rect(x, y, 300, 400, 15)
        fill(200)
        strokeWeight(3)
        rect(x, y + 30, 270, 315, 15)
        fill(0)
        textFont(createFont("UD Digi Kyokasho NP-B", 30))
        textAlign(CENTER)
        text("{} Level: {}".format(self.name.upper(), self.level), x, y - 150, 300, 50)
        textSize(20)
        textAlign(LEFT)
        text("Tower Cost: {}".format(self.cost), x - 120, y - 95)
        text("Selling Price: {}".format(self.price), x - 120, y - 65)
        text("Damage: {}".format(self.dmg), x - 120, y - 35)
        text("Speed: {}".format(self.shootspd), x - 120, y - 5)
        text("Range: {}".format(self.reach), x - 120, y + 25)
        if self.is_splash:
            text("Splash Radius: {}".format(self.radius), x - 120, y + 55)
            text("Upgrade Cost: {}".format(self.upgrade_cost), x - 120, y + 85)
        else:
            text("Upgrade Cost: {}".format(self.upgrade_cost), x - 120, y + 55)
        textSize(16)
        text("Press u to upgrade tower", x - 120, y + 120)
        text("Press s to sell tower", x - 120, y + 145)
        text("(While pressing tower)", x - 120, y + 170)
        rectMode(CORNER)
    def display(self):
        self.draw_tower()
        for p in self.projectiles:
            p.display()
            if self.distance(p.starting[0], p.starting[1], p.ending[0], p.ending[1]) <= self.distance(p.x, p.y, p.starting[0], p.starting[1]):
                self.projectiles.pop(self.projectiles.index(p))
                del p
    def draw_tower(self):
        noStroke()
        if self.name == "Blaster":
            fill(color(self.coloring[0], self.coloring[1], self.coloring[2]))
            triangle(self.x, self.y - 20, self.x - 15, self.y + 20 , self.x + 15, self.y + 20)
        elif self.name == "Blitz":
            fill(self.coloring[0], self.coloring[1], self.coloring[2])
            quad(self.x, self.y - 20, self.x + 15, self.y , self.x, self.y + 20, self.x - 15, self.y)
        elif self.name == "R. Hood":
            fill(self.coloring[0], self.coloring[1], self.coloring[2])
            ellipse(self.x, self.y, 45, 30)
        elif self.name == "Mortar":
            fill(self.coloring[0], self.coloring[1], self.coloring[2])
            quad(self.x - 7.5, self.y - 20, self.x + 7.5, self.y - 20, self.x + 15, self.y + 20, self.x - 15, self.y + 20)
        elif self.name == "Bomber":
            stroke(0)
            strokeWeight(1)
            fill(self.coloring[0], self.coloring[1], self.coloring[2])
            ellipse(self.x, self.y, 40, 40)
            noStroke()
    
    
