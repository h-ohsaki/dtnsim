#!/usr/bin/env python3
#
# A mobility class for CRWP (Constrained Random Waypoint) model on a graph.
# Copyright (c) 2011, Hiroyuki Ohsaki.
# All rights reserved.
#
# $Id: crwp.py,v 1.2 2018/10/15 12:48:51 ohsaki Exp ohsaki $
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

from dtnsim.mobility.graph.randomwalk import RandomWalk

class CRWP(RandomWalk):
    def __init__(self, pause_func=None, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)
        if pause_func is None:
            pause_func = lambda: 0.0  # no pause time by default
        self.pause_func = pause_func
        self.goal = None
        self.goal_edge = None
        self.goal_offset = None
        self.wait = False
        self.pick_goal()
        self.update_velocity()

    def update_velocity(self):
        """Update agent's velocity."""
        self.velocity = self.vel_func()

    def update_goal_cache(self):
        """Compute and store the goal coordinate for later use."""
        self.goal = self.get_coordinate(self.goal_edge, self.goal_offset)

    def select_route(self):
        """Select the link through which the agent should proceed to reach its
        destination (goal).  This code assumes that the agent is just on the
        vertex and the graph is plannar."""
        # NOTE: this code assumes that the current position of the agent is is V
        u, v = self.current_edge
        pv = self.vertex_coordinate(v)
        next_ = u  # for fail safe
        min_angle = None
        # find the vertex W whose angle is closest to the goal
        for w in self.path.graph.neighbors(v):
            # never goes back to the coming direction
            if w == u:
                continue
            pw = self.vertex_coordinate(w)
            angle = self.angle_between_vectors(self.goal - pv, pw - pv)
            if min_angle is None or angle < min_angle:
                min_angle = angle
                next_ = w
        self.move_to_point([v, next_], 0)

    def reverse_current_if_necessary(self):
        """Reverse the current direction if the opposite is closer to the goal."""
        u, v = self.current_edge
        goal = self.goal - self.current
        via_v = self.vertex_coordinate(v) - self.current
        via_u = self.vertex_coordinate(u) - self.current
        if self.angle_between_vectors(
                goal, via_u) < self.angle_between_vectors(goal, via_v):
            length = self.edge_length(self.current_edge)
            self.current_edge = [v, u]
            self.current_offset = length - self.current_offset

    def pick_goal(self):
        """Randomly choose the location to go."""
        edge, offset = self.random_point()
        self.goal_edge = edge
        self.goal_offset = offset
        self.update_goal_cache()
        self.reverse_current_if_necessary()

    def move(self, delta):
        """Move the agent for the duration of DELTA."""
        # sleep until wait timer expires
        self.wait = max(self.wait - delta, 0)
        if self.wait > 0:
            return

        # advance the agent by SPEED * DELTA
        step = self.velocity * delta
        self.current_offset += step
        self.update_current_cache()

        l = self.edge_length(self.current_edge)
        # if close enough to the goal, randomly choose the next goal
        if abs(self.goal - self.current) < step:
            self.wait = self.pause_func()
            self.pick_goal()
            self.update_velocity()
        elif abs(self.current_offset - l) < step or self.current_offset > l:
            self.select_route()
