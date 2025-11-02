# ----------------------------------------------------------------------
# WHACK-A-MOLE PROTOTYPE using Pygame
# Hit the green mole as fast as you can!
# ----------------------------------------------------------------------

import pygame
import sys
import random

# --- 1. INITIALIZATION ---
pygame.init()

# --- 2. CONSTANTS AND SETTINGS ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
FPS = 60
clock = pygame.time.Clock()

# Colors
BACKGROUND_COLOR = (128, 70, 0)  # Brown (Dirt/Table)
HOLE_COLOR = (80, 50, 10)       # Darker Brown (Holes)
MOLE_COLOR = (0, 200, 0)        # Green (Mole)
TEXT_COLOR = (255, 255, 255)    # White

# Game Specifics
HOLE_RADIUS = 50
MOLE_RADIUS = 40
MOLE_UP_TIME_MIN = 800      # Minimum time mole stays up (ms)
MOLE_UP_TIME_MAX = 1500     # Maximum time mole stays up (ms)
MOLE_DOWN_TIME = 1000       # Time between moles (ms)

# Font Setup
font = pygame.font.Font(None, 48) # Default Pygame font, size 48

# Hole positions (3x3 grid centers)
HOLE_CENTERS = [
    (150, 150), (400, 150), (650, 150),
    (150, 300), (400, 300), (650, 300),
    (150, 450), (400, 450), (650, 450)
]

# --- 3. GAME STATE ---
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Pygame Whack-A-Mole")

score = 0
active_mole_index = -1  # -1 means no mole is currently up
last_mole_action_time = 0 # Stores the timestamp of the last mole appearance or disappearance
current_mole_up_duration = 0 # Stores the random duration for the currently active mole

# --- 4. GAME FUNCTIONS ---

def draw_elements():
    """Draws the background, holes, active mole, and score."""
    
    # 1. Background
    screen.fill(BACKGROUND_COLOR)

    # 2. Draw all holes
    for x, y in HOLE_CENTERS:
        pygame.draw.circle(screen, HOLE_COLOR, (x, y), HOLE_RADIUS)

    # 3. Draw active mole
    if active_mole_index != -1:
        x, y = HOLE_CENTERS[active_mole_index]
        pygame.draw.circle(screen, MOLE_COLOR, (x, y), MOLE_RADIUS)

    # 4. Draw Score
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_text, (10, SCREEN_HEIGHT - 40))

    # 5. Update the display
    pygame.display.flip()

def spawn_mole():
    """Selects a random hole for the mole to appear in."""
    global active_mole_index, last_mole_action_time, current_mole_up_duration
    
    # Get a list of all holes excluding the currently active one (if any)
    possible_indices = [i for i in range(len(HOLE_CENTERS)) if i != active_mole_index]
    
    if not possible_indices:
        # Should not happen in a 3x3 grid, but as a safeguard
        return
        
    # Pick a new random hole index
    active_mole_index = random.choice(possible_indices)
    
    # Set the new timer and a random duration for how long it stays up
    last_mole_action_time = pygame.time.get_ticks()
    current_mole_up_duration = random.randint(MOLE_UP_TIME_MIN, MOLE_UP_TIME_MAX)


def check_mole_timing():
    """Handles the timing of the mole appearing and disappearing."""
    global active_mole_index, last_mole_action_time
    current_time = pygame.time.get_ticks()

    if active_mole_index != -1:
        # Mole is UP, check if its time is over
        if current_time - last_mole_action_time > current_mole_up_duration:
            # Time's up! Hide the mole.
            active_mole_index = -1
            last_mole_action_time = current_time # Start "down" timer
    else:
        # No mole is UP, check if it's time to spawn a new one
        if current_time - last_mole_action_time > MOLE_DOWN_TIME:
            spawn_mole()


# --- 5. MAIN GAME LOOP ---
running = True
# Initial spawn to start the game
spawn_mole() 

while running:
    # Get current time for game logic checks
    current_time = pygame.time.get_ticks()

    # ------------------------------------
    # A. Event Handling (Input)
    # ------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Handle Mouse Clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            if active_mole_index != -1:
                mole_x, mole_y = HOLE_CENTERS[active_mole_index]
                
                # Use distance formula to check if the click is inside the mole radius
                distance = ((mouse_x - mole_x)**2 + (mouse_y - mole_y)**2)**0.5
                
                if distance < MOLE_RADIUS:
                    # HIT!
                    score += 1
                    
                    # Immediately hide the mole and trigger the "down" timer
                    active_mole_index = -1
                    last_mole_action_time = current_time 
                    
                    # Optional: Print to console for confirmation
                    print(f"WHACK! Score: {score}")
                
                # Optional: If you want to penalize misses, you would add logic here
                # elif distance < HOLE_RADIUS:
                #     # Missed the mole, but hit the hole
                #     print("Miss!")


    # ------------------------------------
    # B. Game Logic (Update)
    # ------------------------------------
    check_mole_timing()


    # ------------------------------------
    # C. Drawing (Render)
    # ------------------------------------
    draw_elements()

    # Control the game's frame rate
    clock.tick(FPS)

# --- 6. QUIT ---
pygame.quit()
sys.exit()
