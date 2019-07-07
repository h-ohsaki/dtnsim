#!/usr/bin/env3 python3
#
# A class for dummy underlying path.
# Copyright (c) 2011-2018, Hiroyuki Ohsaki.
# All rights reserved.
#
# $Id: none.py,v 1.2 2018/10/15 13:01:19 ohsaki Exp $
#

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

class NONE:
    def __init__(self, width=1000, height=1000, *args, **kwargs):
        self.width = width
        self.height = height
        self.graph = None
