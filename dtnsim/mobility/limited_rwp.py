#!/usr/bin/env python3
#
# A mobility class for RWP (Random WayPoint) mobility model on limited area.
# Copyright (c) 2011-2018, Hiroyuki Ohsaki.
# All rights reserved.
#
# Id: LimitedRandomWaypoint.pm,v 1.8 2015/12/09 14:45:23 ohsaki Exp $
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

import random

from dtnsim.mobility.rwp import RandomWaypoint
from vector_2d import Vector as V

class LimitedRandomWaypoint(RandomWaypoint):
    def __init__(self, xmin=0, ymin=0, xmax=1000, ymax=1000, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

    def random_coordinate(self):
        """Pick a random coordinate on the field."""
        x = random.uniform(self.xmin, self.xmax)
        y = random.uniform(self.ymin, self.ymax)
        return V(x, y)
