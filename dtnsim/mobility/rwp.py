#!/usr/bin/env python3
#
# A mobility class for RWP (Random WayPoint) mobility model.
# Copyright (c) 2011-2018, Hiroyuki Ohsaki.
# All rights reserved.
#
# Id: RandomWaypoint.pm,v 1.20 2015/12/30 02:54:57 ohsaki Exp $
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

from dtnsim.mobility.randomwalk import RandomWalk

class RandomWaypoint(RandomWalk):
    def __init__(self, pause_func=None, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)
        if pause_func is None:
            pause_func = lambda: 0.0  # no pause time by default
        self.pause_func = pause_func
        self.wait = 0
        self.goal = self.goal_coordinate()

    def goal_coordinate(self):
        """Randomly choose the goal on the field."""
        return self.random_coordinate()

    def update_velocity(self):
        """Update agent's velocity using the velocity function."""
        self.velocity = self.vel_func() * (
            self.goal - self.current) / abs(self.goal - self.current)

    def move(self, delta):
        """Move the agent for the duration of DELTA."""
        # sleep until wait time expires
        self.wait = max(self.wait - delta, 0)
        if self.wait > 0:
            return

        self.update_velocity()
        self.current += self.velocity * delta

        # if close enough to the goal, randomly choose another goal
        epsilon = abs(self.velocity) * delta
        if abs(self.goal - self.current) <= epsilon:
            self.goal = self.goal_coordinate()
            self.update_velocity()
            self.wait = self.pause_func()
