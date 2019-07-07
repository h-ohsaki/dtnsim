#!/usr/bin/env python3
#
# A mobility class for random walk.
# Copyright (c) 2011-2013, Hiroyuki Ohsaki.
# All rights reserved.
#
# Id: RandomWalk.pm,v 1.11 2015/12/09 14:45:23 ohsaki Exp $
#

import math
import random

from vector_2d import Vector as V
from dtnsim.mobility.fixed import Fixed

class RandomWalk(Fixed):
    def __init__(self, vel_func=None, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)
        if vel_func is None:
            vel_func = lambda: 1.0  # 1.0 [m/s] by default
        self.vel_func = vel_func
        self.velocity = None
        self.wait = None

    def update_velocity(self):
        """Update agent's velocity using the velocity function."""
        vel = self.vel_func()
        theta = random.uniform(0, 2 * math.pi)
        self.velocity = vel * V(math.cos(theta), math.sin(theta))
        self.wait = False

    def move(self, delta):
        """Move the agent for the duration of DELTA."""
        self.update_velocity()
        self.current += self.velocity * delta
