import os
import shutil

from utils import logger


def mkdir(path, ignore_errors=False):
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
    for (folder_path, folders, filenames) in os.walk(folder):
        for file in filenames:
            yield os.path.join(folder_path, file)
        for folder in folders:
            yield from all_in(folder)


def rm(path):
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)
        return

    if os.path.isfile(path):
        os.remove(path)
        return

    logger.warning(f"not removing '{path}' as it is not a folder or file")
