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
from gaming_state_manager import GamingStateManager
from sprites import SpriteSheet, Sprite, SpriteManager

import yaml
import os

class Config:
    def __init__(self, config_file="config.yaml"):
        """
        Initialize the Config class and load the configuration file.
        If the file is missing or incomplete, default values are used.
        """
        self.default_values = {
            "game_info": {
                "game_title": "Tower Defense Game",
                "game_version": 0.1,
                "game_dev_date": "Nov 24, 2024",
                "screen_width": 800,
                "screen_height": 600,
                "fps": 60,
            }
        }
        self.config = self.load_config(config_file)
        self.initialize_class_variables()

    def load_config(self, config_file):
        """
        Load the configuration file. If it's missing or incomplete,
        merge with default values.
        """
        if not os.path.exists(config_file):
            print(f"Config file '{config_file}' not found. Using default values.")
            return self.default_values

        try:
            with open(config_file, "r") as file:
                config_data = yaml.safe_load(file)
                return self.merge_defaults(config_data)
        except (yaml.YAMLError, IOError) as e:
            print(f"Error reading config file: {e}. Using default values.")
            return self.default_values

    def merge_defaults(self, config_data):
        """
        Merge loaded config data with default values, ensuring missing keys
        are filled in.
        """
        merged_config = self.default_values.copy()
        for key, value in config_data.items():
            if key in merged_config and isinstance(value, dict):
                # Merge sub-dictionaries
                merged_config[key].update(value)
            else:
                merged_config[key] = value
        return merged_config

    def initialize_class_variables(self):
        """
        Initialize class variables from the loaded configuration.
        """
        game_info = self.config.get("game_info", {})
        self.game_title = game_info.get("game_title", self.default_values["game_info"]["game_title"])
        self.game_version = game_info.get("game_version", self.default_values["game_info"]["game_version"])
        self.game_dev_date = game_info.get("game_dev_date", self.default_values["game_info"]["game_dev_date"])
        self.screen_width = game_info.get("screen_width", self.default_values["game_info"]["screen_width"])
        self.screen_height = game_info.get("screen_height", self.default_values["game_info"]["screen_height"])
        self.fps = game_info.get("fps", self.default_values["game_info"]["fps"])

    def __repr__(self):
        """
        String representation for debugging purposes.
        """
        return (
            f"Config("
            f"game_title='{self.game_title}', "
            f"game_version={self.game_version}, "
            f"game_dev_date='{self.game_dev_date}', "
            f"screen_width={self.screen_width}, "
            f"screen_height={self.screen_height}, "
            f"fps={self.fps}"
            f")"
        )



## Class "world"
class World:
    def __init__(self, width_in_tiles, height_in_tiles, tile_size):
        """Initialize the world dimensions and tiles."""
        self.width_in_tiles = width_in_tiles
        self.height_in_tiles = height_in_tiles
        self.tile_size = tile_size  # Size of each tile in pixels

        # Create a 2D array to store tile IDs (integers or sprite IDs)
        self.tiles = np.zeros((height_in_tiles, width_in_tiles), dtype=int)

        # Define the player's view window (top-left corner)
        self.world_x = 0
        self.world_y = 0

        # Viewport dimensions
        self.viewport_width = 800  # Hardcoded screen width
        self.viewport_height = 600  # Hardcoded screen height

    def fill(self, tile_id):
        """
        Fill the entire world with a single tile.
        :param tile_id: The ID of the tile to fill the world with.
        """
        self.tiles.fill(tile_id)

    def place_rectangle(self, tile_id, top_left, bottom_right):
        """
        Place a rectangular area of tiles.
        :param tile_id: The ID of the tile to place.
        :param top_left: (row, col) tuple for the top-left corner of the rectangle.
        :param bottom_right: (row, col) tuple for the bottom-right corner of the rectangle.
        """
        row1, col1 = top_left
        row2, col2 = bottom_right
        self.tiles[row1:row2+1, col1:col2+1] = tile_id

    def place_lake(self, top_left, bottom_right, tile_ids):
        """
        Place a rectangular lake with different tiles for banks and center.
        :param top_left: (row, col) tuple for the top-left corner of the lake.
        :param bottom_right: (row, col) tuple for the bottom-right corner of the lake.
        :param tile_ids: A dictionary of tile IDs for different parts of the lake:
                         {
                             "lt": tile_id,  # Left-top corner
                             "rt": tile_id,  # Right-top corner
                             "lb": tile_id,  # Left-bottom corner
                             "rb": tile_id,  # Right-bottom corner
                             "mt": tile_id,  # Middle-top (horizontal edge)
                             "mb": tile_id,  # Middle-bottom (horizontal edge)
                             "lm": tile_id,  # Left-middle (vertical edge)
                             "rm": tile_id,  # Right-middle (vertical edge)
                             "mm": tile_id,  # Middle-middle (center)
                         }
        """
        row1, col1 = top_left
        row2, col2 = bottom_right

        # Place corners
        self.tiles[row1, col1] = tile_ids["lt"]  # Left-top
        self.tiles[row1, col2] = tile_ids["rt"]  # Right-top
        self.tiles[row2, col1] = tile_ids["lb"]  # Left-bottom
        self.tiles[row2, col2] = tile_ids["rb"]  # Right-bottom

        # Place horizontal edges
        if col2 > col1 + 1:  # Ensure there's a space for horizontal edges
            self.tiles[row1, col1+1:col2] = tile_ids["mt"]  # Top edge
            self.tiles[row2, col1+1:col2] = tile_ids["mb"]  # Bottom edge

        # Place vertical edges
        if row2 > row1 + 1:  # Ensure there's a space for vertical edges
            self.tiles[row1+1:row2, col1] = tile_ids["lm"]  # Left edge
            self.tiles[row1+1:row2, col2] = tile_ids["rm"]  # Right edge

        # Fill the center
        if row2 > row1 + 1 and col2 > col1 + 1:
            self.tiles[row1+1:row2, col1+1:col2] = tile_ids["mm"]  # Center
        
        

    def populate(self, tile_mapping):
        """
        Populate the world with tiles using probabilities.
        :param tile_mapping: A dictionary mapping tile IDs to probabilities.
                             Example: {1: 0.5, 2: 0.5} for ground and water.
        """
        tile_ids = list(tile_mapping.keys())
        probabilities = list(tile_mapping.values())
        # Randomly assign tiles based on the probabilities
        self.tiles = np.random.choice(tile_ids, size=self.tiles.shape, p=probabilities)

    def set_view(self, world_x, world_y):
        """
        Update the top-left corner of the player's view.
        Clamp values to ensure they stay within bounds.
        """
        max_x = (self.width_in_tiles * self.tile_size) - self.viewport_width
        max_y = (self.height_in_tiles * self.tile_size) - self.viewport_height
        self.world_x = max(0, min(world_x, max_x))
        self.world_y = max(0, min(world_y, max_y))

    def render(self, screen, sprite_manager, tile_to_sprite):
        """
        Render the visible portion of the world.
        :param screen: Pygame screen to render on.
        :param sprite_manager: SpriteManager to fetch and render sprites.
        :param tile_to_sprite: Mapping of tile IDs to sprite names.
        """
        # Calculate the range of tiles visible in the window
        start_col = int(self.world_x) // self.tile_size
        start_row = int(self.world_y) // self.tile_size
        end_col = (int(self.world_x) + 800) // self.tile_size + 1
        end_row = (int(self.world_y) + 600) // self.tile_size + 1

        # Offset to adjust tile positions on the screen
        x_offset = -(int(self.world_x) % self.tile_size)
        y_offset = -(int(self.world_y) % self.tile_size)

        # Render each visible tile
        for row in range(start_row, min(end_row, self.height_in_tiles)):
            for col in range(start_col, min(end_col, self.width_in_tiles)):
                tile_id = self.tiles[row, col]
                sprite_name = tile_to_sprite.get(tile_id)
                if sprite_name:
                    sprite = sprite_manager.get_sprite(sprite_name)
                    if sprite:
                        screen.blit(sprite.get_image(), 
                                    (x_offset + (col - start_col) * self.tile_size,
                                     y_offset + (row - start_row) * self.tile_size))

    def move_view(self, dx, dy):
        """
        Move the viewport by a given amount, clamping to the world bounds.
        :param dx: Change in x position (pixels).
        :param dy: Change in y position (pixels).
        """
        self.set_view(self.world_x + dx, self.world_y + dy)


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
    screen = pygame.display.set_mode((800, 600))
    # caption = config.game_title + "  v" + str(config.game_version) 
    # pygame.display.set_caption(caption)
    clock = pygame.time.Clock()

    # Initialize the state manager
    state_manager = GamingStateManager()
    
    # Load sprites ans sprite_manager
    sprite_sheet1 = SpriteSheet("assets/sprites/water-tiles.png")
    sprite_manager = SpriteManager()
    sprite_manager.add_sprite("ground1", sprite_sheet1.sprite_sheet, 0, 0, 32, 32)
    # sprite_manager.add_sprite("water1", sprite_sheet1.sprite_sheet, 256, 320, 32, 32)
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

    # World setup
    world = World(width_in_tiles=128, height_in_tiles=128, tile_size=32)
    tile_to_sprite = {
        1: "ground1",
        200: "water_lt",
        201: "water_lm",
        202: "water_lb",
        203: "water_mt",
        204: "water_mm",
        205: "water_mb",
        206: "water_rt",
        207: "water_rm",
        208: "water_rb",
        11: "water_v",
        12: "water_h"        
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
    world.fill(tile_id=1)  # Assuming 1 is the ground tile

    # Add a body of water (3x3 grid) in the middle of the world
    # world.place_rectangle(tile_id=6, top_left=(10, 10), bottom_right=(12, 12))
    
    # Loop to create the rectangles
    # water_tile_id = 6
    for _ in range(20):
        # Random size for the rectangle (3x3 to 8x8)
        width = random.randint(3, 8)
        height = random.randint(3, 8)

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
    

    # Add a horizontal river
    # world.place_rectangle(tile_id=12, top_left=(15, 0), bottom_right=(15, 127))

    # Add a vertical river
    # world.place_rectangle(tile_id=11, top_left=(0, 20), bottom_right=(127, 20))

    # Render the world
    world.render(screen, sprite_manager, tile_to_sprite)

    

    # Render world
    # world.render(screen, sprite_manager, tile_to_sprite)
    move_speed = 400  # Speed of movement in pixels per second
    
    running = True
    while running:
    
        ## Inital code each loop
        mouse_pos = pygame.mouse.get_pos()
        delta_time = clock.tick(60) / 1000.0  # Time in seconds
        
        ## Update window caption with mouse positions
        caption = config.game_title + "  v" + str(config.game_version) 
        caption += " [" + str(int(world.world_x)) + "," + str(int(world.world_y)) + "]"
        caption += " (" + str(mouse_pos[0]) + "," + str(mouse_pos[1]) + ")"
        pygame.display.set_caption(caption)
        
        ## Lets respond to events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Process input and handle state transitions
            state_manager.handle_event(event, mouse_pos)

            if state_manager.get_state() == "play":
                # Fetch the state of all keys
                keys = pygame.key.get_pressed()

                # Calculate movement deltas
                delta_x = 0
                delta_y = 0

                if keys[pygame.K_w]:  # Move up
                    delta_y -= move_speed * delta_time
                if keys[pygame.K_s]:  # Move down
                    delta_y += move_speed * delta_time
                if keys[pygame.K_a]:  # Move left
                    delta_x -= move_speed * delta_time
                if keys[pygame.K_d]:  # Move right
                    delta_x += move_speed * delta_time

                # Update the world view based on calculated deltas
                world.set_view(world.world_x + delta_x, world.world_y + delta_y)
                    
                # if event.key == pygame.K_q:  # Quit the play state
                if keys[pygame.K_q]:
                    state_manager.set_state("main_menu")
                    print("Returning to main menu.")

            # Trigger explosions in the play state
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1  # Left mouse click
                and state_manager.get_state() == "play"
            ):
                # mouse_x, mouse_y = event.pos
                # flip = mouse_x % 2 == 0  # Flip horizontally for every other explosion
                # sprite_manager.add_animation(mouse_x, mouse_y, flip_horizontal=flip)
                pass

        # Render based on state
        if state_manager.get_state() == "main_menu":
            screen.fill((0, 0, 0))  # Clear the screen
            draw_menu(screen, state_manager.regions)  # Ensure menu rendering

        elif state_manager.get_state() == "play":
            screen.fill((0, 0, 0))  # Clear the screen for the play state
            world.render(screen, sprite_manager, tile_to_sprite)  # Render the world and active sprites
            # sprite_manager.render(screen)  # Render any active animations like explosions

        elif state_manager.get_state() == "setup":
            screen.fill((0, 0, 0))  # Clear the screen
            draw_setup(screen, sprite_manager)  # Add setup rendering if applicable

        elif state_manager.get_state() == "restore":
            screen.fill((0, 0, 0))  # Clear the screen
            draw_restore(screen, sprite_manager)  # Add restore rendering if applicable

        elif state_manager.get_state() == "exit_game":
            running = False  # Exit the loop

        pygame.display.flip()  # Ensure everything is rendered to the screen

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()

