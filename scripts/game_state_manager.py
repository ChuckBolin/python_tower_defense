import time

class GameStateManager:
    def __init__(self, initial_state="initial", level=1):
        self.state = initial_state  # Start with the initial state
        self.g_level = level        # Current game level
        self.start_time = time.time()  # Track time for timers if needed

    def change_state(self, new_state):
        """Change to a new game state."""
        print(f"Changing state from {self.state} to {new_state}")
        self.state = new_state
        self.start_time = time.time()

    def update(self):
        """Handle logic for the current state."""
        if self.state == "initial":
            self.load_config()
            self.change_state("main_menu")

        elif self.state == "main_menu":
            print("Main Menu: Awaiting input...")
            # Simulated input: Transition based on user choice
            user_input = self.get_user_input()
            if user_input == "load_level":
                self.change_state("load_level")
            elif user_input == "help":
                self.change_state("help")
            elif user_input == "exit":
                self.change_state("exit")

        elif self.state == "load_level":
            print(f"Loading Level {self.g_level}...")
            time.sleep(1)  # Simulate loading time
            self.change_state("play_level")

        elif self.state == "play_level":
            print(f"Playing Level {self.g_level}...")
            # Simulate gameplay
            game_outcome = self.simulate_gameplay()
            if game_outcome == "quit":
                self.change_state("quit_level")
            elif game_outcome == "win":
                self.change_state("won_level")
            elif game_outcome == "lose":
                self.change_state("lost_level")

        elif self.state == "quit_level":
            print("Level Quit. Returning to Main Menu.")
            self.change_state("main_menu")

        elif self.state == "won_level":
            print(f"Level {self.g_level} Won! Incrementing level.")
            self.g_level += 1
            self.play_sound("win")
            self.change_state("main_menu")

        elif self.state == "lost_level":
            print(f"Level {self.g_level} Lost. Returning to Main Menu.")
            self.play_sound("lose")
            self.change_state("main_menu")

        elif self.state == "help":
            print("Showing Help. Returning to Main Menu.")
            self.change_state("main_menu")

        elif self.state == "exit":
            print("Exiting the game.")
            exit()

    def load_config(self):
        """Simulate loading configuration."""
        print("Loading configuration...")

    def get_user_input(self):
        """Simulate user input for testing."""
        # In a real game, this would handle keypresses or mouse clicks.
        # Simulated example: always go to 'load_level'
        return "load_level"

    def simulate_gameplay(self):
        """Simulate gameplay outcome."""
        # Return 'win', 'lose', or 'quit' to simulate outcomes.
        return "win"

    def play_sound(self, outcome):
        """Simulate playing a sound."""
        print(f"Playing {outcome} sound...")
