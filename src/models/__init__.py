import os

CUR_DIR = os.path.abspath(os.curdir)
MODULE_DIR = os.path.join(CUR_DIR, "models")

__all__ = [f.replace('.py', '') for f in os.listdir(MODULE_DIR) if
           os.path.isfile(os.path.join(MODULE_DIR, f)) and not f.startswith('__')]

