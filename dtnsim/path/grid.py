#!/usr/bin/env3 python3
#
# A class for Grid-style underlying path.
# Copyright (c) 2011-2018, Hiroyuki Ohsaki.
# All rights reserved.
#
# $Id: grid.py,v 1.2 2018/10/15 12:59:08 ohsaki Exp ohsaki $
#

import graphtools

from dtnsim.path.line import Line
from vector_2d import Vector as V

class Grid(Line):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # create a grid topology
        g = graphtools.Graph(directed=False)
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
