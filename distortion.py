import constants


class DistortionData:
    """Class DistortionData computes the distortion units for the selected trajectories and finds the preferable
    episode if there is one to include."""

    def __init__(self, area_step=0, time_step=0, area_time_step=0):
        self.area_step = area_step
        self.time_step = time_step
        self.area_time_step = area_time_step
        self.area_distortion_limit = 0.1
        self.subqueries = []
        self.distort_area_only = False
        self.distort_time_only = False
        self.distort_area_time = False

    def find_subqueries_not_in_row(self, row):
        found = []

        for subq in range(len(self.subqueries)):
            if row.subquery_exists(self.subqueries[subq].qid) is True:
                continue
            else:
                found.append(self.subqueries[subq])
        return found

    def set_subqueries(self, subqueries):

        if subqueries is None or subqueries == []:
            raise Exception("Invalid subqueries list")

        self.subqueries = subqueries

    def check_by_distort_time(self, row):
        #similar to check_by_distort_area
        pass

    def check_by_distort_area_time(self, row):
        pass

    def check_by_distort_area(self, row):

        if self.subqueries == []:
            raise Exception("Subqueries list is empty")

        #loop over the subqueries of the row
        #and for each subquery iteratively enlarge the area of the subquery
        #for each iteration check with the db by using the  enlarged area
        #if the trajectory is contained in the modified
        #subquery. The inner enlargment iterations finish when the overall
        #area_distortion_unit  exceeds  a certain area_distortion_limit
        #if the trajectory id is found before reaching the area_distortion_limit
        #meaning area_distortion_unit < area_distortion_limit
        #the algorithm continues to examine the next subquery, otherwise it marks
        #the whole row as invalid. If the all subqueries are found after distorting the
        #area to contain the trajectory then the smallest distortion is chosen.

        trace_id = row.get_trace_id()
        subqueries_ = self.find_subqueries_not_in_row(row)
        discard_trc_id = False

        for subq in len(subqueries_):

            if discard_trc_id == True:
                break

            area_distortion_unit = 0.0
            query = subqueries_[subq]

            #this will have to change
            old_area = query['area']

            new_area = old_area + self.area_step*old_area

            area_distortion_unit = (new_area - old_area)/old_area

            while area_distortion_unit < self.area_distortion_limit:
                #haven't reached the distortion limit yet
                #query the db by using the new_area
                query_result = db.query('form the query')

                if query_result is not None and query_result['trace_id'] == trace_id:
                    row.set_subquery_dist_area_unit(subq, area_distortion_unit)
                    break
                old_area = new_area
                new_area = old_area + self.area_step * old_area
                area_distortion_unit = (new_area - old_area) / old_area

                if area_distortion_unit > self.area_distortion_limit:
                    discard_trc_id = True

    def check_by_distortion(self, row):
        if self.distort_area_only is True:
            self.check_by_distort_area(row)
            min_dist_area_unit = row.get_min_area_dist_unit()

            if min_dist_area_unit[0] != constants.INVALID_ID:
                self.subqueries[min_dist_area_unit[0]].distort_area(min_dist_area_unit[1])
                return True

            return False

        elif self.distort_time_only is True:
            self.check_by_distort_time(row)
        elif self.distort_area_time is True:
            self.check_by_distort_time(row)
        else:
            raise Exception("No valid distortion type. Set either distort_area_only or distort_time_only or "
                            "distort_area_time flag to True. ")

    def compute_rows_distortions(self, rows):
        episode_found = False
        for r in range(len(rows)):
            episode_found = self.check_by_distortion(rows[r])
        return episode_found





