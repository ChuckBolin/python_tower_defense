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

def draw_menu(screen, regions):
    """Render the main menu with interactive regions."""
    font = pygame.font.Font(None, 36)
    for name, (x1, y1, x2, y2) in regions.items():
        pygame.draw.rect(screen, (0, 128, 255), (x1, y1, x2 - x1, y2 - y1))
        text_surface = font.render(name, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=((x1 + x2) // 2, (y1 + y2) // 2))
        screen.blit(text_surface, text_rect)

## Main function for game loop        
def main():
    config = Config()

    pygame.init()
    screen = pygame.display.set_mode((config.screen_width, config.screen_height))
    # caption = config.game_title + "  v" + str(config.game_version) 
    # pygame.display.set_caption(caption)
    clock = pygame.time.Clock()

    # Initialize the state manager
    state_manager = GamingStateManager()
    
    # Load sprites ans sprite_manager
    sprite_manager = SpriteManager()
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

    # World setup
    world = World(width_in_tiles=128, height_in_tiles=128, tile_size=32, win_width = config.screen_width, win_height = config.screen_height)
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
        "lt": 200,  # Left-top corner
        "rt": 206,  # Right-top corner
        "lb": 202,  # Left-bottom corner
        "rb": 208,  # Right-bottom corner
        "mt": 203,  # Middle-top (horizontal edge)
        "mb": 205,  # Middle-bottom (horizontal edge)
        "lm": 201,  # Left-middle (vertical edge)
        "rm": 207,  # Right-middle (vertical edge)
        "mm": 204,  # Middle-middle (center)
    }
    
    # world.populate({1: 0.8, 12: 0.2}) #2: 0.05, 4: 0.05, 8: 0.05, 9: 0.05})  # Randomized population
    world.set_view(1648, 3396)  # Initial view position
    
    # Populate the world with a single ground tile first
    world.fill(tile_id=100)  # Assuming 1 is the ground tile
    
    # Loop to create the rectangles
    for _ in range(20):
        # Random size for the rectangle (3x3 to 8x8)
        width = random.randint(3, 18)
        height = random.randint(3, 18)

        # Random top-left position within world bounds
        max_row = world.height_in_tiles - height
        max_col = world.width_in_tiles - width
        top_left_row = random.randint(0, max_row)
        top_left_col = random.randint(0, max_col)

        # Calculate bottom-right corner
        bottom_right_row = top_left_row + height - 1
        bottom_right_col = top_left_col + width - 1

        # Place the rectangle
        # Place a lake in the world
        world.place_lake(top_left=(top_left_row, top_left_col), bottom_right=(bottom_right_row, bottom_right_col), tile_ids=lake_tile_ids)

    # Render the world
    world.render(screen, sprite_manager, tile_to_sprite)

    # Render world
    move_speed = 400  # Speed of movement in pixels per second
    
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
            world.set_view(world.world_x + delta_x, world.world_y + delta_y)

        ## Render based on state
        screen.fill((0, 0, 0))  # Clear the screen
        current_state = state_manager.get_state()

        if current_state == "main_menu":
            draw_menu(screen, state_manager.regions)  # Render main menu
        elif current_state == "play":
        
            world.render(screen, sprite_manager, tile_to_sprite)  # Render the world and active sprites
            
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

