from gamephase import GamePhase

__all__ = ["levels", "entities", "GamePhase"]

import ctypes
import os

if os.name == "nt":
    ctypes.windll.user32.SetProcessDPIAware()
