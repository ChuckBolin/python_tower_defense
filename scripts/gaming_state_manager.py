import pygame
import sys

class GamingStateManager:
    def __init__(self):
        self.current_state = "initial"
        self.current_state = "main_menu"

        # Define clickable regions
        self.regions = {
            "play": (350, 150, 450, 200),
            "setup": (350, 210, 450, 260),
            "restore": (350, 270, 450, 320),
            "exit": (350, 330, 450, 380),
        }

        # Key mappings
        self.keymap = {
            "key_play": pygame.K_p,
            "key_exit": pygame.K_x,
            "key_quit": pygame.K_q,
            "key_pause": pygame.K_SPACE,
            "key_escape": pygame.K_ESCAPE
        }

    def handle_event(self, event, mouse_pos):
        """Process events and update the state accordingly."""
        mouse_x, mouse_y = mouse_pos

        # Process key inputs
        if event.type == pygame.KEYDOWN:
            if self.current_state == "initial":
                self.current_state = "main_menu"
            elif self.current_state == "main_menu":
                if event.key == self.keymap["key_play"]:
                    self.current_state = "play"
                elif event.key == self.keymap["key_exit"]:
                    self.current_state = "exit_game"
                    self.exit_game()
            elif self.current_state == "play" and event.key == self.keymap["key_escape"]:
                self.current_state = "main_menu"
            elif self.current_state == "play" and event.key == self.keymap["key_pause"]:
                self.current_state = "pause"
            elif self.current_state == "pause" and event.key == self.keymap["key_pause"]:
                self.current_state = "play"
            elif self.current_state == "play" and event.key == self.keymap["key_pause"]:
                self.current_state = "pause" 
            elif self.current_state == "restore" and event.key == self.keymap["key_escape"]:
                self.current_state = "main_menu"                 
            elif self.current_state == "setup" and event.key == self.keymap["key_escape"]:
                self.current_state = "main_menu"                 

        # Process mouse inputs
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            if self.current_state == "main_menu":
                if self.is_in_region("play", mouse_x, mouse_y):
                    self.current_state = "play"
                elif self.is_in_region("setup", mouse_x, mouse_y):
                    self.current_state = "setup"
                elif self.is_in_region("restore", mouse_x, mouse_y):
                    self.current_state = "restore"
                    
                elif self.is_in_region("exit", mouse_x, mouse_y):
                    self.current_state = "exit_game"
                    self.exit_game()

        # print(f"Game state: {self.current_state}")

    def is_in_region(self, region_name, x, y):
        """Check if a point is within a defined region."""
        if region_name in self.regions:
            x1, y1, x2, y2 = self.regions[region_name]
            return x1 <= x <= x2 and y1 <= y <= y2
        return False

    def exit_game(self):
        """Exit the game cleanly."""
        print("Exiting game...")
        pygame.quit()
        sys.exit()

    def get_state(self):
        return self.current_state