import pygame
import yaml
import sys


class GamingStateManager:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Initialize the mixer for audio
        pygame.mixer.init()

        # Load config
        with open("config.yaml", "r") as config_file:
            self.config = yaml.safe_load(config_file)

        # Set up screen dimensions from config
        self.screen_width = self.config["game_info"]["screen_width"]
        self.screen_height = self.config["game_info"]["screen_height"]
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(
            f"{self.config['game_info']['game_title']} ({self.config['game_info']['game_version']}) "
            f"Updated: {self.config['game_info']['game_dev_date']}"
        )

        # Load background image
        # self.background = pygame.image.load("assets/maps/map1.png").convert()
        self.background = pygame.Surface((self.screen_width, self.screen_height))
        self.background.fill((0, 0, 0))  # RGB for black
    
        # Set running flag
        self.running = True

        # Clock for controlling the frame rate
        self.clock = pygame.time.Clock()

        # Parse and store key mappings
        self.keymap = self._parse_keymap()

        # Parse regions
        self.regions = {name: tuple(coords) for name, coords in self.config["regions"].items()}

        # Load state transitions
        self.transitions = self.config["state_transitions"]

        # Derive states from transitions
        self.states = self._derive_states_from_transitions()

        # Start in initial state
        self.current_state = "initial"

        # Play intro audio
        # self.play_intro_audio()

        # Process auto transitions immediately
        self.process_auto_transitions()

    def _derive_states_from_transitions(self):
        """Derives a list of unique states from the transitions."""
        states = set()
        for transition in self.transitions:
            current_state, next_state, _ = transition
            states.add(current_state)
            states.add(next_state)
        return list(states)

    def _parse_keymap(self):
        """Converts key names from config to pygame key constants."""
        keys = self.config["keys"]
        keymap = {}
        for action, key_name in keys.items():
            try:
                key_constant = getattr(pygame, f"K_{key_name.lower()}")
                keymap[action] = key_constant
            except AttributeError:
                # Handle common special cases
                special_keys = {
                    "space": pygame.K_SPACE,
                    "escape": pygame.K_ESCAPE,
                    "enter": pygame.K_RETURN,
                    "tab": pygame.K_TAB,
                    "backspace": pygame.K_BACKSPACE,
                }
                keymap[action] = special_keys.get(key_name.lower(), None)
        return keymap

    def play_intro_audio(self):
        """Plays the intro audio in a loop."""
        try:
            pygame.mixer.music.load("assets/audio/assets_sounds_intro.mp3")
            pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
            pygame.mixer.music.play(-1)  # Loop indefinitely
            print("Intro audio playing.")
        except pygame.error as e:
            print(f"Error loading or playing intro audio: {e}")

    def get_active_regions(self):
        """Get regions relevant to the current state."""
        active_regions = {}
        for transition in self.transitions:
            current_state, _, conditions = transition
            if current_state == self.current_state:
                # Extract regions from conditions (e.g., "region play")
                for condition in conditions.split("|"):
                    condition = condition.strip()
                    if condition.startswith("region"):
                        region_name = condition.split()[1]
                        if region_name in self.regions:
                            active_regions[region_name] = self.regions[region_name]
        return active_regions

    def draw_regions(self):
        """Draw interactive regions based on the current state."""
        active_regions = self.get_active_regions()
        font = pygame.font.Font(None, 36)  # Default font, size 36

        for name, coords in active_regions.items():
            # x1, x2, y1, y2 = coords
            x1, y1, x2, y2 = coords
            # Draw the rectangle
            pygame.draw.rect(self.screen, (0, 128, 255), (x1, y1, x2 - x1, y2 - y1))
            # Add text
            text_surface = font.render(name, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=((x1 + x2) // 2, (y1 + y2) // 2))
            self.screen.blit(text_surface, text_rect)


    def process_auto_transitions(self):
        """Checks and processes 'auto' transitions."""
        while True:  # Allow cascading auto transitions
            auto_transition_found = False
            for transition in self.transitions:
                current_state, next_state, condition = transition
                if current_state == self.current_state and condition.strip() == "auto":
                    print(f"Auto-transitioning from {self.current_state} to {next_state}")
                    self.current_state = next_state
                    if self.current_state == "exit_game":
                        self.close()  # Exit immediately
                    auto_transition_found = True
                    break
            if not auto_transition_found:
                break

    def handle_events(self):
        """Handles user input and transitions."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEMOTION:
                # Get mouse coordinates
                mouse_x, mouse_y = event.pos
                # Update the window caption with the coordinates
                caption = (
                    f"{self.config['game_info']['game_title']} "
                    f"({self.config['game_info']['game_version']}) - Mouse: ({mouse_x}, {mouse_y})"
                )
                pygame.display.set_caption(caption)                
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                for transition in self.transitions:
                    if transition[0] == self.current_state:
                        conditions = transition[2].split("|")
                        for condition in conditions:
                            condition = condition.strip()
                            # Handle key-based transitions
                            if condition.startswith("key") and event.type == pygame.KEYDOWN:
                                key_name = condition.split("_")[1]
                                key_code = self.keymap.get(f"key_{key_name}")
                                if key_code and event.key == key_code:
                                    print(f"Transitioning to {transition[1]}")  # Print transition message
                                    self.current_state = transition[1]
                                    if self.current_state == "exit":
                                        self.close()  # Exit immediately
                                    self.process_auto_transitions()  # Handle auto transitions
                                    return
                                    
                            # Handle region-based transitions
                            elif condition.startswith("region") and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                region_name = condition.split()[1]
                                if region_name in self.regions:
                                    x1, y1, x2, y2 = self.regions[region_name]
                                    mouse_x, mouse_y = pygame.mouse.get_pos()
                                    if x1 <= mouse_x <= x2 and y1 <= mouse_y <= y2:
                                        print(f"Transitioning to {transition[1]}")  # Print transition message
                                        self.current_state = transition[1]
                                        if self.current_state == "exit":
                                            self.close()  # Exit immediately
                                        self.process_auto_transitions()  # Handle auto transitions
                                        return

    def update(self):
        """Game state updates."""
        # Example: Add state-specific logic here
        pass

    def render(self):
        """Render the current state."""
        # Draw the black background
        self.screen.blit(self.background, (0, 0))

        # Draw active regions for the current state
        self.draw_regions()

        # Flip the display to render changes
        pygame.display.flip()

    def stop_music(self):
        """Stop the music if it's playing and the mixer is initialized."""
        if pygame.mixer.get_init():  # Check if the mixer is initialized
            if pygame.mixer.music.get_busy():  # Check if music is playing
                pygame.mixer.music.stop()
                print("Music stopped.")
            else:
                print("No music is playing.")
        else:
            print("Mixer not initialized.")
        
    def close(self):
        """Clean up resources and quit."""
        print("Exiting game and cleaning up resources.")
        # pygame.mixer.music.stop()  # Stop the music
        self.stop_music()  # Safely stop music
        pygame.quit()
        sys.exit()

    def main(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.config["game_info"]["fps"])  # Limit to FPS


if __name__ == "__main__":
    # Create game instance
    game = GamingStateManager()
    try:
        game.main()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        game.close()
