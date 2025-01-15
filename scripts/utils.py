import os

def find_directory(dir_name):
    """
    Locates the specified directory (e.g., 'data') by traversing upwards from the current working directory.
    """
    root_dir = os.getcwd()
    while root_dir != os.path.dirname(root_dir):  # Traverse up until the root directory
        if dir_name in os.listdir(root_dir):
            return os.path.join(root_dir, dir_name)
        root_dir = os.path.dirname(root_dir)
    raise ValueError(f"Could not find '{dir_name}' directory in the path hierarchy.")