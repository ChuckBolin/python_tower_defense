import pygame
import sys
import numpy as np
from gaming_state_manager import GamingStateManager


class SpriteSheet:
    def __init__(self, image_path):
        """Initialize with the path to the sprite sheet image."""
        self.sprite_sheet = pygame.image.load(image_path).convert_alpha()

    def get_sprite(self, x, y, width, height, scale=1.0):
        """Extract a sprite at (x, y) with given dimensions, optionally scaled."""
        sprite = self.sprite_sheet.subsurface((x, y, width, height))
        if scale != 1.0:
            scaled_width = int(width * scale)
            scaled_height = int(height * scale)
            sprite = pygame.transform.scale(sprite, (scaled_width, scaled_height))
        return sprite

    def get_animation_frames(self, x, y, width, height, sprites_per_row, rows, scale=1.0):
        """Extract a series of frames for an animation."""
        frames = []
        for row in range(rows):
            for col in range(sprites_per_row):
                frame_x = x + col * width
                frame_y = y + row * height
                frame = self.get_sprite(frame_x, frame_y, width, height, scale)
                frames.append(frame)
        return frames


class Sprite:
    def __init__(self, sprite_id, sprite_sheet, x1, y1, width, height, scale=1.0, 
                 animated=False, sprites_per_row=1, rows=1, frame_time=None):
        """Initialize a Sprite with its properties."""
        self.id = sprite_id
        self.sprite_sheet = sprite_sheet
        self.x1, self.y1 = x1, y1
        self.width, self.height = width, height
        self.animated = animated
        self.sprites_per_row = sprites_per_row
        self.rows = rows
        self.frame_time = frame_time

        # Scale the dimensions
        self.scaled_width = int(width * scale)
        self.scaled_height = int(height * scale)

        # Extract the image or animation frames
        if not animated:
            self.image = sprite_sheet.subsurface((x1, y1, width, height))
            if scale != 1.0:
                self.image = pygame.transform.scale(self.image, (self.scaled_width, self.scaled_height))
        else:
            self.frames = []
            for row in range(rows):
                for col in range(sprites_per_row):
                    frame_x = x1 + col * width
                    frame_y = y1 + row * height
                    frame_image = sprite_sheet.subsurface((frame_x, frame_y, width, height))
                    if scale != 1.0:
                        frame_image = pygame.transform.scale(frame_image, (self.scaled_width, self.scaled_height))
                    self.frames.append(frame_image)

    def get_image(self, frame_index=0, angle=0):
        """Return a specific frame of the sprite, optionally rotated."""
        if self.animated:
            frame = self.frames[frame_index % len(self.frames)]
            if angle != 0:
                return pygame.transform.rotate(frame, angle)
            return frame
        else:
            if angle != 0:
                return pygame.transform.rotate(self.image, angle)
            return self.image


class SpriteManager:
    def __init__(self):
        self.sprites = {}  # Dictionary to store sprites by their unique ID

    def add_sprite(self, sprite_id, sprite_sheet, x1, y1, width, height, scale=1.0):
        """Add a static sprite to the manager."""
        if sprite_id in self.sprites:
            raise ValueError(f"Sprite ID '{sprite_id}' already exists.")
        
        sprite = Sprite(
            sprite_id=sprite_id,
            sprite_sheet=sprite_sheet,
            x1=x1,
            y1=y1,
            width=width,
            height=height,
            scale=scale,
        )
        self.sprites[sprite_id] = sprite

    def add_animation(self, sprite_id, sprite_sheet, x1, y1, width, height, scale=1.0, 
                      sprites_per_row=1, rows=1, frame_time=0.1):
        """Add an animated sprite to the manager."""
        if sprite_id in self.sprites:
            raise ValueError(f"Sprite ID '{sprite_id}' already exists.")
        
        animated_sprite = Sprite(
            sprite_id=sprite_id,
            sprite_sheet=sprite_sheet,
            x1=x1,
            y1=y1,
            width=width,
            height=height,
            scale=scale,
            animated=True,
            sprites_per_row=sprites_per_row,
            rows=rows,
            frame_time=frame_time,
        )
        self.sprites[sprite_id] = animated_sprite

    def get_sprite(self, sprite_id):
        """Retrieve a sprite by its ID."""
        if sprite_id not in self.sprites:
            raise ValueError(f"Sprite ID '{sprite_id}' not found.")
        return self.sprites[sprite_id]




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

    def populate(self, tile_mapping):
        """
        Populate the world with tiles.
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
        
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Simplified State Manager")
    clock = pygame.time.Clock()

    # Initialize the state manager
    state_manager = GamingStateManager()
    
    # Load sprites
    sprite_sheet1 = SpriteSheet("assets/sprites/water-tiles.png")
    sprite_manager = SpriteManager()
    sprite_manager.add_sprite("ground1", sprite_sheet1.sprite_sheet, 0, 0, 32, 32)
    sprite_manager.add_sprite("water1", sprite_sheet1.sprite_sheet, 256, 320, 32, 32)
    



    # World setup
    world = World(width_in_tiles=128, height_in_tiles=128, tile_size=32)
    # Tile-to-sprite mapping
    tile_to_sprite = {
        1: "ground1",
        2: "water1",
    }    
    world.populate({1: 0.5, 2: 0.5})  # Randomized population
    world.set_view(1648, 3396)  # Initial view position

    # Render world
    world.render(screen, sprite_manager, tile_to_sprite)
    move_speed = 200  # Speed of movement in pixels per second
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        delta_time = clock.tick(60) / 1000.0  # Time in seconds
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Process input and handle state transitions
            state_manager.handle_event(event, mouse_pos)

            # Handle key press events
            # if event.type == pygame.KEYDOWN:
            # keys = pygame.key.get_pressed()  # Capture the state of all keys

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

