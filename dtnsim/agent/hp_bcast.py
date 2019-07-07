#!/usr/bin/env python3
#
# An agent class implementing HP-BCAST.
# Copyright (c) 2011-2018, Hiroyuki Ohsaki.
# All rights reserved.
#
# Id: HP_BCAST.pm,v 1.11 2015/12/09 14:45:23 ohsaki Exp $
#

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
