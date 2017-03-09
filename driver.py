from query import *
from zoom_out import *
from distortion import *


K = 50
Rmax = 1.7
Rmin = 1.0

Q = []

Q_1 = Query(1, 500000, 473318.0, 4201118.0, 480000.0, 4209000.0)
Q_1.episodes = 'CAR'
Q.append(Q_1)

Q_2 = Query(2, 500000, 472518.0, 4201118.0, 482000.0, 4206000.0)
Q_2.episodes = 'CAR'
Q.append(Q_2)

Q_3 = Query(3, 500000, 460000.0, 4200000.0, 470000.0, 4202000.0)
Q_3.episodes = 'MOVE'
Q.append(Q_3)

#declare the object that handles the distortions

distortionData = DistortionData(2500.0, 0, True)

#set queries for distortion data
distortionData.set_subqueries(Q)


FQ = zoom(K, Q, Rmin, Rmax, distortionData)

print(Q_1.realx1, Q_1.realy1, Q_1.realx2, Q_1.realy2, Q_2.realx1, Q_2.realy1, Q_2.realx2, Q_2.realy2, Q_3.realx1,
      Q_3.realy1, Q_3.realx2, Q_3.realy2)


