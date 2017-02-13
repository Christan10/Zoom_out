from query import *
from zoom_out import *
from distortion import *

K = 22
Rmax = 1.0
Rmin = 0.5

Q = []

Q_1 = Query(1, 500000, 472518.0, 4201118.0, 482000.0, 4209000.0)
Q_1.episodes = 'CAR'
Q.append(Q_1)

Q_2 = Query(2, 500000, 473518.0, 4201118.0, 480000.0, 4209000.0)
Q_2.episodes = 'BUS'
Q.append(Q_2)

#Q_3 = Query(3, 0, 460000, 4100000, 480000, 4300000)
#Q_3.episodes = ['HOME']
#Q.append(Q_3)

#declare the object that handles the distortions

distortionData = DistortionData(20000.0, 0, True)

#set queries for distortion data
distortionData.set_subqueries(Q)


FQ = zoom(K, Q, Rmin, Rmax, distortionData)

print(Q)


