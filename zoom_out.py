from query import SQuery
from distortion import *
import constants
import random
from pymongo import MongoClient
client = MongoClient()
db = client.MyDB
collection = db.FirstCollection


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

    def set_subquery_dist_area_unit(self, sbqid, area_dist_unit, steps):
        if self.subquery_exists(sbqid) is True:
            raise Exception("Attempt to add area distortion for subquery that does not need distortion")
        self.SQ_dis_units.append({'type': 'area_dist', 'id': sbqid, 'value': area_dist_unit, 'steps': steps})

    def set_subquery_dist_time_unit(self, sbqid, time_dist_unit, steps):
        if self.subquery_exists(sbqid) is True:
            raise Exception("Attempt to add time distortion for subquery that does not need distortion")
        self.SQ_dis_units.append({'type': 'time_dist', 'id': sbqid, 'value': time_dist_unit, 'steps': steps})

    def set_subquery_dist_area_time_unit(self, sbqid, area_time_dist_unit, steps):
        if self.subquery_exists(sbqid) is True:
            raise Exception("Attempt to add area-time distortion for subquery that does not need distortion")
        self.SQ_dis_units.append({'type': 'area_time_dist', 'id': sbqid, 'value': area_time_dist_unit, 'steps': steps})

    def get_min_area_dist_unit(self):
        """This function finds the sub-query id (sbqid) that has the minimum distortion unit value (only for area
        distortion) from a row's SQ_dis_units, and returns it with the value."""
        min_dist = constants.MIN_DIST
        sbqid = constants.INVALID_ID
        step = constants.INVALID_ID
        for e in range(len(self.SQ_dis_units)):
            map = self.SQ_dis_units[e]
            if map['type'] == 'area_dist':
                dist_val = map['value']

                if dist_val < min_dist:
                    min_dist = dist_val
                    sbqid = map['id']
                    step = map['steps']

        return (sbqid, min_dist, step)

    def get_min_time_dist_unit(self):
        """This function finds the sub-query id (sbqid) that has the minimum distortion unit value (only for time
        distortion) from a row's SQ_dis_units, and returns it with the value."""
        min_dist = constants.MIN_DIST
        sbqid = constants.INVALID_ID
        step = constants.INVALID_ID
        for e in range(len(self.SQ_dis_units)):
            map = self.SQ_dis_units[e]
            if map['type'] == 'time_dist':
                dist_val = map['value']

                if dist_val < min_dist:
                    min_dist = dist_val
                    sbqid = map['id']
                    step = map['steps']

        return (sbqid, min_dist, step)

    def get_min_area_time_dist_unit(self):
        """This function finds the sub-query id (sbqid) that has the minimum distortion unit value (for area and time
        distortion) from a row's SQ_dis_units, and returns it with the value."""
        min_dist = constants.MIN_DIST
        sbqid = constants.INVALID_ID
        step = constants.INVALID_ID
        for e in range(len(self.SQ_dis_units)):
            map = self.SQ_dis_units[e]
            if map['type'] == 'area_time_dist':
                dist_val = map['value']

                if dist_val < min_dist:
                    min_dist = dist_val
                    sbqid = map['id']
                    step = map['steps']

        return (sbqid, min_dist, step)


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
        threshold k (k here is the sum of sub-queries the user set)."""
        trajectories = []

        for r in range(len(self.Hmat)):
            row = self.Hmat[r]

            if row.freq < k and row.freq == freq:
                trajectories.append(row)
        return trajectories


def zoom(K, Q, Rmin, Rmax, distortion):

    F_Q = Q
    ntr = len(SQuery.combine(F_Q))
    # We print the ids of these common trajectories.
    print(SQuery.combine(F_Q))
    if ntr >= K or ntr == 0:
        raise Exception("algorithm will not run")

    sth_changed = True
    k = len(F_Q)

    while ntr < K and sth_changed is True:
        sth_changed = False
        hmat = HMat()
        for i in range(len(F_Q)):
            f_q = F_Q[i]
            rslt = f_q.get_results()
            # We print the ids of the trajectories for each subquery.
            print(rslt)
            if rslt is not None:
                for r in rslt:
                    hmat.fill(r, f_q)

        freq = hmat.get_init_max_freq(k)

        next_max_freq_rows = hmat.find_next_max_freq_rows(k, freq)
        episode_found = False
        # We set row_counter=ntr to include the rows already satisfing the criteria (k=len(F_Q))
        row_counter = ntr

        # safeguard we should not be here if this condition is True
        if row_counter == hmat.rows():
            raise Exception("row_counter should not be equal to H matrix number of rows")

        hrows = hmat.rows()

        while episode_found is False and row_counter != hrows:

            random_number = random.uniform(Rmin, Rmax)
            row_counter += len(next_max_freq_rows)
            episode_found = distortion.compute_rows_distortions(next_max_freq_rows, random_number)

            if episode_found is True:
                sth_changed = True
                ntr = len(SQuery.combine(F_Q))
                print(ntr)
                print(SQuery.combine(F_Q))
            if episode_found is False:
                freq = hmat.get_next_max_freq(k, freq)
                next_max_freq_rows = hmat.find_next_max_freq_rows(k, freq)

    return F_Q
