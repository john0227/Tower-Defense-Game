from Game import Game

icons = []
tutorial_shape = []
tutorial_text = []
index = 0
icon_is_pressed = False
tower_is_pressed = False
show_towerinfo = False
show_tower_range = False
show_tutorial = True
tradius = 0

game = Game()

def setup():
    size(1500, 950)
    create_shapes()
    create_tutorial()
    global icons
    game.icons = icons
    # Create game over screen

def draw():
    if show_tutorial:
        game.display_always()
        shape(tutorial_shape[index])
        txt = tutorial_text[index]
        tsize = txt[0]
        fill(0)
        textFont(createFont("UD Digi Kyokasho NP-B", tsize))
        textAlign(LEFT)
        text(txt[1], txt[2], txt[3], txt[4], txt[5])
        if index == 0:
            fill(255)
            textSize(15)
            s = "                 "
            text("[Navigate tutorial with right and left arrow keys]" + s +"[Press enter to start game]", width/2 - 335, height / 2 + 180)
        elif index == 5:
            fill(255)
            textSize(15)
            textAlign(RIGHT)
            text("[Press enter]", width / 2 + 370, height / 2 + 120)
        textAlign(LEFT)
    else:
        game.display()
        if game.gameover():
            rectMode(CENTER)
            fill(0)
            rect(width / 2, height / 2, 540, 380, 15)
            fill(200)
            rect(width / 2, height / 2, 530, 370, 15)
            rectMode(CORNER)
            textAlign(CENTER, CENTER)
            fill(0)
            textFont(createFont("UD Digi Kyokasho NP-B", 40))
            text("GAME OVER", width / 2, height / 2 - 105)
            textSize(30)
            text("Press 'r' to restart\nor\nExit the window to quit", width / 2, height / 2 + 50)
            textAlign(LEFT)
        if show_tower_range:
            t = game.tower_at(mouseX, mouseY)
            fill(color(104, 255, 255, 100))
            ellipse(mouseX, mouseY, 2 * tradius, 2 * tradius)
            fill(255)
            ellipse(mouseX, mouseY, 25, 25)
        if show_towerinfo:
            game.show_tower_info(mouseX, mouseY)

def mousePressed():
    global tradius, icon_is_pressed, show_towerinfo, tower_is_pressed, show_tower_range
    tr = game.radius_at_pos(mouseX, mouseY)
    if tr > 0:
        tradius = tr
        icon_is_pressed = True
        show_towerinfo = True
    elif game.has_tower(mouseX, mouseY):
        tradius = game.tower_at(mouseX, mouseY).reach
        show_towerinfo = True
        tower_is_pressed = True
        show_tower_range = True
    
def mouseDragged():
    global show_tower_range, show_towerinfo
    if icon_is_pressed:
        show_tower_range = True
        show_towerinfo = False
    if tower_is_pressed and not game.has_tower(mouseX, mouseY):
        show_tower_range = False
        show_towerinfo = False

def mouseReleased():
    global icon_is_pressed, show_tower_range, show_towerinfo, tower_is_pressed, tradius
    if show_tower_range and game.is_buildable(mouseX, mouseY):
        game.build_tower(tradius, mouseX, mouseY)
    icon_is_pressed, show_tower_range, show_towerinfo, tower_is_pressed, tradius = False, False, False, False, 0

def keyPressed():
    global tower_is_pressed, show_tutorial, index, tradius
    if key == CODED:
        if keyCode == RIGHT:
            index = index + 1 if index < 5 else 5
        elif keyCode == LEFT:
            index = index - 1 if index > 0 else 0
    else:
        if tower_is_pressed:
            if key == 'u':
                # Upgrade tower if player has money
                game.upgrade_tower(mouseX, mouseY)
            elif key == 's':
                # Sell tower
                game.sell_tower(mouseX, mouseY)
                tradius = 0
        if key == 'b' and not show_tutorial:
            # Begin wave
            game.start_wave()
        elif key == 'r':
            # Restart game
            game.restart()
            show_tutorial = True
        elif key  == ENTER:
            # Start game
            show_tutorial = False

def create_shapes():
    blaster = createShape(TRIANGLE, 780, 136 - 40, 780 - 30, 136 + 40 , 780 + 30, 136 + 40)
    blaster.setFill(color(255,  51,   0))
    blitz = createShape(QUAD, 930, 136 - 40, 930 + 30, 136 , 930, 136 + 40, 930 - 30, 136)
    blitz.setFill(color(255, 255, 153))
    rhood = createShape(ELLIPSE, 1080, 136, 90, 60)
    rhood.setFill(color(  0, 204,   0))
    mortar = createShape(QUAD, 1230 - 15, 136 - 40, 1230 + 15, 136 - 40, 1230 + 30, 136 + 40, 1230 - 30, 136 + 40)
    mortar.setFill(color(  0, 102, 204))
    bomber = createShape(ELLIPSE, 1380, 136, 80, 80)
    bomber.setFill(color( 89,  89,  89))
    global icons
    icons = [blaster, blitz, rhood, mortar, bomber]
def create_tutorial():
    ############## Create Slide 1 #################
    part1 = createShape(GROUP)
    rectMode(CENTER)
    part1_1 = createShape(RECT, width / 2, height / 2, 700, 400, 15)
    part1_1.setFill(color(100, 205, 255))
    part1_2 = createShape(RECT, width / 2, height / 2, 720, 420, 15)
    part1_2.setFill(color(0))
    rectMode(CORNER)
    part1.addChild(part1_2)
    part1.addChild(part1_1)
    s = ("Everything was peaceful during your time as King/Queen ....... until today\n\n"
    "Aliens have invaded Earth and are trying to take over your castle. They seek your gold and other valuables to offer to their alien ruler.\n\n"
    "Build towers and stop the aliens from getting to your castle as they try to break your line of defense!"
    )
    text1 = (25, s, width/2 - 330, height/2 - 170, 600, 400)
    ############## Create Slide 2 #################
    part2 = createShape(GROUP)
    part2_1 = createShape(RECT, 17.5 * 50 - 2.5, 12.5 * 50 + 217.5, 255, 105, 15)
    part2_1.setFill(color(0))
    part2_2 = createShape(RECT, 17.5 * 50, 12.5 * 50 + 220, 250, 100, 15)
    part2_2.setFill(color(100, 205, 255))
    part2.addChild(part2_1)
    part2.addChild(part2_2)
    text2 = (20, "To the right is your castle and castle HP", 17.5 * 50 + 10, 12.5 * 50 + 242, 235, 50)
    ############## Create Slide 3 #################
    rectMode(CENTER)
    part3 = createShape(GROUP)
    part3_1 = createShape(RECT, 1080, 280, 257, 87, 15)
    part3_1.setFill(color(0))
    part3_2 = createShape(RECT, 1080, 280, 250, 80, 15)
    part3_2.setFill(color(100, 205, 255))
    part3.addChild(part3_1)
    part3.addChild(part3_2)
    text3 = (20, "These are your towers", 1080 - 120, 270, 235, 50)
    ############## Create Slide 4 #################
    part4 = createShape(GROUP)
    part4_1 = createShape(RECT, 400, 180, 407, 107, 15)
    part4_1.setFill(color(0))
    part4_2 = createShape(RECT, 400, 180, 400, 100, 15)
    part4_2.setFill(color(100, 205, 255))
    part4.addChild(part4_1)
    part4.addChild(part4_2)
    text4 = (20, "To the left shows the wave number\nEvery 10 wave is a boss level\n... So prepare well!!", 210, 140, 595, 100)
    ############## Create Slide 5 #################
    part5 = createShape(GROUP)
    part5_1 = createShape(RECT, width / 2, height / 2, 820, 490, 15)
    part5_1.setFill(color(0))
    part5_2 = createShape(RECT, width / 2, height / 2, 810, 480, 15)
    part5_2.setFill(color(100, 205, 255))
    part5.addChild(part5_1)
    part5.addChild(part5_2)
    s = ("Building Towers:\n"
         "    First, click the tower icons on top right side.\n"
         "    Then, drag your mouse to one of the gray blocks and release.\n\n"
         "Upgrading Towers:\n"
         "    First, press down on one of the towers you have built.\n"
         "    Then, type 'u' (lowercase) while pressing your mouse down.\n\n"
         "Selling Towers:\n"
         "    Similar to Upgrading Towers, except press 's' (lowercase)\n\n"
         "Display Tower Info:\n"
         "    If you press down on tower icons or towers you have built,\n"
         "    Game will display the tower's stats and range.")
    text5 = (23, s, width / 2 - 390, height / 2 - 215, 780, 450)
    ############## Create Slide 6 #################
    part6 = createShape(GROUP)
    part6_1 = createShape(RECT, width / 2, height / 2, 780, 280, 15)
    part6_1.setFill(color(0))
    part6_2 = createShape(RECT, width / 2, height / 2, 770, 270, 15)
    part6_2.setFill(color(100, 205, 255))
    part6.addChild(part6_1)
    part6.addChild(part6_2)
    s = ("Restarting Game:\n"
         "    Press 'r' (lowercase) anytime to restart.\n\n"
         "Starting Waves Early:\n"
         "    If you (think you) are prepared, press 'b' (lowercase)\n"
         "    If the wave has not started yet, it will skip cooldown time.\n"
         "    If a wave has started already, the next wave of enemies\n"
         "       will come swarming.")
    text6 = (23, s, width / 2 - 355, height / 2 - 120, 780, 250)
    rectMode(CORNER)
    global tutorial_shape, tutorial_text
    tutorial_shape = [part1, part2, part3, part4, part5, part6]
    tutorial_text = [text1, text2, text3, text4, text5, text6]
