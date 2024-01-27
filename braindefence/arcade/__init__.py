__all__ = ["levels", "entities"]

import ctypes
import os

if os.name == 'nt':
    ctypes.windll.user32.SetProcessDPIAware()