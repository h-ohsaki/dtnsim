#!/usr/bin/env python3
#
# A mobility class for stationary agents.
# Copyright (c) 2013-2018, Hiroyuki Ohsaki.
# All rights reserved.
#
# Id: Fixed.pm,v 1.13 2015/12/30 02:54:47 ohsaki Exp $
#

import math, random
from vector_2d import Vector as V

class Fixed:
    def __init__(self, width=1000, height=1000, current=None, *kargs,
                 **kwargs):
        self.width = width
        self.height = height
        if current is None:
            current = self.random_coordinate()
        self.current = current
        self.wait = True

    def __repr__(self):
        name = self.__class__.__name__
        return f'{name}(width={self.width!r}, height={self.height!r}, current={self.current!r}, wait={self.wait!r})'

    def random_coordinate(self):
        """Pick a random coordinate on the field."""
        return V(random.uniform(0, self.width), random.uniform(0, self.height))

    def angle_between_vectors(self, v1, v2):
        """Return the angle between two vectors V1 and V2."""
        if abs(v1) == 0 or abs(v2) == 0:
            return math.pi / 2
        try:
            return math.acos((v1 * v2) / (abs(v1) * abs(v2)))
        except ValueError:
            return math.pi / 2  # ???

    def move(self, delta):
        """Move the agent for the duration of DELTA."""
        pass
