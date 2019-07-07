#!/usr/bin/env python3
#
# An agent class implementing P-BCAST (PUSH-based BroadCAST).
# Copyright (c) 2011-2015, Hiroyuki Ohsaki.
# All rights reserved.
#
# Id: P_BCAST.pm,v 1.32 2015/12/09 14:45:23 ohsaki Exp $
#

from dtnsim.agent.carryonly import CarryOnly

class P_BCAST(CarryOnly):
    """Try to deliver its carrying messages to all encountered agents."""

    def forward(self):
        encounters = self.encounters()
        for agent in encounters:
            for msg in self.received:
                self.sendmsg(agent, msg)
