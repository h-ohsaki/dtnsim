#!/usr/bin/env3 python3
#
# A class for Grid-style underlying path.
# Copyright (c) 2011-2018, Hiroyuki Ohsaki.
# All rights reserved.
#
# $Id: grid.py,v 1.2 2018/10/15 12:59:08 ohsaki Exp ohsaki $
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

from dtnsim.path.line import Line
from vector_2d import Vector as V

class Grid(Line):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # create a grid topology
        g = graph_tools.Graph(directed=False)
        self.graph = g
        g.create_graph('lattice', 2, self.size)

        # save the positions of vertices as Vector object
        for j in range(1, self.size + 1):
            for i in range(1, self.size + 1):
                v = g._lattice_vertex(2, self.size, i, j)
                x, y = ((0.5 + i - 1) / self.size * self.width,
                        (0.5 + j - 1) / self.size * self.height)
                g.set_vertex_attribute(v, 'xy', V(x, y))
        self.compute_edge_lengths()
