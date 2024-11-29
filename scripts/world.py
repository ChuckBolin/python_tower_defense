import numpy as np
import pygame

class World:
    def __init__(self, width_in_tiles, height_in_tiles, tile_size, win_width, win_height):
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
        self.viewport_width = win_width  # Hardcoded screen width
        self.viewport_height = win_height  # Hardcoded screen height

        # Mini-map visibility toggle
        self.show_minimap = False

        # Mini-map colors
        self.colors = {
            "land": (194, 178, 128),  # Sandy brown
            "water": (173, 216, 230),  # Light blue
        }


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

    def render_map(self, screen):
        """
        Render a mini-map of the world in the top-right corner of the screen.
        """
        # Mini-map dimensions
        map_width = self.width_in_tiles
        map_height = self.height_in_tiles
        map_surface = pygame.Surface((map_width, map_height))

        # Set alpha for transparency (0 is fully transparent, 255 is fully opaque)
        alpha_value = 120  # Example: Semi-transparent
        map_surface.set_alpha(alpha_value)
    

        # Fill the map based on tile types
        for row in range(self.height_in_tiles):
            for col in range(self.width_in_tiles):
                tile_id = self.tiles[row, col]
                if tile_id < 200: #== 1:  # Land tile
                    color = self.colors["land"]
                elif tile_id < 300: #>= 2:  # Water tiles
                    color = self.colors["water"]
                else:
                    color = (0, 0, 0)  # Default black for uninitialized
                map_surface.set_at((col, row), color)

        # Scale the mini-map to fit within a border
        map_surface = pygame.transform.scale(map_surface, (128, 128))

        # Draw border for the mini-map
        border_rect = pygame.Rect(screen.get_width() - 138, 10, 128 + 10, 128 + 10)
        pygame.draw.rect(screen, (50, 50, 50), border_rect)

        # Blit the mini-map onto the screen
        screen.blit(map_surface, (screen.get_width() - 133, 15))

        # Draw the viewport rectangle
        viewport_col = int(self.world_x / self.tile_size / self.width_in_tiles * 128)
        viewport_row = int(self.world_y / self.tile_size / self.height_in_tiles * 128)
        viewport_width = int(self.viewport_width / self.tile_size / self.width_in_tiles * 128)
        viewport_height = int(self.viewport_height / self.tile_size / self.height_in_tiles * 128)

        pygame.draw.rect(
            screen,
            (255, 0, 0),
            pygame.Rect(
                screen.get_width() - 133 + viewport_col,
                15 + viewport_row,
                viewport_width,
                viewport_height,
            ),
            1,
        )

    def toggle_minimap(self):
        """Toggle the visibility of the mini-map."""
        self.show_minimap = not self.show_minimap
        # print(f"Mini-map visibility: {self.show_minimap}")
            
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