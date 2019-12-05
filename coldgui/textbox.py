import pygame
from . import keys
from . import RUNTIME

class TextBox:
    def __init__(self, parent, width=0, height=0, position=(0, 0), placeholder="", multiline=False, sysfont="Calibri", font=None, font_size=10, line_gap=3, border_size=2, padding=0, style="win95", active=True, numeric_only=False, selectable=True, tag=None, visible=True):
        self.tag = tag

        self.parent = parent
        parent.add(self)

        self.font_size = font_size
        if font: self.font = pygame.font.Font(font, self.font_size)
        else: self.font = pygame.font.SysFont(sysfont, self.font_size)

        self.border_size = border_size

        if width == 0: self._width = (self.font.size("\u2588")[0] * 10) + self.border_size * 2 + padding * 2
        else: self._width = width# - self.border_size * 2 + padding * 2

        self.line_height = self.font.size("\u2588")[1]
        if height == 0: self._height = self.line_height + self.border_size * 2 + padding * 2
        else: self._height = height# - self.border_size * 2 + padding * 2

        self._position = position
        self._padding = padding
        #Placeholder text is applied only on single-line textboxes
        self.placeholder = placeholder
        self.line_gap = line_gap
        self.lines = ["",]
        self.tab_length = 4

        self.get_abs_position()

        self.scroll_x = 0
        self.scroll_y = 0
        self.cursor_x = 0
        self.cursor_y = 0

        self.style = style

        # win95 style properties
        self.b1 = (255, 255, 255)
        self.b2 = (0, 0, 0)
        # win95 style properties

        self.font_fore_color = (0, 0, 0)
        self.placeholder_fore_color = (100, 100, 100)
        self.body_color = (255, 255, 255)

        self.hover = False
        self.pressed = False

        self.numeric_only = numeric_only

        self.selectable = selectable
        self.selecting = False
        self.selected = False
        self.start_x = (0, 0)
        self.mmx = (0, 0)

        self._visible = visible
        self._active = active
        self.event_funcs = dict()
        self.surface = pygame.Surface((self._width, self._height))

        self.render(True)

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

    def render(self, placeholder=False, cursor=True):
        if self.visible:
            self.surface.set_alpha(255)
            self.surface.fill(self.body_color)

            if (self.selecting and len(self.lines[self.cursor_y]) > 0) or self.selected:
                if self.mmx != self.start_x:
                    mmx2 = self.font.size(self.lines[self.cursor_y][self.mmx[0]])[0]/2
                    stx2 = self.font.size(self.lines[self.cursor_y][self.start_x[0]])[0]/2
                    pygame.draw.rect(self.surface, (111, 164, 237), (self.mmx[1] - mmx2 - self.scroll_x, self.border_size + self.padding, (self.start_x[1] - stx2) - (self.mmx[1] - mmx2), self.height - (self.border_size + self.padding*2)))

            if placeholder:
                self.surface.blit(self.font.render(self.placeholder, True, self.placeholder_fore_color), (self.border_size + self.padding, self.border_size + self.padding))

            else:
                for i, line in enumerate(self.lines):
                    self.surface.blit(self.font.render(line, True, self.font_fore_color), (-self.scroll_x + self.border_size + self.padding, self.scroll_y + i * (self.line_height + self.line_gap) + self.border_size + self.padding))
                    if i * (self.line_height + self.line_gap) > self.width: break

                if cursor and not self.selecting: pygame.draw.line(self.surface, (50, 50, 50), (self.font.size(self.lines[self.cursor_y][0:self.cursor_x])[0] - self.scroll_x + self.border_size + self.padding, self.cursor_y * self.line_height + self.border_size + self.padding), (self.font.size(self.lines[self.cursor_y][0:self.cursor_x])[0] - self.scroll_x + self.border_size + self.padding, self.cursor_y * self.line_height + self.line_height + self.border_size + self.padding), 1)

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
                pygame.draw.rect(self.surface, self.body_color, (self.width - (self.padding + self.border_size), self.border_size, self.padding + self.border_size/2 + 1, self.height - self.border_size*2), 0)

            if not self.active: self.surface.set_alpha(64)

    def get_width_list(self):
        self.width_list = list()
        for chr in self.lines[self.cursor_y]:
            self.width_list.append(self.font.size(chr)[0])

        if len(self.width_list) > 0: self.width_list.append(self.width_list[len(self.width_list)-1])

    def get_mouse_x(self, rmx):
        if len(self.width_list) > 0:
            i = 0
            str = 0
            while i < len(self.width_list)- 1:
                str += self.width_list[i]

                i += 1

                if rmx < str: break

            return i-1, str

    def handle_select(self):
        #Get cursor x related to text
        if len(self.lines[self.cursor_y]) > 0:
            rmx = (pygame.mouse.get_pos()[0] + self.scroll_x - (self.position[0] + self.parent.position[0])) - self.border_size - self.padding
            self.get_width_list()
            self.mmx = self.get_mouse_x(rmx)
            if self.selecting: self.render()

    def update(self):
        if self.active and self.visible:
            mx, my = pygame.mouse.get_pos()

            if RUNTIME.keyboard_focus == self:
                self.handle_select()

            if pygame.Rect(self.position, (self.width, self.height)).collidepoint((mx - self.parent.position[0], my - self.parent.position[1])):
                self.hover = True
                #if self.selecting: self.render()
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

                            self.selected = False
                            self.selecting = True
                            self.handle_select()
                            self.start_x = self.mmx

                            self.render()

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.pressed:
                            if "released" in self.event_funcs: self.event_funcs["released"]()
                            if "clicked" in self.event_funcs and self.hover: self.event_funcs["clicked"]()
                            RUNTIME.focus = None
                        if RUNTIME.keyboard_focus == self:
                            self.selecting = False
                            if self.mmx != self.start_x: self.selected = True
                            self.cursor_x = self.mmx[0]
                        self.pressed = False
                        self.hover = False
                        if RUNTIME.keyboard_focus == self: self.render()

                if event.type == pygame.KEYDOWN and RUNTIME.keyboard_focus == self:
                    if "key_pressed" in self.event_funcs: self.event_funcs["key_pressed"](keys.inv_key_dictionary[event.key])

                    if not self.selecting:
                        self.selected = False

                        if event.key in keys.specials:

                            if event.key == pygame.K_LEFT:
                                self.cursor_x -= 1
                                if self.cursor_x < 0: self.cursor_x = 0
                                if self.font.size(self.lines[self.cursor_y][0:self.cursor_x])[0] < self.scroll_x:
                                    self.scroll_x -= self.scroll_x - self.font.size(self.lines[self.cursor_y][0:self.cursor_x])[0]

                                self.render()

                            elif event.key == pygame.K_RIGHT:
                                self.cursor_x += 1
                                if self.cursor_x > len(self.lines[self.cursor_y]): self.cursor_x = len(self.lines[self.cursor_y])
                                if self.font.size(self.lines[self.cursor_y][0:self.cursor_x])[0] - self.scroll_x > (self.width - (self.border_size*2 + self.padding*2)):
                                    self.scroll_x += (self.font.size(self.lines[self.cursor_y][0:self.cursor_x])[0] - self.scroll_x) - (self.width - (self.border_size*2 + self.padding*2))

                                self.render()

                            elif event.key == pygame.K_BACKSPACE:
                                if len(self.lines[self.cursor_y]) > 0 and self.cursor_x != 0:
                                    s = list(self.lines[self.cursor_y])
                                    s.pop(self.cursor_x - 1)
                                    self.lines[self.cursor_y] = "".join(s)

                                    self.cursor_x -= 1
                                    if self.cursor_x < 0: self.cursor_x = 0
                                    if self.font.size(self.lines[self.cursor_y][0:self.cursor_x])[0] < self.scroll_x:
                                        self.scroll_x -= self.scroll_x - self.font.size(self.lines[self.cursor_y][0:self.cursor_x])[0]

                                    self.render()

                            elif event.key == pygame.K_TAB:
                                s = list(self.lines[self.cursor_y])
                                for i in range(self.tab_length): s.insert(self.cursor_x, " ")
                                self.lines[self.cursor_y] = "".join(s)
                                self.cursor_x += self.tab_length

                                if self.font.size(self.lines[self.cursor_y][0:self.cursor_x])[0] - self.scroll_x > (self.width - (self.border_size*2 + self.padding*2)):
                                    self.scroll_x += (self.font.size(self.lines[self.cursor_y][0:self.cursor_x])[0] - self.scroll_x) - (self.width - (self.border_size*2 + self.padding*2))

                                self.render()

                        else:
                            if self.numeric_only and not event.key in keys.numbers: return
                            l = list(self.lines[self.cursor_y])
                            l.insert(self.cursor_x, chr(event.key))
                            self.lines[self.cursor_y] = "".join(l)
                            self.cursor_x += 1

                            if self.cursor_x == len(self.lines[self.cursor_y]) and self.font.size(self.lines[self.cursor_y])[0] - self.scroll_x > (self.width - (self.border_size*2 + self.padding*2)):
                                self.scroll_x += (self.font.size(self.lines[self.cursor_y])[0] - self.scroll_x) - (self.width - (self.border_size*2 + self.padding*2))
                            elif self.font.size(self.lines[self.cursor_y][0:self.cursor_x])[0] - self.scroll_x > (self.width - (self.border_size*2 + self.padding*2)):
                                self.scroll_x += (self.font.size(self.lines[self.cursor_y][0:self.cursor_x])[0] - self.scroll_x) - (self.width - (self.border_size*2 + self.padding*2))

                            self.render()

    def deactive(self):
        self.selected = False
        if len(self.lines) == 1 and len(self.lines[self.cursor_y]) == 0: self.render(placeholder=True)
        else: self.render(cursor=False)


    @property
    def text(self):
        return self.lines[self.cursor_y]

    @text.setter
    def text(self, text):
        self.lines[self.cursor_y] = text
        self.cursor_x = len(text)
        self.selected = False
        if RUNTIME.keyboard_focus != self and len(self.lines[self.cursor_y]) == 0 and len(self.lines) == 1: self.render(True)
        else: self.render(cursor=RUNTIME.keyboard_focus == self)
        if "text_changed" in self.event_funcs: self.event_funcs["text_changed"]()

    @property
    def padding(self):
        return self._padding

    @padding.setter
    def padding(self, padding):
        self._padding = padding
        if RUNTIME.keyboard_focus != self and len(self.lines[self.cursor_y]) == 0 and len(self.lines) == 1: self.render(True)
        else: self.render(cursor=RUNTIME.keyboard_focus == self)
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
        if RUNTIME.keyboard_focus != self and len(self.lines[self.cursor_y]) == 0 and len(self.lines) == 1: self.render(True)
        else: self.render(cursor=RUNTIME.keyboard_focus == self)
        if "width_changed" in self.event_funcs: self.event_funcs["width_changed"]()
        if "size_changed" in self.event_funcs: self.event_funcs["size_changed"]()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height
        if RUNTIME.keyboard_focus != self and len(self.lines[self.cursor_y]) == 0 and len(self.lines) == 1: self.render(True)
        else: self.render(cursor=RUNTIME.keyboard_focus == self)
        if "height_changed" in self.event_funcs: self.event_funcs["height_changed"]()
        if "size_changed" in self.event_funcs: self.event_funcs["size_changed"]()

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, active):
        self._active = active
        self.selected = False
        if RUNTIME.keyboard_focus != self and len(self.lines[self.cursor_y]) == 0 and len(self.lines) == 1: self.render(True)
        else: self.render(cursor=RUNTIME.keyboard_focus == self)
        if "state_changed" in self.event_funcs: self.event_funcs["state_changed"]()

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, visible):
        self._visible = visible
        self.render()
        if "visibility_changed" in self.event_funcs: self.event_funcs["visibility_changed"]()
