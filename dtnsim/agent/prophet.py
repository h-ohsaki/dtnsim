#!/usr/bin/env python3
#
# Agent class implementing infinite-copy ProPHET routing.
# Copyright (c) 2011-2018, Hiroyuki Ohsaki.
# All rights reserved.
#
# Id: ProPHET.pm,v 1.8 2016/01/19 17:25:53 ohsaki Exp $
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

from collections import defaultdict

from dtnsim.agent.epidemic import Epidemic

P_INIT = 0.75
BETA = 0.25
GAMMA = 0.999

class ProPHET(Epidemic):
    def __init__(self, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)
        self.d_pred = defaultdict(float)

    def update_d_pred(self, encounters):
        """Update delivery predictabilities to all destination agents."""
        encoutered_with = defaultdict(int)
        for agent in encounters:
            # refresh delivery predictability
            neighbor = agent.id_
            encoutered_with[neighbor] += 1
            self.d_pred[neighbor] += (1 - self.d_pred[neighbor]) * P_INIT
            # update delivery predictabilities using transitivity
            for dst in agent.d_pred:
                if dst == self.id_:
                    continue
                self.d_pred[dst] += (
                    1 - self.d_pred[dst]
                ) * self.d_pred[neighbor] * agent.d_pred[dst] * BETA

        # decay delivery predictabilities to all destinations
        # FIXME: do not decay for encountered agents
        for dst in self.d_pred:
            if encoutered_with[dst]:
                continue
            self.d_pred[dst] *= GAMMA

    def should_forward(self, agent, msg):
        """Check whether the message MSG should be forwarded to an encountered
        agent AGENT."""
        # do not forward if the neighbor already has the message
        if agent.received[msg]:
            return
        # forward only when neighbor is closer to the destination than itself
        dst = self.msg_dst(msg)
        if dst not in agent.d_pred:
            return
        return agent.d_pred[dst] > self.d_pred[dst]

    def forward(self):
        """Try to deliver its carrying messages to all encountered agents."""
        encounters = self.encounters()
        self.update_d_pred(encounters)
        for agent in encounters:
            for msg in self.pending_messages():
                dst = self.msg_dst(msg)
                if agent.id_ == dst:
                    self.sendmsg(agent, msg)
                    del self.received[msg]
                    self.delivered[msg] += 1
                else:
                    if not self.should_forward(agent, msg):
                        continue
                    self.sendmsg(agent, msg)
