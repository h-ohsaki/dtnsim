#!/usr/bin/env python3
#
# A simple implementation of vector class.
# Copyright (c) 2018-2019, Hiroyuki Ohsaki.
# All rights reserved.
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

import math

class Vector:
    def __init__(self, x=0, y=0):
        self.x = float(x)
        self.y = float(y)

    def __iter__(self):
        return iter([self.x, self.y])

    def __getitem__(self, pos):
        if pos == 0:
            return self.x
        elif pos == 1:
            return self.y
        else:
            raise IndexError

    def __len__(self):
        return 2

    def __repr__(self):
        name = type(self).__name__
        return f'{name}({self.x:.3f}, {self.y:.3f})'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return self.x == 0 and self.y == 0

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        else:
            return Vector(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)
