from zoom_out import *
from distortion import *
from auditor_check_overlapping import *


K = 2
userid = 1
Rmax = 1.7
Rmin = 1.0

Q = []

Q_1 = SQuery(1, 500000, 473318.0, 4201118.0, 480000.0, 4209000.0)
Q_1.episodes = 'CAR'
Q.append(Q_1)

Q_2 = SQuery(2, 500000, 472518.0, 4201118.0, 482000.0, 4206000.0)
Q_2.episodes = 'CAR'
Q.append(Q_2)

#Q_3 = SQuery(3, 500000, 460000.0, 4200000.0, 470000.0, 4202000.0)
#Q_3.episodes = 'MOVE'
#Q.append(Q_3)

# declare the object that handles the distortions

distortionData = DistortionData(2500.0, 0, True)

# set queries for distortion data
distortionData.set_subqueries(Q)

ntr = len(SQuery.combine(Q))
print(ntr)

if ntr < K and ntr != 0:
    if len(Q) == 1:
        raise ValueError("zoom out can not work with only one subquery. Refuse answer.")

    FQ = zoom(K, Q, Rmin, Rmax, distortionData)
    print(Q_1.realx1, Q_1.realy1, Q_1.realx2, Q_1.realy2)
    querytoadd = []
    for i in range(len(FQ)):
        sq = FQ[i]
        querytoadd.append(SQuery.conversion(sq))
    if check_for_overlap(K, querytoadd, userid, FQ) is True:
        print("We have overlap the user must not get an answer")
    else:
        print("The user can safely get the answer to his query")
        result = db.QueriesCollection.insert_one({"urid": userid, "query": querytoadd})
elif ntr >= K and ntr != 0:
    FQ = Q
    querytoadd = []
    for i in range(len(FQ)):
        sq = FQ[i]
        querytoadd.append(SQuery.conversion(sq))
    if check_for_overlap(K, querytoadd, userid, FQ) is True:
        print("We have overlap the user must not get an answer")
    else:
        print("The user can safely get the answer to his query")
        result = db.QueriesCollection.insert_one({"urid": userid, "query": querytoadd})
else:
    print("The subqueries have no common trajectories")

