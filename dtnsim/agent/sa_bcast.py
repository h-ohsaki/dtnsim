#!/usr/bin/env python3
#
# An agent class implementing SA-BCAST (Self-Adaptive BroadCAST).
# Copyright (c) 2011-2018, Hiroyuki Ohsaki.
# All rights reserved.
#
# Id: SA_BCAST.pm,v 1.16 2015/12/09 14:45:23 ohsaki Exp $
#

import random

from dtnsim.agent.p_bcast import P_BCAST

# default control parameters for SA-BCAST
C = 1.5
MIN_P = 0.01
N_TH = 50

class SA_BCAST(P_BCAST):
    def __init__(self, c=C, min_p=MIN_P, n_th=N_TH, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)
        self.c = c
        self.min_p = min_p
        self.n_th = n_th

    def forward(self):
        """Try to deliver its carrying messages to all encountered agents."""
        encounters = self.encounters()
        if not encounters:
            return

        # forward only when N-th% of neighbors has changed
        neighbors = self.neighbors()
        change_ratio = len(encounters) / len(neighbors)
        if change_ratio < self.n_th / 100:
            return

        for agent in encounters:
            for msg in self.received:
                # change forwarding probability based on the number of duplicates
                ndups = max(self.received[msg] - 1, 0)
                p = max(1 / self.c**ndups, self.min_p)
                if random.uniform(0, 1) > p:
                    continue
                self.sendmsg(agent, msg)
