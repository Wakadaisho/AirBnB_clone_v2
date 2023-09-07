#!/usr/bin/python3
"""Contains Fabric tasks to manage web servers and files"""

from fabric.api import *
import os
from datetime import datetime


def do_pack():
    """Pack web_static folder"""
    if not os.path.isdir("versions"):
        os.makedirs("versions")

    version = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
    filename = "versions/web_static_{}.tgz".format(version)

    print("Packing web_static to", filename)
    local("tar -cvzf {} web_static".format(filename))
    if os.path.isfile(filename):
        size = os.path.getsize(filename)
        print("web_static packed: {} -> {}Bytes".format(filename, size))
        return True
    return False
