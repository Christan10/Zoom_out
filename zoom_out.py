from pymongo import MongoClient
client = MongoClient()
db = client.MyDB
collection = db.FirstCollection

#transfered in query.py

#class Query:
#    """ This class represents a user sub-query """

#    def __init__(self, duration=0, realx1=None, realy1=None, realx2=None, realy2=None):
#        """ Constructor: Initialize the sub-query and has as members the columns that will be used """
#        self.QueryCount = -1
#        self.episodes = []
#        self.duration = duration
#        self.realx1 = realx1
#        self.realy1 = realy1
#        self.realx2 = realx2
#        self.realy2 = realy2

#    def get_results(self):
#        """Returns the trajectories, as tr_ids, that included in the parameters, the user set at the sub-query"""
#        records = db.FirstCollection.find({ "loc": { "$geoWithin": { "$box": [ [self.realx1, self.realy1],
                                                                             [self.realx2, self.realy2] ] } } } )
#        return records

#    @staticmethod
#    def combine(Q):
#        """The function 'combine' returns the intersection of the results from the user's sub-queries"""
#        common_tr_ids = Q[0].get_results()
#        for i in range(len(Q)):
#            common_tr_ids = set(common_tr_ids).intersection(Q[i].get_results())
#        return common_tr_ids

class HRow:
    """Class HRow models one row from the matrix H."""

    def __init__(self, tr_id=-1):
        self.tr_id = tr_id
        self.freq = 0
        self.SQueries = []
        self.SQ_dis_units = []

class HMat:
    """Class HMat represents the matrix H, which is a list from HRow objects."""

    def __init__(self):
			
        self.Hmat = []

    def get_row_with_trace_id(self,tr_id):
			"""For the given trajectory id tr_id returns the row that has this trajectory.
				 if no row is found it returns None 
			"""
        for r in range(len(self.Hmat)):
            row = self.Hmat[r]
            if row.tr_id == tr_id:
                return row
        return None

    def fill(self, tr_id, Q_i):
        """This function checks if a tr_id is already in matrix H. If the answer is yes it increases the frequency
        and adds the sub-query that we examine. If not it adds the tr_id for the first time, with frequency=1 and adds
         the sub-query."""
        row = self.get_row_with_trace_id(tr_id)
        if row not None:
            row.freq +=1
            row.SQueries.append(Q_i)
        else:
            row = HRow(tr_id)
            row.freq =1
            row.SQueries.append(Q_i)
            self.Hmat.append(row)

    def rows(self):
        """It counts how many records matrix H has."""
        return len(self.Hmat)

    def find_next_max_freq(self, k):
        """This function finds the tr_id which: has the maximum frequency, but doesn't exceeds the threshold k."""
        for r in range(len(self.Hmat)):
            row = self.Hmat[r]
        # we want to start with a row that has frequency lower than the threshold k
            if row.freq < k:
                max_freq = row.freq
                z = row.tr_id
            for r in range(len(self.Hmat)):
        # we want to compare the row we started with every row in HMat in order to find the row with the maximum
        # frequency but also < k
                new_row = self.Hmat[r]
                if new_row.freq > max_freq and new_row.freq < k:
                    max_freq = new_row.freq
                    z = new_row.tr_id
            return z


    def compute_distortions(self):
		pass

    def add_new_episode(self):
        pass
def zoom_out(k, Q, Rmin, Rmax):
    F_Q = Q
    Hmat = HMat
    ntr = Query.combine(F_Q)
    sth_changed = False
    while ntr!= k and sth_changed == True:
        sth_changed = False
        for i in range(len(F_Q)):
            rslt = F_Q[i].get_results()
            if rslt is valid:
                Hmat.fill(rslt["tr_id"], F_Q[i])


