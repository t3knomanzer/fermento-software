import os


def file_exists(path):
    try:
        dirname, filename = path.rsplit("/", 1)
    except ValueError:
        dirname, filename = ".", path

    try:
        return filename in os.listdir(dirname)
    except OSError:
        return False
