# -*- coding: utf-8 -*-
"""
Get TexLive installation metadata from Python.
Wrap and parse tlmgr output.

Documentation at: https://github.com/YtoTech/python-texlivemetadata

Copyright (c) 2019 Yoan Tournade <yoan@ytotech.com>
Released under MIT License. See LICENSE file.
"""
from .packages import (
    list_packages,
    list_installed_packages,
    get_package_info,
    get_ctan_link,
)
