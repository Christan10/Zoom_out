from zoom_out import *
from distortion import *
from auditor_check_overlapping import *


K = 87
userid = 1
Rmax = 1.7
Rmin = 1.0

Q = []

Q_1 = Query(1, 500000, 473318.0, 4201118.0, 480000.0, 4209000.0)
Q_1.episodes = 'CAR'
Q.append(Q_1)

#Q_2 = Query(2, 500000, 472518.0, 4201118.0, 482000.0, 4206000.0)
#Q_2.episodes = 'CAR'
#Q.append(Q_2)

#Q_3 = Query(3, 500000, 460000.0, 4200000.0, 470000.0, 4202000.0)
#Q_3.episodes = 'MOVE'
#Q.append(Q_3)

# declare the object that handles the distortions

distortionData = DistortionData(2500.0, 0, True)

# set queries for distortion data
distortionData.set_subqueries(Q)

ntr = len(Query.combine(Q))
if ntr < K and ntr != 0:
    FQ = zoom(K, Q, Rmin, Rmax, distortionData)
    print(Q_1.realx1, Q_1.realy1, Q_1.realx2, Q_1.realy2)
    if check_for_overlap(K, FQ, userid) is True:
        print("We have overlap the user must not get an answer")
    else:
        print("The user can safely get the answer to his query")
        result = db.QueriesCollection.insert_one({"urid": userid, "query": FQ})
elif ntr >= K and ntr != 0:
    FQ = Q
    if check_for_overlap(K, FQ, userid) is True:
        print("We have overlap the user must not get an answer")
    else:
        print("The user can safely get the answer to his query")
        result = db.QueriesCollection.insert_one({"urid": userid, "query": FQ})
else:
    print("The subqueries have no common trajectories")

