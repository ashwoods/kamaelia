#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-
# 
# (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
# Licensed to the BBC under a Contributor Agreement: PO

import Axon
import threading

class MessageAdder(Axon.Component.component):
    def __init__(self, outboxes, **argd):
        self.Outboxes = outboxes
        super(MessageAdder, self).__init__(**argd)
        self.lock = threading.Lock()
        self.messages = {}
        for outboxName in outboxes:
            self.messages[outboxName] = []
        self._stop_within_iterations = None
        
    def addMessage(self, msg, outbox):
        self.lock.acquire()
        try:
            self.messages[outbox].append(msg)
        finally:
            self.lock.release()
    
    def stopMessageAdder(self, within_iterations = 0):
        self._stop_within_iterations = within_iterations
        
    def _getOutboxLength(self, outbox):
        self.lock.acquire()
        try:
            return len(self.messages[outbox])
        finally:
            self.lock.release()
    
    def main(self):
        while self._stop_within_iterations is None or self._stop_within_iterations > 0:
            for outbox in self.Outboxes:
                self.lock.acquire()
                try:
                    while len(self.messages[outbox]) > 0:
                        msg = self.messages[outbox].pop(0)
                        self.send(msg, outbox)
                finally:
                    self.lock.release()
            if self._stop_within_iterations is not None:
                self._stop_within_iterations = self._stop_within_iterations - 1
            yield 1