#!/usr/bin/env3 python3
#
# A class for dummy underlying path.
# Copyright (c) 2011-2018, Hiroyuki Ohsaki.
# All rights reserved.
#
# $Id: none.py,v 1.2 2018/10/15 13:01:19 ohsaki Exp $
#

class NONE:
    def __init__(self, width=1000, height=1000, *args, **kwargs):
        self.width = width
        self.height = height
        self.graph = None
