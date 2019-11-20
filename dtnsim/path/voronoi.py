#!/usr/bin/env3 python3
#
# A class for Voronoi path.
# Copyright (c) 2011-2019, Hiroyuki Ohsaki.
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

import graph_tools

from dtnsim.path.line import Line
from dtnsim.vector import Vector as V

class Voronoi(Line):
    def __init__(self, npoints=100, *args, **kwargs):
        self.npoints = npoints
        super().__init__(*args, **kwargs)

        # create a Voronoi topology
        g = graph_tools.Graph(directed=False)
        self.graph = g
        g.create_graph('voronoi', self.npoints, self.width, self.height)

        # save the positions of vertices as Vector object
        for v in g.vertices():
            x, y = g.get_vertex_attribute(v, 'pos').split(',')
            x, y = float(x), float(y)
            g.set_vertex_attribute(v, 'xy', V(x, y))

        self.compute_edge_lengths()
