from app import app
import json
import unittest


class FlaskEndPointTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    def test_search_no_query(self):
        result = self.app.get('/search')
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.get_data(as_text=True))
        self.assertEqual(data['result'], [])

    def test_search_with_query(self):
        result = self.app.get('/search?term=test')
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.get_data(as_text=True))
        self.assertEqual(data['result'], ['test'])

    def test_404(self):
        result = self.app.get('/wrong?term=test')
        self.assertEqual(result.status_code, 404)

if __name__ == '__main__':
    unittest.main()
