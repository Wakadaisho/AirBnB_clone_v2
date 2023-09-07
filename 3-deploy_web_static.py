#!/usr/bin/python3
"""Contains Fabric tasks to manage web servers and files"""

from fabric.api import *
import os
from datetime import datetime

env.hosts = [
    '100.26.165.122',
    '100.26.215.117'
]
env.user = 'ubuntu'


def do_pack():
    """Pack web_static folder"""
    if not os.path.isdir("versions"):
        os.makedirs("versions")

    version = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
    filename = f"versions/web_static_{version}.tgz"

    print("Packing web_static to", filename)
    local(f"tar -cvzf {filename} web_static")
    if os.path.isfile(filename):
        size = os.path.getsize(filename)
        print(f"web_static packed: {filename} -> {size}Bytes")
        return filename
    return False


def do_deploy(archive_path):
    """Copy web files over to remote servers

    Args:
        archive_path (str): location of files to send to remote

    Returns:
        True if successful, False otherwise
    """
    if os.path.isfile(archive_path) is False:
        return False

    archive = archive_path.split("/")[-1]
    basename = archive.partition(".")[0]

    try:
        put(archive_path, f"/tmp/{archive}")
        run(f"mkdir -p /data/web_static/releases/{basename}/")
        run(f"tar -xzf /tmp/{basename}.tgz "
            f"-C /data/web_static/releases/{basename}/")
        run(f"rm /tmp/{archive}")
        run(f"cp -r "
            f"/data/web_static/releases/{basename}/web_static/* "
            f"/data/web_static/releases/{basename}/")
        run(f"rm -rf /data/web_static/releases/{basename}/web_static")
        run(f"ln -sf /data/web_static/releases/{basename} "
            f"/data/web_static/current")
        print("New version deployed!")
    except Exception:
        return False

    return True


@runs_once
def deploy():
    """Create a new packed version of website and deploy to remote servers"""

    archive_path = execute(do_pack)

    archive_path = list(archive_path.values())[0]

    if archive_path is False:
        return False

    exit_code = execute(do_deploy, archive_path)
    exit_code = list(exit_code.values())[0]

    return exit_code
