import pygame
import yaml
import sys


class GamingStateManager:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Load config
        with open("config.yaml", "r") as config_file:
            self.config = yaml.safe_load(config_file)

        # Set up screen dimensions from config
        self.screen_width = self.config.get(self.config['screen_width'], 800)
        self.screen_height = self.config.get(self.config['screen_height'], 600)
        self.screen = pygame.display.set_mode((self.config['screen_width'], self.config['screen_height']))
        pygame.display.set_caption(self.config['game_title'] + " (" + str(self.config['game_version']) + ") Updated: " + self.config['game_dev_date'])

        # Load background image
        self.background = pygame.image.load("assets/maps/map1.png").convert()

        # Set running flag
        self.running = True

        # Clock for controlling the frame rate
        self.clock = pygame.time.Clock()
        
        # Parse and store key mappings
        self.keymap = self._parse_keymap()       

    def _parse_keymap(self):
        """Converts key names from config to pygame key constants."""
        keys = self.config.get("keys", {})
        keymap = {}
        for action, key_name in keys.items():
            try:
                # Attempt to get the key constant dynamically
                key_constant = getattr(pygame, f"K_{key_name.lower()}")
                keymap[action] = key_constant
            except AttributeError:
                # If dynamic lookup fails, map known special cases manually
                special_keys = {
                    "space": pygame.K_SPACE,
                    "escape": pygame.K_ESCAPE,
                    "enter": pygame.K_RETURN,
                    "tab": pygame.K_TAB,
                    "backspace": pygame.K_BACKSPACE,
                }
                if key_name.lower() in special_keys:
                    keymap[action] = special_keys[key_name.lower()]
                else:
                    print(f"Warning: Key '{key_name}' for action '{action}' is invalid.")
                    keymap[action] = None  # Handle invalid keys gracefully
        return keymap


    def key_action(self, key, action):
        """Checks if a key matches a configured action."""
        return key == self.keymap.get(action)

    def update(self):
        # Handle game state updates
        pass  # To be implemented later

    def render(self):
        # Draw the game frame
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and self.key_action(event.key, "key_exit")):
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.key_action(event.key, "key_play"):
                    print("Game started or resumed!")  # Example action for 'Play'
                elif self.key_action(event.key, "key_pause"):
                    print("Game paused!")  # Example action for 'Pause'

    def main(self):
        # Main game loop
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)  # Limit to 60 FPS

    def close(self):
        # Clean up resources and quit
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    # Create game instance
    game = GamingStateManager()
    try:
        game.main()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        game.close()
