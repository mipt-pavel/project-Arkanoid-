import pygame as pg
import os.path

pg.mixer.pre_init(44100, -16, 1, 512)
pg.init()

back = (200, 255, 255)  # background color.

sound_hit = pg.mixer.Sound('sounds/Hit.wav')
sound_kill = pg.mixer.Sound('sounds/Kill.wav')
sound_shoot = pg.mixer.Sound('sounds/Shoot.wav')


# class Area from pygame.Rect
class Area:
    """Rectangle sprite background for sprite."""
    def __init__(self, x: int = 0, y: int = 0,
                 width: int = 10, height: int = 10, color=None):
        self.rect = pg.Rect(x, y, width, height)
        self.fill_color = back
        if color:
            self.fill_color = color
        self.score = 0

    # color func
    def color(self, new_color):
        self.fill_color = new_color

    def fill(self, screen):
        """Fill background area by color."""
        pg.draw.rect(screen, self.fill_color, self.rect)

    def collidepoint(self, x, y):
        """Check points of intersections."""
        return self.rect.collidepoint(x, y)

    def colliderect(self, rect):
        """Check if coordinates of two rects intersected."""
        return pg.Rect.colliderect(self.rect, rect)


class GameTable(Area):
    """Makes game table for interface and player`s indicators"""
    def __init__(self, screen, color, x=500, y=0, width=250, height=500):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=color)
        self.screen = screen
        self.score = 0
        self.level = 1

    def write_score(self, text, color):
        """Writes score, which player reached"""
        text_score = text.render('Score: ' + str(self.score), True, color)
        self.screen.blit(text_score, (515, 50))

    def write_level(self, text, color):
        """Writes level, which player on"""
        text_level = text.render('Level: ' + str(self.level), True, color)
        self.screen.blit(text_level, (515, 450))

    def draw(self):
        """Draw game table objects in main window"""
        self.screen.blit(self.rect, (self.rect.x, self.rect.y))


class Picture(Area):
    """Picture rectangle objects class."""
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pg.image.load(os.path.join(
            'sprites', filename)).convert_alpha()

# draw picture (start or ending screen) in main window
    def draw(self, screen):
        """Draw Picture objects in main window"""
        screen.blit(self.image, (self.rect.x, self.rect.y))
