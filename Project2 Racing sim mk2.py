import pygame
import time
from math import cos as cosine, sin as sine, pi

def cos(angle): return cosine((pi*angle)/180)
def sin(angle): return sine((pi*angle)/180)
pygame.init() 

#this set of global varables are used in the creation of the classes ---------------------

# SCEEN GLOBAL VARABLES
SCREEN_SCALE = .75
SCREEN_WIDTH = 1920*SCREEN_SCALE
SCREEN_HEIGHT = 1080*SCREEN_SCALE
SCREEN_MWIDTH = SCREEN_HEIGHT/2
SCREEN_MHEIGHT = SCREEN_HEIGHT/2
ACCELERATION = 0.012 # SHOULD BE POSITIVE


# sprite images 
TRACK_IMAGE = 'RACE_TRACK.png'
PLAYER_IMAGE = 'CAR.png'
CHECK_IMAGE = 'CHECK_POINT.png'

font = pygame.font.Font(None, 74)

run = True


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Load the sprite image

#outputs RAW track times into a readable txt file
def write_endfile():
    f = open("Laptimes.txt", "w")
    for i in range(len(check1.lap_times)):
        f.write("lap "+str(i+1)+" "+str(check1.lap_times[i])+"\n")

# Function to find intersection points between a ray and the track mask
def cast_ray_to_mask(start_pos, angle, track_mask, track_rect):
    max_distance = 1000  # Maximum length of the ray
    for distance in range(0, max_distance):
        x = start_pos[0] + cos(angle) * distance
        y = start_pos[1] - sin(angle) * distance
        if track_rect.collidepoint(x, y) and track_mask.get_at((int(x - track_rect.left), int(y - track_rect.top))):
            return (x, y)  # Return the point of intersection
    return None  # No intersection found
    
#self explanitory
class Track(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #import image, scale image to screen, mask elements
        self.image = pygame.image.load(TRACK_IMAGE).convert_alpha()
        new_width = int(self.image.get_width() * SCREEN_SCALE)
        new_height = int(self.image.get_height() * SCREEN_SCALE)
        self.image = pygame.transform.scale(self.image,(new_width,new_height))
        self.image_mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()


#similar to track but moves the sprite after collition with next point method
class Checkpoints(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #list of cordnites of check point spots 
        self.points = [(105,300),(200,110),(600,200)]
        self.prev_point = None
        self.c_point = 0
        self.num_points = len(self.points)
        #recording lap time varables
        self.lap_times = [] #lap time is recorded and append after the last checkpoint is passed (see Checkpoints class)
        self.lap_time_start = None
        self.lap_first = True
        

        #copied from Track Class
        #import image, scale image to screen, mask elements
        self.image = pygame.image.load(CHECK_IMAGE).convert_alpha()
        new_width = int(self.image.get_width() * SCREEN_SCALE)
        new_height = int(self.image.get_height() * SCREEN_SCALE)
        self.image = pygame.transform.scale(self.image,(new_width,new_height))
        self.image_mask = pygame.mask.from_surface(self.image)
        
        self.x,self.y = self.points[self.c_point]

        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def Next_Point(self):
        self.prev_point = self.points[self.c_point]
        if self.c_point+1 == self.num_points:
            
            self.c_point = 0

        elif self.c_point == 0:
            if self.lap_first != True:
                lap_time_end = time.time()
                self.lap_times.append(lap_time_end - self.lap_time_start)
                self.lap_time_start = lap_time_end
            else:
                self.lap_time_start = time.time()
                self.lap_first = False
            self.c_point +=1

        else:self.c_point +=1

        self.x,self.y = self.points[self.c_point]
        self.rect = self.image.get_rect(center=(self.x, self.y))




#pygame.draw.aalines()
#car class that player controls and debug windows related to the player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bug = False
        self.image = pygame.image.load(PLAYER_IMAGE).convert_alpha()
        
        new_width = int(self.image.get_width() * SCREEN_SCALE)
        new_height = int(self.image.get_height() * SCREEN_SCALE)
        self.original_image = pygame.transform.scale(self.image,(new_width,new_height))
        self.image = self.original_image.copy()
        self.image_mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()  # Create a rect for positioning
        self.rect.center = (SCREEN_MWIDTH, SCREEN_MHEIGHT)  # Set initial 

        self.x = SCREEN_MWIDTH-250
        self.y = SCREEN_MHEIGHT+50
        self.respawn_p = (self.x,self.y)

        self.angle = 90
        self.c_speed = 0
        self.max_speed = 1
        self.min_speed = -.5
        self.friction = 0.001

    

    def debug(self):
        self.bug = not self.bug
    
    def set_pos(self,t):
        print(t)
        self.x, self.y = t[0],t[1]
        
    
    def set_respawn(self,t):
        self.respawn_p = t
        
    
    def respawn(self):
        self.c_speed = 0
        self.set_pos(self.respawn_p)

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
            if self.c_speed < 0: 
                self.c_speed = 0

        elif self.c_speed < 0: # Going backwards
            self.c_speed += self.friction
            if self.c_speed > 0: 
                self.c_speed = 0

        # Make sure current speed is within min and max limits
        if   self.c_speed >= self.max_speed: 
            self.c_speed = self.max_speed
        elif self.c_speed <= self.min_speed: 
            self.c_speed = self.min_speed

        # Update position        
        self.x += cos(self.angle)*self.c_speed
        self.y -= sin(self.angle)*self.c_speed

        self.image = pygame.transform.rotate(self.original_image, self.angle-90)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.image_mask = pygame.mask.from_surface(self.image)

    def cast_rays(self, track):
        for angle_offset in range(-45, 46, 15):  # Cast rays at 15-degree intervals
            
            ray_angle = (self.angle + angle_offset) % 360
            intersection = cast_ray_to_mask((self.x, self.y), ray_angle, track.image_mask, track.rect)
            if intersection:
                pygame.draw.circle(screen, (255, 0, 0), (int(intersection[0]), int(intersection[1])), 5)
        
        



      #code for dots around car (thank you brandon and also IDK what to do with this yet)
    ''' pygame.draw.circle(screen, (255,255,255), (self.x+(cos(self.angle)*(half_w+fb_dist)), self.y-(sin(self.angle)*(half_w+fb_dist))), 2)
        pygame.draw.circle(screen, (0,0,255), (self.x+(sin(self.angle)*(half_h+lr_dist)), self.y+(cos(self.angle)*(half_h+lr_dist))), 2)
        pygame.draw.circle(screen, (0,255,0), (self.x-(sin(self.angle)*(half_h+lr_dist)), self.y-(cos(self.angle)*(half_h+lr_dist))), 2)
        pygame.draw.circle(screen, (255,255,255), (self.x-(cos(self.angle)*(half_w+fb_dist)), self.y+(sin(self.angle)*(half_w+fb_dist))), 2)
    '''


#creates  objecsts
player1 = Player() 
track1 = Track()
check1 = Checkpoints()

#create sprite groups 
track_sprites = pygame.sprite.Group()
track_sprites.add(track1)

Check_sprites = pygame.sprite.Group()
Check_sprites.add(check1)

player_sprites = pygame.sprite.Group()
player_sprites.add(player1)

#this set of global varables are used in running pygame ---------------------

prev_key = None #used so debug keys arn't pressed multiple times at once
Check_overlap = False #used to stop multiple collitions from happening at once on a checkpoint


while run:
    screen.fill((255, 255, 255))
    


    key = pygame.key.get_pressed()
    

    accel = 0
    rotation = 0

    if True in (key[pygame.K_w], key[pygame.K_UP]): accel += ACCELERATION
    if True in (key[pygame.K_a], key[pygame.K_LEFT]): rotation += 1
    if True in (key[pygame.K_s], key[pygame.K_DOWN]): accel -= ACCELERATION
    if True in (key[pygame.K_d], key[pygame.K_RIGHT]): rotation -= 1
    if key[pygame.K_n] == True and prev_key != key: check1.Next_Point()

    
    # key toggle code
    if key[pygame.K_F5] == True: 
        run = False
        write_endfile()

    if key[pygame.K_F4] == True and prev_key != key: player1.debug()
    prev_key = key

    player1.move(accel,rotation)
    player1.cast_rays(track1)

    offset = (int(player1.rect.left - track1.rect.left), int(player1.rect.top - track1.rect.top))
    track_collision = track1.image_mask.overlap(player1.image_mask, offset)

    checkpoint_offset = (int(player1.rect.left - check1.rect.left), int(player1.rect.top - check1.rect.top))
    checkpoint_collision = check1.image_mask.overlap(player1.image_mask, checkpoint_offset)
    



    # checks collision and changes the track to red if collision is detected VERY DISORENTATING
    if track_collision is not None:
        player1.respawn()
    elif (checkpoint_collision is not None) and (Check_overlap == False):
        Check_overlap = True
        check1.Next_Point()
        player1.set_respawn(check1.prev_point)
        Check_overlap = False
        
    
    # Commented out because cannot reach x button to close window. Use f5
    # Commented Back in because it magic and IMPORTANT DO NOT REMOVE IDK WHY
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            write_endfile()
            run = False
    

    track_sprites.draw(screen)
    player_sprites.draw(screen)
    Check_sprites.draw(screen)
    pygame.display.flip()
    #pygame.display.update()


