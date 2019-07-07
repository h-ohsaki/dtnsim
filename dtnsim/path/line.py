#!/usr/bin/env3 python3
#
# A class for straight underlying path.
# Copyright (c) 2011-2018, Hiroyuki Ohsaki.
# All rights reserved.
#
# $Id: line.py,v 1.2 2018/10/15 13:00:47 ohsaki Exp ohsaki $
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

import graph_tools

from dtnsim.path.none import NONE
from vector_2d import Vector as V

class Line(NONE):
    def __init__(self, size=5, *args, **kwargs):
        self.size = size
        super().__init__(*args, **kwargs)

        # create a linear topology
        g = graph_tools.Graph(directed=False)
        self.graph = g
        g.create_graph('lattice', 1, self.size)

        # save the positions of vertices as Vector object
        for v in range(1, self.size + 1):
            x, y = ((v - 0.5) / self.size * self.width, 0.5 * self.height)
            g.set_vertex_attribute(v, 'xy', V(x, y))

        self.compute_edge_lengths()

    def compute_edge_lengths(self):
        """Pre-compute the lengths of all edges."""
        g = self.graph
        for u, v in g.unique_edges():
            length = abs(
                g.get_vertex_attribute(u, 'xy') -
                g.get_vertex_attribute(v, 'xy'))
            g.set_edge_weight_by_id(u, v, 0, length)
            g.set_edge_weight_by_id(v, u, 0, length)
