import pygame

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