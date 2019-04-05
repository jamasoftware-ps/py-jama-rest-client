from unittest import TestCase
from core import Core
import os


class TestCore(TestCase):
    jama_url = os.environ['JAMA_API_URL']
    jama_api_username = os.environ['JAMA_API_USERNAME']
    jama_api_password = os.environ['JAMA_API_PASSWORD']
    core = Core(jama_url, (jama_api_username, jama_api_password))

    def test_delete(self):
        self.fail()

    def test_get(self):
        response = self.core.get('projects')
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, len(response.json()['data']) > 0)

    def test_patch(self):
        self.fail()

    def test_post(self):
        self.fail()

    def test_put(self):
        self.fail()

    def test_oauth(self):
        oauth_core = Core(TestCore.jama_url,
                          (os.environ['JAMA_CLIENT_ID'], os.environ['JAMA_CLIENT_SECRET']),
                          oauth=True)
        response = oauth_core.get('projects')
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, len(response.json()['data']) > 0)







