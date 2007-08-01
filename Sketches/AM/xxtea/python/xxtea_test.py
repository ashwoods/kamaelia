#!/usr/bin/python
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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

import xxtea
sss = 'abcdefghijklmnopqrstuvwxyz'
ccc = xxtea.xxbtea(sss,2,"AABBCCDDEE0123456789AABBCCDDEEFF")
#print sss
#print ccc
tt = xxtea.xxbtea(ccc,-2,"AABBCCDDEE0123456789AABBCCDDEEFF")
print tt
#status = xxtea.enc_xxtea("xxtea.pyx", "xxtea.enc", "AABBCCDDEE0123456789AABBCCDDEEFF") 
#if(status == 0):
#    print "encryption success"
#else:
#    print "encryption failed:" + str(status)


#status = xxtea.dec_xxtea("xxtea.enc", "xxtea.dec", "AABBCCDDEE0123456789AABBCCDDEEFF") 
#if(status == 0):
#    print "decryption success, check that xxtea.dec and xxtea.pyx should be same"
#else:
#    print "decryption failed:" + str(status)

