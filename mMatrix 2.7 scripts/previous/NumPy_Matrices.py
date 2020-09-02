import numpy as np

guestMatrix0 = np.arange(12).reshape(3,4)
flipMatrix90 = guestMatrix0.transpose()
guestMatrix270 = flipMatrix90[::-1]
flipMatrix180 = guestMatrix270.transpose()
guestMatrix180 = flipMatrix180[::-1]
flipMatrix270 = guestMatrix180.transpose()
guestMatrix90 = flipMatrix270[::-1]
flipMatrix0 = guestMatrix90.transpose()

print guestMatrix0
print "guestMatrix0\n"
print guestMatrix90
print "guestMatrix90\n"
print guestMatrix180
print 'guestMatrix180\n'
print guestMatrix270
print "guestMatrix270\n"

print flipMatrix0
print "flipMatrix0\n"
print flipMatrix90
print "flipMatrix90\n"
print flipMatrix180
print "flipMatrix180\n"
print flipMatrix270
print 'flipMatrix270\n'
