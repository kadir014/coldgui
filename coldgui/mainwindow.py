import pygame
from . import errors
from .frame import Frame
from . import RUNTIME

im = errors.InstanceMemory()

class MainWindow():

    def __init__(self, size, title="coldGUI Window", icon=None, fps=60, body_color=(219, 215, 204)):

        if len(im.instances) == 1:
            raise errors.MultipleInstanceError(f"Pygame {pygame.version.ver} doesn't support multiple windows in one process.")

        im.instances.append(self)

        self.size = size
        self.title = title
        self.icon = icon
        self.fps = fps
        self.body_color = body_color

        pygame.init()
        self.surface = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)
        pygame.display.set_icon(pygame.Surface((0, 0)))
        if self.icon: pygame.display.set_icon(pygame.image.load(self.icon))
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(400, 50)

        self.frame = Frame(self, position=(0, 0), width=self.size[0], height=self.size[1], show_borders=False, tag="mainwindow-frame")
        self.position = self.frame.position
        self.width, self.height = self.frame.width, self.frame.height
        self.border_size, self.padding = self.frame.border_size, self.frame.padding

        self.running = False

    def update(self):
        self.clock.tick(self.fps)

        RUNTIME.events = pygame.event.get()

        for event in RUNTIME.events:
            if event.type == pygame.QUIT: self.running = False

        self.frame.update()

        self.surface.blit(self.frame.surface, self.frame.position)

        pygame.display.flip()

    def add(self, widget):
        if widget.tag != "mainwindow-frame":
            self.frame.add(widget)

    def start(self):
        self.running = True

        while self.running:
            self.update()

        pygame.quit()
