from pymongo import MongoClient
client = MongoClient()
db = client.MyDB
collection = db.FirstCollection


class Query:
    """ This class represents a user sub-query """

    def __init__(self, qid, duration=1, realx1=None, realy1=None, realx2=None, realy2=None, episodes = 'MOVE'):
        """ Constructor: Initialize the sub-query and has as members the columns that will be used """
        self.qid = qid
        self.episodes = episodes
        self.duration = duration
        self.realx1 = realx1
        self.realy1 = realy1
        self.realx2 = realx2
        self.realy2 = realy2

    def distort_area(self, steps_, areastep, randnumber):
        """This function changes the query bounding box properly in order to include a new trajectory"""
        self.realx1 -= (steps_ * areastep) * randnumber
        self.realy1 -= (steps_ * areastep) * randnumber
        self.realx2 += (steps_ * areastep) * randnumber
        self.realy2 += (steps_ * areastep) * randnumber

    def distort_time(self, steps_, timestep):
        self.duration += steps_ * timestep

    def distort_area_time(self, steps_, areastep, timestep, randnumber):
        self.realx1 -= (steps_ * areastep) * randnumber
        self.realy1 -= (steps_ * areastep) * randnumber
        self.realx2 += (steps_ * areastep) * randnumber
        self.realy2 += (steps_ * areastep) * randnumber
        self.duration += steps_ * timestep

    def get_results(self):
        """Returns the trajectories, as tr_ids, that included in the parameters, the user set at the sub-query"""

        #quick return if any of these is None then simply return None
        if self.realx1 is None or self.realx2 is None or self.realy1 is None or self.realy2 is None:
            return None

        documents = db.FirstCollection.find({"loc": {"$geoWithin": {"$box": [[self.realx1, self.realy1],
                                                                             [self.realx2, self.realy2]]}},
                                             "duration": {"$lt": self.duration}, "episodes": self.episodes})

        trajc_ids = []

        for doc in documents:
            trajc_ids.append(doc['MOid'])
        traj_id = set(trajc_ids)
        trajectories_ids = list(traj_id)
        return trajectories_ids

    @staticmethod
    def combine(Q):

        """The function 'combine' returns the intersection of the results from the user's sub-queries.
        input: Q a list of subqueries of type Query"""

        if Q is None:
            raise ValueError("Argument is None")

        #first we collect all the results
        total_results = []
        stopper = 0
        for q in range(len(Q)):
            query_result = Q[q].get_results()
            if query_result is not None and query_result != []:
                total_results.append(query_result)
            else:
                stopper = 1

        if stopper == 1:
            raise ValueError("one or more queries have no trajectory as a result")

        results = total_results[0]

        for r in range(len(total_results)):
            results = set(results).intersection(total_results[r])
        result = list(results)
        return result
