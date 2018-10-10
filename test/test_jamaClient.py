import json
from unittest import TestCase
from jama.client import JamaClient


class TestJamaClient(TestCase):
    jama_client = JamaClient('https://your_jama_instance.jamacloud.com', ('username', 'password'))

    def test_get_projects(self):
        projects = self.jama_client.get_projects()
        self.assertIsNotNone(projects)

    def test_get_items(self):
        project_id = 116
        items = self.jama_client.get_items(project_id)
        self.assertIsNotNone(items)
        self.assertGreater(len(items), 0)

    def test_get_abstract_items_from_doc_key(self):
        doc_key_list = ['UT-CMP-1', 'UT-CMP-4', 'UT-CMP-5']
        items = self.jama_client.get_abstract_items_from_doc_key(doc_key_list)
        self.assertIsNotNone(items)
        self.assertEqual(len(items), len(doc_key_list))

    def test_get_testruns(self):
        test_cycle_id = 66983
        test_runs = self.jama_client.get_testruns(test_cycle_id)
        self.assertIsNotNone(test_runs)
        self.assertEqual(len(test_runs), 2)

    def test_get_test_cycle(self):
        test_cycle_id = 66983
        test_cycle = self.jama_client.get_test_cycle(test_cycle_id)
        self.assertIsNotNone(test_cycle)
        self.assertEqual(test_cycle['id'], test_cycle_id)

    def test_put_test_run(self):
        test_run_id = 66985
        data_to_send = {"fields": {"status": "PASS"}}
        data_to_send = json.dumps(data_to_send)
        res_status = self.jama_client.put_test_run(test_run_id, data=data_to_send)
        self.assertEqual(res_status, 200)

    def test_post_items(self):
        project_id = 116
        item_type = 104
        child_item_type = 104
        location = {
            'item': 66997
        }
        fields = {
            'name': 'testing post',
            'description': 'this was posted through the API via the python client.',
            'custom_field': 'this field needs to be appended with $ item type to post properly'
        }

        item_id = self.jama_client.post_item(project_id, item_type, child_item_type, location, fields)
        self.assertIsNotNone(item_id)

