from python.configure import Config
from ctypes import *
from python.bindings.utils.structures import MYSQL, MYSQL_RES
from python.bindings.utils.parsers import BufferParser, TableParser


class MySQLCWrapper:
    """
    This Class is a wrapper for MySQL function from c shared-lib
    """

    ENCODED_FORMAT = 'utf8'
    QUERY_DATABASES_STATEMENT = "SHOW DATABASES;"
    QUERY_TABLES_STATEMENT = "SHOW TABLES FROM"
    QUERY_TABLE_COLUMNS_STATEMENT = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS"

    def __init__(self, path_to_shared_lib: str = Config.SHARED_LIB_PATH) -> None:
        print(path_to_shared_lib)
        self._shared_c_lib = CDLL(path_to_shared_lib)
        self.initialize_shared_lib()
        self.mysql_pointer = self._get_mysql_object()


 

    def initialize_shared_lib(self):
        """
        Initialize arguments types and return types for each function imported from c shared lib
        :return:
        :rtype:
        """
        self._shared_c_lib.init_mysql_object.argtypes = []
        self._shared_c_lib.init_mysql_object.restype = POINTER(MYSQL)

        self._shared_c_lib.close_connection_to_mysql.argtypes = [POINTER(MYSQL)]
        self._shared_c_lib.close_connection_to_mysql.restype = None

        self._shared_c_lib.connect_to_db.argtypes = [POINTER(MYSQL), c_char_p]
        self._shared_c_lib.connect_to_db.restype = c_int

        self._shared_c_lib.execute_query.argtypes = [POINTER(MYSQL), c_char_p]
        self._shared_c_lib.execute_query.restype = POINTER(MYSQL_RES)

        self._shared_c_lib.execute_query_and_get_results.argtypes = [POINTER(MYSQL), c_char_p, c_char_p]
        self._shared_c_lib.execute_query_and_get_results.restype = c_int

        self._shared_c_lib.get_databases.argtypes = [POINTER(MYSQL), c_char_p, c_char_p]
        self._shared_c_lib.get_databases.restype = c_int

        self._shared_c_lib.get_table_name.argtypes = [POINTER(MYSQL_RES)]
        self._shared_c_lib.get_table_name.restype = c_char_p

        self._shared_c_lib.get_database_name.argtypes = [POINTER(MYSQL)]
        self._shared_c_lib.get_database_name.restype = c_char_p

        self._shared_c_lib.get_results.argtypes = [POINTER(MYSQL_RES), c_char_p]
        self._shared_c_lib.get_results.restype  = c_int

        self._shared_c_lib.connect_to_mysql.argtypes = [POINTER(MYSQL), c_char_p, c_char_p, c_char_p, c_char_p, c_uint, c_char_p, c_uint]
        self._shared_c_lib.connect_to_mysql.restype = c_int
    
    def _get_mysql_object(self) -> POINTER(MYSQL):
        """
        This Function return a MySQL object
        :return: Pointer to MySQL object
        :rtype: POINTER(MYSQL)
        """
        return self._shared_c_lib.init_mysql_object()

    def connect_to_mysql(self, host: str, user: str, password: str, db: str, port: int = 3306, socket: str = None, flags: int = 0) -> int:
        """
        This Function tries to connect to MySql database, on success returns 1 on failure returns 0
        :param host: hostname (example: localhost)
        :type host: str
        :param user: MySQL username
        :type user: str
        :param password: MySQL password
        :type password: str
        :param db: database name
        :type db: str
        :param port: MySQL service port (default 3306)
        :type port: int
        :param socket: unix socket (default None)
        :type socket: str
        :param flags: MySQL connection flags (default 0)
        :type flags: int
        :return: 1 if sucessfull login else 0
        :rtype: int
        """
        host_ptr = c_char_p(host.encode())
        user_ptr = c_char_p(user.encode())
        passwd_ptr = c_char_p(password.encode())
        db_ptr = c_char_p(db.encode()) if db else None
        return self._shared_c_lib.connect_to_mysql(self.mysql_pointer, host_ptr, user_ptr, passwd_ptr, db_ptr, c_uint(port), socket, c_uint(flags))

    def close_connection(self):
        """
        Closing connection to MySQL database
        :return:
        :rtype:
        """
        self._shared_c_lib.close_connection_to_mysql(self.mysql_pointer)
    
    def connect_to_db(self, db_name: str) -> int:
        """
        This Function tries to connect to Database, on Success returns 1 else 0
        :param db_name: Database name
        :type db_name: str
        :return: 1 or 0
        :rtype: int
        """
        db_ptr = c_char_p(db_name.encode())
        return self._shared_c_lib.connect_to_db(self.mysql_pointer, db_ptr)
    
    def execute_query(self, statement: str) -> [POINTER(MYSQL_RES), None]:
        """
        This Function execute query and return pointer to MYSQL_RES if successfully executed else None
        :param statement: MySQL statement string
        :type statement: str
        :return: pointer to MYSQL_RES or None
        :rtype: POINTER(MYSQL_RES)
        """
        statement_ptr = c_char_p(statement.encode(MySQLCWrapper.ENCODED_FORMAT))
        res = self._shared_c_lib.execute_query(self.mysql_pointer, statement_ptr)
        try:
            if isinstance(res.contents, str):
                res = None
        except ValueError:
            res = None
        return res
    
    def execute_query_and_get_results(self, statement: str) -> [str]:
        """
        This Function execute query and get num of results, returns the query output.
        :param statement: MySQL statment string
        :type statement: str
        :return: list of query results
        :rtype: [str]
        """
        statement_ptr = c_char_p(statement.encode(MySQLCWrapper.ENCODED_FORMAT))
        buffer = create_string_buffer(4096)
        num_of_results = self._shared_c_lib.execute_query_and_get_results(self.mysql_pointer, statement_ptr, buffer)
        return buffer, num_of_results

    def get_table_columns(self, db_name: str,  table_name: str):
        statement = f"{MySQLCWrapper.QUERY_TABLE_COLUMNS_STATEMENT} WHERE TABLE_SCHEMA = '{db_name}' AND TABLE_NAME = '{table_name}' ORDER BY ordinal_position;"
        return self.execute_query_and_get_results(statement)

    def _get_table_name(self, query_results: POINTER(MYSQL_RES)) -> str:
        table_name_ptr = self._shared_c_lib.get_table_name(query_results)
        return table_name_ptr.decode()

    def _get_database_name(self):
        db_name_ptr = self._shared_c_lib.get_database_name(self.mysql_pointer)
        return db_name_ptr.decode()

    def get_databases(self, wild_keyword: str = None) -> [str]:
        buffer = create_string_buffer(4096)
        wild_keyword_ptr = c_char_p(wild_keyword.encode()) if wild_keyword else None
        num_of_results = self._shared_c_lib.get_databases(self.mysql_pointer, wild_keyword_ptr, buffer) 
        return BufferParser.get_content(buffer, num_of_results)

    def get_table_details_by_query(self, statement: str) -> dict:
        query_res_ptr = self.execute_query(statement)
        table_name = self._get_table_name(query_res_ptr)
        content, content_num_of_results = self.get_results(query_res_ptr)
        table_columns, headers_num_of_results = self.get_table_columns(self._get_database_name(), table_name)
        table = TableParser.from_buffers({"buffer": table_columns, "num_of_results": headers_num_of_results}, {"buffer": content, "num_of_results": content_num_of_results})
        return table.to_dict()

    def get_results(self, query_results: POINTER(MYSQL_RES)) -> [str]:
        buffer = create_string_buffer(4096)
        num_of_results = self._shared_c_lib.get_results(query_results, buffer)
        return buffer, num_of_results
