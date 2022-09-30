import os.path
from pathlib import Path

class Config:

    ROOT_DIR = Path(__file__).parent.parent
    SHARED_LIB_PATH = os.path.join(ROOT_DIR, "c/libsqlfunc.so")