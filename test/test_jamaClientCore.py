from unittest import TestCase
from jama.core import Core


class TestCore(TestCase):
    def test_get(self):
        my_jama_client = Core('https://your_jama_instance.jamacloud.com', ('mchalen', 'password'))
        response = my_jama_client.get('projects')
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, len(response.json()['data']) > 0)

