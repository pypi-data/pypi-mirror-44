# -*- coding: UTF-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
"""
An utility package
"""

__author__ = "the01"
__email__ = "jungflor@gmail.com"
__copyright__ = "Copyright (C) 2013-19, Florian JUNG"
__license__ = "MIT"
__version__ = "0.5.1"
__date__ = "2019-04-14"

import logging

from .loadable import Loadable, load_file, save_file, \
    load_json_file, save_json_file, load_yaml_file, save_yaml_file
from .logable import Logable, ModuleLogable, get_logger
from .runable import StartStopable, Startable, Stopable, StartException
from .convenience import FromToDictBase, PrintableBase


logger = logging.getLogger(__name__)
__all__ = [
    "logable", "Logable", "ModuleLogable", "get_logger",
    "loadable", "Loadable", "load_file", "save_file",
    "load_json_file", "save_json_file", "load_yaml_file", "save_yaml_file",
    "runable", "Startable", "StartException", "Stopable", "StartStopable",
    "convenience", "FromToDictBase", "PrintableBase"
]
