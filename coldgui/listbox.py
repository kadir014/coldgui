import pygame
from . import errors
from . import draw
from . import CENTER

class ListBox:

    def __init__(self, parent, position=(0, 0), width=150, height=300, border_size=2, padding=0, row_size=4, style="win95", active=True, tag=None, visible=True):
        self.tag = tag

        self.parent = parent
        parent.add(self)

        self._position = position
        self._padding = padding
        self._width = width + border_size * 2 + self.padding * 2
        self._height = height + border_size * 2 + self.padding * 2
        self.row_size = row_size

        self.items = list()

        self.style = style

        # win95 style properties
        self.b1 = (255, 255, 255)
        self.b2 = (0, 0, 0)
        # win95 style properties

        self.body_color = self.parent.body_color
        self.border_size = border_size

        #Apply constants
        if CENTER in self._position: self._position = list(self._position)
        if self._position[0] == CENTER: self._position[0] = (self.parent.width - (self.parent.border_size * 2 + self.parent.padding * 2)) / 2 - self.width / 2
        if self._position[1] == CENTER: self._position[1] = (self.parent.height - (self.parent.border_size * 2 + self.parent.padding * 2)) / 2 - self.height / 2
        self._position = tuple(self._position)

        self._visible = visible
        self._active = active
        self.event_funcs = dict()

        self.surface = pygame.Surface((self._width, self._height))
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
            self.surface.fill(self.body_color)

            dashed_line = pygame.Surface((self.width, 3), pygame.SRCALPHA)
            draw.dashed_line(dashed_line, (0, 0, 0), (self.border_size, 0), (self.width - self.border_size*2, 0), 1, 1, True)

            y = self.border_size + self.padding
            for item in self.items:

                if item.body_color != self.body_color:
                    pygame.draw.rect(self.surface, item.body_color, (self.padding + self.border_size, y, self.width- (self.padding*2 + self.border_size*2), item.font.size(item.text)[1]+self.row_size))

                #Text aligning
                if item.text_align == "left":
                    ty = y + self.row_size / 2
                    tx = self.padding + self.border_size

                elif item.text_align == "top-left":
                    ty = y
                    tx = self.padding + self.border_size

                elif item.text_align == "bottom-left":
                    ty = y + self.row_size
                    tx = self.padding + self.border_size

                elif item.text_align == "center":
                    ty = y + self.row_size / 2
                    tx = (self.width - (self.border_size * 2 + self.padding * 2)) / 2 - item.font.size(item.text)[0] / 2

                elif item.text_align == "top":
                    ty = y
                    tx = (self.width - (self.border_size * 2 + self.padding * 2)) / 2 - item.font.size(item.text)[0] / 2

                elif item.text_align == "bottom":
                    ty = y + self.row_size
                    tx = (self.width - (self.border_size * 2 + self.padding * 2)) / 2 - item.font.size(item.text)[0] / 2

                elif item.text_align == "right":
                    ty = y + self.row_size / 2
                    tx = (self.width - (self.border_size * 2 + self.padding * 2)) - item.font.size(item.text)[0]

                elif item.text_align == "top-right":
                    ty = y
                    tx = (self.width - (self.border_size * 2 + self.padding * 2)) - item.font.size(item.text)[0]

                elif item.text_align == "bottom-right":
                    ty = y + self.row_size
                    tx = (self.width - (self.border_size * 2 + self.padding * 2)) - item.font.size(item.text)[0]

                else: raise errors.UnknownAlignError(f"{item.text_align} is not a valid text align format.")

                self.surface.blit(item.surface, (tx, ty))
                if y != self.border_size + self.padding: self.surface.blit(dashed_line, (0, y))

                y += item.font.size(item.text)[1] + self.row_size

            if self.style == "win95":
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

            if self.padding > 0:
                pygame.draw.rect(self.surface, self.body_color, (self.border_size / 2 + 1, self.border_size, self.padding + self.border_size/2 - 2, self.height - self.border_size*2), 0)
                pygame.draw.rect(self.surface, self.body_color, (self.width - (self.padding + self.border_size), self.border_size, self.padding + self.border_size/2 - 1, self.height - self.border_size*2), 0)
                pygame.draw.rect(self.surface, self.body_color, (self.border_size-1 + self.padding, self.height - (self.border_size + self.padding), self.width - (self.border_size*2 + self.padding*2), self.padding + self.border_size/2 - 1), 0)

            if not self.active: self.surface.set_alpha(64)

    def update(self):
        pass

    #Item operations
    def __getitem__(self, index):
        return self.items[index]

    def add(self, **kwargs):
        self.items.append(ListBoxItem(self, **kwargs))
        self.render()

    def remove(self, index):
        self.items.pop(index)
        self.render()

    def clear(self):
        self.items.clear()
        self.render()

    def replace(self, index1, index2):
        pass

    def insert(self):
        pass


    @property
    def length(self):
        return len(self.items)

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
    def padding(self):
        return self._padding

    @padding.setter
    def padding(self, padding):
        self._padding = padding
        self.render()
        if "padding_changed" in self.event_funcs: self.event_funcs["padding_changed"]()

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

class ListBoxItem:

    def __init__(self, parent, text="", text_align="left", font_size=16, sysfont="Calibri", font=None, font_fore_color=(0, 0, 0), body_color=None):
        if not isinstance(parent, ListBox):
            raise errors.OutOfListBox("An instance of class \"ListBoxItem\" can only be created in class \"ListBox\"")

        self.parent = parent

        self._text = text
        self.text_align = text_align

        self.font_size = font_size
        if font: self.font = pygame.font.Font(font, self.font_size)
        else: self.font = pygame.font.SysFont(sysfont, self.font_size)

        self.font_fore_color = font_fore_color
        if body_color: self.body_color = body_color
        else: self.body_color = self.parent.body_color

        self.surface = pygame.Surface(self.font.size(self.text))
        self.surface = self.surface.convert_alpha()

        self.render()

    def render(self):
        self.surface = self.font.render(self.text, True, self.font_fore_color, self.body_color)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self.render()
