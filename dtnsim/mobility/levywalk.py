#!/usr/bin/env python3
#
# A mobility class for Levy walk.
# Copyright (c) 2011-2015, Hiroyuki Ohsaki.
# All rights reserved.
#
# Id: LevyWalk.pm,v 1.11 2015/12/09 14:45:23 ohsaki Exp $
#

import random
import math

from dtnsim.mobility.rwp import RandomWaypoint
from vector_2d import Vector as V

def pareto(scale, shape):
    """Generate a random variable following the Pareto distribution with
    parameters SCALE and SHAPE.  Note that the mean of the Pareto distribution
    is given by SHAPE * SCALE / (SHAPE - 1)."""
    return scale / random.uniform(0, 1 / shape)

class LevyWalk(RandomWaypoint):
    def __init__(self, scale=100, shape=1.5, *kargs, **kwargs):
        # NOTE: must be assigned before calling __init__
        self.scale = scale
        self.shape = shape
        super().__init__(*kargs, **kwargs)

    def goal_coordinate(self):
        """Randomly choose the goal in the field so that the distance from the
        current coordinate follows Pareto distribution."""
        length = pareto(self.scale, self.shape)
        theta = random.uniform(0, 2 * math.pi)
        goal = self.current + length * V(math.cos(theta), math.sin(theta))
        # FIXME: the goal coordinate is simply limited by the field boundaries.
        # A node should *bounce back* with the boundaries.
        x = max(0, min(goal[0], self.width))
        y = max(0, min(goal[1], self.height))
        return V(x, y)
