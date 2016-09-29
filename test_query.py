from query import*
import unittest

class TestQuery(unittest.TestCase):
	"""Class that performs unit testing on the Query class"""

	def setUp(self):
		pass

	def test_get_results1(self):
		"""Test the get_results function with empty query"""
		print("Testing empty query")
		#create the query-empty
		q = Query()
		results = q.get_results()

		#this should return None
		self.assertEqual(None,results)

	def test_get_results2(self):
		"""Test the get_results function with query"""
		print("Testing  query")
		q = Query(0,476342.1468,4204003.745,481957.3449995738,4205906.679483968)
		results = q.get_results()
		
		#make sure this is a list
		islist = isinstance(results,list)
		self.assertEqual(True,islist)

	def test_combine(self):
		"""Test the static mehtod combine in Query"""
		print("Testing Query.combine")
		q1 = Query(0,0.0,0.0,5000.0,5000.0)
		q2 = Query(0,-1.0,-1.0,5000.0*0.5,5000.0*0.5)
		results = Query.combine([q1,q2])

		#make sure this is a list
		islist = isinstance(results,list)
		self.assertEqual(True,islist)


if __name__ =='__main__':
	unittest.main()
		
	
