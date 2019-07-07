#!/usr/bin/env python3
#
# A monitor class for visualizing simulation with cell.
# Copyright (c) 2011-2018, Hiroyuki Ohsaki.
# All rights reserved.
#
# Id: Cell.pm,v 1.3 2017/11/08 03:22:30 ohsaki Exp ohsaki $
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

import math
import random

from dtnsim.monitor.null import Null

def float2str(v, fmt='9.3f'):
    """Return string representation of a number V using the format FMT.  All
    white spaces are replaced with double-underscores."""
    astr = ('%' + fmt) % v
    astr = astr.replace(' ', '__')
    return astr

def to_geometry(v):
    """Convert the relative length V to the absolute length.  This code
    assumes both the width and the height of the field is 1,000."""
    return v / 1000

class Cell(Null):
    def open(self):
        """Initialize the color palette."""
        print('palette c_vertex    0.4 0.8 1.0 0.2')
        print('palette c_edge      0.4 0.8 1.0 0.2')
        print('palette c_sus_range 0.2 0.7 1.0 0.1')
        print('palette c_sus       0.4 0.8 1.0 0.7')
        print('palette c_inf_range 1.0 0.7 0.0 0.2')
        print('palette c_inf       1.0 0.8 0.0 0.7')
        print('palette c_delivery  1.0 0.8 0.0 0.2')
        print('palette c_dst_range 1.0 0.4 0.2 0.2')
        print('palette c_dst       1.0 0.4 0.2 0.7')

    def close(self):
        pass

    def display_path(self, path):
        """Draw all underlying paths on the field."""
        graph = path.graph
        if not graph:
            return
        for v in sorted(graph.vertices()):
            p = graph.get_vertex_attribute(v, 'xy')
            x, y = to_geometry(p[0]), to_geometry(p[1])
            print('define v{} ellipse 2 2 c_vertex {} {}'.format(v, x, y))
            #print('define v{0}t text {0} 14 white {1} {2}'.format(v, x, y))
        for u, v in graph.edges():
            print('define - link v{} v{} 1 c_edge'.format(u, v))
        # NOTE: this code assumes paths will not move indefinitely
        print('fix /./')

    def change_agent_status(self, agent):
        """Update the color of agent if it has already received a message."""
        id_ = agent.id_
        color = 'c_sus'
        if agent.received or agent.receive_queue:
            color = 'c_inf'
        print('color agent{} {}'.format(id_, color))
        print('color agentr{} {}_range'.format(id_, color))

    def display_agents(self):
        """Draw all agents on the field."""
        for agent in self.scheduler.agents:
            id_ = agent.id_
            p = agent.mobility.current
            x, y = to_geometry(p[0]), to_geometry(p[1])
            r = to_geometry(agent.range_)
            print('define agent{} ellipse 4 4 white {} {}'.format(id_, x, y))
            print('define agentr{0} ellipse {1} {1} white {2} {3}'.format(
                id_, r, x, y))
            self.change_agent_status(agent)

    def move_agent(self, agent):
        """Reposition the location of the agent AGENT."""
        id_ = agent.id_
        p = agent.mobility.current
        x, y = to_geometry(p[0]), to_geometry(p[1])
        print('move agent{} {} {}'.format(id_, x, y))
        print('move agentr{} {} {}'.format(id_, x, y))

    def display_status(self):
        """Display the current statistics at the top of the screen."""
        time = float2str(self.scheduler.time, '10.2f')
        tx = float2str(self.tx_total, '10g')
        rx = float2str(self.rx_total, '10g')
        dup = float2str(self.dup_total, '10g')
        uniq_total = float2str(self.uniq_total, '10g')
        delivered_total = float2str(self.delivered_total, '10g')
        uniq_delivered_total = float2str(self.uniq_delivered_total, '10g')
        print(
            'define status_l text Time:{},____TX:{},____RX:{},____DUP:{},____Delivered:{}__/__{},____Arrived:{} 14 white 0.5 0.05'
            .format(time, tx, rx, dup, uniq_delivered_total, uniq_total,
                    delivered_total))

    def display_forward(self, src_agent, dst_agent, msg):
        """Display the completion of message delivery for agents of Fixed
        class."""
        super().display_forward(src_agent, dst_agent, msg)
        if not self.is_delivered(dst_agent, msg):
            return
        if 'Fixed' not in dst_agent.mobility.__class__.__name__:
            return

        src, dst = dst_agent.msg_src(msg), dst_agent.msg_dst(msg)
        src_p = self.scheduler.agent_by_id(src).mobility.current
        dst_p = self.scheduler.agent_by_id(dst).mobility.current
        x1, y1, x2, y2 = to_geometry(src_p[0]), to_geometry(
            src_p[1]), to_geometry(dst_p[0]), to_geometry(dst_p[1])
        print('define - line {} {} {} {} 1 c_delivery'.format(x1, y1, x2, y2))

    def update(self):
        print('display')
