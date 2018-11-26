from Enemy import Enemy
from Tower import Tower
from Timer import Timer

class Game:
    
    path = [[0, 0, 0, 1, 1, 1, 1, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 0, 0, 0, 0],
            [0, 2, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0],
            [0, 0, 0, 1, 1, 1, 1, 0, 2, 0, 0, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 2, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 2, 0],
            [0, 0, 0, 1, 1, 1, 1, 0, 2, 0, 0, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 2, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 2, 0],
            [0, 0, 0, 1, 1, 1, 1, 0, 2, 0, 0, 2, 0, 1, 1, 1, 1, 0, 2, 0, 0, 2, 0, 1, 1, 1, 1, 0, 0, 0],
            [0, 2, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 2, 0],
            [0, 0, 0, 1, 1, 1, 1, 0, 2, 0, 0, 2, 0, 1, 1, 1, 1, 0, 2, 0, 0, 2, 0, 1, 1, 1, 1, 0, 0, 0],
            [0, 2, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 2, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 2, 0, 0, 2, 0, 1, 1, 1, 1, 0, 0, 0],
            [0, 2, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 2, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2, 0, 0, 2, 0, 1, 1, 1, 1, 0, 0, 0],
            [0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 0, 2, 0],
            [0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 0, 0, 2, 0, 3, 3, 3, 3, 0, 0, 0]]
    enemies = []
    towers = {}
    ticons = [Tower("Blaster", 1,  780, 136), 
              Tower("Blitz"  , 1,  930, 136),
              Tower("R. Hood", 1, 1080, 136),
              Tower("Mortar" , 1, 1230, 136),
              Tower("Bomber" , 1, 1380, 136)]
    
    def __init__(self):
        self.score = 0
        self.highscore = 0
        self.wave = 0
        self.money = 100
        self.MAX_MONEY = 99999
        self.castleHP = 500
        self.totalHP = 500
        self.wave_timer = Timer()
        self.wave_interval = 20
        self.spawn_timer = Timer()
        self.spawn_rate = 1
        self.spawn_interval = 700
        self.icons = []
        self.no_money = False
        self.blink = 40
        self.blink_count = 0
        self.max_enemies = 20
    
    def restart(self):
        temp_icons, temp_hs = self.icons, self.highscore
        self.__init__()
        self.icons = temp_icons
        self.highscore = temp_hs
        for e in self.enemies:
            self.enemies.pop(self.enemies.index(e))
            del e
        self.enemies = []
        for t in self.towers:
            del self.towers[t]
        self.towers = {}
    
    def at_rowcol(self, x, y):
        return int((y - 200) // 50), int(x // 50)
    def row_to_pos(self, r, c):
        return c * 50 + 25, r * 50 + 200 + 25
    def is_buildable(self, x, y):
        if y >= 200:
            r, c = self.at_rowcol(x, y)
            return self.path[r][c] == 2 and not (r, c) in self.towers
        else:
            return False
    def has_tower(self, x, y):
        if y >= 200:
            r, c = self.at_rowcol(x, y)
            return self.path[r][c] == 2 and (r, c) in self.towers
        else:
            return False
    def tower_at(self, x, y):
        if y >= 200:
            r, c = self.at_rowcol(x, y)
            return self.towers.get((r, c), None)
        else:
            return None
    def radius_at_pos(self, x, y):
        if y >= 86 and y <= 186:
            if x >= 730 and x <= 830:
                return 250
            elif x >= 880 and x <= 980:
                return 300
            elif x >= 1030 and x <= 1130:
                return 500
            elif x >= 1180 and x <= 1280:
                return 225
            elif x >= 1330 and x <= 1430:
                return 275
            return -1
        return -1
    def gameover(self):
        return self.castleHP <= 0
    def build_tower(self, tower_reach, x, y):
        t = None
        r, c = self.at_rowcol(x, y)
        if tower_reach == 250:
            t = Tower("Blaster", 1, c * 50 + 25, 225 + r * 50)
        elif tower_reach == 300:
            t = Tower("Blitz", 1, c * 50 + 25, 225 + r * 50)
        elif tower_reach == 500:
            t = Tower("R. Hood", 1, c * 50 + 25, 225 + r * 50)
        elif tower_reach == 225:
            t = Tower("Mortar", 1, c * 50 + 25, 225 + r * 50)
        elif tower_reach == 275:
            t = Tower("Bomber", 1, c * 50 + 25, 225 + r * 50)
        if t is not None and t.cost <= self.money:
            self.towers[(r, c)] = t
            self.money -= t.cost
        elif t is not None:
            self.no_money = True
            self.blink_count = 0
            del t
    def upgrade_tower(self, x, y):
        t = self.tower_at(x, y)
        if t is not None and t.level < 3 and self.money >= t.upgrade_cost:
            self.money -= t.upgrade_cost
            t.upgrade()
        elif t is not None and t.level < 3 and self.money < t.upgrade_cost:
            self.no_money = True
            self.blink_count = 0
    def sell_tower(self, x, y):
        t = self.tower_at(x, y)
        if t is not None:
            madd = t.price
            if self.money + madd > self.MAX_MONEY:
                madd = self.MAX_MONEY - self.money
            self.money += madd
            r, c = self.at_rowcol(x, y)
            del self.towers[(r, c)]
            del t
    def select_target(self, tower):
        if tower.target is None or self.distance(tower, tower.target) - tower.target.radius > tower.reach:
        # If tower does not have a target or old target is out of tower's range, select new one
            if tower.targeting == "close":
                distance, target = 3000, None
                for e in self.enemies:
                    d = self.distance(tower, e)
                    if d < distance and d - e.radius <= tower.reach:
                        distance = d
                        target = e
                return target
            elif tower.targeting == "far":
                distance, target = -1, None
                for e in self.enemies:
                    d = self.distance(tower, e)
                    if d > distance and d - e.radius <= tower.reach:
                        distance = d
                        target = e
                return target
        else:
            return tower.target
    def distance(self, obj1, obj2):
        return sqrt(pow(obj1.x - obj2.x, 2) + pow(obj1.y - obj2.y, 2))
    def generate_enemies(self):
        if self.wave == 1:
            self.enemies.extend([Enemy(1), Enemy(1), Enemy(1)])
        elif self.wave == 2:
            self.enemies.extend([Enemy(1), Enemy(1), Enemy(1), Enemy(1)])
        elif self.wave == 3:
            self.enemies.extend([Enemy(1), Enemy(1), Enemy(1), Enemy(1), Enemy(1)])
        elif self.wave == 4:
            self.enemies.extend([Enemy(2), Enemy(2), Enemy(2)])
        elif self.wave == 5:
            self.enemies.extend([Enemy(1), Enemy(1), Enemy(2), Enemy(2), Enemy(1), Enemy(2)])
        elif self.wave == 6:
            self.enemies.extend([Enemy(2), Enemy(2), Enemy(2), Enemy(1), Enemy(1), Enemy(1), Enemy(3), Enemy(1), Enemy(3), Enemy(1), Enemy(2), Enemy(2)])
        elif self.wave == 7:
            self.enemies.extend([Enemy(2), Enemy(2), Enemy(2), Enemy(1), Enemy(1), Enemy(1), Enemy(4), Enemy(4),
                                 Enemy(3), Enemy(1), Enemy(3), Enemy(1), Enemy(2), Enemy(2), Enemy(5), Enemy(5)])
        elif self.wave == 10:
            self.enemies.extend([Enemy(7), Enemy(1), Enemy(1), Enemy(2), Enemy(1), Enemy(2), Enemy(2), Enemy(3), Enemy(3), Enemy(1), Enemy(3), Enemy(1), Enemy(3)])
        elif self.wave == 20:
            self.enemies.extend([Enemy(8), Enemy(8), Enemy(7), Enemy(7), Enemy(7)])
        else:
            enemy_num = int(1.5 * self.max_enemies) if self.wave % 10 == 0 else self.max_enemies
            for i in range(enemy_num):
                egenerator = random(0, 200)
                if egenerator < 10 or egenerator >= 195 and egenerator < 200:
                    self.enemies.append(Enemy(8))
                elif egenerator >= 10 and egenerator < 30:
                    self.enemies.append(Enemy(7))
                elif egenerator >= 30 and egenerator < 50:
                    self.enemies.append(Enemy(6))
                elif egenerator >= 50 and egenerator < 100:
                    self.enemies.append(Enemy(1))
                elif egenerator >= 100 and egenerator < 120 or egenerator >= 190 and egenerator < 195:
                    self.enemies.append(Enemy(3))
                elif egenerator >= 120 and egenerator < 135 or egenerator >= 185 and egenerator < 190:
                    self.enemies.append(Enemy(2))
                elif egenerator >= 135 and egenerator < 165:
                    self.enemies.append(Enemy(4))
                elif egenerator >= 165 and egenerator < 185:
                    self.enemies.append(Enemy(5))
        if self.wave % 20 == 0:
            # After every 20 waves, increase total number of enemies generated
            self.max_enemies += 10
        if self.wave % 10 == 0:
            # After every 10 waves, increase enemy health
            Enemy.difficulty_scale += self.wave / 10
    def start_wave(self):
        # if not self.enemies:
        if self.enemies:
            self.wave += 1
        self.wave_interval = 10
        self.generate_enemies()
        self.wave_timer.reset()
        self.spawn_timer.start_timer()
    def display(self):
        # Display Map
        for r in range(len(self.path)):
            for c in range(len(self.path[r])):
                noStroke()
                if self.path[r][c] == 0:
                    # Print green blocks
                    fill(0, 230, 0)
                elif self.path[r][c] == 1:
                    # Print brown blocks
                    fill(130, 80, 80)
                elif self.path[r][c] == 2:
                    # Print gray blocks
                    fill(100)
                elif self.path[r][c] == 3:
                    # Print black
                    fill(0, 0, 0)
                rect(c * 50, r * 50 + 200, 50, 50)
        if not self.gameover():
            # If self.enemies is empty and wave has started, generate enemies and display
            if not self.enemies:
                if not self.wave_timer.is_set:
                    self.wave += 1
                    self.wave_timer.start_timer()
                    self.spawn_timer.reset()
                    self.spawn_rate = 1
                elif self.wave_timer.time >= self.wave_interval * 1000:
                    self.wave_interval = 10
                    self.generate_enemies()
                    self.wave_timer.reset()
                    self.spawn_timer.start_timer()
            # Display enemies
            if self.enemies:
                index = 0
                while index < self.spawn_rate and index < len(self.enemies):
                # Spawn enemies in a set interval (not all at once)
                    e = self.enemies[index]
                    if e.is_defeated():
                            # increase player's coins, score, highscore, etc
                            madd = e.loot
                            if self.money + madd > self.MAX_MONEY:
                                madd = self.MAX_MONEY - self.money
                            self.money += madd
                            self.score += e.radius
                            self.highscore = self.score if self.score > self.highscore else self.highscore
                            self.enemies.pop(self.enemies.index(e))
                            del e
                    elif e.visible:
                        r, c = self.at_rowcol(e.x, e.y)
                        if (r >= 0 and r <= 9 and c >= 3 and c <= 6) or (r >= 6 and r <= 12 and c >= 23 and c <= 26):
                            # Going down
                            vx = floor(random(-0.3, 1.5))
                            if c == 3 or c == 23:
                                vx = 1
                            elif c == 6 or c == 26:
                                vx = -1
                            e.move_and_display(vx, 1)
                        elif (r >= 10 and r <= 12 and c >= 4 and c <= 9) or (r >= 2 and r <= 5 and c >= 20 and c <= 26):
                            # Going down right
                            vx, vy = random(0.5, 1), floor(random(-0.5, 1.5))
                            if r == 11 and c == 4 or r == 12 and c == 5:
                                vy = 0
                            elif r == 12:
                                vx, vy = 0.5, -1
                            elif r == 10 or r == 2 or r == 3 and c == 25 or r == 4 and c == 26:
                                vx, vy = 0.5, 1
                            elif c == 26:
                                vx, vy = -1, 1
                            elif c == 25:
                                vx, vy = -0.5, 1
                            e.move_and_display(vx, vy)
                        elif (r >= 9 and r <= 12 and c >= 10 and c <= 15) or (r >= 2 and r <= 5 and c >= 13 and c <= 19):
                            # Going up right
                            vx, vy = random(0.5, 1.5), -random(0, 1)
                            e.move_and_display(vx, vy)
                        elif r >= 5 and r <= 9 and c >= 13 and c <= 16:
                            # Going up
                            vx = floor(random(-0.5, 1.5))
                            if c == 13:
                                vx = 1
                            elif c == 16:
                                vx = -1
                            e.move_and_display(vx, -1)
                        elif r >= 13 and c >= 23 and c <= 26:
                            e.visible = False
                            self.castleHP -= e.radius
                            if self.castleHP <= 0:
                                self.castleHP == 0
                            self.enemies.pop(self.enemies.index(e))
                            del e
                    index += 1
            # Display Towers
            for keyval in self.towers:
                t = self.towers[keyval]
                t.display()
                t.target = self.select_target(t)
                if t.target is not None and t.target.visible:
                    if t.timer.time >= t.shootspd * 1000:
                        # Shoot, reset timer, remove enemy health
                        # If enemy is killed, collect loot and increase point
                        t.shoot(t.target.x, t.target.y)
                        t.target.hp -= t.dmg
                        if t.is_splash:
                            index = 0
                            while index < self.spawn_rate and index < len(self.enemies):
                            # Spawn enemies in a set interval (not all at once)
                                e = self.enemies[index]
                                if e != t.target and self.distance(e, t.target) - e.radius < t.radius:
                                    e.hp -= t.dmg
                                index += 1
                if t.target is None or t.target.is_defeated() or not t.target.visible:
                        t.target = None
            if self.spawn_timer.time >= self.spawn_interval:
                    rate_inc = 3
                    if self.spawn_rate + rate_inc > len(self.enemies):
                        rate_inc = len(self.enemies) - self.spawn_rate
                    self.spawn_rate += rate_inc
                    self.spawn_timer.reset()
                    self.spawn_timer.start_timer()
        # Display Castle Health
        fill(255, 0, 0)
        rect(1175, 900, 150, 20)
        if not self.gameover():
            fill(0, 150, 0)
            rect(1175, 900, 150 * self.castleHP / self.totalHP, 20)
        # Display score, highscore, money, etc
        self.display_scorebar()
        self.display_icons()
        if self.wave_timer.is_set:
            fill(0, 0, 255)
            rect(170, 220, (170 / self.wave_interval) * (self.wave_interval * 1000 - self.wave_timer.time) / 1000, 15)
    def display_always(self):
        # Display this when game should not be running
        for r in range(len(self.path)):
            for c in range(len(self.path[r])):
                noStroke()
                if self.path[r][c] == 0:
                    # Print green blocks
                    fill(0, 230, 0)
                elif self.path[r][c] == 1:
                    # Print brown blocks
                    fill(130, 80, 80)
                elif self.path[r][c] == 2:
                    # Print gray blocks
                    fill(100)
                elif self.path[r][c] == 3:
                    # Print black
                    fill(0, 0, 0)
                rect(c * 50, r * 50 + 200, 50, 50)
        self.display_scorebar()
        self.display_icons()
        # Show Castle HP
        fill(0, 150, 0)
        rect(1175, 900, 150, 20)
        # Unmoving timer
        fill(0, 0, 255)
        rect(170, 220, 170, 15)
    def display_scorebar(self):
        fill(204, 255, 255)
        rect(0, 0, 1500, 200)
        fill(0)
        textFont(createFont("UD Digi Kyokasho NP-B", 40))
        textAlign(LEFT)
        text("Money:", 1150, 22, 200, 50)
        text("Score: {}".format(self.score), 5, 18, 750, 50)
        text("High Score: {}".format(self.highscore), 5, 72, 700, 50)
        wavestr = str(self.wave) + " (Boss Stage)" if self.wave % 10 == 0 and self.wave > 0 else self.wave
        text("Wave: {}".format(wavestr), 5, 126, 700, 50)
        textAlign(RIGHT)
        if self.no_money:
            if self.blink_count < self.blink and self.blink_count % 5 == 0:
                fill(255, 0, 0)
            self.blink_count += 1
            if self.blink_count > self.blink:
                self.no_money = False
                self.blink_count = 0
        text(str(self.money), 1200, 20, 290, 55)
    def display_icons(self):
        for i in range(5):
            stroke(0)
            strokeWeight(4)
            fill(100)
            rect(730 + 150 * i, 86, 100, 100)
            noStroke()
            shape(self.icons[i])
    def show_tower_info(self, x, y):
        t = self.tower_at(x, y)
        if t is not None:
            t.show_info(x, y)
        else:
            if x >= 730 and x <= 830:
                self.ticons[0].show_info(x, y)
            elif x >= 880 and x <= 980:
                self.ticons[1].show_info(x, y)
            elif x >= 1030 and x <= 1130:
                self.ticons[2].show_info(x, y)
            elif x >= 1180 and x <= 1280:
                self.ticons[3].show_info(x, y)
            elif x >= 1330 and x <= 1430:
                self.ticons[4].show_info(x, y)  
