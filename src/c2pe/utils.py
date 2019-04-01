import os


def load_file(path: str) -> str:
    """
    Will load file and extract all characters as strings, given relative or absolute path
    :param path:
    :return str:
    """
    # if path begins with ~, will expand path
    path = os.path.expanduser(path)
    data = None
    with open(path, 'r') as f:
        data = f.read()
    return data
