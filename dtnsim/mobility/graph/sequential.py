#!/usr/bin/env3 python3
#
# A mobility class for visiting vertices sequentially.
# Copyright (c) 2011-2018, Hiroyuki Ohsaki.
# All rights reserved.
#
# $Id: sequential.py,v 1.2 2018/10/15 12:57:10 ohsaki Exp ohsaki $
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

from dtnsim.mobility.graph.crwp import CRWP

class Sequential(CRWP):
    def __init__(self, next_goal=2, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)
        self.next_goal = next_goal
        # reposition to vertex 1
        self.move_to_point(self.vertex_point(1))

    def pick_goal(self):
        """Select the next goal; visit vertices in the ascending order of
        their IDs."""
        edge, offset = self.vertex_point(self.next_goal)
        self.goal_edge = edge
        self.goal_offset = offset
        self.update_goal_cache()
        self.reverse_current_if_necessary()

        nvertices = len(self.path.graph.vertices())
        next_goal = self.next_goal + 1
        if next_goal > nvertices:
            next_goal = 1
        self.next_goal = next_goal
