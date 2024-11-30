"""
    Program: Battlefront Blitz
    Date: November 2024
    Purpose: 2D Dropdown Tower Defense Game
"""

## Include libraries
import pygame
import sys
import numpy as np
import random
import yaml
import os

from gaming_state_manager import GamingStateManager
from sprites import SpriteSheet, Sprite, SpriteManager
from world import World
from config import Config





## Functions    
def draw_play(screen, sprite_manager):
    """Render the play state and explosions."""
    font = pygame.font.Font(None, 36)
    text_surface = font.render("State: play... Press ESC to quit playing.", True, (255, 255, 255))
    screen.blit(text_surface, (200, 250))
    
    # Render explosions
    # sprite_manager.render(screen)

def draw_setup(screen, sprite_manager):
    """Render the play state and explosions."""
    font = pygame.font.Font(None, 36)
    text_surface = font.render("State: setup... Press ESC to exit setup.", True, (255, 255, 255))
    screen.blit(text_surface, (200, 250))
    
    # Render explosions
    # sprite_manager.render(screen)
    
def draw_restore(screen, sprite_manager):
    """Render the play state and explosions."""
    font = pygame.font.Font(None, 36)
    text_surface = font.render("State: restore... Press ESC to exit restore.", True, (255, 255, 255))
    screen.blit(text_surface, (200, 250))
    
    # Render explosions
    # sprite_manager.render(screen)    

# def draw_menu(screen, regions, scale=1):
    # """Render the main menu with interactive regions."""
    # font = pygame.font.Font(None, 36)
    # for name, (x1, y1, x2, y2) in regions.items():
        # pygame.draw.rect(screen, (0, 128, 255), (x1, y1, x2 - x1, y2 - y1))
        # text_surface = font.render(name, True, (255, 255, 255))
        # text_rect = text_surface.get_rect(center=((x1 + x2) // 2, (y1 + y2) // 2))
        # screen.blit(text_surface, text_rect)

def draw_menu(screen, regions, scale=1):
    """Render the main menu with interactive regions, dynamically centered and scaled."""
    screen_width, screen_height = screen.get_size()  # Get current screen dimensions
    font = pygame.font.Font(None, int(36 * scale))  # Scale font size

    for index, (name, (x1, y1, x2, y2)) in enumerate(regions.items()):
        # Calculate button dimensions
        button_width = int((x2 - x1) * scale)
        button_height = int((y2 - y1) * scale)
        
        # Calculate dynamic position to center the button
        center_x = screen_width // 2
        start_y = screen_height // 2 - (len(regions) * button_height) // 2  # Top of button stack
        center_y = start_y + index * (button_height + 10)  # Add spacing between buttons

        # Calculate top-left corner of the scaled button
        scaled_x1 = center_x - button_width 
        scaled_y1 = center_y - button_height

        # Draw the scaled rectangle
        pygame.draw.rect(
            screen, 
            (0, 128, 255), 
            (scaled_x1 + button_width/2 , scaled_y1, button_width, button_height)
        )

        # Render the text and center it in the button
        text_surface = font.render(name, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(center_x, center_y - button_height/2))
        screen.blit(text_surface, text_rect)

def load_sprites(sprite_manager):
    """Load all the sprites and animations into the SpriteManager."""
    sprite_sheet1 = SpriteSheet("assets/sprites/water-tiles.png")
    sprite_manager.add_sprite("ground1", sprite_sheet1.sprite_sheet, 0, 0, 32, 32)
    sprite_manager.add_sprite("water_lt", sprite_sheet1.sprite_sheet, 256, 32, 32, 32)
    sprite_manager.add_sprite("water_lm", sprite_sheet1.sprite_sheet, 224, 320, 32, 32)
    sprite_manager.add_sprite("water_lb", sprite_sheet1.sprite_sheet, 224, 96, 32, 32)
    sprite_manager.add_sprite("water_mt", sprite_sheet1.sprite_sheet, 288, 32, 32, 32)
    sprite_manager.add_sprite("water_mm", sprite_sheet1.sprite_sheet, 288, 64, 32, 32)
    sprite_manager.add_sprite("water_mb", sprite_sheet1.sprite_sheet, 256, 416, 32, 32)
    sprite_manager.add_sprite("water_rt", sprite_sheet1.sprite_sheet, 320, 32, 32, 32)
    sprite_manager.add_sprite("water_rm", sprite_sheet1.sprite_sheet, 544, 378, 32, 32)
    sprite_manager.add_sprite("water_rb", sprite_sheet1.sprite_sheet, 352, 96, 32, 32)
    sprite_manager.add_sprite("water_v", sprite_sheet1.sprite_sheet, 480, 160, 32, 32)
    sprite_manager.add_sprite("water_h", sprite_sheet1.sprite_sheet, 512, 224, 32, 32)

    explosion = SpriteSheet("assets/sprites/effects.png")
    sprite_manager.add_animation("explosion1", explosion.sprite_sheet, 0, 0, 63, 64, scale=1.0,
                                  sprites_per_row=12, rows=4, frame_time=0.1)
    return sprite_manager

def initialize_world(config, sprite_manager):
    """Initialize the world with tiles and lakes."""
    world = World(width_in_tiles=128, height_in_tiles=128, tile_size=32,
                  win_width=config.screen_width, win_height=config.screen_height)

    tile_to_sprite = {
        100: "ground1",
        200: "water_lt",
        201: "water_lm",
        202: "water_lb",
        203: "water_mt",
        204: "water_mm",
        205: "water_mb",
        206: "water_rt",
        207: "water_rm",
        208: "water_rb",
        209: "water_v",
        210: "water_h"
    }

    # Define tile IDs for the lake
    lake_tile_ids = {
        "lt": 200, "rt": 206, "lb": 202, "rb": 208,
        "mt": 203, "mb": 205, "lm": 201, "rm": 207, "mm": 204
    }

    world.set_view(1648, 3396)  # Initial view position
    
    # Fill the world with ground tiles
    world.fill(tile_id=100)

    # Populate with lakes
    for _ in range(2):
        width = random.randint(13, 58)
        height = random.randint(15, 34)
        max_row = world.height_in_tiles - height
        max_col = world.width_in_tiles - width
        top_left_row = random.randint(0, max_row)
        top_left_col = random.randint(0, max_col)
        bottom_right_row = top_left_row + height - 1
        bottom_right_col = top_left_col + width - 1

        world.place_lake(top_left=(top_left_row, top_left_col),
                         bottom_right=(bottom_right_row, bottom_right_col),
                         tile_ids=lake_tile_ids)

    return world, tile_to_sprite


## Main function for game loop        
def main():

    ## Variables
    scale = 1.0
    move_speed = 1200  # Speed of movement in pixels per second

    ## Initializaton
    config = Config() ## Read config file
    pygame.init()     ## Initialize pygame
    screen = pygame.display.set_mode((config.screen_width, config.screen_height)) 
    clock = pygame.time.Clock()
    
    state_manager = GamingStateManager(scale=scale) # Initialize the state manager

    # Load sprites ans sprite_manager
    sprite_manager = SpriteManager()
    sprite_manager = load_sprites(sprite_manager)

    ## Initialize the world
    world, tile_to_sprite = initialize_world(config, sprite_manager)


    ## Loop when running
    running = True
    while running:
    
        ## Update per loop
        mouse_pos = pygame.mouse.get_pos()
        delta_time = clock.tick(config.fps) / 1000.0  # Time in seconds

        ## Update window caption with mouse positions
        caption = f"{config.game_title}  v{config.game_version} Date: {config.game_dev_date} "
        caption += f"[{int(world.world_x)},{int(world.world_y)}] "
        caption += f"({mouse_pos[0]},{mouse_pos[1]})"
        pygame.display.set_caption(caption)

        ## Handle events
        keys = pygame.key.get_pressed()  # Fetch the state of all keys once per frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # State-independent key events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:  # Toggle mini-map visibility
                    world.toggle_minimap()
                    
                # if event.key == pygame.K_F11:  # Toggle fullscreen
                    # fullscreen = not fullscreen
                    # if fullscreen:
                        # os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"
                        # screen = pygame.display.set_mode(
                            # (fullscreen_width, fullscreen_height), pygame.NOFRAME
                        # )
                        # scale = fullscreen_width / config.screen_width  # Calculate scale factor
                        # state_manager.update_scale(scale)  # Update regions with the new scale
                    # else:
                        # screen = pygame.display.set_mode((config.screen_width, config.screen_height))
                        # state_manager.update_scale(1.0)  # Reset regions to 1:1 scale
     

            # Handle state-specific events
            state_manager.handle_event(event, mouse_pos)

            # Trigger explosions in the play state
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1  # Left mouse click
                and state_manager.get_state() == "play"
            ):
                mouse_x, mouse_y = event.pos
                flip = mouse_x % 2 == 0  # Flip horizontally for every other explosion
                pass



        ## Handle state-specific updates
        if state_manager.get_state() == "play":
            # Handle world scrolling
            delta_x = delta_y = 0
            if keys[pygame.K_w]:  # Move up
                delta_y -= move_speed * delta_time
            if keys[pygame.K_s]:  # Move down
                delta_y += move_speed * delta_time
            if keys[pygame.K_a]:  # Move left
                delta_x -= move_speed * delta_time
            if keys[pygame.K_d]:  # Move right
                delta_x += move_speed * delta_time
            world.move_view(delta_x, delta_y)

            # Determine the tile under the mouse cursor
            tile_x = int((world.world_x + mouse_pos[0]) // world.tile_size)
            tile_y = int((world.world_y + mouse_pos[1]) // world.tile_size)

            if 0 <= tile_x < world.width_in_tiles and 0 <= tile_y < world.height_in_tiles:
                tile_id = world.tiles[tile_y, tile_x]
                if 100 <= tile_id < 200:
                    tile_type = "Land"
                elif 200 <= tile_id < 300:
                    tile_type = "Water"
                else:
                    tile_type = "Unknown"
            else:
                tile_type = "Out of Bounds"
            

        ## Render based on state
        screen.fill((0, 0, 0))  # Clear the screen
        current_state = state_manager.get_state()

        if current_state == "main_menu":
            draw_menu(screen, state_manager.regions, scale=1)  # Render main menu
        elif current_state == "play":
        
            world.render(screen, sprite_manager, tile_to_sprite, scale)  # Render the world and active sprites
            
            # Display the tile type
            font = pygame.font.Font(None, 36)
            text_surface = font.render(f"Tile: {tile_type}", True, (255, 255, 255))
            screen.blit(text_surface, (10, 10))  # Render at the top-left corner            
            
            
            # Render the mini-map if it's toggled on
            if world.show_minimap:
                world.render_map(screen)
        
            # sprite_manager.render(screen)  # Render any active animations
        elif current_state == "setup":
            draw_setup(screen, sprite_manager)  # Render setup state
        elif current_state == "restore":
            draw_restore(screen, sprite_manager)  # Render restore state
        elif current_state == "exit_game":
            running = False  # Exit the loop

        pygame.display.flip()  # Update the display 

        clock.tick(config.fps)

    pygame.quit()


if __name__ == "__main__":
    main()

