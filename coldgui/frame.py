import pygame
from . import errors
from . import RUNTIME

class Frame:
    def __init__(self, parent, width=60, height=100, position=(0, 0), show_borders=True, border_size=2, style="win95", padding=0, active=True, tag=None, visible=True):
        self.tag = tag

        self.widgets = list()
        self.parent = parent
        self.parent.add(self)

        self._position = position
        self._width = width
        self._height = height
        self._padding = padding

        self.get_abs_position()

        self.style = style

        # win95 style properties
        self.b1 = (255, 255, 255)
        self.b2 = (0, 0, 0)
        # win95 style properties

        self.body_color = self.parent.body_color
        self.border_size = border_size
        self.show_borders = show_borders

        self._visible = visible
        self._active = active
        self.event_funcs = dict()
        self.surface = pygame.Surface((self.width, self.height))

        self.render()

    def event(self):
        self.event_funcs[func.__name__] = func

    def get_abs_position(self):
        #Absolute position relative to the Pygame display screen
        try:
            self.abs_position = tuple(map(sum, zip(self.parent.abs_position, self.position)))
        except Exception as e:
            if isinstance(e, AttributeError):
                self.abs_position = self._position
            else: raise e

    def render(self, from_update=False):
        if self.visible:
            self.surface.set_alpha(255)
            self.surface.fill(self.body_color)
            if not from_update:
                for widget in self.widgets:
                    if widget.visible:
                        self.surface.blit(widget.surface, (widget.position[0] + self.padding, widget.position[1] + self.padding))

            if self.style == "win95" and self.show_borders:
                if self.border_size % 2 == 0:
                    pygame.draw.rect(self.surface, (self.b2), (0, 0, self.width - 1, self.height - 1), self.border_size)
                    pygame.draw.line(self.surface, (self.b1), (self.border_size / 2 + 1, self.height - 2), (self.border_size + self.width, self.height - 2), self.border_size)
                    pygame.draw.line(self.surface, (self.b1), (self.width - 2, 0), (self.width - 2, self.height), self.border_size)

                else:
                    pygame.draw.rect(self.surface, (self.b2), (0, 0, self.width, self.height), self.border_size)
                    pygame.draw.line(self.surface, (self.b1), (self.border_size / 2 + 1, self.height - 1), (self.border_size + self.width, self.height - 1), self.border_size)
                    pygame.draw.line(self.surface, (self.b1), (self.width - 2, 0), (self.width - 2, self.height), self.border_size)

                #Corners
                pygame.draw.polygon(self.surface, (self.b1), ((0, self.height), (self.border_size/2, self.height), (self.border_size/2, self.height - self.border_size/2)))
                pygame.draw.polygon(self.surface, (self.b2), ((self.width, 0), (self.width - self.border_size/2 - 1, 0), (self.width - self.border_size/2 - 1, self.border_size/2)))

            if not self.active: self.surface.set_alpha(64)

    def update(self):
        if self.active and self.visible:
            self.render(True)

            for event in RUNTIME.events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(self.position, (self.width, self.height)).collidepoint((pygame.mouse.get_pos()[0] - self.parent.position[0], pygame.mouse.get_pos()[1] - self.parent.position[1])):
                        RUNTIME.focus = None
                        if RUNTIME.keyboard_focus: RUNTIME.keyboard_focus.deactive()
                        RUNTIME.keyboard_focus = None

            for widget in self.widgets:
                widget.update()
                #Widgets are blitted again in two different methods due optimization
                if widget.visible:
                    self.surface.blit(widget.surface, (widget.position[0] + self.padding, widget.position[1] + self.padding))

    def add(self, widget):
        if widget != self:
            self.widgets.append(widget)

    def deactive(self):
        pass


    @property
    def padding(self):
        return self._padding

    @padding.setter
    def padding(self, padding):
        self._padding = padding
        self.render()
        if "padding_changed" in self.event_funcs: self.event_funcs["padding_changed"]()

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
        self._position[0] = x
        self.get_abs_position()
        if "position_changed" in self.event_funcs: self.event_funcs["position_changed"]()

    @property
    def y(self):
        return self._position[1]

    @y.setter
    def y(self, y):
        self._position[1] = y
        self.get_abs_position()
        if "position_changed" in self.event_funcs: self.event_funcs["position_changed"]()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width
        self.render()
        if "width_changed" in self.event_funcs: self.event_funcs["width_changed"]()
        if "size_changed" in self.event_funcs: self.event_funcs["size_changed"]()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height
        self.render()
        if "height_changed" in self.event_funcs: self.event_funcs["height_changed"]()
        if "size_changed" in self.event_funcs: self.event_funcs["size_changed"]()

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
