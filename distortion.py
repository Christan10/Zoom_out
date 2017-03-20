import constants
from zoom_out import *
from pymongo import MongoClient
client = MongoClient()
db = client.MyDB
collection = db.FirstCollection


class DistortionData:
    """Class DistortionData computes the distortion units for the selected trajectories and finds the preferable
    episode if there is one to include."""

    def __init__(self, area_step=0, time_step=0, distort_area_only=False, distort_time_only=False,
                 distort_area_time=False):
        self.area_step = area_step
        self.time_step = time_step
        self.area_distortion_limit = 10000.0
        self.time_distortion_limit = 0.2
        self.area_time_distortion_limit = 0.2
        self.subqueries = []
        self.distort_area_only = distort_area_only
        self.distort_time_only = distort_time_only
        self.distort_area_time = distort_area_time

    def find_subqueries_not_in_row(self, row):
        """This function finds and returns a list (found[]) with the subqueries who do not contain episode of the
        trajectory (they are not included in the SQueries[] list for the trajectory we examine)"""
        found = []

        for subq in range(len(self.subqueries)):
            if row.subquery_exists(self.subqueries[subq].qid) is True:
                continue
            else:
                found.append(self.subqueries[subq])
        return found

    def set_subqueries(self, subqueries):
        """Initializes the subqueries[] list (we use this in the driver code to load the user's subqueries"""

        if subqueries is None or subqueries == []:
            raise Exception("Invalid subqueries list")
        self.subqueries = subqueries

    def check_by_distort_area_time(self, row):

        trace_id = row.get_trace_id()
        subqueries_ = self.find_subqueries_not_in_row(row)
        discard_trc_id = False
        to_add = []

        for subq in range(len(subqueries_)):

            if discard_trc_id is True:
                break

            query_ = subqueries_[subq]
            start_area = (query_.realx2 - query_.realx1) * (query_.realy2 - query_.realy1)
            x1 = query_.realx1
            x2 = query_.realx2
            y1 = query_.realy1
            y2 = query_.realy2
            steps = 1
            new_area = (x2 - x1 + 2 * steps * self.area_step) * (y2 - y1 + 2 * steps * self.area_step)
            start_time = query_.duration
            new_time = start_time + self.time_step * steps
            area_time_distortion_unit = (((new_area - start_area)/start_area) + ((new_time - start_time)/start_time))/2

            while area_time_distortion_unit < self.area_time_distortion_limit:
                q_r = db.FirstCollection.find({"loc": {"$geoWithin": {"$box": [
                    [x1-steps*self.area_step, y1-steps*self.area_step],
                    [x2+steps*self.area_step, y2+steps*self.area_step]]}}, "duration": {"$lt": new_time},
                    "episodes": query_.episodes, 'MOid': trace_id})
                query_rslt = []
                for i in q_r:
                    query_rslt.append(i['MOid'])
                q_reslt = set(query_rslt)
                query_result = list(q_reslt)
                out = False
                for i in query_result:
                    if query_result is not None and i == trace_id:
                        elements = [subqueries_[subq].qid, area_time_distortion_unit, steps]
                        to_add.append(elements)
                        out = True
                        break
                if out is True:
                    break
                steps += 1
                new_area = (x2 - x1 + 2 * steps * self.area_step) * (y2 - y1 + 2 * steps * self.area_step)
                new_time = start_time + self.time_step * steps
                area_time_distortion_unit = (((new_area - start_area)/start_area) + ((new_time - start_time)/start_time)
                                             )/2

                if area_time_distortion_unit > self.area_time_distortion_limit:
                    discard_trc_id = True

        if discard_trc_id is not True:
            for i in to_add:
                row.set_subquery_dist_area_unit(i[0], i[1], i[2])

    def check_by_distort_area(self, row):

        #loop over the subqueries of the row and for each subquery iteratively enlarge the area of the subquery
        #for each iteration check with the db by using the enlarged area if the trajectory is contained in the modified
        #subquery. The inner enlargment iterations finish when the overall area_distortion_unit  exceeds a certain
        #area_distortion_limit. If the trajectory id is found before reaching the area_distortion_limit meaning
        #area_distortion_unit < area_distortion_limit the algorithm continues to examine the next subquery, otherwise
        #it marks the whole row as invalid. If the all subqueries are found after distorting the area to contain the
        #trajectory then the smallest distortion will be chosen.

        trace_id = row.get_trace_id()
        subqueries_ = self.find_subqueries_not_in_row(row)
        discard_trc_id = False
        to_add = []

        for subq in range(len(subqueries_)):

            if discard_trc_id is True:
                break

            query_ = subqueries_[subq]
            start_area = (query_.realx2 - query_.realx1)*(query_.realy2 - query_.realy1)
            x1 = query_.realx1
            x2 = query_.realx2
            y1 = query_.realy1
            y2 = query_.realy2
            steps = 1
            new_area = (x2 - x1 + 2*steps*self.area_step)*(y2 - y1 + 2*steps*self.area_step)
            area_distortion_unit = (new_area - start_area)/start_area

            while area_distortion_unit < self.area_distortion_limit:
                #haven't reached the distortion limit yet so query the db by using the new_area
                q_r = db.FirstCollection.find({"loc": {"$geoWithin": {"$box": [
                    [x1-steps*self.area_step, y1-steps*self.area_step], [x2+steps*self.area_step,
                                                                         y2+steps*self.area_step]]}}, "duration":
                    {"$lt": query_.duration}, "episodes": query_.episodes, 'MOid': trace_id})
                query_rslt = []
                for i in q_r:
                    query_rslt.append(i['MOid'])
                q_reslt = set(query_rslt)
                query_result = list(q_reslt)
                out = False
                for i in query_result:
                    if query_result is not None and i == trace_id:
                        elements = [subqueries_[subq].qid, area_distortion_unit, steps]
                        to_add.append(elements)
                        out = True
                        break
                if out is True:
                    break
                steps += 1
                new_area = (x2 - x1 + 2*steps*self.area_step)*(y2 - y1 + 2*steps*self.area_step)
                area_distortion_unit = (new_area - start_area) / start_area

                if area_distortion_unit > self.area_distortion_limit:
                    discard_trc_id = True

        if discard_trc_id is not True:
            for i in to_add:
                row.set_subquery_dist_area_unit(i[0], i[1], i[2])

    def check_by_distort_time(self, row):

        trace_id = row.get_trace_id()
        subqueries_ = self.find_subqueries_not_in_row(row)
        discard_trc_id = False
        to_add = []

        for subq in range(len(subqueries_)):

            if discard_trc_id is True:
                break

            query_ = subqueries_[subq]
            x1 = query_.realx1
            x2 = query_.realx2
            y1 = query_.realy1
            y2 = query_.realy2
            start_time = query_.duration
            steps = 1
            new_time = start_time + self.time_step * steps
            time_distortion_unit = (new_time - start_time)/start_time

            while time_distortion_unit < self.time_distortion_limit:
                q_r = db.FirstCollection.find({"loc": {"$geoWithin": {"$box": [[x1, y1], [x2, y2]]}},
                                               "duration": {"$lt": new_time}, "episodes": query_.episodes,
                                               'MOid': trace_id})
                query_rslt = []
                for i in q_r:
                    query_rslt.append(i['MOid'])
                q_reslt = set(query_rslt)
                query_result = list(q_reslt)
                out = False
                for i in query_result:
                    if query_result is not None and i == trace_id:
                        elements = [subqueries_[subq].qid, time_distortion_unit, steps]
                        to_add.append(elements)
                        out = True
                        break
                if out is True:
                    break
                steps += 1
                new_time = start_time + self.time_step * steps
                time_distortion_unit = (new_time - start_time)/start_time

                if time_distortion_unit > self.time_distortion_limit:
                    discard_trc_id = True

        if discard_trc_id is not True:
            for i in to_add:
                row.set_subquery_dist_area_unit(i[0], i[1], i[2])

    def check_by_distortion(self, row):

        if self.distort_area_only is True:
            self.check_by_distort_area(row)
            min_dist_area_unit = row.get_min_area_dist_unit()

            if min_dist_area_unit[0] != constants.INVALID_ID:
                return [row.get_trace_id(), min_dist_area_unit[0], min_dist_area_unit[1], min_dist_area_unit[2]]
            return [-1, -1, -1, -1]

        elif self.distort_time_only is True:
            self.check_by_distort_time(row)
            min_dist_time_unit = row.get_min_time_dist_unit()

            if min_dist_time_unit[0] != constants.INVALID_ID:
                return [row.get_trace_id(), min_dist_time_unit[0], min_dist_time_unit[1], min_dist_time_unit[2]]
            return [-1, -1, -1, -1]

        elif self.distort_area_time is True:
            self.check_by_distort_area_time(row)
            min_dist_area_time_unit = row.get_min_area_time_dist_unit()

            if min_dist_area_time_unit[0] != constants.INVALID_ID:
                return [row.get_trace_id(), min_dist_area_time_unit[0], min_dist_area_time_unit[1],
                        min_dist_area_time_unit[2]]
            return [-1, -1, -1, -1]

        else:
            raise Exception("No valid distortion type. Set either distort_area_only or distort_time_only or "
                            "distort_area_time flag to True. ")

    def compute_rows_distortions(self, rows, ran_num):
        episode_found = []
        minimum_dist_unit = constants.LARGE_VALUE
        steps_ = constants.INVALID_ID
        subquery = constants.INVALID_ID
        for r in range(len(rows)):
            episode_found.append(self.check_by_distortion(rows[r]))
        #loop over episode_found list if a True exists return True else False
        for x in episode_found:
            if x[2] != -1 and x[2] < minimum_dist_unit:
                minimum_dist_unit = x[2]
                steps_ = x[3]
                subquery = x[1]

        if minimum_dist_unit != constants.LARGE_VALUE:
            if self.distort_area_only is True:
                for q in self.subqueries:
                    if q.qid == subquery:
                        q.distort_area(steps_, self.area_step, ran_num)
            elif self.distort_time_only is True:
                for q in self.subqueries:
                    if q.qid == subquery:
                        q.distort_time(steps_, self.time_step)
            else:
                for q in self.subqueries:
                    if q.qid == subquery:
                        q.distort_area_time(steps_, self.area_step, self.time_step, ran_num)
            return True
        return False
