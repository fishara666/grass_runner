import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks()/ 1000) - start_time
    score_surf = test_font.render(f'{current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = ( 350, 50))
    screen.blit(score_surf,score_rect)
    return current_time

def remove_old_obstacles(obstacles):
    good_obstacles = []
    for obstacle_type, obstacle in obstacles:
        if obstacle.x > -100:  
            good_obstacles.append((obstacle_type,obstacle))
    return good_obstacles


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_type, obstacle_rect in obstacle_list:
            obstacle_rect.x -= 6
            if obstacle_type  == 'fly':
                screen.blit(fly_surf,obstacle_rect)
            else:screen.blit(snail_surface,obstacle_rect)
        return obstacle_list
    else: return []
    
def collision(obstacle_rect_list):
    if obstacle_rect_list:
        for obstacle_type, obstacle_rect in obstacle_rect_list:
            if obstacle_rect.colliderect(player_rect):
                return False
    return True

pygame.init()
pygame.display.set_caption("fishara666")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((700, 400))
test_font = pygame.font.Font("Pixeltype.ttf", 64)
game_active = False
start_time = 0
score = 0


sky = pygame.image.load("sky.webp").convert()
sky = pygame.transform.scale(sky, (700, 400))


backGraund_serface = pygame.image.load("grass.webp").convert()
backGraund_serface = pygame.transform.scale(backGraund_serface, (700, 100))

#obstacles
snail_surface = pygame.image.load("snail1.png").convert_alpha()

fly_surf = pygame.image.load("Fly1.png").convert_alpha()
fly_rect = fly_surf.get_rect(center = (700, 180))
obstacle_rect_list = []


player_surf = pygame.image.load("player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_gravity = 0

#game menu
player_stand = pygame.image.load("player_stand.png").convert_alpha()
bigger_player = pygame.transform.scale(player_stand, (150, 160))
player_stand_rect = bigger_player.get_rect(center = (350,270))



instructions_surf1 = test_font.render(f"Welcome to fishara666 game",True, "Black")
instructions_surf2 = test_font.render(f" Press 'SPACE' to start!",True, "Black")
instructions_rect1 = instructions_surf1.get_rect(center = (350, 100))
instructions_rect2 = instructions_surf2.get_rect(center = (350,140))



game_over_surf = test_font.render("Game over", False, (200,70,100))
game_over_rect = game_over_surf.get_rect(center = (350,200))
bigger_game_over = game_over_rect.inflate(40,40)

"""timer"""
obstacle_timer = pygame.USEREVENT + 1 #create my own UNIQE obstacle type (+1 bec there are anothen numbers of events so +1 make its UNIQE)
pygame.time.set_timer(obstacle_timer,1400)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player_rect.bottom == 300:
                        player_gravity = -20
                            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    if player_rect.bottom == 300:
                        player_gravity = -20

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
               
                start_time = int(pygame.time.get_ticks()/ 1000)
                
        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(('snail', snail_surface.get_rect(midbottom=(randint(900,1101), 300))))
            else:obstacle_rect_list.append(('fly', fly_surf.get_rect(center=(randint(1000,1200), 120))))
            
    if game_active:
        screen.blit(sky, (0, 0))
        screen.blit(backGraund_serface, (0, 300))

        score = display_score()
        
        """obstacle movement"""
        obstacle_rect_list = obstacle_movement(obstacle_rect_list) #returns list where are obstacles moved 5 pixels left on the sceen
        obstacle_rect_list = remove_old_obstacles(obstacle_rect_list)
        if not collision(obstacle_rect_list):
            obstacle_rect_list = []
            game_active = False
        
        """player"""
        player_gravity += 1
        player_rect.y += player_gravity      
        if player_rect.bottom >= 300:player_rect.bottom = 300
        screen.blit(player_surf, player_rect)
        
  
        """fly obstacle"""
        
    else:
        screen.fill((94,129,162))
        screen.blit(bigger_player,player_stand_rect)
        background_rect1 = instructions_rect1.inflate(20, 10)  
        background_rect2 = instructions_rect2.inflate(20, 10)
        score_message = test_font.render(f"Your score: {score}",False,(111,196,169))
        score_message_rect = score_message.get_rect(center = (350,150))
        player_rect.midbottom =(80,300)
        player_gravity = 0
        
        if score == 0:
            pygame.draw.rect(screen,"white",  background_rect1)
            pygame.draw.rect(screen,"white",  background_rect2)
            screen.blit(instructions_surf1, instructions_rect1)  
            screen.blit(instructions_surf2, instructions_rect2)  
        elif score != 0: screen.blit(score_message,score_message_rect)
            
            
    pygame.display.update()
    clock.tick(60)
