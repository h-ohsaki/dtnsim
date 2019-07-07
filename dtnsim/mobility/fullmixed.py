#!/usr/bin/env python3
#
# A mobility class for simulating FullMixed model.
# Copyright (c) 2016-2018, Hiroyuki Ohsaki.
# All rights reserved.
#
# Id: FullMixed.pm,v 1.5 2016/07/03 10:32:54 ohsaki Exp $
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

# NOTE: communication range must be set to a sufficiently small value

import random

from dtnsim.mobility.fixed import Fixed
from vector_2d import Vector as V

NODE_SEPERATION = 25
max_id = 0

class FullMixed(Fixed):
    def coordinate_for(self, n):
        """Return the coordinate of N-th agent.  Agents are placed such that
        any pair of agents are not reachable."""
        return V(n * NODE_SEPERATION, self.height / 2)

    def __init__(self, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)
        global max_id
        max_id += 1
        self.id_ = max_id
        self.rate = 1 / 1000  # encounter rate
        self.visit_list = []
        self.current = self.coordinate_for(self.id_)

    def move(self, delta):
        """Move the agent for the duration of DELTA."""
        # randomly choose other nodes to encouter
        for to_id in range(1, max_id + 1):
            if to_id >= self.id_:
                break
            if random.uniform(0, 1) <= self.rate / delta:
                self.visit_list.append(to_id)

        # visit other to-count agents sequentially
        if self.visit_list():
            to_id = self.visit_list.pop(0)
            self.current = self.coordinate_for(to_id)
        else:
            self.current = self.coordinate_for(self.id_)
