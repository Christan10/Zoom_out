from query import SQuery
from pymongo import MongoClient
client = MongoClient()
db = client.MyDB
collection = db.QueriesCollection


def check_tag_overlap(q1, q2):
    """This function checks for tag overlap when duration and bounding box are the same."""
    flag = True
    for i in range(len(q1)):
        sqn = q1[i]
        sqo = q2[i]

        if sqn[2] != sqo[2] or sqn[3] != sqo[3] or sqn[4] != sqo[4] or sqn[5] != sqo[5] or sqn[1] != sqo[1]:
            flag = False
            break

    if flag is False:
        return False
    return True


def check_spatial_overlap(q1, q2):
    """This function checks for spatial overlap when duration and tag are the same."""
    flag = True
    for i in range(len(q1)):
        sqn = q1[i]
        sqo = q2[i]

        if sqn[6] != sqo[6] or sqn[1] != sqo[1]:
            flag = False
            break

    if flag is False:
        return False

    for i in range(len(q1)):
        sqn = q1[i]
        sqo = q2[i]

        if sqn[2] <= sqo[2] and sqn[3] <= sqo[3] and sqn[4] >= sqo[4] and sqn[5] >= sqo[5]:
            return True
        elif sqo[2] <= sqn[2] and sqo[3] <= sqn[3] and sqo[4] >= sqn[4] and sqo[5] >= sqn[5]:
            return True
        else:
            return False


def check_time_overlap(q1, q2):
    """This function checks for time overlap when tag and bounding box are the same."""
    flag = True
    for i in range(len(q1)):
        sqn = q1[i]
        sqo = q2[i]

        if sqn[2] != sqo[2] or sqn[3] != sqo[3] or sqn[4] != sqo[4] or sqn[5] != sqo[5] or sqn[6] != sqo[6]:
            flag = False
            break

    if flag is False:
        return False
    return True


def check_overlap_by_subqueries_number(q1, q2):
    flag = False
    sqo = q2[0]
    for i in range(len(q1)):
        sqn = q1[i]
        if sqn == sqo:
            flag = True
            break

    if flag is True:
        return True
    return False


def check_for_overlap(k, new_query, user_id, finalnewquery):
    # First we search to find the queries this user had previously done.They have one subquery.
    start_queries = db.QueriesCollection.find({"urid": user_id, "query": {"$size": 1}}, {"_id": 0, "query": 1})
    list_queries_to_exam = []
    for query in start_queries:
        list_queries_to_exam.append(query["query"])
    # This is the part of code if this user is not the first time he makes a query.The queries list is not empty.
    if len(list_queries_to_exam) != 0:

        if len(new_query) == 1:
            for i in list_queries_to_exam:
                if check_spatial_overlap(new_query, i) is True:
                    print("spatial overlapping")
                    return True
                elif check_time_overlap(new_query, i) is True:
                    print("time overlapping")
                    return True
                elif check_tag_overlap(new_query, i) is True:
                    print("tag overlapping")
                    return True
        else:
            for i in list_queries_to_exam:
                if check_overlap_by_subqueries_number(new_query, i) is True:
                    pastquery = []
                    for y in i:
                        subquery = SQuery(y[0], y[1], y[2], y[3], y[4], y[5], y[6])
                        pastquery.append(subquery)
                    count1 = len(SQuery.combine(finalnewquery))
                    count2 = len(SQuery.combine(pastquery))
                    if abs(count1 - count2) < k:
                        print("overlapping by subqueries number")
                        return True
    # If queries list is empty (it is the first time the user makes a query) or we do not have overlap, answer false.
    return False
