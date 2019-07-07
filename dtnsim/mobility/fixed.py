#!/usr/bin/env python3
#
# A mobility class for stationary agents.
# Copyright (c) 2013-2018, Hiroyuki Ohsaki.
# All rights reserved.
#
# Id: Fixed.pm,v 1.13 2015/12/30 02:54:47 ohsaki Exp $
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

import math, random
from vector_2d import Vector as V

class Fixed:
    def __init__(self, width=1000, height=1000, current=None, *kargs,
                 **kwargs):
        self.width = width
        self.height = height
        if current is None:
            current = self.random_coordinate()
        self.current = current
        self.wait = True

    def __repr__(self):
        name = self.__class__.__name__
        return '{}(width={!r}, height={!r}, current={!r}, wait={!r})'.format(
            name, self.width, self.height, self.current, self.wait)

    def random_coordinate(self):
        """Pick a random coordinate on the field."""
        return V(random.uniform(0, self.width), random.uniform(0, self.height))

    def angle_between_vectors(self, v1, v2):
        """Return the angle between two vectors V1 and V2."""
        if abs(v1) == 0 or abs(v2) == 0:
            return math.pi / 2
        try:
            return math.acos((v1 * v2) / (abs(v1) * abs(v2)))
        except ValueError:
            return math.pi / 2  # ???

    def move(self, delta):
        """Move the agent for the duration of DELTA."""
        pass
