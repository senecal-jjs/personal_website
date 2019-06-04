import requests
import unittest
import time


class TestEndPoint(unittest.TestCase):		
	def test_predict(self):
		url = 'http://localhost:80/predict'
		files = {'media': open('web/app/static/search_images/aeroplane/2008_000716.jpg', 'rb')}
		r=requests.post(url, files=files)
		self.assertEqual(r.status_code, 200)

	def test_index(self):
		url = 'http://localhost:80/'
		r = requests.get(url)
		self.assertEqual(r.status_code, 200)

if __name__ == '__main__':
	time.sleep(5)
	unittest.main(verbosity=2)

