import os
import sys
if hasattr(sys, '_MEIPASS'):
    BASE_PATH = sys._MEIPASS
else:
    BASE_PATH= os.path.dirname(os.path.abspath(__file__))  # apunta a app/config/
    BASE_PATH = os.path.normpath(os.path.join(BASE_PATH, ".."))  # sube a app/