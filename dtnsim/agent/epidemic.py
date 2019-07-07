#!/usr/bin/env python3
#
# Agent class for infinite-copy Epidemic routing.
# Copyright (c) 2011-2018, Hiroyuki Ohsaki.
# All rights reserved.
#
# Id: Epidemic.pm,v 1.8 2015/12/10 08:26:08 ohsaki Exp $
#

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
