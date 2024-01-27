__all__ = ["levels", "entities"]

import ctypes
import logging
import os

if os.name == 'nt':
    ctypes.windll.user32.SetProcessDPIAware()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
