#!/usr/bin/env python3
#
# A dummy class without simulation monitoring.
# Copyright (c) 2011-2018, Hiroyuki Ohsaki.
# All rights reserved.
#
# Id: Log.pm,v 1.12 2015/12/30 02:55:06 ohsaki Exp $
#

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
