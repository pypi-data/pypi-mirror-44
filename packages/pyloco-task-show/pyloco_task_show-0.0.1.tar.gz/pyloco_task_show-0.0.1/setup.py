# -*- coding: utf-8 -*-

"pyloco task setup script"

from setuptools import setup, find_packages

__taskname__ = "show"

setup(
    name="pyloco_task_"+__taskname__,
    version="0.0.1",
    packages=find_packages(),
    install_requires=['pyloco'],
    entry_points = {"pyloco_tasks": ["{name} = pyloco_task_{name}:entry_task".format(name=__taskname__)]},
)
