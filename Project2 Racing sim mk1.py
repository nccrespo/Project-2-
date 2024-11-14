import pygame
from math import cos as cosine, sin as sine, pi

def cos(angle): return cosine((pi*angle)/180)
def sin(angle): return sine((pi*angle)/180)


pygame.init() # SCEEN GLOBAL VARABLES
SCREEN_SCALE = .75
SCREEN_WIDTH = 1920*SCREEN_SCALE
SCREEN_HEIGHT = 1080*SCREEN_SCALE
SCREEN_MWIDTH = SCREEN_HEIGHT/2
SCREEN_MHEIGHT = SCREEN_HEIGHT/2
ACCELERATION = 0.0012 # SHOULD BE POSITIVE

#points for the track here
OUT_LOOP = ((100,700),(100,20),(500,700))
IN_LOOP = ()
font = pygame.font.Font(None, 74)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

run = True

class Track():
    def __init__(self):
        self.w = 15
        self.h = 15
        self.img = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.sprite.Sprite()
        pygame.draw.lines(self.img, (0,255,0), True, OUT_LOOP)

    def draw(self,screen):
        screen.blit(self.img,(20,10))
    

#pygame.draw.aalines()
#car class that player controls and debug windows related to the player
class Player():
    def __init__(self):
        self.w = 25
        self.h = 12
        self.bug = False
        self.img = pygame.Surface((self.w,self.h)) #Creates new surface
        self.img.set_colorkey((255,255,255)) # Set backgrond color to black
        self.img.fill((255,0,0)) # Fill surface with color red

        self.x = SCREEN_MWIDTH
        self.y = SCREEN_MHEIGHT
        self.angle = 0
        self.c_speed = 0
        self.max_speed = 0.85
        self.min_speed = -0.85
        self.friction = 0.0004

    

    def debug(self):
        self.bug = not self.bug

    def move(self, acceleration, rotation):
        # Update angle
        self.angle = (self.angle+rotation)%360
        #if   self.c_speed > 0: self.angle = (self.angle+rotation)%360
        #elif self.c_speed < 0: self.angle = (self.angle-rotation)%360
        #else:                  pass

        # Apply acceleration
        self.c_speed += acceleration
        
        # Apply Friction
        if self.c_speed > 0: # Going forward
            self.c_speed -= self.friction
            if self.c_speed < 0: self.c_speed = 0
        elif self.c_speed < 0: # Going backwards
            self.c_speed += self.friction
            if self.c_speed > 0: self.c_speed = 0

        # Make sure current speed is within min and max limits
        if   self.c_speed >= self.max_speed: self.c_speed = self.max_speed
        elif self.c_speed <= self.min_speed: self.c_speed = self.min_speed

        # Update position        
        self.x += cos(self.angle)*self.c_speed
        self.y -= sin(self.angle)*self.c_speed
        
        #print(self.angle) # Debug code


    def draw(self, screen):
        speed_text = font.render("speed: "+str(self.c_speed), True, (255,255,255)) 
        pos_text = font.render("position: ("+str(int(self.x))+","+str(int(self.y))+")", True, (255,255,255))
        imgCopy = self.img.copy() # Creates a copy of the Player Img
        imgCopy = pygame.transform.rotate(imgCopy, self.angle)
        rect = imgCopy.get_rect() # Gets the rectangle of player
        rect.center = (self.x, self.y) # Center the surface on the coordinates

        screen.blit(imgCopy, rect)
        if self.bug == True:
            screen.blit(pos_text,(10,10))
            screen.blit(speed_text,(10,60))


        half_w = self.w/2
        half_h = self.h/2
        fb_dist = 25
        lr_dist = 12
        #code for dots around car (thank you brandon and also IDK what to do with this yet)
        pygame.draw.circle(screen, (255,255,255), (self.x+(cos(self.angle)*(half_w+fb_dist)), self.y-(sin(self.angle)*(half_w+fb_dist))), 2)
        pygame.draw.circle(screen, (0,0,255), (self.x+(sin(self.angle)*(half_h+lr_dist)), self.y+(cos(self.angle)*(half_h+lr_dist))), 2)
        pygame.draw.circle(screen, (0,255,0), (self.x-(sin(self.angle)*(half_h+lr_dist)), self.y-(cos(self.angle)*(half_h+lr_dist))), 2)
        pygame.draw.circle(screen, (255,255,255), (self.x-(cos(self.angle)*(half_w+fb_dist)), self.y+(sin(self.angle)*(half_w+fb_dist))), 2)



player1 = Player() #creates player class
Track1 = Track()
prev_key = None #used so debug toggle isn't pressed on every frame

while run:
    screen.fill((0, 0, 0))
    


    key = pygame.key.get_pressed()
    

    accel = 0
    rotation = 0

    if True in (key[pygame.K_w], key[pygame.K_UP]): accel += ACCELERATION
    if True in (key[pygame.K_a], key[pygame.K_LEFT]): rotation += 0.5
    if True in (key[pygame.K_s], key[pygame.K_DOWN]): accel -= ACCELERATION
    if True in (key[pygame.K_d], key[pygame.K_RIGHT]): rotation -= 0.5

    player1.move(accel, rotation)

    if key[pygame.K_F5] == True: run = False
    if key[pygame.K_F4] == True and prev_key != key: player1.debug()

    prev_key = key
    
    # Commented out because cannot reach x button to close window. Use f5
    # Commented Back in because it magic and IMPORTANT DO NOT REMOVE IDK WHY
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    Track1.draw(screen)
    player1.draw(screen)
    pygame.display.flip()
    #pygame.display.update()


