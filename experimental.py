from zoom_out import *
from auditor_check_overlapping import *

Rmax = 1.7
Rmin = 1.0
K = 4
list_of_zoom_repetitions = 0
# this is a counter that counts only the repetitions that used the algorithm zoom_out and we want to reach 100 examples
tags = ['MOVE', 'STOP', 'CAR', 'HOME', 'WALKING', 'BUS', 'CROSSING', 'TRANSPORTATION', 'BICYCLE', 'RELAXING', 'Null']
queries_we_used_zoom = 0
queries_we_answer_without_zoom = 0
queries_we_reject_to_answer = 0
queries_we_reject_to_answer_for_overlap = 0
no_common_traj_queries = 0
total_queries = 0

while list_of_zoom_repetitions < 10:
    total_queries += 1
    userid = random.randint(1, 200)
    # num_of_subqueries is the number of the subqueries this query will have
    num_of_subqueries = random.randint(2, 3)

    Q = []
    for i in range(num_of_subqueries):
        x1 = random.uniform(467711.5701, 482209.8285)
        x2 = x1 + 1562.226
        y1 = random.uniform(4197384.607, 4215496.4685)
        y2 = y1 + 1562.226
        time = 80000
        tag = random.choice(tags)
        Q_i = SQuery(i + 1, time, x1, y1, x2, y2, tag)
        Q.append(Q_i)

    distortionData = DistortionData(156.223, 2500.0, True, False, False)
    if SQuery.combine(Q) is not None:
        ntr = len(SQuery.combine(Q))

        if ntr >= K:
            FQ = Q
            querytoadd = []
            for i in range(len(FQ)):
                sq = FQ[i]
                querytoadd.append(SQuery.conversion(sq))
            if check_for_overlap(K, querytoadd, userid, FQ) is False:
                result = db.QueriesCollection.insert_one({"urid": userid, "query": querytoadd})
                queries_we_answer_without_zoom += 1
            else:
                queries_we_reject_to_answer += 1
                queries_we_reject_to_answer_for_overlap += 1
        elif ntr < K and ntr != 0:
            list_of_zoom_repetitions += 1
            FQ = zoom(K, Q, Rmin, Rmax, distortionData)
            ntr = len(SQuery.combine(FQ))
            if ntr < K:
                queries_we_reject_to_answer += 1
            else:
                querytoadd = []
                for i in range(len(FQ)):
                    sq = FQ[i]
                    querytoadd.append(SQuery.conversion(sq))
                if check_for_overlap(K, querytoadd, userid, FQ) is False:
                    result = db.QueriesCollection.insert_one({"urid": userid, "query": querytoadd})
                    queries_we_used_zoom += 1
                else:
                    queries_we_reject_to_answer += 1
                    queries_we_reject_to_answer_for_overlap += 1
        else:
            queries_we_reject_to_answer += 1
            no_common_traj_queries += 1

print("total queries = ", total_queries, "queries we used zoom effectively= ", queries_we_used_zoom)
print("queries we answer without zoom = ", queries_we_answer_without_zoom)
print("queries we reject to answer = ", queries_we_reject_to_answer, "queries we reject to answer for overlap = ",
      queries_we_reject_to_answer_for_overlap)
print("queries with no common trajectories = ", no_common_traj_queries)
