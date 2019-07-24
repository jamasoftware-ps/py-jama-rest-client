import json
import time
import os
import unittest
from unittest import TestCase
from py_jama_rest_client.client import JamaClient


class TestJamaClient(TestCase):
    jama_url = os.environ['JAMA_API_URL']
    jama_api_username = os.environ['JAMA_API_USERNAME']
    jama_api_password = os.environ['JAMA_API_PASSWORD']
    jama_client = JamaClient(jama_url, (jama_api_username, jama_api_password))

    def test_get_projects(self):
        projects = self.jama_client.get_projects()
        self.assertIsNotNone(projects)

    def test_get_items(self):
        project_id = 116
        items = self.jama_client.get_items(project_id)
        self.assertIsNotNone(items)
        self.assertGreater(len(items), 0)

    def test_get_filter_results(self):
        filter_id = 151
        filter_id_with_cur_proj = 162
        project_id = 115

        #test without project id
        filter_results = self.jama_client.get_filter_results(filter_id)
        self.assertIsNotNone(filter_results)
        self.assertGreater(len(filter_results), 0)

        #test with project id
        filter_results = self.jama_client.get_filter_results(filter_id_with_cur_proj, project_id)
        self.assertIsNotNone(filter_results)
        self.assertGreater(len(filter_results), 0)

    def test_get_item(self):
        item_id = 66977
        item = self.jama_client.get_item(item_id)
        self.assertIsNotNone(item)

    def test_get_attachment(self):
        attachment_id = 67548
        attachment = self.jama_client.get_attachment(attachment_id)
        self.assertIsNotNone(attachment)

    def test_get_relationship_types(self):
        relationship_types = self.jama_client.get_relationship_types()
        self.assertIsNotNone(relationship_types)
        self.assertGreater(len(relationship_types), 1)

    def test_get_relationship_type(self):
        relationship_id = 4
        relationship = self.jama_client.get_relationship_type(relationship_id)
        relationship_name = relationship.get('name')
        self.assertIsNotNone(relationship)
        self.assertEqual(relationship_name, 'Related to')

    def test_get_relationship(self):
        relationship_id = 1184
        relationship = self.jama_client.get_relationship(relationship_id)
        from_item = relationship.get('fromItem')
        to_item = relationship.get('toItem')
        self.assertIsNotNone(relationship)
        self.assertEqual(from_item, 66999)
        self.assertEqual(to_item, 66998)

    def test_get_relationships(self):
        project_id = 116
        relationships = self.jama_client.get_relationships(project_id)
        self.assertIsNotNone(relationships)
        self.assertGreater(len(relationships), 1)

    def test_get_tags(self):
        project_id = 116
        tags = self.jama_client.get_tags(project_id)
        self.assertIsNotNone(tags)
        self.assertGreater(len(tags), 1)

    def test_get_item_types(self):
        item_types = self.jama_client.get_item_types()
        self.assertIsNotNone(item_types)
        self.assertGreater(len(item_types), 1)

    def test_get_item_type(self):
        item_type_id = 184
        item_type = self.jama_client.get_item_type(item_type_id)
        self.assertEqual(item_type.get('id'), item_type_id)
        self.assertEqual(item_type.get('display'), 'Suggestion')

    def test_get_abstract_items_from_doc_key(self):
        doc_key_list = ['UT-CMP-1', 'UT-CMP-4', 'UT-CMP-5']
        items = self.jama_client.get_abstract_items_from_doc_key(doc_key_list)
        self.assertIsNotNone(items)
        self.assertEqual(len(items), len(doc_key_list))

    def test_get_pick_lists(self):
        pick_lists = self.jama_client.get_pick_lists()
        self.assertIsNotNone(pick_lists)
        self.assertGreater(len(pick_lists), 1)

    def test_get_pick_list(self):
        pick_list_id = 62
        pick_list = self.jama_client.get_pick_list(pick_list_id)
        self.assertIsNotNone(pick_list)
        self.assertEqual(pick_list.get('name'), 'Priority')

    def test_get_pick_list_options(self):
        pick_list_id = 62
        pick_list_options = self.jama_client.get_pick_list_options(pick_list_id)
        self.assertIsNotNone(pick_list_options)
        self.assertGreater(len(pick_list_options), 1)

    def test_get_pick_list_option(self):
        pick_list_option_id = 300
        pick_list_option = self.jama_client.get_pick_list_option(pick_list_option_id)
        self.assertIsNotNone(pick_list_option)
        self.assertEqual(pick_list_option.get('name'), 'Low')

    def test_get_items_upstream_relationships(self):
        item_id = 66977
        upstream_relationships = self.jama_client.get_items_upstream_relationships(item_id)
        self.assertIsNotNone(upstream_relationships)
        self.assertEqual(len(upstream_relationships), 1)

    def test_get_items_downstream_relationships(self):
        item_id = 66977
        downstream_relationships = self.jama_client.get_items_downstream_relationships(item_id)
        self.assertIsNotNone(downstream_relationships)
        self.assertEqual(len(downstream_relationships), 2)

    def test_get_abstract_items(self):
        project = 116
        item_type = 104
        items = self.jama_client.get_abstract_items(project=project, item_type=item_type)
        self.assertIsNotNone(items)

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

    def test_get_item_children(self):
        item_id = 66979
        children = self.jama_client.get_item_children(item_id)
        self.assertIsNotNone(children)
        self.assertEqual(len(children), 2)

    def test_put_test_run(self):
        test_run_id = 66985
        data_to_send = {"fields": {"status": "PASS"}}
        data_to_send = json.dumps(data_to_send)
        res_status = self.jama_client.put_test_run(test_run_id, data=data_to_send)
        self.assertEqual(200, res_status)

    def test_get_available_endpoints(self):
        projects = self.jama_client.get_available_endpoints()
        self.assertIsNotNone(projects)
        self.assertEqual(len(projects), 24)

    def test_patch_item(self):
        test_item_id = 77962
        patches = [
            {
                "op": "replace",
                "path": "/fields/name",
                "value": "PATCHED: "
            }
        ]

        res_status = self.jama_client.patch_item(test_item_id, patches)
        self.assertEqual("OK", res_status)

    @unittest.skip('Entity Already Exists')
    def test_post_relationship(self):
        from_item = 104755
        to_item = 104752
        relationship_type = 4
        relationship = self.jama_client.post_relationship(from_item, to_item, relationship_type)
        self.assertIsNotNone(relationship)
        #

    @unittest.skip('Entity Already Exists')
    def test_post_tag(self):
        project_id = 116
        tag_name = 'Test_tag'
        tag_id = self.jama_client.post_tag(tag_name, project_id)
        self.assertIsNotNone(tag_id)

    def test_post_items(self):
        project_id = 116
        item_type = 104
        child_item_type = 104
        location = {
            'item': 66997
        }
        embedded_image = '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAPAAAADSCAMAAABD772dAAAA2FBMVEX////' \
                         'BEhwAAAD8/Pz19fXi4uKdnZ3FxcVtbW07OzvKSEzAAA3ACBW8AADVfH6pqanx8fFmZmbq6urd3d3S0tLs7OzKysrV1d' \
                         'Wurq51dXW5ubnGxsa/v7+0tLSjo6OQkJBPT0+JiYmZmZlYWFhzc3NISEiKiop9fX0wMDBgYGBVVVU0NDRBQUEqKir78' \
                         'PH88/T14OHGPkL25OXw0NHx1NXqwMHQamzipqgcHBzclJXmtLbNXmDBIicRERHZh4nDLDHNX2LbkpPHQkbkra7LU1bX' \
                         'goTTdHbCJizWsPXtAAAPeklEQVR4nO1da4ObthJlFz9w7I3fz7XBz/W7adom3abZJmnS9v//o6uRhC3bmgG8YAPX50s' \
                         'IeIFBQjM6ZzQYxg033HDDDTfccMMNNyQaJse17+JCYJZmMhWGTCbzf2A0s7ZSy2brgGytknaTubn1Rivf7/X6+Vajnn' \
                         'KTmb3M3P7AHjsMY7vTb9VrKbbYNCu1dr4zHlmrZdWyqsv5uNxvZ1kjX/vOogGzN9vo26PqzM6CiWatPJnbvUa2ktI2Z' \
                         'v250cvNN2Nlnz3JDRrZdDYxs7fN7C00xH/fiX8ak3GvXUulxWalnrfnhRZs//rx/ef3Xz/AZmuZ69ebKezUZibb6owm' \
                         'I9j++lAslUrFhx/QzM683GKv8ZVvL3RAhx441Q0Y9v7hTuDhPRwaOoNG+jq17NCPbPMP115m8V+G7NRpa2IYoTuj5ZR' \
                         't/rK3l1n8M9szh06driY2M812z7G2Gbb9o6gYXIJOnRk6vXYzVRazkOPRns86bPO72sCsiX9n+wZVO5+qTg0devC0nM' \
                         'Dmob3M4p/Y3uWok6ZxyzSb9f54usiy7Y/FI4OLP9je2nCcpk4NLrg8H0JI+etxA7MmhvgjN7UfU+OMpQsuwPZ/pROD7' \
                         '+7AzlWKnDFzwf1cl8fQf502MGvit+xIfZWaCFPElKs52/xZZy+z+Dd2bJQWZyxd8Bpc8Btdh2bO+Av8buakY9okYspN' \
                         'j23+rm9g1sR/sKP5ZS4NzljGlEu2+RNmL7P4F3bcGnVaiW9i1qGZC7a4C/7z2AXvUfyTHa9sUuCMIaYsz2c22/yANzB' \
                         'r4k/sF2Ur8c6Yx5ROdQibd/oRy7UY7Fw+Jd0ZCxe8bbPNf6gGdp3xcAzO+Np3fT5ETLkCWuc32l5m8a9G4uke4YKrBT' \
                         'DgC9mh76QzNmbOIMHOWNI6fYNwwUoTJ94ZSxdsGUe0DmoxOOPuvJPUCBM6NHPB24pxROugnfoN+2UluTNjSeuU2eYnP' \
                         'w3Mmvg7+23HsvOJHLckrbMyNLQOajHQPZNk0j0urVNn2//66dCA4lf26+wKnHHiLJYu2DG0tA7axOCMx90Ezoy5VOhU' \
                         '17Ctd8H6nZ/BziRqL+CCc10uFf6hbeCS/jE8/GOAhMq1lyRZzBoYpMKugbtgZDKRTO2Fx5Rjaw0uWE/rPHxAXm0eYWa' \
                         'SRvcIF7wZGCfKikTxIzv0r/YQ1156ydJeFBf8Tu+RuMOljlWfEuSMBa0zXQOt81VrFG9FLADjzri5GfcS44xpZeVOBs' \
                         '2AN/rHAdqLnRztRSorM9jUKitiJAYgIzineyaJoXuEC16gyorIcxDQ+2jujNtJ0V48lZXSnfJrJPxIkPYilZUCKCvvM' \
                         'Re8h57q4okQCaF7mAsGWgdXVrgL3gNxxkD39KsJoHskrVM1UGWl+O7wD7Q/EnTPdBR/uke44G3TQF3w96O/0AsSJUiE' \
                         'aMaf7mEdmrngWc5ADfn75G/0khPXXpgzjjfdoygrBuJifzn5I6rrr2IeYQKtw1wwrqzwwegY+sHtAQa3+iTWdA+PKUe' \
                         'EsiLUhRMg7gvonqc4O2OprCxgmwgoToEEKP/BsTjTPVxZ6W5AWUFCxn+Rv0RC0G9GrFNthQuegLLizwUrQEY4mGRMRz' \
                         'Ht1DAL7o2tBVdWvGPKQyA+LNaptp7KCs/jwHCSgikeEUQpMU21FbQOd8Hv9FIwp24wIC+BSLWNpTMWysoalBWktX4n/' \
                         '54g+2qzGNI9ktbBlRUx4yNAzCVzXTtuiRDqmpVALngPxBmX4Fj8Um0FrbMGWuebF62DgfhDqb1EboZvyEVYsGYFSZgt' \
                         '+jgL0TVipr2oyooPWgcD8vLDhNLcxIruEbSOl7LijY+U9hIjuofHlE9UwizpgvegHLgVn0QImdzwXDPOdMF7ENpLjNa' \
                         '9KMoKERL7gz69yXXG8dBeJK0DyoqBdMmfvc6xA6aewzRr6MSjU4uE2bUvZcUbyEQaUm3bnO65uvYiaJ0Joaz8F+h8cd' \
                         'de3GWjfB00Tk35B0GGmcMYOGPPNSs+XfAeb3G6M399usdbWXlAaR0MBKFtjcrXrYHh0jrgggkBIRj0vq0oUm2vTPeAs' \
                         'mJTa1a4RBQUxKMrXzfVVnHBJuKCT5UVb1Cc5+SaztjkLni6BmWFkHmDA9FegNXODq+ovZyrrHgDccZXXvcCLnjgWMSa' \
                         'FU9aBwPy/CA5xLye9iJpnaNSJKq9b88+N6W9XCvVVior4IKpdKszT/6ZSLW9jvYiaR2urBAJdecC8XLgjDPXWYQqE2a' \
                         'hFMkZyoo3CCphYF1Be5HKCk+YDdEF7/ETkmoLzrh6ebrHpXUgYZZIe34NCDrwCs7YW1k51wXvQWiu40vTPaqygixdON' \
                         'cF76Ef+6+z7kUmzOJrVng+7GuBaC983YsopBfCRXzBm9b5HMq9IPHbxde9qNXA0DUrYYAQXjNA91xq3PJes/I6F7yHf' \
                         'tHipde9KMrKu7BoHexSBN0DzvgynZqqBibu5zhh9nwgQdxFa46JhFlqzcppwuz5ILSXC617kbTOxqBzu8MCMhErCbrn' \
                         'Es5YUVaQhNlvoV6PmGrXhxdwxpLWoVxwyFdElj4B3XMB7cWtBhaasuINhO6B53oB7cWzFEkRS5g9H0SqeeTai3c1sNB' \
                         'c8B7vtBdy172Uo6w5JkuRLGDNCuIvgisr3kC0F3DGEdM9SsIscRPhg9BeOlHSPaqyQnSz8IGxovD6RFnVlseU3S0vRR' \
                         'KmsuINQnquR0f3SFrnyUBjymDJDUGAzEKl9hJNhKlWAyOCgWiABDlf4GZmEUWYUSor3iAShCJa94IVeVcQacRDLK6Ph' \
                         'O6RysrzSZH3/bXDoXUwUNpLFIkQ3spKNC54j8tqL0qRd4zW8Zcwez6o64bujNUi7wSxFi0QwvCrIWqOhdqpBa1DVAML' \
                         'kDB7PghVNjcNdd2LWuSdUKqjBqK98FTbcNe9KNXACPkjeniXOQnnOnLNCl4NrBSpC1aAdK+Q172oRd7/vnRMeQiq5lh' \
                         '4dA/r0D6qgV0GhPjeD0t74S54xKuBXY7WwUClV4RUYt4t8k4kzIanrHiDCPNCKjHvXYrkjec5wgTBpYWivbjJDQadLH' \
                         'Y5RF1zTJQi4bQOkZt/SRCptvXVq9e9yAqzoKwQCZ+XRZRlTlRlhUjpvSyoVOXXLkKVykreIEqRDMoobPYm1Gzdkd7+G' \
                         'pX8aHLvYmGNBk02/BDnrFCq5Su1F2XNCq7T3hPYsmeuPyI/YGpkrZNDHSNDnbOLjp6vLjEvlJXpMyTM4uQ/dXMLwxjq' \
                         'j9TFJUbaZ1GjzjknF5S8qsS8dykScMHUzbEJZVV/pMmvoG1+NtpS54RcC6IY2ytKzEtlhSjyzjsRdXPMfXf1R/gV5ro' \
                         'j7DVoUOeENUMI3VN8Hd0jq4F5uWAPg3WdVhqsNuRzobAVW6zLPnoZTGov55aYly6YUFZEwqw9HTl2p//YaszkLa0arV' \
                         'a+V86NpuxhOXJntTfolO2c8zTvTi2x2nj3LHI1ec16fr6B4WzeHY3LA3bO1rP8idNqPfYH5fFoXuG/JOapvMR88E7tX' \
                         'eT9JGF2KW9uqu7M3e8a7hhr117iNmSz3+eP9mNLd5md5nl0j6gGRrvgI7jjk6XutHU7D40p+zC4f3yA0l7OKXMii7xT' \
                         '31k5OaOls63sdunTayzkoZfsGQZjedpnai9qKRLf1cCmui7tGrw8vcg+wOqiJi9Qg+lU26Al5pXP5/pfs+Ia3NUZrGn' \
                         'hjjL2zsoZ0uDjd9igtZegdI9UVoZGoITZOWXwtmtZ1eVkuFk838tI2ny5VzEZaO6QMBhb98JLzAdzxlJZWRMJszplhT' \
                         'RYhfuSn/hbpxLAYLLEfLCaY2dWAwtssOagHcBgD+3FP92j0DqBlJXgBhuNl+Njs8NGJg3Gvv0Kx4LQPUGKvL/S4H0kt' \
                         'sPLwehFGkxrL77pHkVZocq2ncKdJ2gNfh7OZoX1Yvv88nLfUX+QsY9aeejf4FDKnEhaZ+GzyLuCoIHHDo3DadNAY/Cp' \
                         'H+agSsz7pXuCFnnfY0oZrAk81IsOlKnx2r/BIZSY95EwiyU3aGNpfwYztLY7i2v7vXhoKYCl2sqaY96d2l02GqDI+w7' \
                         'ubOmg97qTh4mXwYbpTi9d/kc1uIf9FREI+ioxL5UVohQJntww0RnsTg+HngYb7VODTXc+3EH/iipz4l1iXq0GhkRuuL' \
                         'Iy1Bk8ljs33gbXTw3OuAbjU0jsu9V83YtnVVuxZoUq8k6sWXG75MHr6vrZRTabrdfb7UYLuItOjt1Fpms3lF/W3Qf2s' \
                         'r/DjOuyjiMwBZT24lVzzPPzueQ66ILOYC1RJyzgr/ez5Thjx3lS2E3FjzfdfWPiuoT24tB0j6B1rIXHWTC4lM3B+DS9' \
                         '14P10RVySBmkdwy1Q1yXqjlG0z2S1sHXrDyQyQ2uzxyqOxFeGvSFkzhaQB2Qs+7OEXVhYt3LI6W9eBd5L5HJDa7BB+M' \
                         'TojywcKqtP3DgcXfjWNegQIyvXTzCdKuBgQs+pxrYbj6/VU+/1pvF7DqZNgCmzYNz7gymIlPyMylEzbFXVwOzl1XA8s' \
                         'CF9MTOY0zaRn++PbJ2WW4endKci58vGwYJJEbi614wukfSOuCCqe/zhYvsY7/MxmhnXO63jo0NAioKRr4oyGPKnCjyH' \
                         'lEpkiiBRJi8zIme7pG0DvEF+9LbGOMvpFMK7UWTaqsmzOqXF7DnFWfob1lULtc5Y7lmBS9FklBgJeZZh254KCsJhb7m' \
                         'mFsNDE+YTSz4dJaXmFfHLc9SJAmGrsQ8H7FkNTC/H3RPDmTNMXXcEiPWFi/ynmiIEvMrddyCApVPE5iB6WPKhEPUHOP' \
                         'ymmswizm6BWhgvcqccPAlGZmZ/egO1Gam3h/zN1g/C048+Lg1He/6NHuFew7v0X+msYGla3JGg/bO4HbvacUmdaae10' \
                         'k+QE/MMYObqsGQPKRP50gB+KilGMy6NM+Z1aujiQfXT+dPg907zAct+CY0RmonHDwntKAMWtwt8cDy00MKO7X4mKC1d' \
                         '0uGCYFHlXNvHz4/FEtpQvGhBHGHOeQpEAdzhxVnBs1Pb9+kCW8/8VbtTlUqT8wOpzOaC00yutXD3DyY/w+c6XDjwYYm' \
                         'FI2h5XQaKq1lAic9GM+X60mnZqYLtcFy2HU6rWzlkPKoZBs9+6m7HC62hTRhUZh0R7leK3tE1ILF7fzAdkaQsZ4eTOc' \
                         'jJzfItw/bV1icqdUbj71O2bZzqYFtlzu9fKNeO7EX3uNMpZatN1qtx3xq8NhqNepZMFerprFWrjRrtWyKUKs1Kxm9ud' \
                         'JmZnS6YF79s3I33HDDDTfcgOB/zPIbdHl4DXkAAAAASUVORK5CYII=" >'
        fields = {
            'name': 'testing post',
            'description': 'this was posted through the API via the python client.' + embedded_image,
            'custom_field': 'this field needs to be appended with $ item type to post properly'
        }

        item_id = self.jama_client.post_item(project_id, item_type, child_item_type, location, fields)
        self.assertIsNotNone(item_id)

    def test_put_attachments_file(self):
        project_id = 116

        name = 'test_image.png'
        description = 'Item posted by python client automated testing'

        item_id = self.jama_client.post_project_attachment(project_id, name, description)
        # Ensure the attachment item posted
        self.assertIsNotNone(item_id)

        # Now upload the file
        file_to_upload = 'test_image.png'
        upload_status = self.jama_client.put_attachments_file(item_id, file_to_upload)

        # Ensure the upload was a success
        self.assertEqual(upload_status, 200)

    def test_get_items_synceditems(self):

        # get synced items
        synced_items = self.jama_client.get_items_synceditems(71038)

        self.assertIsNotNone(synced_items)

        self.assertGreater(len(synced_items), 0)

    def test_get_items_synceditems_syncstatus(self):

        # get status
        sync_status = self.jama_client.get_items_synceditems_status(71038, 149715)

        self.assertIsNotNone(sync_status)

        self.assertFalse(sync_status.get('inSync'))

    def test_get_item_lock(self):
        item_id = 71038

        #get lock status
        lock_status = self.jama_client.get_item_lock(item_id)

        self.assertIsNotNone(lock_status)
        self.assertIsNotNone(lock_status.get('locked'))

    def test_put_item_lock(self):
        item_id = 71038

        self.jama_client.put_item_lock(item_id, True)
        self.jama_client.put_item_lock(item_id, False)

    @unittest.skip('Entity Already Exists')
    def test_post_item_attachment(self):
        # TODO Can only run this once... need to make anew item and post a new attachment to it each time
        item_id = 66972
        attachment_id = 67548

        res_status = self.jama_client.post_item_attachment(item_id, attachment_id)
        self.assertEqual(res_status, 201)

    @unittest.skip('Entity Already Exists')
    def test_post_item_tag(self):
        item_id = 66972
        tag_id = 25

        res_status = self.jama_client.post_item_tag(item_id, tag_id)
        self.assertEqual(res_status, 201)

    def test_post_testplan_testcycles(self):
        testplan_id = 66982
        testplan_name = 'unittest'

        testcycle_id = self.jama_client.post_testplans_testcycles(testplan_id,
                                                                  testplan_name,
                                                                  '2018-10-19',
                                                                  '2020-01-01')
        self.assertIsNotNone(testcycle_id)
