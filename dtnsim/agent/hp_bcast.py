#!/usr/bin/env python3
#
# An agent class implementing HP-BCAST.
# Copyright (c) 2011-2018, Hiroyuki Ohsaki.
# All rights reserved.
#
# Id: HP_BCAST.pm,v 1.11 2015/12/09 14:45:23 ohsaki Exp $
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

from dtnsim.agent.p_bcast import P_BCAST

class HP_BCAST(P_BCAST):
    def __init__(self, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)
        self.history = defaultdict(dict)

    def forward(self):
        """Try to deliver its carrying messages to all encountered agents."""
        encounters = self.encounters()
        for agent in encounters:
            for msg in self.received:
                # do not forward if the encountered agent already has the message
                if agent.id_ in self.history[msg]:
                    continue
                self.sendmsg(agent, msg)

                # receiver then knows sender has the message
                agent.history[msg][self.id_] = True
                # sender transfers its history with piggy backing
                for _ in self.history[msg]:
                    agent.history[msg][_] = True
