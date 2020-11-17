import os
import shutil

from projectstarter.utils import logger


def mkdir(path, ignore_errors=False):
    """
    Create a directory if folder does not exist. It creates every folder in
    the given path.
    :param ignore_errors: If True, do not throw error when folder already exists
    :returns: True on success, False on error
    """
    if not ignore_errors and os.path.exists(path):
        logger.warning(f"Folder '{path}' already exists.")
        return False

    try:
        os.makedirs(path)
    except IOError as e:
        if not ignore_errors:
            logger.error(e)
        return ignore_errors

    return True


def all_in(folder):
    """
    Generator that yields every file in a folder and its sub-folders.
    """
    for (folder_path, folders, filenames) in os.walk(folder):
        for file in filenames:
            yield os.path.join(folder_path, file)
        for folder in folders:
            yield from all_in(folder)


def rm(path):
    """
    Remove the given path. The path can be either a directory or a regular file.
    """
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)
        return

    if os.path.isfile(path):
        os.remove(path)
        return

    logger.warning(f"not removing '{path}' as it is not a folder or file")
