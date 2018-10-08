from unittest import TestCase
from jama.core import Core


class TestCore(TestCase):

    core = Core('https://your_jama_instance.jamacloud.com', ('username', 'password'))

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





