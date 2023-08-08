import sys

def is_venv():
    return sys.prefix != sys.base_prefix

print(is_venv())
