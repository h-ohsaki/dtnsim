#!/usr/bin/env python3
#
# A monitor class for visualizing simulation with cell.
# Copyright (c) 2011-2018, Hiroyuki Ohsaki.
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
        print('palette c_edge   heat50 .6')
        print('palette c_vertex heat50 .9')
        print('palette c_sus_range heat10 .6')
        print('palette c_sus       heat10 .9')
        print('palette c_inf_range heat85 .6')
        print('palette c_inf       heat85 .9')
        print('palette c_wait_sus_range heat30 .6')
        print('palette c_wait_sus       heat30 .9')

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
        if agent.mobility.wait:
            color = 'c_wait_sus'
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

    def update(self):
        print('display')
