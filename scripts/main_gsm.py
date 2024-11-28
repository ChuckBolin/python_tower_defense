import pygame
import sys
from gaming_state_manager import GamingStateManager


class SpriteManager:
    def __init__(self, duration=4):
        """Initialize the SpriteManager for handling explosions."""
        self.sprite_sheet = None
        self.sprites = []
        self.explosions = []
        self.frame_time = float(duration) / 48  # Duration of one explosion divided by 48 frames
        self.sprite_width = 63  # Hardcoding sprite dimensions
        self.sprite_height = 64
        self.load_sprites()

    def load_sprites(self):
        """Load the sprite sheet and extract 48 explosion frames."""
        self.sprite_sheet = pygame.image.load("./assets/sprites/effects.png").convert_alpha()
        sprites_per_row = 12
        rows = 4

        # Extract all 48 sprites
        for row in range(rows):
            for col in range(sprites_per_row):
                x = col * self.sprite_width
                y = row * self.sprite_height
                sprite = self.sprite_sheet.subsurface((x, y, self.sprite_width, self.sprite_height))
                self.sprites.append(sprite)

    def add_explosion(self, x, y, flip_horizontal=False):
        """Add a new explosion centered at the given position."""
        explosion = {
            "x": x - self.sprite_width // 2,  # Offset x to center the sprite
            "y": y - self.sprite_height // 2,  # Offset y to center the sprite
            "current_frame": 0,
            "elapsed_time": 0,
            "animation_done": False,
            "flip_horizontal": flip_horizontal,
        }
        self.explosions.append(explosion)

    def update(self, delta_time):
        """Update all explosions."""
        for explosion in self.explosions:
            if explosion["animation_done"]:
                continue

            explosion["elapsed_time"] += delta_time
            if explosion["elapsed_time"] >= self.frame_time:
                explosion["elapsed_time"] -= self.frame_time
                explosion["current_frame"] += 1

                if explosion["current_frame"] >= len(self.sprites):
                    explosion["animation_done"] = True  # Animation completed

        # Remove completed explosions
        self.explosions = [e for e in self.explosions if not e["animation_done"]]

    def render(self, screen):
        """Render all active explosions."""
        for explosion in self.explosions:
            if not explosion["animation_done"]:
                sprite = self.sprites[explosion["current_frame"]]
                if explosion["flip_horizontal"]:
                    sprite = pygame.transform.flip(sprite, True, False)
                screen.blit(sprite, (explosion["x"], explosion["y"]))



    
def draw_play(screen, sprite_manager):
    """Render the play state and explosions."""
    font = pygame.font.Font(None, 36)
    text_surface = font.render("State: play... Press ESC to quit playing.", True, (255, 255, 255))
    screen.blit(text_surface, (200, 250))
    
    # Render explosions
    sprite_manager.render(screen)

def draw_setup(screen, sprite_manager):
    """Render the play state and explosions."""
    font = pygame.font.Font(None, 36)
    text_surface = font.render("State: setup... Press ESC to exit setup.", True, (255, 255, 255))
    screen.blit(text_surface, (200, 250))
    
    # Render explosions
    sprite_manager.render(screen)
    
def draw_restore(screen, sprite_manager):
    """Render the play state and explosions."""
    font = pygame.font.Font(None, 36)
    text_surface = font.render("State: restore... Press ESC to exit restore.", True, (255, 255, 255))
    screen.blit(text_surface, (200, 250))
    
    # Render explosions
    sprite_manager.render(screen)    

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
    
    # Initialize the SpriteManager
    sprite_manager = SpriteManager(duration=0.5)  # Explosion lasts 2 seconds    

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Process input and handle state transitions
            state_manager.handle_event(event, mouse_pos)

            # Trigger explosions in the play state
            if (
                event.type == pygame.MOUSEBUTTONDOWN 
                and event.button == 1  # Left mouse click
                and state_manager.get_state() == "play"
            ):
                mouse_x, mouse_y = event.pos
                flip = mouse_x % 2 == 0  # Flip horizontally for every other explosion
                
                if state_manager.current_state == 'play':
                    sprite_manager.add_explosion(mouse_x, mouse_y, flip_horizontal=flip)                
                

        # Update explosions
        delta_time = clock.tick(60) / 1000.0  # Time in seconds
        sprite_manager.update(delta_time)

        # Render based on state
        screen.fill((0, 0, 0))  # Clear the screen
        if state_manager.get_state() == "main_menu":
            draw_menu(screen, state_manager.regions)
        elif state_manager.get_state() == "play":
            draw_play(screen, sprite_manager)
        elif state_manager.get_state() == "setup":
            draw_setup(screen, sprite_manager)            
        elif state_manager.get_state() == "restore":
            draw_restore(screen, sprite_manager)            
        elif state_manager.get_state() == "exit_game":
            running = False  # Exit the loop

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()

