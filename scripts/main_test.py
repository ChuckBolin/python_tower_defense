import pygame


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


def main():
    pygame.init()

    # Screen setup
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Explosion Demo")
    clock = pygame.time.Clock()

    # Background color
    background_color = (0, 0, 0)

    # Initialize the SpriteManager
    sprite_manager = SpriteManager(duration=2)  # Explosion lasts 2 seconds

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse click
                mouse_x, mouse_y = event.pos
                flip = mouse_x % 2 == 0  # Flip horizontally for every other explosion
                sprite_manager.add_explosion(mouse_x, mouse_y, flip_horizontal=flip)

        # Update explosions
        delta_time = clock.tick(60) / 1000.0  # Time in seconds
        sprite_manager.update(delta_time)

        # Render
        screen.fill(background_color)  # Clear the screen
        sprite_manager.render(screen)
        pygame.display.flip()  # Update the display

    pygame.quit()


if __name__ == "__main__":
    main()



# import pygame


# class SpriteManager:
    # def __init__(self, x, y, duration=4, flip_horizontal=False):
        # """Initialize the SpriteManager with the explosion position."""
        # self.x = x
        # self.y = y
        # self.sprite_sheet = None
        # self.sprites = []
        # self.current_frame = 0
        # self.frame_time = float(duration) / 48  # 4 seconds / 48 frames
        # self.elapsed_time = 0
        # self.animation_done = False
        # self.flip_horizontal = flip_horizontal

    # def initial(self):
        # """Load the sprite sheet and extract 48 explosion frames."""
        # self.sprite_sheet = pygame.image.load("./assets/sprites/effects.png").convert_alpha()
        # sprite_width = 63
        # sprite_height = 64
        # sprites_per_row = 12
        # rows = 4

        # Extract all 48 sprites
        # for row in range(rows):
            # for col in range(sprites_per_row):
                # x = col * sprite_width
                # y = row * sprite_height
                # sprite = self.sprite_sheet.subsurface((x, y, sprite_width, sprite_height))
                # self.sprites.append(sprite)

    # def update(self, delta_time):
        # """Update the current frame based on elapsed time."""
        # if self.animation_done:
            # return

        # self.elapsed_time += delta_time
        # if self.elapsed_time >= self.frame_time:
            # self.elapsed_time -= self.frame_time
            # self.current_frame += 1

            # if self.current_frame >= len(self.sprites):
                # self.animation_done = True  # Animation completed

    # def render(self, screen):
        # """Render the current frame of the explosion."""
        # if not self.animation_done:
            # sprite = self.sprites[self.current_frame]
            # screen.blit(sprite, (self.x, self.y))


# def main():
    # pygame.init()

    # Screen setup
    # screen_width, screen_height = 800, 600
    # screen = pygame.display.set_mode((screen_width, screen_height))
    # pygame.display.set_caption("Explosion Demo")
    # clock = pygame.time.Clock()

    # Background color
    # background_color = (0, 0, 0)

    # Explosion manager
    # explosions = []

    # running = True
    # while running:
        # Handle events
        # for event in pygame.event.get():
            # if event.type == pygame.QUIT:
                # running = False
            # elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse click
                # mouse_x, mouse_y = event.pos
                # Alternate flipping based on some condition for variety
                # flip = mouse_x % 2 == 0  # Flip horizontally for every other explosion
                # explosion = SpriteManager(mouse_x, mouse_y, duration=0.1, flip_horizontal=flip)
                # explosion.initial()
                # explosions.append(explosion)

        # Update explosions
        # delta_time = clock.tick(60) / 1000.0  # Time in seconds
        # for explosion in explosions:
            # explosion.update(delta_time)

        # Remove completed explosions
        # explosions = [e for e in explosions if not e.animation_done]

        # Render
        # screen.fill(background_color)  # Clear the screen
        # for explosion in explosions:
            # explosion.render(screen)
        # pygame.display.flip()  # Update the display

    # pygame.quit()


# if __name__ == "__main__":
    # main()
