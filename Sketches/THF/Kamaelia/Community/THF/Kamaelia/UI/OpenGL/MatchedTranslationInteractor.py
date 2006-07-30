#!/usr/bin/env python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
"""\
=====================
Matched Translation Interactor
=====================
"""


import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import Axon
from Intersect3D import *
from Interactor import *

class MatchedTranslationInteractor(Interactor):
    
    def __init__(self, **argd):
        super(MatchedTranslationInteractor, self).__init__(**argd)

        self.grabbed = False
        self.position = None
        self.oldpoint = None
            

    def setup(self):
        self.addListenEvents( [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP ])


    def handleEvents(self):
        while self.dataReady("events"):
            event = self.recv("events")

            if self.position is not None:
                if event.type == pygame.MOUSEBUTTONDOWN or pygame.MOUSEMOTION and self.grabbed:
                    p1 = self.position.copy()
                    p1.x += 10
                    p2 = self.position.copy()
                    p2.y += 10
                    z = Intersect3D.ray_Plane(Vector(0,0,0), event.direction, [self.position, p1, p2])
                    newpoint = event.direction * z
                    
                if event.type == pygame.MOUSEBUTTONDOWN and self.identifier in event.hitobjects:
                    if event.button == 1:
                        self.grabbed = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.grabbed = False
                if event.type == pygame.MOUSEMOTION:
                    if self.grabbed == True:
                        if self.oldpoint is not None:
                            diff = newpoint-self.oldpoint
                            amount = (diff.x, diff.y)
                            self.send(amount, "outbox")

                try:
                    self.oldpoint = newpoint
                except NameError: pass            


    def frame(self):
        while self.dataReady("inbox"):
            self.position = self.recv("inbox")


if __name__=='__main__':
    from SimpleCube import *

    o1 = SimpleCube(position=(6, 0,-30), name="center").activate()
    i1 = MatchedTranslationInteractor(victim=o1).activate()

    o2 = SimpleCube(position=(0, 0,-20), name="center").activate()
    i2 = MatchedTranslationInteractor(victim=o2).activate()

    o3 = SimpleCube(position=(-3, 0,-10), name="center").activate()
    i3 = MatchedTranslationInteractor(victim=o3).activate()

    o4 = SimpleCube(position=(15, 0,-40), name="center").activate()
    i4 = MatchedTranslationInteractor(victim=o4).activate()
    
    o1.link( (o1, "position"), (i1, "inbox"))
    i1.link( (i1, "outbox"), (o1, "rel_position"))

    o2.link( (o2, "position"), (i2, "inbox"))
    i2.link( (i2, "outbox"), (o2, "rel_position"))

    o3.link( (o3, "position"), (i3, "inbox"))
    i3.link( (i3, "outbox"), (o3, "rel_position"))

    o4.link( (o4, "position"), (i4, "inbox"))
    i4.link( (i4, "outbox"), (o4, "rel_position"))
    
    Axon.Scheduler.scheduler.run.runThreads()  
