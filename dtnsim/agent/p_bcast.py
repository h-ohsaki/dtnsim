#!/usr/bin/env python3
#
# An agent class implementing P-BCAST (PUSH-based BroadCAST).
# Copyright (c) 2011-2015, Hiroyuki Ohsaki.
# All rights reserved.
#
# Id: P_BCAST.pm,v 1.32 2015/12/09 14:45:23 ohsaki Exp $
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

class P_BCAST(CarryOnly):
    """Try to deliver its carrying messages to all encountered agents."""

    def forward(self):
        encounters = self.encounters()
        for agent in encounters:
            for msg in self.received:
                self.sendmsg(agent, msg)
