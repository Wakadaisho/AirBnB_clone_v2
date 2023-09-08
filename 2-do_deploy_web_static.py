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

    def executeBoth(cmd):
        run(cmd)
        local(cmd)

    try:
        put(archive_path, f"/tmp/{archive}")
        local(f"cp {archive_path} /tmp/")
        executeBoth(f"mkdir -p /data/web_static/releases/{basename}/")
        executeBoth(f"tar -xzf /tmp/{archive} "
                    f"-C /data/web_static/releases/{basename}/")
        executeBoth(f"rm /tmp/{archive}")
        executeBoth(f"cp -r "
                    f"/data/web_static/releases/{basename}/web_static/* "
                    f"/data/web_static/releases/{basename}/")
        executeBoth(f"rm -rf /data/web_static/releases/{basename}/web_static")
        executeBoth(f"rm -rf /data/web_static/current")
        executeBoth(f"ln -sf /data/web_static/releases/{basename}/ "
                    f"/data/web_static/current")
        print("New version deployed!")
    except Exception:
        return False

    return True
