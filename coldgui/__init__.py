version = "0.0.0"
version_tuple = (0, 0, 0)
state = "Alpha"
author = "Kadir Aksoy"
license = "GNU Lesser General Public License v3.0"

from .errors import MultipleInstanceError, InstanceMemory

im = InstanceMemory()

class RuntimeGlobalObject:
    def __init__(self):
        if len(im.instances) == 1:
            raise MultipleInstanceError(f"Just one RuntimeGlobalObject can be created in one process.")

        im.instances.append(self)

        self.focus = None
        self.keyboard_focus = None

RUNTIME = RuntimeGlobalObject()

from .mainwindow import MainWindow
from .frame import Frame
from .label import Label
from .button import Button
from .textbox import TextBox

import os
import pygame.version

if os.name == "nt": os.system("cls") #Windows
else: os.system("clear") #MacOS and Linux

print(f"You are using GUI Project {version} powered by Pygame {pygame.version.ver}")

del os
del pygame.version
