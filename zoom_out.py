import constants
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
#                                                                             [self.realx2, self.realy2] ] } } } )
#        return records


class HRow:
    """Class HRow models one row from the matrix H."""

    def __init__(self, tr_id=constants.INVALID_ID, freq=constants.INVALID_ID):
        self.tr_id = tr_id
        self.freq = freq
        self.SQueries = []
        self.SQ_dis_units = []

    def get_trace_id(self):
        if self.tr_id < 0:
            raise Exception("Invalid trace id")
        return self.tr_id

    def subquery_exists(self, qid):
        """This function returns true if the sub-query with id qid is in the list SQueries. Else it returns false."""
        for subquery in self.SQueries:
            if subquery.qid == qid:
                return True
        return False

    def set_subquery_dist_area_unit(self, sbqid, area_dist_unit):
        if self.subquery_exists(sbqid) is True:
            raise Exception("Attempt to add area distortion for subquery that does not need distortion")
        self.SQ_dis_units.append({'type': 'area_dist', 'id': sbqid, 'value': area_dist_unit})

    def set_subquery_dist_time_unit(self, sbqid, time_dist_unit):
        if self.subquery_exists(sbqid) is True:
            raise Exception("Attempt to add time distortion for subquery that does not need distortion")
        self.SQ_dis_units.append({'type': 'time_dist', 'id': sbqid, 'value': time_dist_unit})

    def set_subquery_dist_area_time_unit(self, sbqid, area_time_dist_unit):
        if self.subquery_exists(sbqid) is True:
            raise Exception("Attempt to add area-time distortion for subquery that does not need distortion")
        self.SQ_dis_units.append({'type': 'area_time_dist', 'id': sbqid, 'value': area_time_dist_unit})

    def get_min_area_dist_unit(self):
        """This function finds the sub-query id (sbqid) that has the minimum distortion unit value (only for area
        distortion) from a row's SQ_dis_units, and returns it with the value."""
        min_dist = constants.MIN_DIST
        sbqid = constants.INVALID_ID
        rslt = (sbqid, min_dist)
        for e in range(len(self.SQ_dis_units)):
            map = self.SQ_dis_units[e]
            for key in map.keys():
                if key == 'type' and map[key] == 'area_dist':
                    dist_val = map['value']

                    if dist_val < min_dist:
                        min_dist = dist_val
                        sbqid = map['id']
        rslt[0] = sbqid
        rslt[1] = min_dist
        return rslt



class HMat:
    """Class HMat represents the matrix H, which is a list from HRow objects."""

    def __init__(self):
        self.Hmat = []

    def get_row_with_trace_id(self, tr_id):
        """For the given trajectory id tr_id returns the row that has this trajectory. if no row is found it
		returns None"""
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
        if row is not None:
            row.freq += 1
            row.SQueries.append(Q_i)
        else:
            row = HRow(tr_id=tr_id, freq=1)
            row.SQueries.append(Q_i)
            self.Hmat.append(row)

    def rows(self):
        """It counts how many records matrix H has."""
        return len(self.Hmat)

    def get_init_max_freq(self, k):
        """This function finds the next max frequency as number from the row frequencies of matrix H for the first time.
        next_max_freq must be < k where k here is the sum of sub-queries the user set (as his total query). """
        next_max_freq = constants.INVALID_ID

        for r in range(len(self.Hmat)):
            row = self.Hmat[r]
            row_freq = row.freq

            if row_freq < k:
                if row_freq > next_max_freq:
                    next_max_freq = row_freq
        return next_max_freq

    def get_next_max_freq(self, k, freq):
        """This function finds the next max frequency as number from the row frequencies of matrix H. NOT for the first
         time."""
        next_max_freq = constants.INVALID_ID

        for r in range(len(self.Hmat)):
            row = self.Hmat[r]
            row_freq = row.freq

            if row_freq < k and row_freq < freq:
                if row_freq > next_max_freq:
                    next_max_freq = row_freq
        return next_max_freq

    def find_next_max_freq_rows(self, k, freq):
        """This function finds the tr_ids which: have the maximum frequency (=freq), but don't exceed the
        threshold k."""
        trajectories = []

        for r in range(len(self.Hmat)):
            row = self.Hmat[r]

            if row.freq < k and row.freq == freq:
                trajectories.append(row.tr_id)
        return trajectories



def zoom(k, Q, Rmin, Rmax,distortion):

    return None

    #F_Q = Q
    #hmat = HMat()
    #ntr = Query.combine(F_Q)
    #sth_changed = False
    #freq = INVALID_ID
    #k = len(F_Q)
    iterations_started = False

    #while ntr != k and sth_changed is True:
        #sth_changed = False
        #for i in range(len(F_Q)):
        #    rslt = F_Q[i].get_results()
        #    if rslt is not None:
        #        for r in rslt:
        #            hmat.fill(rslt[r], F_Q[i])
        #
        # if iterations_started == False:
        #    freq = hmat.get_init_max_freq(k)
        #    iterations_started = True
        #
        #next_max_freq_rows = hmat.find_next_max_freq(k,freq)
        #episode_found = False
        #row_counter = 0
        #hrows = hmat.rows()
        #
        # while episode_found is False and row_counter != hrows:
        #loop over the rows and compute distortions
        #
        #  row_counter += len(next_max_freq_rows)
        #  episode_found = distortion.compute_rows_distortions(next_max_freq_rows)
        #  if episode_found == True:
        #   sth_changed = True
        #   ntr = Query.combine(F_Q)
        #  if episode_found == False:
        #   freq = hmat.get_next_max_freq(k,freq)
        #
        #
        #
        #
        #
        #best_query_id = -1
        #best_tr_id = -1
        #episode_found = False
        #hrows = hmat.rows()
        #row_counter = 0
        #while episode_found is False and row_counter != hrows:
        #    D_Unit_St
        #    hmat.compute_distortions(row_max_next_trace, D_Unit_St)
   #return F_Q



