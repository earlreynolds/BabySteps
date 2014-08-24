#Level Loader Test

"""This code tests a level loading function to change levels when the
player exits the current level though a door."""

########TO DO########

#Make the text prompt interactive.
#Make it possible to enter doors from any side
#Set camera to particular coordinates for each level when it is loaded.
#Organizational bother.
#More interesting level building


import pygame, os, sys, random
from pygame import *



pygame.init()

load_coords = None

CAMINIT = True
chars = []
walls = []
doors = []
background = []

WINWIDTH = 800
WINHEIGHT = 600

CAMERASLACK = 200
P_FAST = 5
P_SLOW = 3
STOP = 0
PLAYERSPEED = P_SLOW
wall_width = 100
wall_height = 100

doorimg = pygame.image.load('door.png')
wallimg = pygame.image.load('wall.png')
playerimg = pygame.image.load('player.png')
npcimg = pygame.image.load('npc.png')
npc2img = pygame.image.load('walk1.png')
talking = False

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

FILLCOLOR = BLUE

current_text = "What? Why is this here? This doesn't belong here."
dialog_font = pygame.font.Font('freesansbold.ttf', 16)
dialog_text = dialog_font.render(current_text, True, WHITE)
dialog_rect = dialog_text.get_rect()
dialog_rect.center = (WINWIDTH/2, 500)
press = None

##wtf = True
##wtf_count = 0



#images = {'player': pygame.image.load('player.png'),}

#Definition of Character class. Each character has a name, an associated image,
#and a rectangle used to keep track of their location and size. This class also
#has a function used to move the character around the map. Player-controlled
#characters move according to user input; NPCs are controlled by scripts or
#semi-random movement functions around a designated point.

class Character(object):
    def __init__(self, name, width, length):
        #                       xpos ypos wid len
        self.rect = pygame.Rect(300, 300, width, length)
        self.name = name
        self.dialog = []
        chars.append(self)
        #self.image = images(self)
        
    def move(self, dx, dy):
            if dx != 0:
                self.move_single_axis(dx, 0)
            if dy != 0:
                self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):
        #move character
        self.rect.x += dx
        self.rect.y += dy

        #Another part of the move function is to keep players from walking over
        #or through walls, doors, and other characters.The following loop takes
        #care of that by matching wall edges to player edges in the event of
        #collisions.

        for stuff in walls+chars+doors: #so none of these get bumped into
            if self != stuff:
                if self.rect.colliderect(stuff.rect):
                    if dx > 0: #this covers moving right and hitting a wall
                        self.rect.right = stuff.rect.left
                    if dx < 0: #moving left bump
                        self.rect.left = stuff.rect.right
                    if dy > 0: #bump the top side
                        self.rect.bottom = stuff.rect.top 
                    if dy < 0: #bump the bottom (heh heh heh)
                        self.rect.top = stuff.rect.bottom


                       


#Definition of Wall class. This class stores wall coordinates as lists
#to be parsed by the wall_build function, which turns them into
#into standard blocks of the map that characters cannot move through from
#any side.
        
class Wall(object):
    def __init__(self, pos):
        
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], wall_width, wall_height)

class Door(object):
    def __init__(self, pos, door_id):
        doors.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], wall_width, wall_height)
        self.door_id = door_id
        self.load_coords = (self.rect.x, self.rect.y + wall_height)

                       
class Background(object):
    def __init__(self, pos):
        
        background.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], wall_width, wall_height)

#This is a simple function to determine if two object rectangles are adjacent.
#This is necessary because the built-in "collide" function is being used for bumping stuff together.
        
def adjacent(thing1, thing2):
    #((thing2.rect.centerx - thing2.rect.centerx)**2 + (thing1.rect.centery - thing2.rect.centery)**2)**0.5 <= max((thing1.rect.width + thing2.rect.width)/2, (thing1.rect.height + thing2.rect.height)/2):
    TB = thing1.rect.top == thing2.rect.bottom
    BT = thing1.rect.bottom == thing2.rect.top
    LR = thing1.rect.left == thing2.rect.right
    RL = thing1.rect.right == thing2.rect.left

    left_dist = abs(thing1.rect.midleft[1] - thing2.rect.midright[1])
    right_dist = abs(thing1.rect.midright[1] - thing2.rect.midright[1])
    top_dist = abs(thing1.rect.midtop[0] - thing2.rect.midbottom[0])
    bottom_dist = abs(thing1.rect.midbottom[0] - thing2.rect.midtop[0])

   
    
    if (TB and top_dist < 50) or (BT and bottom_dist < 50) or (LR and left_dist < 50) or (RL and right_dist < 50):
        return True
    else:
        return False

transition = False
#This function builds the level from level strings, stored elsewhere
door_id_range = [str(x) for x in range(10)]
def level_build(ListOfWalls, ListOfDoors, ListOfBackgrounds, LevelOfInterest):
    global CAMINIT, walls, doors, background, levels, transition
    
    walls = []
    
    doors = []
   
    background = []
    
    CAMINIT = True
    
    x = y = 0
    for row in LevelOfInterest:
        for col in row:
            if col == "W":
                Wall((x, y))
                
            elif col in door_id_range:
                Door((x, y), col)
                
            elif col == 'P':
                player.rect.x = x
                player.rect.y = y
                
            elif col == 'K':
                npc.rect.x = x
                npc.rect.y = y
                
            elif col == 'H':
                npc2.rect.x = x
                npc2.rect.y = y
                
            Background((x, y))
            x += wall_width
            
        y += wall_height
        x = 0
    return None

doorno = None
def level_change():
    global transition, doorno
    for door in doors:
        if adjacent(player, door):
            transition = True
            doorno = door.door_id
##        level_build(walls, doors, background, levels[int(door.door_id)-1])
    

alpha=0
andwereback = None

def fade_out():
    global transition, fade_screen, alpha, andwereback
    if transition == True:
        if alpha < 255:
            fade_screen.fill((0, 0, 0, alpha))
            alpha += 10
            #print "alpha =", alpha
        else:
            #print "huh?"
            alpha = 255
            fade_screen.fill((0, 0, 0, alpha))
            andwereback = True
            transition = False
            #print "bong"
        
def fade_in():
    global alpha, andwereback, transition, fade_screen, doorno
    
    if andwereback == True and alpha >= 0:
        level_build(walls, doors, background, levels[int(doorno)-1])
        fade_screen.fill((0, 0, 0, alpha))
        alpha -= 10
        #print "now alpha is", alpha
    elif andwereback == True and alpha <=0:
        alpha = 0
        #print "what"
        fade_screen.fill((0, 0, 0, alpha))
        andwereback = False
        #print "crackpipe"

player = Character('HERO', 79, 100)

npc = Character("EARL'S BIG HEAD", 150, 250)

npc2 = Character("CORY", 73, 197)

npc.dialog.append("MY BUTT SURE DOES ITCH")
npc.dialog.append("YEP. MIGHTY ITCHY, THESE BUNS.")
npc.dialog.append("MAYBE IT'D HELP IF I SHAVED.")
npc.dialog.append("YOU THINK?")

npc2.dialog.append("I'm just here for the investment meeting.")
npc2.dialog.append("And the timeshare seminar.")


#This function defines a camera that follows the player. It works by drawing
#the level environment relative to the player's absolute position, which is
#changed by keyboard input. The player can move a little way outside a central
#box before the camera starts to follow. It stops when the player stops.

#For this function to work, there MUST be a Character instance assigned to
#"player" (not the string. There's a better way to word this).




def player_cam():
    global CAMINIT, CAMERASLACK, CAMERAX, CAMERAY


    #initialize the camera so it centers on the player
    if CAMINIT == True:
        
        CAMERAX = (player.rect.x - WINWIDTH/2)
        CAMERAY = (player.rect.y - WINHEIGHT/2)    
        CAMINIT = False

     #this loop iterates through the list and puts a wall at each coordinate pair
        

    #######DDDDDDDDDDDDDDRRRRRRAAAAAAAAAWWWWWWWWWW#######
    for bg in background:
        pygame.draw.rect(screen, WHITE, (bg.rect[0] - CAMERAX, bg.rect[1] - CAMERAY, 75, 75))
    for wall in walls:
        screen.blit(wallimg, (wall.rect[0] - CAMERAX, wall.rect[1] - CAMERAY))
    for door in doors:
        screen.blit(doorimg, (door.rect[0] - CAMERAX, door.rect[1] - CAMERAY))
        
    screen.blit(npc2img, (npc2.rect.x - CAMERAX, npc2.rect.y - CAMERAY))
    screen.blit(npcimg, (npc.rect.x - CAMERAX, npc.rect.y - CAMERAY))
    screen.blit(playerimg, (player.rect.x - CAMERAX, player.rect.y - CAMERAY))
    
    
    key = pygame.key.get_pressed()
    
    if key[pygame.K_LEFT]:
        player.move(-PLAYERSPEED, 0)
        if CAMERAX + CAMERASLACK > player.rect.x:
            CAMERAX -= PLAYERSPEED

        
    if key[pygame.K_RIGHT]:
        player.move(PLAYERSPEED, 0)
        if CAMERAX - CAMERASLACK - player.rect[2] + WINWIDTH < player.rect.x:
            CAMERAX += PLAYERSPEED
        
    if key[pygame.K_UP]:
        player.move(0, -PLAYERSPEED)
        if CAMERAY + CAMERASLACK > player.rect.y:
            CAMERAY -= PLAYERSPEED
        
    if key[pygame.K_DOWN]:
        player.move(0, PLAYERSPEED)
        if CAMERAY - CAMERASLACK + WINHEIGHT - player.rect[3] < player.rect.y:
            CAMERAY += PLAYERSPEED
        return None



  
#Controls NPC interactions. This is run inside the main loop, but only as a
#check unless a character is nearby and the d-key is pressed.
TALKING = None
dialog_counter = None
CURRENT_NPC = player

def dialog():
    global dialog_counter, CURRENT_NPC, TALKING, PLAYERSPEED, dialog_text, dialog_rect, dialog_font, current_text, screen

    if TALKING == True:
        dialog_counter = 0
        CURRENT_NPC = player
        TALKING = False
    else:
        for char in chars:
            if char != player and adjacent(player, char):
                CURRENT_NPC = char
                TALKING = True
                dialog_counter = 0



    
    print CURRENT_NPC.name
                
#This function displays text by creating a display area, then blitting the
#text over it. If the text is dialog, it displays the speaking character in
#the uppper left above the main text.
def text_disp():
    global current_text, dialog_text
    if TALKING == True:
        current_text = CURRENT_NPC.dialog[dialog_counter]
        dialog_text = dialog_font.render(current_text, True, WHITE)
        pygame.draw.rect(screen, BLUE, (0, 400, 800, 200))
        name = dialog_font.render(CURRENT_NPC.name, True, WHITE)
        name_rect = name.get_rect()
        name_rect.left = 20
        name_rect.top = 420
        screen.blit(name, name_rect)
        screen.blit(dialog_text, dialog_rect)
    
        
        

level1 = [
"WWWWWWWWWWWWWWWWWWWWWWWWWW",
"W      WW   K    WW      W",
"W      WW        WW      W",
"W      WW        WW      W",
"W      WWWW    WWWW      W",
"W      W2WW    WW3W      W",
"W       P                W",
"W                        W",
"W               H        W",
"W                        W",
"W                        W",
"WWWWWWWWWWWWWWWWWWWWWWWWWW"
]

level2 = [
"WWWWWWW",
"W  K  W",
"W     W",  
"W     W",
"W     W",
"W     WWWW1WWWWWWWWWWWWWWW",
"W         P         3    W",
"W               H        W",
"W                        W",
"WWWWWWWWWWWWWWWWWWWWWWWWWW"
]

level3  = [
"WWWWWWWWWWWWWWWWWW",
"W                W",
"WWWWWWW          W",
"W     W          W",
"W     WWWW1WW    W",
"W     WWWWWWW    W",
"W          2W    W",
"W          WW    W",
"W     P          W",
"W                W",
"WWWWWWWWWWWWWWWWWW"
]
levels = [level1, level2, level3]
level_build(walls, doors, background, level2)

screen = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
new_screen = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
fade_screen = new_screen.convert_alpha()
#os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.display.set_caption("HEY GUYS LOOK AT MY BIG OL VIDEOJAME.")
clock = pygame.time.Clock()


fade_screen.fill((0, 0, 0, 0))
running = True 
while running:

##    for char in chars:
##        if char != player:
##            if adjacent(player, char):
##                print char.name
    
    for event in pygame.event.get(): #event handler
        #standard quit game stuff
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif event.type==KEYDOWN:
            if event.key == K_a:
                PLAYERSPEED = P_FAST
                FILLCOLOR = RED
            
        elif event.type==KEYUP:
            if event.key == K_a:
                PLAYERSPEED = P_SLOW
                FILLCOLOR = BLUE
            elif event.key == K_d:
                if TALKING == True and dialog_counter < (len(CURRENT_NPC.dialog)-1):
                    dialog_counter += 1
                else:
                    dialog()
                level_change()
            elif event.key == K_l:
                transition = True
                
                
                
    screen.fill(FILLCOLOR)
    player_cam()
    fade_out()
    fade_in()

    screen.blit(fade_screen, (0, 0))
    if TALKING == True:
        text_disp()

    
    pygame.display.flip()
    clock.tick(60)
