from query import *
from zoom_out import *
from distortion import *

k = 4
Rmax = 1.0
Rmin = 0.5

Q=[]
Q.append(Query(0))
Q.append(Query(1))
Q.append(Query(2))

#fix the queries

#declare the object that handles the
#distortions
distortionData = DistortionData()

#fix distortion data

#set queries for distortion data

distortionData.set_subqueries(Q)


FQ = zoom(k,Rmin,Rmax,Q,distortionData)


