import pygame
import sys

class GamingStateManager:
    def __init__(self, scale=1.0):
        self.current_state = "main_menu"
        self.scale = scale

        # Define base clickable regions (unscaled coordinates)
        self.regions = {
            "play": (350, 150, 450, 200),
            "setup": (350, 210, 450, 260),
            "restore": (350, 270, 450, 320),
            "exit": (350, 330, 450, 380),
        }

        # Initialize scaled regions
        # self.regions = self.scale_regions(scale)

        # Key mappings
        self.keymap = {
            "key_play": pygame.K_p,
            "key_exit": pygame.K_x,
            "key_quit": pygame.K_q,
            "key_pause": pygame.K_SPACE,
            "key_escape": pygame.K_ESCAPE,
        }

    # def scale_regions(self, scale=1.0):
        # """Scale the clickable regions based on the provided scale factor."""
        # scaled_regions = {}
        # for name, (x1, y1, x2, y2) in self.regions.items():
            # scaled_regions[name] = (
                # int(x1 * scale),
                # int(y1 * scale),
                # int(x2 * scale),
                # int(y2 * scale),
            # )
        # return scaled_regions

    # def update_scale(self, new_scale):
        # """Update the scale and recalculate regions."""
        # self.scale = new_scale
        # self.regions = self.scale_regions(new_scale)

    def handle_event(self, event, mouse_pos):
        """Process events and update the state accordingly."""
        # Scale the mouse position to match the unscaled regions
        mouse_x = int(mouse_pos[0]) # / self.scale)
        mouse_y = int(mouse_pos[1])# / self.scale)

        # Handle key inputs
        if event.type == pygame.KEYDOWN:
            if self.current_state == "main_menu":
                if event.key == self.keymap["key_play"]:
                    self.current_state = "play"
                elif event.key == self.keymap["key_exit"]:
                    self.current_state = "exit_game"
                    self.exit_game()
            elif self.current_state == "play" and event.key == self.keymap["key_escape"]:
                self.current_state = "main_menu"
            elif self.current_state == "setup" and event.key == self.keymap["key_escape"]:
                self.current_state = "main_menu"
            elif self.current_state == "restore" and event.key == self.keymap["key_escape"]:
                self.current_state = "main_menu"

        # Handle mouse inputs
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            if self.current_state == "main_menu":
                if self.is_in_region("play", mouse_x, mouse_y):
                    self.current_state = "play"
                    print("Transitioning to play state.")
                elif self.is_in_region("setup", mouse_x, mouse_y):
                    self.current_state = "setup"
                    print("Transitioning to setup state.")
                elif self.is_in_region("restore", mouse_x, mouse_y):
                    self.current_state = "restore"
                    print("Transitioning to restore state.")
                elif self.is_in_region("exit", mouse_x, mouse_y):
                    self.current_state = "exit_game"
                    print("Exiting game.")
                    self.exit_game()

    def is_in_region(self, region_name, x, y):
        """Check if a point is within a defined region."""
        if region_name in self.regions:
            x1, y1, x2, y2 = self.regions[region_name]
            print(x1, y1, x2, y2)
            return x1 <= x <= x2 and y1 <= y <= y2
        return False

    def exit_game(self):
        """Exit the game cleanly."""
        print("Exiting game...")
        pygame.quit()
        sys.exit()

    def get_state(self):
        return self.current_state
