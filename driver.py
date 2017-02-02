from query import *
from zoom_out import *
from distortion import *

K = 4
Rmax = 1.0
Rmin = 0.5

Q = []

Q_1 = Query(1, 0, 472518, 4201118, 482000, 4209000)
Q_1.episodes = ['CAR']
Q.append(Q_1)

Q_2 = Query(2, 0, 462518, 4100008, 479000, 4200000)
Q_2.episodes = ['HOME']
Q.append(Q_2)

Q_3 = Query(3, 0, 450000, 4100000, 460000, 4187000)
Q_3.episodes = ['CAR']
Q.append(Q_3)

#declare the object that handles the distortions

distortionData = DistortionData(100, 0, True)

#set queries for distortion data
distortionData.set_subqueries(Q)


FQ = zoom(K, Q, Rmin, Rmax, distortionData)




