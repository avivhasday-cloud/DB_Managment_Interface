from python.bindings.wrappers.mysql_wrapper import MySQLCWrapper
from python.bindings.utils.parsers import BufferParser
import unittest

DUMMY_HOST = "127.0.0.1"
DUMMY_USER = "root"
DUMMY_PASSWD = "root"
DUMMY_DB = "test"
DUMMY_STATEMENT = "SELECT * FROM Users"
DUMMY_PORT = 1552
DUMMY_SIZE = 4096


class TestMySQLWrapper(unittest.TestCase):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.mysql_wrapper = MySQLCWrapper()

    def setUp(self) -> None:
        super().setUp()
        self.mysql_wrapper.connect_to_mysql(DUMMY_HOST, DUMMY_USER, DUMMY_PASSWD, None, DUMMY_PORT)

    def tearDown(self) -> None:
        super().tearDown()
        self.mysql_wrapper.close_connection()


    def connect_to_dummy_db(self, db: str = DUMMY_DB):
        return self.mysql_wrapper.connect_to_db(db)

    def execute_dummy_query(self, statement: str = DUMMY_STATEMENT):
        return self.mysql_wrapper.execute_query(statement)

    def execute_dummy_query_and_get_results(self, statement: str = DUMMY_STATEMENT):
        buffer, num_of_results = self.mysql_wrapper.execute_query_and_get_results(statement)
        return BufferParser.get_content(buffer, num_of_results)

    def get_dummy_databases(self, keyword: str = None):
        return self.mysql_wrapper.get_databases(keyword)

    def get_table_details_by_dummy_query(self, statement: str):
        return self.mysql_wrapper.get_table_details_by_query(statement)

    def test_connect_to_db(self):
        self.assertEqual(1, self.connect_to_dummy_db(db=DUMMY_DB))
        self.assertNotEqual(1, self.connect_to_dummy_db(db="Dummy"))
    
    def test_execute_query(self):
        self.connect_to_dummy_db(db=DUMMY_DB)
        res = self.execute_dummy_query(statement=DUMMY_STATEMENT)
        self.assertNotEqual(None, res)
        res = self.execute_dummy_query(statement="SELECT * FROM Dummies")
        self.assertEqual(None, res)

    def test_get_databases(self):
        expected_value = ['information_schema', 'mysql', 'performance_schema', 'sys', 'test']
        self.assertEqual(expected_value, self.get_dummy_databases())
        expected_value = ["test"]
        self.assertEqual(expected_value, self.get_dummy_databases("test"))
        self.assertNotEqual(expected_value, self.get_dummy_databases("bla"))

    def test_execute_query_and_get_results(self):
        self.assertEqual(1, self.connect_to_dummy_db(db=DUMMY_DB))
        expected_value = ['1','test_full_name_1','test_email_1','test_hashed_password_1','2','test_full_name_2','test_email_2','test_hashed_password_2']
        self.assertEqual(expected_value, self.execute_dummy_query_and_get_results(statement=DUMMY_STATEMENT))
        self.assertNotEqual(expected_value, self.execute_dummy_query_and_get_results(statement="SELECT * FROM Dummies"))
        self.assertEqual(list(), self.execute_dummy_query_and_get_results(statement="SELECT * FROM Dummies"))

    def test_get_table_details_by_query(self):
        self.assertEqual(1, self.connect_to_dummy_db(db=DUMMY_DB))
        expected_value = {'headers': ['id', 'full_name', 'email', 'hashed_password'], 'rows': [['1','test_full_name_1','test_email_1','test_hashed_password_1'], ['2','test_full_name_2','test_email_2','test_hashed_password_2']]}
        self.assertEqual(expected_value, self.get_table_details_by_dummy_query(statement=DUMMY_STATEMENT))

if __name__ == '__main__':
    unittest.main()