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
    def __init__(self, screen, color, x=500, y=0, width=250, height=500):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=color)
        self.screen = screen
        self.score = 0
        self.level = 1
        
    def write_score(self, text, color):
        text_score = text.render('Score: ' + str(self.score), True, color)
        self.screen.blit(text_score, (515, 50))
        
    def draw(self):
        """Draw Picture objects in main window"""
        self.screen.blit(self.rect, (self.rect.x, self.rect.y))
        
        
class AbilitiesButttons(Area):
    def __init__(self, icon_name, screen, price, x, y, x_icon=510, y_icon=100, width=16, height=45):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.icon_image = pg.image.load(os.path.join(
            'sprites', icon_name+'.png')).convert_alpha()
        self.icon_name = icon_name
        self.screen = screen
        self.rect_icon = pg.Rect(x_icon, y_icon, 75, 75)
        self.available = False 
        self.button_pressed = False
        self.price = price
        
    def check_pressed(self, mouse_x, mouse_y):
        if self.available:
            if (self.rect_icon.x <= mouse_x <= self.rect_icon.x + 75) and (self.rect_icon.y <= mouse_y <= self.rect_icon.y + 75):
                self.button_pressed = True
            else:
                self.button_pressed = False
        else:
            self.button_pressed = False
            
    def IsAvailable(self, table):
        if table.score >= self.price:
            self.available = True
        else:
            self.available = False
            
          
    def draw_icon(self):
        """Draw Picture objects in main window"""
        if self.available:
            self.icon_image = pg.image.load(os.path.join(
                'sprites', self.icon_name+str(1)+'.png')).convert_alpha()
        else:
            self.icon_image = pg.image.load(os.path.join(
                'sprites', self.icon_name+'.png')).convert_alpha()
        self.screen.blit(self.icon_image, (self.rect_icon.x, self.rect_icon.y))
        
        
class Gun(AbilitiesButttons):
    def __init__(self, icon_name, filename, screen, price, platform, x=400, y=400):
        AbilitiesButttons.__init__(self, icon_name=icon_name, screen=screen, price=price, x=x, y=y)
        self.filename = filename
        self.image = pg.image.load(os.path.join(
            'sprites', filename+'.png')).convert_alpha()
        self.rect.x = platform.rect.x + platform.width/2
        self.rect.y = platform.rect.y + platform.height/2
        self.vy = -3
        self.shot = False
        
    def shoot(self, platform, table):
        if self.button_pressed and not(self.shot): 
            self.rect.x = platform.rect.x + platform.width/2
            self.rect.y = platform.rect.y - platform.height
            self.shot = True
            self.available = False
            table.score -= self.price
        elif not(self.button_pressed) and self.shot:
            self.available = False
            
    def move(self):
        self.rect.y += self.vy
        if self.rect.y <= 0:
            self.shot = False
        
    def draw(self):
        if self.shot:
            self.screen.blit(self.image, (self.rect.x, self.rect.y))
            
    def kill_enemy(self, obj):
        if self.colliderect(obj.rect):
            obj.lives -= 1
            self.shot = False


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
            'sprites', picture_name + '.png')).convert_alpha()
        self.picture_name = picture_name
        self.moving_right = False
        self.moving_left = False
        self.vx = 0
        self.width = width
        self.height = height
        self.lives = 5
        
    def draw(self, screen):
         """Draw platform in main window"""
         screen.blit(self.image, (self.rect.x, self.rect.y))
         
    def move(self):
        """ Moving platform depending on keydown: moving right or left """
        if self.rect.x >= 250:
            self.moving_right = False
            
        if self.moving_left:
            self.vx = -3
            self.rect.x += self.vx

        if self.moving_right:
            self.vx = 3
            self.rect.x += self.vx
            
        if not(self.moving_right) and not(self.moving_left):
            self.vx = 0
            
    def check_health(self):
        if self.lives == 4:
            self.image = pg.image.load(os.path.join(
                'sprites', self.picture_name+str(4)+'.png')).convert_alpha()
        elif self.lives == 3:
            self.image = pg.image.load(os.path.join(
                'sprites', self.picture_name+str(3)+'.png')).convert_alpha()
        elif self.lives == 2:
            self.image = pg.image.load(os.path.join(
                'sprites', self.picture_name+str(2)+'.png')).convert_alpha()
        elif self.lives == 1:
            self.image = pg.image.load(os.path.join(
                'sprites', self.picture_name+str(1)+'.png')).convert_alpha()
            
                   
class Ball(Area):
    """ Ball class """
    def __init__(self, picture_name, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pg.image.load(os.path.join(
            'sprites', picture_name)).convert_alpha()
        self.width = width
        self.height = height
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
            self.vx += 0.42*obj.vx
            
    def kill_enemy(self, obj):
        if self.rect.colliderect(obj.rect):
            obj.lives -= 1
            if self.rect.y >= obj.rect.y + obj.height/2:
                self.vy *= -1
            else:
                self.vx *= -1

            
class Enemy(Area):
    """ Enemy class """
    def __init__(self, picture_name, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pg.image.load(os.path.join(
            'sprites', picture_name)).convert_alpha()
        self.width = width
        self.height = height
        self.lives = 1
        self.points = 10

    def draw(self, screen):
         """Draw enemy in main window"""
         screen.blit(self.image, (self.rect.x, self.rect.y))
                  
    def check_death(self, screen, list_obj, table, isoptions = False):
        """ Checking hit with object (ball) and killing (or not) the enemy """
        if self.lives == 0:
            list_obj.remove(self)
            table.score += self.points
            self.fill(screen)
            if isoptions:
                self.fill_bullet(screen)
            
            
class ArmoredEnemy(Enemy):
    def __init__(self, picture_name, x=0, y=0, width=10, height=10):
        Enemy.__init__(self, picture_name, x=x, y=y, width=width, height=height)
        self.image = pg.image.load(os.path.join(
            'sprites', picture_name)).convert_alpha()
        self.lives = 3
        self.points = 30
        
        
class ShooterEnemy(Enemy):
    def __init__(self, picture_name, bullet_image, x=0, y=0, width=10, height=10):
        Enemy.__init__(self, picture_name, x=x, y=y, width=width, height=width)
        self.image = pg.image.load(os.path.join(
            'sprites', picture_name)).convert_alpha()
        self.width = width
        self.height = height
        self.rect_bullet = pg.Rect(self.rect.x + width/2, self.rect.y +3*height/2, 20, 35)
        self.bullet_image = pg.image.load(os.path.join(
            'sprites', bullet_image)).convert_alpha()
        self.bullet_vy = 2
        self.lives = 2
        self.points = 40
        self.shot = False
        self.timer = 0
        
    def shooting(self):
        if self.timer >= 60 and not(self.shot):
            self.rect_bullet.x = self.rect.x + self.width/2
            self.rect_bullet.y = self.rect.y + 3*self.height/2
            self.shot = True
            self.timer = 0
        else:
            self.timer += 1
            
    def fill_bullet(self, screen):
        pg.draw.rect(screen, self.fill_color, self.rect_bullet)
            
    def draw_bullet(self, screen):
        if self.shot and self.lives != 0:
            screen.blit(self.bullet_image, (self.rect_bullet.x, self.rect_bullet.y))
            
    def move_bullet(self):
        if self.shot:
            self.rect_bullet.y += self.bullet_vy
        if self.rect_bullet.y >= 500:
            self.shot = False
            
    def check_hit(self, obj):
        if type(obj) == Platform:
            if self.rect_bullet.colliderect(obj.rect):
                obj.lives -= 1
                self.shot = False
        if type(obj) == Ball:
            if self.rect_bullet.colliderect(obj.rect):
                obj.vy *= -1
                self.shot = False