from datetime import datetime, timedelta
import unittest
from app import create_app
from config import Config


class TestConfig(Config):
    TESTING = True

class DeploymentCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def test_status_code(self):
        c = self.app.test_client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main(verbosity=2)
