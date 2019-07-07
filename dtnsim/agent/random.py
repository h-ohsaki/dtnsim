#!/usr/bin/env python3
#
# An implementation of a single-copy random routing.
# Copyright (c) 2011-2018, Hiroyuki Ohsaki.
# All rights reserved.
#
# Id: Random.pm,v 1.4 2015/12/09 14:45:23 ohsaki Exp $
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

from dtnsim.agent.carryonly import CarryOnly

DEFAULT_FORWARD_PROB = 0.5

class Random(CarryOnly):
    def __init__(self, forward_prob=DEFAULT_FORWARD_PROB, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)
        self.forward_prob = forward_prob

    def forward(self):
        """Try to deliver its carrying messages to all encountered agents."""
        encounters = self.encounters()
        for agent in encounters:
            for msg in self.pending_messages():
                dst = self.msg_dst(msg)
                if agent.id_ == dst:
                    self.sendmsg(agent, msg)
                    del self.received[msg]
                    self.delivered[msg] += 1
                else:
                    if random.uniform(0, 1) > self.forward_prob:
                        continue
                    self.sendmsg(agent, msg)
                    del self.received[msg]
