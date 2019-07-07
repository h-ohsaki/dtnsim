#!/usr/bin/env python3
#
# A class for managing the simulator virtual clock.
# Copyright (c) 2018-2019, Hiroyuki Ohsaki.
# All rights reserved.
#
# $Id: scheduler.py,v 1.4 2018/11/13 06:36:42 ohsaki Exp $
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

VERSION = '1.0'

def version():
    return """
This is dtnsim, version {}.
Copyright (c) 2010-2019, Hiroyuki Ohsaki.
All rights reserved.""".format(VERSION)

class Scheduler:
    def __init__(self, time=0, delta=10, max_time=10000):
        self.time = time  # simulation clock [s]
        self.delta = delta  # slot length [s]
        self.max_time = max_time
        self.agents = []
        self.zone_cache = {}

    def __repr__(self):
        name = self.__class__.__name__
        return '{}(time={!r}, delta={!r}, max_time={!r})'.format(
            name, self.time, self.delta, self.max_time)

    def advance(self):
        """Advance the simulator clock by DELTA."""
        self.time += self.delta

    def is_running(self):
        """Check if the simulation is running."""
        return self.time <= self.max_time

    def add_agent(self, agent):
        """Register an agent AGENT to the scheduler."""
        self.agents.append(agent)

    def agent_by_id(self, n):
        """Return an agent whose identifier is N.  Th identifier is an integer
        starting from 1."""
        return self.agents[n - 1]

    def cache_zones(self):
        """Refresh the zone information of all agents (i..e., the location of
        grids (zones) in which every agent exists.  The zone information is
        utilized to speed-up the detection of agent-to-agent encounters."""
        self.zone_cache = {}
        for agent in self.agents:
            agent.cache_zone()
