"""
utils.py

This is the helper function holding multiple reusable scripts. I found that my .ipynb contained many
repeated codes and became messy. 

"""
from pathlib import Path

def ensure_directory(path):
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p
