import pygame as pg
import os.path

back = (200, 255, 255)  # background color.


# class Area from pygame.Rect
class Area:
    """Rectangle sprite background for sprite."""
    def __init__(self, x: int = 0, y: int = 0,
                 width: int = 10, height: int = 10, color=None):
        self.rect = pg.Rect(x, y, width, height)
        self.fill_color = back
        if color:
            self.fill_color = color

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
        return self.rect.colliderect(rect)


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
    
        
class Platform(Area):
    """ Platform class """
    def __init__(self, picture_name, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pg.image.load(os.path.join(
            'sprites', picture_name)).convert_alpha()
        self.moving_right = False
        self.moving_left = False
        
    def draw(self, screen):
         """Draw platform in main window"""
         screen.blit(self.image, (self.rect.x, self.rect.y))
         
    def move(self):
        """ Moving platform depending on keydown: moving right or left """
        if self.moving_left:
            self.rect.x -= 3

        if self.moving_right:
            self.rect.x += 3
            
            
class Ball(Area):
    """ Ball class """
    def __init__(self, picture_name, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pg.image.load(os.path.join(
            'sprites', picture_name)).convert_alpha()
        self.vx = 3
        self.vy = 3

    def draw(self, screen):
         """Draw ball in main window"""
         screen.blit(self.image, (self.rect.x, self.rect.y))
         
    def move(self):
        """ Moving ball by its velocity parametrs. Considers reflecting from borders """
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.y < 0:
            self.vy *= -1

        if self.rect.x > 450 or self.rect.x < 0:
            self.vx *= -1
            
    def check_hit(self, obj):
        """ Checking hit on object (platform) and changing velocity """
        if self.rect.colliderect(obj.rect):
            self.vy *= - 1

            
class Enemy(Area):
    """ Enemy class """
    def __init__(self, picture_name, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pg.image.load(os.path.join(
            'sprites', picture_name)).convert_alpha()

    def draw(self, screen):
         """Draw enemy in main window"""
         screen.blit(self.image, (self.rect.x, self.rect.y))
         
    def check_death(self, screen, obj, list_obj):
        """ Checking hit with object (ball) and killing (or not) the enemy """
        if self.rect.colliderect(obj.rect):
            list_obj.remove(self)
            self.fill(screen)
            obj.vy *= -1
