import classes


class Platform(classes.Area):
    """ Platform class """
    def __init__(self, picture_name, x=0, y=0, width=10, height=10):
        classes.Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = classes.pg.image.load(classes.os.path.join(
            'sprites', 'platform', picture_name + '.png')).convert_alpha()
        self.picture_name = picture_name
        self.width = width
        self.height = height
        self.moving_right = False
        self.moving_left = False
        self.vx = 0
        self.lives = 5
        self.shield = False
        self.shield_lives = 2

    def draw(self, screen):
        """Draw platform in main window"""
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def move(self):
        """ Moving platform depending on keydown: moving right or left and considering walls"""
        self.rect.x += self.vx
        if self.moving_left and not self.moving_right and self.rect.x >= 0:
            if self.vx >= -8:
                self.vx -= 1

        elif not self.moving_left and self.moving_right and self.rect.x <= 325:
            if self.vx <= 8:
                self.vx += 1

        elif (self.rect.x >= 0) and self.rect.x <= 325:
            self.vx *= 0.9

        else:
            self.vx = 0

    def check_health(self):
        """Check platform health and change platform`s image depending on it"""
        if not self.shield:
            if self.lives == 5:
                self.image = classes.pg.image.load(classes.os.path.join(
                    'sprites', 'platform', self.picture_name+'.png')).convert_alpha()
            elif self.lives == 4:
                self.image = classes.pg.image.load(classes.os.path.join(
                    'sprites', 'platform', self.picture_name+str(4)+'.png')).convert_alpha()
            elif self.lives == 3:
                self.image = classes.pg.image.load(classes.os.path.join(
                    'sprites', 'platform', self.picture_name+str(3)+'.png')).convert_alpha()
            elif self.lives == 2:
                self.image = classes.pg.image.load(classes.os.path.join(
                    'sprites', 'platform', self.picture_name+str(2)+'.png')).convert_alpha()
            elif self.lives == 1:
                self.image = classes.pg.image.load(classes.os.path.join(
                    'sprites', 'platform', self.picture_name+str(1)+'.png')).convert_alpha()


class Ball(classes.Area):
    """ Ball class """
    def __init__(self, picture_name, x=0, y=0, width=10, height=10):
        classes.Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = classes.pg.image.load(classes.os.path.join(
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

        if self.rect.x > 450:
            if 0 <= self.vx <= 10:
                self.vx *= -1
            elif self.vx >= 10:
                self.vx *= -0.9
        elif self.rect.x < 0:
            if -10 <= self.vx <= 0:
                self.vx *= -1
            elif self.vx <= -10:
                self.vx *= -0.9

    def check_hit(self, obj):
        """ Checking hit on object (platform) and changing velocity """
        if self.rect.colliderect(obj.rect):
            if self.rect.y + self.height < obj.rect.y + obj.height/2 and self.vy > 0:
                self.vy *= - 1
                self.vx += 0.42*obj.vx
            elif self.rect.x > obj.rect.x + obj.width/2 and self.vx - obj.vx < 0:
                self.vx = -self.vx + 2*obj.vx
            elif self.rect.x + self.width <= obj.rect.x + obj.width/2 and self.vx - obj.vx > 0:
                self.vx = -self.vx + 2*obj.vx

    def kill_enemy(self, obj):
        """Checking hit on enemy and changing velocity"""
        if self.rect.colliderect(obj.rect):
            obj.lives -= 1
            classes.sound_hit.play()
            if self.rect.y >= obj.rect.y + obj.height/2 and self.vy < 0:
                self.vy *= -1
            elif self.rect.y < obj.rect.y + obj.height/2:
                self.vx *= -1
