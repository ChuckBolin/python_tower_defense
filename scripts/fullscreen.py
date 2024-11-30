import pygame
import os

def main():
    pygame.init()

    # Ensure the window starts at the top-left corner
    os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"

    # Default windowed resolution
    screen_width, screen_height = 800, 600
    fullscreen = False

    # Detect current display resolution
    display_info = pygame.display.Info()
    fullscreen_width, fullscreen_height = display_info.current_w, display_info.current_h

    # Start in windowed mode
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Fullscreen Toggle Example")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Allow closing via window manager

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:  # Toggle fullscreen
                    fullscreen = not fullscreen
                    if fullscreen:
                        os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"
                        screen = pygame.display.set_mode(
                            (fullscreen_width, fullscreen_height), pygame.NOFRAME
                        )
                    else:
                        screen = pygame.display.set_mode((screen_width, screen_height))
                elif event.key == pygame.K_ESCAPE:  # Quit with ESC
                    running = False

        # Clear screen and update display
        screen.fill((30, 30, 30))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
