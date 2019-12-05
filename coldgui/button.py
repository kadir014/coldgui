import pygame
from . import errors
from . import RUNTIME

class Button:

    def __init__(self, parent, width=0, height=0, position=(0, 0), text="", text_align="center", border_size=2, sysfont="Calibri", font=None, font_size=10, style="win95", padding=0, active=True, tag=None, visible=True):
        self.tag = tag

        self.parent = parent
        parent.add(self)

        self._position = position
        self._text = text
        self._text_align = text_align
        self._padding = padding

        self.get_abs_position()

        self.font_size = font_size
        if font: self.font = pygame.font.Font(font, self.font_size)
        else: self.font = pygame.font.SysFont(sysfont, self.font_size)

        self._width = width
        self._height = height
        if self._width == 0: self._width = self.font.size(self._text)[0] + border_size * 4 + 10 + self.padding
        if self._height == 0: self._height = self.font.size(self._text)[1] + border_size * 2 + 10 + self.padding

        self.style = style

        # win95 style properties
        self.b1 = (255, 255, 255)
        self.b2 = (0, 0, 0)
        # win95 style properties

        self.font_fore_color = (0, 0, 0)
        self.body_color = self.parent.body_color
        self.border_size = border_size

        self.hover = False
        self.pressed = False

        self._visible = visible
        self._active = active
        self.event_funcs = dict()
        self.surface = pygame.Surface((self.width, self.height))

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
            self.surface.fill(self.body_color)

            if self.text_align == "center":
                self.surface.blit(self.font.render(self.text, True, self.font_fore_color), (self.width / 2 - self.font.size(self.text)[0] / 2, self.height / 2 - self.font.size(self.text)[1] / 2))

            elif self.text_align == "right":
                self.surface.blit(self.font.render(self.text, True, self.font_fore_color), (self.width - self.border_size - self.font.size(self.text)[0] - self.padding, self.height / 2 - self.font.size(self.text)[1] / 2))

            elif self.text_align == "top-right":
                self.surface.blit(self.font.render(self.text, True, self.font_fore_color), (self.width - self.border_size - self.font.size(self.text)[0] - self.padding, self.border_size + self.padding))

            elif self.text_align == "top":
                self.surface.blit(self.font.render(self.text, True, self.font_fore_color), (self.width / 2 - self.font.size(self.text)[0] / 2, self.border_size + self.padding))

            elif self.text_align == "top-left":
                self.surface.blit(self.font.render(self.text, True, self.font_fore_color), (self.border_size + self.padding, self.border_size + self.padding))

            elif self.text_align == "left":
                self.surface.blit(self.font.render(self.text, True, self.font_fore_color), (self.border_size + self.padding, self.height / 2 - self.font.size(self.text)[1] / 2))

            elif self.text_align == "bottom-left":
                self.surface.blit(self.font.render(self.text, True, self.font_fore_color), (self.border_size + self.padding, self.height - self.font.size(self.text)[1] - self.padding))

            elif self.text_align == "bottom":
                self.surface.blit(self.font.render(self.text, True, self.font_fore_color), (self.width / 2 - self.font.size(self.text)[0] / 2, self.height - self.font.size(self.text)[1] - self.padding))

            elif self.text_align == "bottom-right":
                self.surface.blit(self.font.render(self.text, True, self.font_fore_color), (self.width - self.border_size - self.font.size(self.text)[0] - self.padding, self.height - self.font.size(self.text)[1] - self.padding))

            else: raise errors.UnknownAlignError(f"{self.text_align} is not a valid text align format.")

            if self.style == "win95":
                if self.border_size % 2 == 0:
                    pygame.draw.rect(self.surface, self.b1, (0, 0, self.width - 1, self.height - 1), self.border_size)
                    pygame.draw.line(self.surface, self.b2, (self.border_size / 2 + 1, self.height - 2), (self.border_size + self.width, self.height - 2), self.border_size)
                    pygame.draw.line(self.surface, self.b2, (self.width - 2, 0), (self.width - 2, self.border_size + self.height + self.border_size), self.border_size)

                else:
                    pygame.draw.rect(self.surface, self.b1, (0, 0, self.width, self.height), self.border_size)
                    pygame.draw.line(self.surface, self.b2, (self.border_size / 2 + 1, self.height - 1), (self.border_size + self.width, self.height - 1), self.border_size)
                    pygame.draw.line(self.surface, self.b2, (self.width - 2, 0), (self.width - 2, self.border_size + self.height + self.border_size), self.border_size)

                #Corners
                pygame.draw.polygon(self.surface, self.b2, ((0, self.height), (self.border_size/2, self.height), (self.border_size/2, self.height - self.border_size/2)))
                pygame.draw.polygon(self.surface, self.b1, ((self.width, 0), (self.width - self.border_size/2 - 1, 0), (self.width - self.border_size/2 - 1, self.border_size/2)))

            if not self.active: self.surface.set_alpha(64)

    def update(self):
        if self.active and self.visible:
            if pygame.Rect(self.abs_position, (self.width, self.height)).collidepoint((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])): self.hover = True
            else: self.hover = False

            for event in RUNTIME.events:

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.hover:
                            if "pressed" in self.event_funcs: self.event_funcs["pressed"]()
                            self.pressed = True
                            if RUNTIME.keyboard_focus: RUNTIME.keyboard_focus.deactive()
                            RUNTIME.focus = self
                            RUNTIME.keyboard_focus = self
                            self.b1 = (0, 0, 0)
                            self.b2 = (255, 255, 255)
                            self.render()

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.pressed:
                            if "released" in self.event_funcs: self.event_funcs["released"]()
                            if "clicked" in self.event_funcs and self.hover: self.event_funcs["clicked"]()
                            RUNTIME.focus = None
                            self.b1 = (255, 255, 255)
                            self.b2 = (0, 0, 0)
                            self.render()
                        self.pressed = False
                        self.hover = False

    def deactive(self):
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
    def text_align(self):
        return self._text_align

    @text_align.setter
    def text_align(self, text_align):
        self._text_align = text_align
        self.render()
        if "text_align_changed" in self.event_funcs: self.event_funcs["text_align_changed"]()

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
