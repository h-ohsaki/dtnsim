#!/usr/bin/env python3
#
# Agent class for infinite-copy Epidemic routing.
# Copyright (c) 2011-2018, Hiroyuki Ohsaki.
# All rights reserved.
#
# Id: Epidemic.pm,v 1.8 2015/12/10 08:26:08 ohsaki Exp $
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

from dtnsim.agent.carryonly import CarryOnly

class Epidemic(CarryOnly):
    def forward(self):
        """Try to deliver its carrying message to all encountered agents."""
        encounters = self.encounters()
        for agent in encounters:
            for msg in self.pending_messages():
                dst = self.msg_dst(msg)
                if agent.id_ == dst:
                    self.sendmsg(agent, msg)
                    del self.received[msg]
                    self.delivered[msg] += 1
                else:
                    self.sendmsg(agent, msg)
