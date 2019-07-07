#!/usr/bin/env python3
#
# A mobility class for RandomWalk on a graph.
# Copyright (c) 2011-2018, Hiroyuki Ohsaki.
# All rights reserved.
#
# $Id: randomwalk.py,v 1.2 2018/10/15 12:54:39 ohsaki Exp ohsaki $
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

# NOTE: this program implements per-node random walk, rather than
# random walk on an edge.  An agent never goes back the currently
# walking edge.

import random

from dtnsim.mobility.graph.fixed import Fixed

class RandomWalk(Fixed):
    def __init__(self, vel_func=None, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)
        if vel_func is None:
            vel_func = lambda: 1.0  # 1.0 [m/s] by default
        self.velocity = None
        self.vel_func = vel_func

    def update_velocity(self):
        """Update agent's velocity."""
        self.velocity = self.vel_func()
        self.wait = False

    def select_route(self):
        """Randomly choose the next edge to go; this program assumes that the
        agent is currenly on the end of the edge."""
        edge = self.current_edge
        current_vertex = edge[1]
        neighbors = self.path.graph.neighbors(edge[1])
        next_vertex = random.choice(neighbors)
        self.move_to_point([current_vertex, next_vertex], 0)

    def move(self, delta):
        """Move the agent for the duration of DELTA."""
        self.update_velocity()

        # advance the agent by SPEED * DELTA
        step = self.velocity * delta
        self.current_offset += step
        self.update_current_cache()

        # if very close to either of corners, choose the next route
        length = self.edge_length(self.current_edge)
        if abs(self.current_offset -
               length) < step or self.current_offset > length:
            self.select_route()
