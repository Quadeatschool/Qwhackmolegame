import pygame
import sys
import random
import os

pygame.init()
pygame.mixer.init()  # Initialize the sound mixer

#screen dimentions------------
screen_width = 800
screen_height = 600
screen_size = (screen_width, screen_height)
FPS = 60
clock = pygame.time.Clock()

#color palet-------------
background_color = (0, 0, 0)
spider_color = (255, 140, 0)  # Changed to red to make spider visible
hole_color = (255, 255, 255)
text_color = (100, 100, 100)



#game specs----------------
hole_radius = 50
spider_radius = 40
min_time_spider_is_volnurable = 700
max_time_spider_is_volnurable = 1600
time_spider_is_hidden = 1000

#sound effects----------------
try:
    hit_sound = pygame.mixer.Sound("sounds/hit.wav")
    print("Loaded hit.wav successfully.")
except Exception as e:
    print(f"Error loading hit.wav: {e}")
    hit_sound = None
try:
    miss_sound = pygame.mixer.Sound("sounds/miss.wav")
    print("Loaded miss.wav successfully.")
except Exception as e:
    print(f"Error loading miss.wav: {e}")
    miss_sound = None
try:
    spawn_sound = pygame.mixer.Sound("sounds/spawn.wav")
    print("Loaded spawn.wav successfully.")
except Exception as e:
    print(f"Error loading spawn.wav: {e}")
    spawn_sound = None

#fonts--------------------
font = pygame.font.Font(None, 48)

#hole placement grid--------------
hole_grid = [
    (160, 120), (320, 120), (480, 120), (640, 120),
    (160, 240), (320, 240), (480, 240), (640, 240),
    (160, 360), (320, 360), (480, 360), (640, 360),
    (160, 480), (320, 480), (480, 480), (640, 480)
]
#game state ---------------
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Pygame Whack-A-Spider")

score = 0
active_spider_index = -1
last_spider_action_time = 0
current_spider_up_duration = 0


#game functions----------

def Render_elements():
    screen.fill(background_color)
    for x, y in hole_grid:
        pygame.draw.circle(screen, hole_color, (x, y), hole_radius)

    if active_spider_index != -1:
        x, y = hole_grid[active_spider_index]
        pygame.draw.circle(screen, spider_color, (x, y), spider_radius)

    score_text = font.render(f"SCORE: {score}", True, text_color)
    screen.blit(score_text, (10, screen_height - 40))

    pygame.display.flip()

def spawn_spider():
    global active_spider_index, last_spider_action_time, current_spider_up_duration

    possible_indices = [indices for indices in range(len(hole_grid)) if indices != active_spider_index]

    if not possible_indices:
        return
    
    active_spider_index = random.choice(possible_indices)

    last_spider_action_time = pygame.time.get_ticks()
    current_spider_up_duration = random.randint(min_time_spider_is_volnurable, max_time_spider_is_volnurable)
    
    # Play spawn sound if available
    if spawn_sound:
        try:
            spawn_sound.play()
            print("Playing spawn sound.")
        except Exception as e:
            print(f"Error playing spawn sound: {e}")

def check_spider_timig(): 
    global active_spider_index, last_spider_action_time
    current_time = pygame.time.get_ticks()

    if active_spider_index != -1:
        if current_time - last_spider_action_time > current_spider_up_duration:
            active_spider_index = -1
            last_spider_action_time = current_time
    else:
        if current_time - last_spider_action_time > time_spider_is_hidden:
            spawn_spider()

#main game loop-----------
running = True

#start game------------
spawn_spider()

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                if active_spider_index != -1:
                    spider_x, spider_y = hole_grid[active_spider_index]

                    distance = ((mouse_x - spider_x)**2 + (mouse_y - spider_y)**2)**0.5    

                    if distance < spider_radius:
                        # a hit 
                        score += 1
                        active_spider_index = -1
                        last_spider_action_time = current_time
                        
                        # Play hit sound if available
                        if hit_sound:
                            try:
                                hit_sound.play()
                                print("Playing hit sound.")
                            except Exception as e:
                                print(f"Error playing hit sound: {e}")
                        
                        print(f"YOU WHACKED IT! SCORE: {score}")

                    elif distance < hole_radius:
                        score += -1
                        # Play miss sound if available
                        if miss_sound:
                            try:
                                miss_sound.play()
                                print("Playing miss sound.")
                            except Exception as e:
                                print(f"Error playing miss sound: {e}")
                        print("ha ha you missed")
                        
    #game logic call----------
    check_spider_timig()

    #render call--------------
    Render_elements()

    #frame rate controls------
    clock.tick(FPS)

#quit----------------
pygame.quit()
sys.exit()
