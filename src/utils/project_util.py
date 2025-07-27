from pathlib import Path
import sys


def get_root_path():
    current_file = Path(__file__).resolve()
    root_dir = current_file.parent.parent.parent
    if str(root_dir) not in sys.path:
        sys.path.insert(0, str(root_dir))
    return root_dir
