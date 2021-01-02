
import os


def createDirectory(path):

    if not os.path.exists(os.path.expandvars(path)):
        os.makedirs(os.path.expandvars(path))
