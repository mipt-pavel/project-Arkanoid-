import classes


class AbilitiesButttons(classes.Area):
    """Abilities class"""
    def __init__(self, icon_name, screen, price, 
                 x, y,  width, height, 
                 x_icon, y_icon, width_icon, height_icon):
        classes.Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.icon_image = classes.pg.image.load(classes.os.path.join(
            'sprites', 'buttons', icon_name+'.png')).convert_alpha()
        self.icon_name = icon_name
        self.width_icon = width_icon
        self.height_icon = height_icon
        self.screen = screen
        self.rect_icon = classes.pg.Rect(x_icon, y_icon, self.width_icon, self.height_icon)
        self.available = False
        self.button_pressed = False
        self.price = price

    def check_pressed(self, mouse_x, mouse_y):
        """Check was button pressed or not"""
        if self.available:
            if ((self.rect_icon.x <= mouse_x <= self.rect_icon.x + self.width_icon) 
                    and (self.rect_icon.y <= mouse_y <= self.rect_icon.y + self.height_icon)):
                self.button_pressed = True
            else:
                self.button_pressed = False
        else:
            self.button_pressed = False

    def is_available(self, table):
        """Check is ability available or not (depending on player`s score)"""
        if table.score >= self.price:
            self.available = True
        else:
            self.available = False

    def draw_icon(self):
        """Draw Picture objects in main window"""
        if self.available:
            self.icon_image = classes.pg.image.load(classes.os.path.join(
                'sprites', 'buttons', self.icon_name+str(1)+'.png')).convert_alpha()
        else:
            self.icon_image = classes.pg.image.load(classes.os.path.join(
                'sprites', 'buttons', self.icon_name+'.png')).convert_alpha()
        self.screen.blit(self.icon_image, (self.rect_icon.x, self.rect_icon.y))


class InterfaceButton(AbilitiesButttons):
    """Interface buttons"""
    def __init__(self, icon_name, filename, screen, price, width=235, height=100, x_icon=510, y_icon=395,
                 x=510, y=290, width_icon=50, height_icon=50):
        AbilitiesButttons.__init__(self, icon_name=icon_name, screen=screen, price=price, x=x, y=y, width=width,
                                   height=height, x_icon=x_icon, y_icon=y_icon,
                                   width_icon=width_icon, height_icon=height_icon)
        self.image = classes.pg.image.load(classes.os.path.join(
            'sprites', 'buttons', filename+'.png')).convert_alpha()

    def draw_button(self):
        """Draw button ability if it was pressed"""
        if self.button_pressed:
            self.screen.blit(self.image, (self.rect.x, self.rect.y))


class Gun(AbilitiesButttons):
    """Gun ability"""
    def __init__(self, icon_name, filename, screen, price, platform, width=16, height=45, x_icon=510, y_icon=100,
                 width_icon=75, height_icon=75, x=400, y=-55):
        AbilitiesButttons.__init__(self, icon_name=icon_name, screen=screen, price=price, x=x, y=y, width=width,
                                   height=height, x_icon=x_icon, y_icon=y_icon,
                                   width_icon=width_icon, height_icon=height_icon)
        self.filename = filename
        self.image = classes.pg.image.load(classes.os.path.join(
            'sprites', 'buttons', filename+'.png')).convert_alpha()
        self.rect.x = platform.rect.x + platform.width/2
        self.rect.y = platform.rect.y + platform.height/2
        self.vy = -3
        self.shot = False

    def shoot(self, platform, table):
        """Shooting bullet"""
        if self.button_pressed and not self.shot:
            self.rect.x = platform.rect.x + platform.width/2
            self.rect.y = platform.rect.y - platform.height
            self.shot = True
            self.available = False
            table.score -= self.price
            classes.sound_shoot.play()
        elif not self.button_pressed and self.shot:
            self.available = False

    def move(self):
        """Moving bullet"""
        if self.shot:
            self.rect.y += self.vy
            if self.rect.y <= 0:
                self.shot = False

    def draw(self):
        """Draw bullet on the screen"""
        if self.shot:
            self.screen.blit(self.image, (self.rect.x, self.rect.y))

    def kill_enemy(self, obj):
        """Check has bullet hit enemy or not"""
        if self.colliderect(obj.rect):
            obj.lives -= 1
            self.shot = False
            self.rect.y = -55
            classes.sound_hit.play()


class Shield(AbilitiesButttons):
    def __init__(self, icon_name, filename, screen, price, width=16, height=45, x_icon=590, y_icon=100,
                 width_icon=75, height_icon=75, x=400, y=-55):
        AbilitiesButttons.__init__(self, icon_name=icon_name, screen=screen, price=price, x=x, y=y, width=width,
                                   height=height, x_icon=x_icon, y_icon=y_icon,
                                   width_icon=width_icon, height_icon=height_icon)
        self.filename = filename
        self.lives = 2

    def activate_shield(self, obj, table):
        if self.button_pressed and not obj.shield:
            obj.shield_lives = 2
            obj.shield = True
            table.score -= self.price
            self.available = False
            self.button_pressed = False

        if obj.shield:
            if obj.shield_lives == 2:
                obj.image = classes.pg.image.load(classes.os.path.join(
                    'sprites', 'platform', self.filename + '.png')).convert_alpha()
            if obj.shield_lives == 1:
                obj.image = classes.pg.image.load(classes.os.path.join(
                    'sprites', 'platform', self.filename + '1.png')).convert_alpha()

        if obj.shield_lives == 0:
            obj.shield = False
            if table.score >= self.price:
                self.available = True


class Heal(AbilitiesButttons):
    def __init__(self, icon_name, screen, price, width=16, height=45, x_icon=670, y_icon=100,
                 width_icon=75, height_icon=75, x=400, y=-55):
        AbilitiesButttons.__init__(self, icon_name=icon_name, screen=screen, price=price, x=x, y=y,
                                   width=width, height=height, x_icon=x_icon, y_icon=y_icon,
                                   width_icon=width_icon, height_icon=height_icon)

    def heal(self, obj, table):
        if self.button_pressed and obj.lives != 5:
            obj.lives += 1
            table.score -= self.price
            self.button_pressed = False
