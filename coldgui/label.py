import pygame
from . import CENTER

class Label:

    def __init__(self, parent, position=(0, 0), text="", sysfont="Calibri", font=None, font_size=10, fore_color=(0, 0, 0), back_color=None, antialias=True, active=True, tag=None, visible=True):
        self.tag = tag

        self.parent = parent
        parent.add(self)

        self._position = position
        self._text = text

        self.font_size = font_size
        if font: self.font = pygame.font.Font(font, self.font_size)
        else: self.font = pygame.font.SysFont(sysfont, self.font_size)

        self.fore_color = fore_color
        self.back_color = back_color
        self.antialias = antialias

        #Apply constants
        if CENTER in self._position: self._position = list(self._position)
        if self._position[0] == CENTER: self._position[0] = (self.parent.width - (self.parent.border_size * 2 + self.parent.padding * 2)) / 2 - self.font.size(self.text)[0] / 2
        if self._position[1] == CENTER: self._position[1] = (self.parent.height - (self.parent.border_size * 2 + self.parent.padding * 2)) / 2 - self.font.size(self.text)[1] / 2
        self._position = tuple(self._position)

        self._visible = visible
        self._active = active
        self.event_funcs = dict()

        self.surface = pygame.Surface(self.font.size(self.text))
        self.surface = self.surface.convert_alpha()

        self.get_abs_position()
        self.render()

    def event(self, func):
        self.event_funcs[func.__name__] = func

    def get_abs_position(self):
        #Absolute position relative to the Pygame display screen
        try:
            self.abs_position = tuple(map(sum, zip(self.parent.abs_position, self.position)))
        except Exception as e:
            if isinstance(e, AttributeError):
                self.abs_position = self._position
            else: raise e

    def render(self):
        if self.visible:
            self.surface.set_alpha(255)
            self.surface = self.font.render(self.text, self.antialias, self.fore_color, self.back_color)
            if not self.active: self.surface.set_alpha(64)

    def update(self):
        pass

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self.render()
        if "text_changed" in self.event_funcs: self.event_funcs["text_changed"]()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position
        self.get_abs_position()
        if "position_changed" in self.event_funcs: self.event_funcs["position_changed"]()

    @property
    def x(self):
        return self._position[0]

    @x.setter
    def x(self, x):
        self._position = list(self._position)
        self._position[0] = x
        self._position = tuple(self._position)
        self.get_abs_position()
        if "position_changed" in self.event_funcs: self.event_funcs["position_changed"]()

    @property
    def y(self):
        return self._position[1]

    @y.setter
    def y(self, y):
        self._position = list(self._position)
        self._position[1] = y
        self._position = tuple(self._position)
        self.get_abs_position()
        if "position_changed" in self.event_funcs: self.event_funcs["position_changed"]()

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, active):
        self._active = active
        self.render()
        if "state_changed" in self.event_funcs: self.event_funcs["state_changed"]()

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, visible):
        self._visible = visible
        self.render()
        if "visibility_changed" in self.event_funcs: self.event_funcs["visibility_changed"]()
