import pygame
from sys import exit
import random

pygame.init()

obstacle_array = []

#initialization
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
gravity = 0
start_x_pos = 100
start_y_pos = 500
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
secs_counter = 3
allow_count = True
obstacle_speed = 8

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Incel Bird (Press W to jump)')
clock = pygame.time.Clock()

background = pygame.image.load('background/room.png').convert()

grass = pygame.image.load('background/grass.png').convert_alpha()
grass_rect = grass.get_rect(topright = (SCREEN_WIDTH, SCREEN_HEIGHT - 25))
floor = grass_rect.top



incel1 = pygame.image.load('entities/incel.png').convert_alpha()
incel2 = pygame.image.load('entities/incel2.png').convert_alpha()
player_sprite = incel1


class Obstacle:
    
    def __init__(self):
        
        self.gap_bottom = random.randint(400, SCREEN_HEIGHT - 100)
        self.bottom_obstacle = pygame.image.load('entities/soap.png').convert_alpha()
        self.bottom_hitbox = self.bottom_obstacle.get_rect(topleft = (SCREEN_WIDTH, self.gap_bottom))
        self.top_obstacle = pygame.image.load('entities/soap.png').convert_alpha()
        self.top_hitbox = self.top_obstacle.get_rect(bottomleft = (SCREEN_WIDTH, self.gap_bottom - 300))
        

class Player:
    
    def __init__(self, start_x_pos, start_y_pos):
        
        self.sprite = pygame.image.load('entities/incel.png').convert_alpha()
        self.rect = self.sprite.get_rect(center = (start_x_pos, start_y_pos))


player = Player(start_x_pos, start_y_pos)

def spawn_obstacle():
    '''creates a new obstacle with a random gap and stores it in the array'''
    global obstacle_array
    obstacle = Obstacle()
    obstacle_array.append(obstacle)

def remove_obstacle(obstacle_array) -> bool:
    '''deletes an obstacle if it is off the screen'''
    global allow_count
    for obstacle in obstacle_array:
        if obstacle.bottom_hitbox.right <= 0:
            obstacle_array.remove(obstacle)
            return True
        else:
            return False

def move_obstacle(obstacle_array, speed):
    '''moves the top and bottom hitboxes'''
    for obstacle in obstacle_array:
        obstacle.bottom_hitbox.left -= speed
        obstacle.top_hitbox.left -= speed
        screen.blit(obstacle.bottom_obstacle, obstacle.bottom_hitbox)
        screen.blit(obstacle.top_obstacle, obstacle.top_hitbox)
        

def check_collision(player, obstacle_array) -> bool:
    '''checks if player is colliding with obstacle'''
    
    for obstacle in obstacle_array:
        global allow_count
        if(player.rect.right >= obstacle.bottom_hitbox.left
           and player.rect.left <= obstacle.bottom_hitbox.right):
            if(player.rect.bottom >= obstacle.bottom_hitbox.top
               or player.rect.top <= obstacle.top_hitbox.bottom):
                allow_count = False
                return  True
            else:
                allow_count = True
                return False
        
def check_if_floor(player, floor) -> bool:
    '''checks if the player is touching the floor'''
    if player.rect.bottom == floor:
        return True
    else:
        return False

def count_score(player, obstacle_array):
    global allow_count
    for obstacle in obstacle_array:
        if player.rect.left >= obstacle.bottom_hitbox.right:
            if allow_count:
                global score
                score += 1
                allow_count = False

#Game1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_w:
                gravity = -15            

    text = font.render(str(score), True, (255,255,255), (0,0,0))
    
    gravity += .7
    player.rect.bottom += gravity
    if player.rect.bottom>= floor: player.rect.bottom = floor
    
    screen.blit(background, (0,0))
    
    '''
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        print('space')
    if keys[pygame.K_d]:
        player.rect.x += 4
    if keys[pygame.K_a]:
        player.rect.x -= 4
    '''
    
    screen.blit(player.sprite, player.rect)

    #spawns obstacle after 3 seconds of flight time, resets timer
    if secs_counter == 90:
        spawn_obstacle()
        secs_counter = 0
    
    #functions that run the game
    move_obstacle(obstacle_array, obstacle_speed)
    remove_obstacle(obstacle_array)
    
    if check_collision(player, obstacle_array) or check_if_floor(player, floor):
        obstacle_speed = 0
        player.sprite = incel2
    else:
        obstacle_speed = 8
        player.sprite = incel1
        secs_counter += 1
    count_score(player, obstacle_array)
        
    
    screen.blit(grass, grass_rect)
    screen.blit(text, (SCREEN_WIDTH - 100, 100))
    pygame.display.update()
    clock.tick(60)