#!/usr/bin/env python3
#
# Agent class for single-copy and carry-only routing.
# Copyright (c) 2011-2019, Hiroyuki Ohsaki.
# All rights reserved.
#
# Id: CarryOnly.pm,v 1.11 2015/12/11 08:14:04 ohsaki Exp $
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
import math

from perlcompat import die

MAX_RANGE = 50

class CarryOnly():
    def __init__(self,
                 id_=None,
                 scheduler=None,
                 mobility=None,
                 monitor=None,
                 range_=50):
        if id_ is None:
            id_ = len(scheduler.agents) + 1
        if not scheduler:
            die("Scheduler class must be specified.")
        if not mobility:
            die("Mobility class must be specified.")
        if not monitor:
            die("Monitor class must be specified.")
        if range_ > MAX_RANGE:
            die(f"range cannot exceed MAX_RANGE ({MAX_RANGE})")
        self.id_ = id_
        self.scheduler = scheduler
        self.mobility = mobility
        self.monitor = monitor
        self.range_ = range_

        self.last_neighbors = []
        self.received = defaultdict(int)
        self.receive_queue = defaultdict(int)
        self.delivered = defaultdict(int)
        self.tx_count = 0
        self.rx_count = 0
        self.dup_count = 0

        self.scheduler.add_agent(self)

    def __repr__(self):
        name = self.__class__.__name__
        return '{}(id_={!r}, mobility={!r}, range_={!r}'.format(
            name, self.id_, self.mobility, self.range_)

    def msg_src(self, msg):
        src = msg.split('-')[0]
        return int(src)

    def msg_dst(self, msg):
        dst = msg.split('-')[1]
        return int(dst)

    def msg_id(self, msg):
        id_ = msg.split('-')[2]
        return int(id_)

    def zone(self, x=None, y=None):
        """Return the zone (I, J) corresponding the geometry (X, Y)."""
        if x is None:
            x = self.mobility.current[0]
        if y is None:
            y = self.mobility.current[1]
        i = max(0, int(x / MAX_RANGE))
        j = max(0, int(y / MAX_RANGE))
        return i, j

    def cache_zone(self):
        """Record the zone of the current agent in the global zone cache."""
        i, j = self.zone()
        cache = self.scheduler.zone_cache
        cache.setdefault(j, {})
        cache[j].setdefault(i, [])
        self.scheduler.zone_cache[j][i].append(self)

    def neighbors(self):
        """Return neighbor agents within the communication range."""
        cache = self.scheduler.zone_cache
        if not cache:
            die("update_zone() must have been called for zone caching.")

        p = self.mobility.current
        i, j = self.zone()
        neighbors = []
        # check nine zones including/surrounding the current one
        for dj in [-1, 0, 1]:
            if j + dj < 0:
                continue
            for di in [-1, 0, 1]:
                if i + di < 0:
                    continue
                if not cache.get(j + dj, None):
                    continue
                if not cache[j + dj].get(i + di, None):
                    continue
                for agent in self.scheduler.zone_cache[j + dj][i + di]:
                    if agent == self:
                        continue
                    q = agent.mobility.current
                    if abs(p[0] - q[0]) > self.range_:
                        continue
                    if abs(p[1] - q[1]) > self.range_:
                        continue
                    if math.sqrt((p[0] - q[0])**2 +
                                 (p[1] - q[1])**2) > self.range_:
                        continue
                    neighbors.append(agent)
        return neighbors

    def encounters(self):
        """Return encoutered agents (i.e., newly visible agents)."""
        neighbors = self.neighbors()
        encounters = {agent.id_: agent for agent in neighbors}
        for agent in self.last_neighbors:
            try:
                del encounters[agent.id_]
            except KeyError:
                pass
        self.last_neighbors = neighbors
        return list(encounters.values())

    def sendmsg(self, agent, msg):
        """Send a message MSG to the agent AGENT."""
        agent.recvmsg(self, msg)
        self.tx_count += 1
        self.monitor.display_forward(self, agent, msg)
        self.monitor.change_agent_status(self)

    def recvmsg(self, agent, msg):
        """Receive a message MSG from the agent AGENT.  Note that the received
        message is temporally stored in the reception queue."""
        self.receive_queue[msg] += 1
        self.rx_count += 1
        if msg in self.received:
            self.dup_count += 1
        self.monitor.change_agent_status(self)

    def messages(self):
        """Return all received messages."""
        return [msg for msg in self.received if self.received[msg] > 0]

    def pending_messages(self):
        """Return all messages need to be delivered."""
        return [
            msg for msg in self.messages()
            if self.msg_dst(msg) != self.id_ and not msg in self.delivered
        ]

    def accepted_messages(self):
        """Return successfully-received messages by the agent."""
        return [
            msg for msg in self.messages() if self.msg_dst(msg) == self.id_
        ]

    def forward(self):
        """Try to forward carrying messages to all encountered agents."""
        encounters = self.encounters()
        for agent in encounters:
            for msg in self.pending_messages():
                # forward carrying messages only to the destination
                dst = self.msg_dst(msg)
                if agent.id_ != dst:
                    continue
                self.sendmsg(agent, msg)
                del self.received[msg]
                self.delivered[msg] += 1

    def advance(self):
        """Advance the simulation for a delta time."""
        self.mobility.move(self.scheduler.delta)
        self.monitor.move_agent(self)
        self.forward()

    def flush(self):
        """Merge all newly-received messages with existing ones."""
        # NOTE: expand list to avoid run-time error
        for msg in list(self.receive_queue.keys()):
            self.received[msg] += self.receive_queue[msg]
            del self.receive_queue[msg]
