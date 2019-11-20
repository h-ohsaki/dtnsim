#!/usr/bin/env python3
#
# A dummy class without simulation monitoring.
# Copyright (c) 2011-2019, Hiroyuki Ohsaki.
# All rights reserved.
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

from dtnsim.monitor.null import Null

class Log(Null):
    # NOTE: this code must be invoked before calling flush()
    def display_forward(self, src_agent, dst_agent, msg):
        """Update the statistics when the message MSG is forwarded from
        SRC_AGENT to DST_AGENT."""
        super().display_forward(src_agent, dst_agent, msg)
        stat = []
        if self.is_delivered(dst_agent, msg):
            stat.append('delivered')
        if self.is_duplicate(dst_agent, msg):
            stat.append('dup')
        stat_str = ','.join(stat)
        print('\t'.join([
            str(self.scheduler.time), 'forward',
            str(src_agent.id_),
            str(dst_agent.id_), msg, stat_str
        ]))
        print('\t'.join([
            str(self.scheduler.time), 'status',
            str(self.tx_total),
            str(self.rx_total),
            str(self.dup_total),
            str(self.uniq_total),
            str(self.delivered_total),
            str(self.uniq_delivered_total)
        ]))
