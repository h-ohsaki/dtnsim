#!/usr/bin/env python3
#
# A monitor class for visualizing simulation with cell.
# Copyright (c) 2011-2018, Hiroyuki Ohsaki.
# All rights reserved.
#
# Id: Cell.pm,v 1.3 2017/11/08 03:22:30 ohsaki Exp ohsaki $
#

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
            print(f'define v{v} ellipse 2 2 c_vertex {x} {y}')
            #print(f'define v{v}t text {v} 14 white {x} {y}')
        for u, v in graph.edges():
            print(f'define - link v{u} v{v} 1 c_edge')
        # NOTE: this code assumes paths will not move indefinitely
        print('fix /./')

    def change_agent_status(self, agent):
        """Update the color of agent if it has already received a message."""
        id = agent.id_
        color = 'c_sus'
        if agent.received or agent.receive_queue:
            color = 'c_inf'
        print(f'color agent{id} {color}')
        print(f'color agentr{id} {color}_range')

    def display_agents(self):
        """Draw all agents on the field."""
        for agent in self.scheduler.agents:
            id = agent.id_
            p = agent.mobility.current
            x, y = to_geometry(p[0]), to_geometry(p[1])
            r = to_geometry(agent.range_)
            print(f'define agent{id} ellipse 4 4 white {x} {y}')
            print(f'define agentr{id} ellipse {r} {r} white {x} {y}')
            self.change_agent_status(agent)

    def move_agent(self, agent):
        """Reposition the location of the agent AGENT."""
        id = agent.id_
        p = agent.mobility.current
        x, y = to_geometry(p[0]), to_geometry(p[1])
        print(f'move agent{id} {x} {y}')
        print(f'move agentr{id} {x} {y}')

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
            f'define status_l text Time:{time},____TX:{tx},____RX:{rx},____DUP:{dup},____Delivered:{uniq_delivered_total}__/__{uniq_total},____Arrived:{delivered_total} 14 white 0.5 0.05'
        )

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
        print(f'define - line {x1} {y1} {x2} {y2} 1 c_delivery')

    def update(self):
        print('display')
