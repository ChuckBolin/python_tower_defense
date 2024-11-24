import pygame
import sys
import yaml

# Load configuration from config.yaml
def load_config(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

# Initialize the game
def init_game(config):
    pygame.init()
    screen = pygame.display.set_mode(
        (config['screen_width'], config['screen_height'])
    )
    caption = config['game_title'] + "(v" + str(config['game_version']) + ") Updated: " + config['game_dev_date']
    
    pygame.display.set_caption(caption)
    clock = pygame.time.Clock()
    return screen, clock

# Process events (keyboard and mouse)
def process_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        # Keydown events
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Quit on ESC
                return False
            elif event.key == pygame.K_a:  # Key A
                print("Key A pressed")
            elif event.key == pygame.K_s:  # Key S
                print("Key S pressed")
            elif event.key == pygame.K_w:  # Key W
                print("Key W pressed")
            elif event.key == pygame.K_d:  # Key D
                print("Key D pressed")
            elif event.key == pygame.K_q:  # Key Q
                print("Key Q pressed")

        # Mouse button events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                print(f"Left mouse button clicked at {event.pos}")
            elif event.button == 3:  # Right mouse button
                print(f"Right mouse button clicked at {event.pos}")

        # Mouse motion events
        elif event.type == pygame.MOUSEMOTION:
            print(f"Mouse moved to {event.pos}")

    return True

# Update game state
def update(delta_time):
    # Add logic for updating game state (e.g., positions, collisions)
    pass

# Render the game
def render(screen, map_image, camera_x, camera_y, map_width, map_height):
    screen.fill((0, 0, 0))  # Clear screen with black
    
    # Define the camera viewport
    camera_width, camera_height = screen.get_size()
    map_view = pygame.Rect(camera_x, camera_y, camera_width, camera_height)

    # Ensure camera stays within the map boundaries
    camera_x = max(0, min(camera_x, map_width - camera_width))
    camera_y = max(0, min(camera_y, map_height - camera_height))

    # Draw the cropped portion of the map
    screen.blit(map_image, (0, 0), map_view)

    # Update the screen
    pygame.display.flip()

# Show a simple menu
def show_menu(screen):
    screen.fill((50, 50, 50))  # Background for the menu
    font = pygame.font.Font(None, 36)
    text = font.render("Press SPACE to Start the Game", True, (255, 255, 255))
    screen.blit(text, (150, 250))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

# Main game function
def main():
    config = load_config("config.yaml")  # Ensure config.yaml exists
    screen, clock = init_game(config)
    
    # Load the map image
    map_image = pygame.image.load("assets/maps/map_demo1.jpg").convert()
    map_width, map_height = map_image.get_width(), map_image.get_height()

    # Camera position
    camera_x, camera_y = 0, 0
    
    # Show the menu before starting the game loop
    show_menu(screen)
    
    # Load an image
    
    
    
    running = True
    while running:
        delta_time = clock.tick(config['fps']) / 1000.0  # Convert to seconds
        
        running = process_events()  # Handle input
        
        # Handle scrolling (example)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            camera_x -= 5
        if keys[pygame.K_RIGHT]:
            camera_x += 5
        if keys[pygame.K_UP]:
            camera_y -= 5
        if keys[pygame.K_DOWN]:
            camera_y += 5
            
        update(delta_time)          # Update game state
        # render(screen)              # Render the game
                # Clamp camera position within bounds
        camera_x = max(0, min(camera_x, map_width - config['screen_width']))
        camera_y = max(0, min(camera_y, map_height - config['screen_height']))

        render(screen, map_image, camera_x, camera_y, map_width, map_height)  # Render the game


    pygame.quit()

if __name__ == "__main__":
    main()
