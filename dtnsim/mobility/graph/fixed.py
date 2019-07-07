#!/usr/bin/env3 python3
#
# A mobility class for stationary agents on a graph.
# Copyright (c) 2013-2018, Hiroyuki Ohsaki.
# All rights reserved.
#
# $Id: fixed.py,v 1.2 2018/10/15 12:53:08 ohsaki Exp ohsaki $
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

from dtnsim.mobility.fixed import Fixed as _Fixed
from perlcompat import die

class Fixed(_Fixed):
    def __init__(self, path=None, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)
        if not path:
            die("Underlying path class must be specified.")
        if not path.graph:
            die("Path class doesn't return a valid graph via path.graph.")
        self.path = path
        self.current_edge = None
        self.current_offset = None
        self.wait = True
        # choose a random point on a graph
        self.move_to_point(*self.random_point())

    def vertex_coordinate(self, v):
        """Return the coordinate of the vertex V."""
        return self.path.graph.get_vertex_attribute(v, 'xy')

    def distance_between_vertices(self, u, v):
        """Return the Euclid distance between two vertices U and V."""
        return abs(self.vertex_coordinate(u) - self.vertex_coordinate(v))

    def edge_length(self, edge):
        """Return the legnth of edge EDGE."""
        return self.path.graph.get_edge_weight_by_id(*edge, 0)

    def random_offset(self, edge):
        """Randomly choose an offset between zero and the length of edge EDGE."""
        return random.uniform(0, self.edge_length(edge))

    def random_point(self):
        """Pick a random point, which is defined by the edge and the offset,
        on a graph."""
        # FIXME: must choose an edge with a probability proportional to
        # its length
        edge = self.path.graph.random_edge()
        return edge, self.random_offset(edge)

    def get_coordinate(self, edge, offset):
        """Return the coordinate of the point specified by EDGE and OFFSET."""
        pu = self.vertex_coordinate(edge[0])
        pv = self.vertex_coordinate(edge[1])
        length = self.edge_length(edge)
        if length == 0:
            return pu
        return pu + (pv - pu) * offset / length

    def move_to_point(self, edge, offset=0):
        """Directly jump to the point defined by (EDGE, OFFSET)."""
        self.current_edge = edge
        self.current_offset = offset
        self.update_current_cache()

    def vertex_point(self, v):
        """Return the pair (edge, offset) of the vertex V."""
        g = self.path.graph
        neighbors = sorted(g.neighbors(v))
        u = neighbors.pop(0)
        return [v, u], 0

    def move_to_vertex(self, v):
        """Directly jump to the vertex V."""
        self.move_to_point(self.vertex_point(v))

    def update_current_cache(self):
        """Compute and store the current coordinate for later use."""
        self.current = self.get_coordinate(self.current_edge,
                                           self.current_offset)

    def move(self, delta):
        """Move the agent for the duration of DELTA."""
        pass
