import constants


class DistortionData:
    """Class DistortionData computes the distortion units for the selected trajectories and finds the preferable
    episode if there is one to include."""

    def __init__(self, area_step=0, time_step=0, distort_area_only=False, distort_time_only=False, distort_area_time=False):
        self.area_step = area_step
        self.time_step = time_step
        self.area_distortion_limit = 0.3
        self.time_distortion_limit = 0.3
        self.area_time_distortion_limit = 0.3
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

    def check_by_distort_time(self, row):

        if self.subqueries == []:
            raise Exception("Subqueries list is empty")

        trace_id = row.get_trace_id()
        subqueries_= self.find_subqueries_not_in_row(row)
        discard_trc_id = False

        for subq in range(len(subqueries_)):

            if discard_trc_id is True:
                break

            time_distortion_unit = 0.0
            query = subqueries_[subq]
            #modify old_time correctly (using mongo probably)
            old_time = query['duration']
            new_time = old_time + self.time_step * old_time
            time_distortion_unit = (new_time - old_time)/old_time

            while time_distortion_unit < self.time_distortion_limit:
                query_result = db.query('form the query chris')

                if query_result is not None and query_result['trace_id'] == trace_id:
                    row.set_subquery_dist_time_unit(subq, time_distortion_unit)
                    break
                old_time = new_time
                new_time = old_time + self.time_step * old_time
                time_distortion_unit = (new_time - old_time)/old_time

                if time_distortion_unit > self.time_distortion_limit:
                    discard_trc_id = True

    def check_by_distort_area_time(self, row):

        if self.subqueries == []:
            raise Exception("Subqueries list is empty")

        trace_id = row.get_trace_id()
        subqueries_ = self.find_subqueries_not_in_row(row)
        discard_trc_id = False

        for subq in range(len(subqueries_)):

            if discard_trc_id is True:
                break

            area_time_distortion_unit = 0.0
            query = subqueries_[subq]
            old_area = query['area']
            new_area = old_area + self.area_step * old_area
            old_time = query['duration']
            new_time = old_time + self.time_step * old_time
            area_time_distortion_unit = (((new_area - old_area)/old_area) + ((new_time - old_time)/old_time))/2

            while area_time_distortion_unit < self.area_time_distortion_limit:
                query_result = db.query('form the query chris')

                if query_result is not None and query_result['trace_id'] == trace_id:
                    row.set_subquery_dist_area_time_unit(subq, area_time_distortion_unit)
                    break
                old_area = new_area
                new_area = old_area + self.area_step * old_area
                old_time = new_time
                new_time = old_time + self.time_step * old_time
                area_time_distortion_unit = (((new_area - old_area)/old_area) + ((new_time - old_time)/old_time))/2

                if area_time_distortion_unit > self.area_time_distortion_limit:
                    discard_trc_id = True

    def check_by_distort_area(self, row):

        if self.subqueries == []:
            raise Exception("Subqueries list is empty")

        #loop over the subqueries of the row and for each subquery iteratively enlarge the area of the subquery
        #for each iteration check with the db by using the enlarged area if the trajectory is contained in the modified
        #subquery. The inner enlargment iterations finish when the overall area_distortion_unit  exceeds a certain
        #area_distortion_limit. if the trajectory id is found before reaching the area_distortion_limit meaning
        #area_distortion_unit < area_distortion_limit the algorithm continues to examine the next subquery, otherwise
        #it marks the whole row as invalid. If the all subqueries are found after distorting the area to contain the
        #trajectory then the smallest distortion is chosen.

        trace_id = row.get_trace_id()
        subqueries_ = self.find_subqueries_not_in_row(row)
        discard_trc_id = False

        for subq in range(len(subqueries_)):

            if discard_trc_id is True:
                break

            area_distortion_unit = 0.0
            query = subqueries_[subq]

            start_area = (query.realx2 - query.realx1)*(query.realy2 - query.realy1)
            x1 = query.realx1
            x2 = query.realx2
            y1 = query.realy1
            y2 = query.realy2
            steps = 1
            new_area = (x2 - x1 + 2*steps*self.area_step)*(y2 - y1 + 2*steps*self.area_step)

            area_distortion_unit = (new_area - start_area)/start_area

            while area_distortion_unit < self.area_distortion_limit:
                #haven't reached the distortion limit yet so query the db by using the new_area
                query_result = db.FirstCollection.find({"loc": {"$geoWithin": {"$box": [
                    [x1-steps*self.area_step, y1-steps*self.area_step], [x2+steps*self.area_step,
                                                                         y2+steps*self.area_step]]}}, 'MOid': trace_id})

                if query_result is not None and query_result['MOid'] == trace_id:
                    row.set_subquery_dist_area_unit(subq, area_distortion_unit)
                    break
                steps += 1
                new_area = (x2 - x1 + 2*steps*self.area_step)*(y2 - y1 + 2*steps*self.area_step)
                area_distortion_unit = (new_area - start_area) / start_area

                if area_distortion_unit > self.area_distortion_limit:
                    discard_trc_id = True

    def check_by_distortion(self, row):

        if self.distort_area_only is True:
            self.check_by_distort_area(row)
            min_dist_area_unit = row.get_min_area_dist_unit()

            if min_dist_area_unit[0] != constants.INVALID_ID:
                #self.subqueries[min_dist_area_unit[0]].distort_area(steps)
                return (row.get_trace_id(),min_dist_area_unit[0],min_dist_area_unit[1])
               #return True
            return (-1,-1,-1)

        elif self.distort_time_only is True:
            self.check_by_distort_time(row)
            min_dist_time_unit = row.get_min_time_dist_unit()

            if min_dist_time_unit[0] != constants.INVALID_ID:
                self.subqueries[min_dist_time_unit[0]].distort_time(min_dist_time_unit[1])
                return True
            return False

        elif self.distort_area_time is True:
            self.check_by_distort_area_time(row)
            min_dist_area_time_unit = row.get_min_area_time_dist_unit()

            if min_dist_area_time_unit[0] != constants.INVALID_ID:
                self.subqueries[min_dist_area_time_unit[0]].distort_area_time(min_dist_area_time_unit[1])
                return True
            return False

        else:
            raise Exception("No valid distortion type. Set either distort_area_only or distort_time_only or "
                            "distort_area_time flag to True. ")

    def compute_rows_distortions(self, rows):
        episode_found = False
        episode_found = []
        for r in range(len(rows)):
            episode_found.append(self.check_by_distortion(rows[r]))
        #loop over episode_found list if a True exists return True else False
        return episode_found





