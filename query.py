from pymongo import MongoClient
client = MongoClient()
db = client.MyDB
collection = db.FirstCollection

class Query:
	""" This class represents a user sub-query """

	def __init__(self, qid,duration=0, realx1=None, realy1=None, realx2=None, realy2=None):
		""" Constructor: Initialize the sub-query and has as members the columns that will be used """
		self.qid = qid
		self.QueryCount = -1
		self.episodes = []
		self.duration = duration
		self.realx1 = realx1
		self.realy1 = realy1
		self.realx2 = realx2
		self.realy2 = realy2

	def distort_area(self,area_dist_unit):
		pass


	def get_results(self):

		"""Returns the trajectories, as tr_ids, that included in the parameters, the user set at the sub-query"""

		#quick return if any of these is None then simply return None
		if self.realx1 == None or self.realx2 == None or self.realy1 == None or self.realy2 == None:
			return None

		documents = db.FirstCollection.find({ "loc": { "$geoWithin": { "$box": [ [self.realx1, self.realy1],
                                                                             [self.realx2, self.realy2] ] } } } )

		trajectories_ids = []

		for doc in documents:
			trajectories_ids.append(doc['MOid'])

		return trajectories_ids

	@staticmethod
	def combine(Q):

		"""The function 'combine' returns the intersection of the results from the user's sub-queries.
			input: Q a list of subqueries of type Query"""

		if Q == None:
			raise ValueError("Argumet is None")

		#first we collect all the results
		total_results = []
		for q in range(len(Q)):
			query_result = Q[q].get_results()
			if query_result != None and query_result != []:
				total_results.append(query_result)

		#now we need to find the intersection in these
		#lists

		#make sure we don't have an empty list if there is
		#only one result set don't bother finding the intersection
		if total_results == [] or len(total_results) == 1:
			return total_results

		results = total_results[0]
		
		for r in range(len(results)):
			results = set(results).intersection(results[r])
		return results
