#!/usr/bin/env python
# This source file is part of Yoda.
#
# Yoda is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Yoda is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Yoda. If not, see <http://www.gnu.org/licenses/gpl-3.0.html>.

import pkg_resources

from pycolorizer import Color
from yoda import Output


def get_version():
    """Get version from package resources."""
    requirement = pkg_resources.Requirement.parse("yoda")
    provider = pkg_resources.get_provider(requirement)
    return provider.version


def custom_version_output():
    """Print customized version for --version option."""
    out = Output()
    color = Color()
    out.info("""
 ::\`--._,'.::.`._.--'/:: Multiple
 ::::.  ` __::__ '  .::::   repositories
 ::::::-:.`'..`'.:-::::::          manager
 ::::::::\ `--' /::::::::
""")
    return "Yoda %s" % color.colored(get_version(), "blue")
