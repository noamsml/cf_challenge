import unittest
from storage.transacters import TestTransacter
from storage import schema

class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.transacter = TestTransacter()
        self.clear_all_data()
        self.integrationSetUp()

    def integrationSetUp(self):
        pass

    def clear_all_data(self):
        with self.transacter.raw_connection() as conn:
            schema.metadata.drop_all(conn)
            schema.metadata.create_all(conn)
