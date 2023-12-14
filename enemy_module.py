import classes
import objects_module


class Enemy(classes.Area):
    """ Enemy class """
    def __init__(self, picture_name, x, y=0, width=10, height=10):
        classes.Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = classes.pg.image.load(classes.os.path.join(
            'sprites', 'enemies', picture_name)).convert_alpha()
        self.width = width
        self.height = height
        self.lives = 1
        self.points = 10

    def draw(self, screen):
        """Draw enemy in main window"""
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def check_death(self, screen, list_obj, table):
        """ Checking hit with object (ball) and killing (or not) the enemy """
        if self.lives == 0:
            list_obj.remove(self)
            table.score += self.points
            classes.sound_kill.play()
            self.fill(screen)


class ArmoredEnemy(Enemy):
    def __init__(self, picture_name, x=0, y=0, width=10, height=10):
        Enemy.__init__(self, picture_name, x=x, y=y, width=width, height=height)
        self.image = classes.pg.image.load(classes.os.path.join(
            'sprites', 'enemies', picture_name)).convert_alpha()
        self.lives = 3
        self.points = 30


class ShooterEnemy(Enemy):
    def __init__(self, picture_name, fireball_image, x=0, y=0, width=10, height=10):
        Enemy.__init__(self, picture_name, x=x, y=y, width=width, height=width)
        self.image = classes.pg.image.load(classes.os.path.join(
            'sprites', 'enemies', picture_name)).convert_alpha()
        self.width = width
        self.height = height
        self.rect_fireball = classes.pg.Rect(self.rect.x + width/2, self.rect.y + 3*height/2, 20, 35)
        self.fireball_image = classes.pg.image.load(classes.os.path.join(
            'sprites', 'enemies', fireball_image)).convert_alpha()
        self.fireball_vy = 2
        self.lives = 2
        self.points = 40
        self.shot = False
        self.timer = 0

    def respawn_fireball(self):
        self.rect_fireball.x = self.rect.x + self.width/2
        self.rect_fireball.y = self.rect.y + 3*self.height/2

    def shooting(self):
        if self.timer >= 60 and not self.shot:
            self.respawn_fireball()
            self.shot = True
            self.timer = 0
        else:
            self.timer += 1

    def fill_fireball(self, screen):
        classes.pg.draw.rect(screen, self.fill_color, self.rect_fireball)

    def draw_fireball(self, screen):
        if self.shot and self.lives != 0:
            screen.blit(self.fireball_image, (self.rect_fireball.x, self.rect_fireball.y))

    def move_fireball(self):
        if self.shot:
            self.rect_fireball.y += self.fireball_vy
        if self.rect_fireball.y >= 500:
            self.shot = False

    def check_hit(self, obj, screen):
        if self.rect_fireball.colliderect(obj.rect):
            if isinstance(obj, objects_module.Platform):
                if not obj.shield:
                    obj.lives -= 1
                else:
                    obj.shield_lives -= 1
            if isinstance(obj, objects_module.Ball):
                if obj.vy > 0:
                    obj.vy *= 1
                elif obj.vy < -1:
                    obj.vy *= 1
            self.shot = False
            self.fill_fireball(screen)
            self.respawn_fireball()
