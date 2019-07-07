#!/usr/bin/env python3
#
# A dummy class without simulation monitoring.
# Copyright (c) 2011-2018, Hiroyuki Ohsaki.
# All rights reserved.
#
# Id: Null.pm,v 1.14 2015/12/28 10:28:46 ohsaki Exp $
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

from perlcompat import die

class Null:
    def __init__(self, scheduler=None):
        if scheduler is None:
            die("Scheduler class must be specified.")
        self.scheduler = scheduler
        self.tx_total = 0
        self.rx_total = 0
        self.dup_total = 0
        self.uniq_total = 0
        self.delivered_total = 0
        self.uniq_delivered_total = 0

    def open(self):
        pass

    def update(self):
        pass

    def close(self):
        pass

    def display_path(self, path):
        pass

    def display_agents(self):
        pass

    def move_agent(self, agent):
        pass

    def change_agent_status(self, agent):
        pass

    def display_status(self):
        pass

    def is_delivered(self, agent, msg):
        """Check if the destination of the message MSG is AGENT."""
        return agent.msg_dst(msg) == agent.id_

    def is_duplicate(self, agent, msg):
        """Check if the agent AGENT already has the message MSG."""
        return agent.received.get(msg, None)

    def display_forward(self, src_agent, dst_agent, msg):
        """Update the statistics when the message MSG is forwarded from
        SRC_AGENT to DST_AGENT."""
        self.tx_total += 1
        self.rx_total += 1
        if self.is_duplicate(dst_agent, msg):
            self.dup_total += 1
        if self.is_delivered(dst_agent, msg):
            self.delivered_total += 1
        if self.is_delivered(dst_agent,
                             msg) and not dst_agent.received.get(msg, None):
            self.uniq_delivered_total += 1
