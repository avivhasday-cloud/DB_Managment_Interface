from ctypes import *
from python.bindings.utils.enums import enum_resultset_metadata, mysql_status, enum_field_types

class st_mysql_options(Structure):
    pass

class MYSQL_METHODS(Structure):
    pass



class LIST(Structure):
    pass

class LIST(Structure):
    _fields_ = [
        ("prev", POINTER(LIST)),
        ("next", POINTER(LIST)),
        ("data", POINTER(c_void_p))
    ]

class MEM_ROOT(Structure):
    pass

class Vio(Structure):
    pass

class CHARSET_INFO(Structure):
    pass

class NET(Structure):
    _fields_ = [
        ("vio", Vio),
        ("buff", POINTER(c_ubyte)),
        ("buff_end", POINTER(c_ubyte)),
        ("write_pos", POINTER(c_ubyte)),
        ("read_pos", POINTER(c_ubyte)),
        ("remain_in_buf", c_ulong),
        ("length", c_ulong),
        ("buf_length", c_ulong),
        ("where_b", c_ulong),
        ("max_packet", c_ulong),
        ("max_packet_size", c_ulong),
        ("pkt_nr", c_ulong),
        ("compress_pkt_nr", c_ulong),
        ("write_timeout", c_ulong),
        ("read_timeout", c_ulong),
        ("retry_count", c_ulong),
        ("fcntl", c_int),
        ("return_status", POINTER(c_ulong)),
        ("reading_or_writing", c_ubyte),
        ("save_char", c_ubyte),
        ("compress", c_bool),
        ("last_errno", c_uint),
        ("error", c_ubyte),
        ("last_error", c_char),
        ("sqlstate", c_char),
        ("extension", POINTER(c_void_p))

    ]

class MYSQL_FIELD(Structure):
    _fields_ = [
        ("name", POINTER(c_char)),
        ("org_name", POINTER(c_char)),
        ("table", POINTER(c_char)),
        ("org_table", POINTER(c_char)),
        ("db", POINTER(c_char)),
        ("catalog", POINTER(c_char)),
        ("def", POINTER(c_char)),
        ("length", c_ulong),
        ("max_length", c_ulong),
        ("name_length", c_ulong),
        ("org_name_length", c_ulong),
        ("table_length", c_ulong),
        ("org_table_length", c_ulong),
        ("db_length", c_ulong),
        ("catalog_length", c_ulong),
        ("def_length", c_ulong),
        ("flags", c_ulong),
        ("decimals", c_ulong),
        ("charsetnr", c_ulong),
        ("type", enum_field_types),
        ("extension", POINTER(c_void_p))
    ]

class MYSQL(Structure):
    _fields_ = [
        ("net", NET),
        ("connector_fd", POINTER(c_ubyte)),
        ("host", c_char_p),
        ("user", c_char_p),
        ("passwd", c_char_p),
        ("unix_socket", c_char_p),
        ("server_version", c_char_p),
        ("host_info", c_char_p),
        ("info", c_char_p),
        ("db", c_char_p),
        ("charset", c_char_p),
        ("fields", c_char_p),
        ("field_alloc", c_char_p),
        ("affected_rows", c_ulonglong),
        ("insert_id", c_ulonglong),
        ("extra_info", c_ulonglong),
        ("thread_id", c_ulong),
        ("packet_length", c_ulong),
        ("port", c_uint),
        ("client_flag", c_ulong),
        ("server_capabilities", c_ulong),
        ("protocol_version", c_uint),
        ("field_count", c_uint),
        ("server_status", c_uint),
        ("server_language", c_uint),
        ("warning_count", c_uint),
        ("options", st_mysql_options),
        ("status", mysql_status),
        ("resultset_metadata", enum_resultset_metadata),
        ("free_me", c_bool),
        ("reconnect", c_bool),
        ("scramble", c_char),
        ("stmts", POINTER(LIST)),
        ("methods", POINTER(MYSQL_METHODS)),
        ("thd", POINTER(c_void_p)),
        ("unbuffered_fetch_owner", POINTER(c_bool)),
        ("extension", POINTER(c_void_p)),

    ]

MYSQL_ROW = POINTER(c_char_p)


class MYSQL_ROWS(Structure):
    pass

class MYSQL_ROWS(Structure):
    _fields_ = [
        ("next", POINTER(MYSQL_ROWS)),
        ("data", MYSQL_ROW),
        ("length", c_ulong)

    ]

class MYSQL_DATA(Structure):
    _fields_ = [
        ("data", POINTER(MYSQL_ROWS)),
    ]

class MYSQL_RES(Structure):
    _fields_ = [
        ("row_count", c_uint64),
        ("fields", MYSQL_FIELD),
        ("data", POINTER(MYSQL_DATA)),
        ("data_cursor", POINTER(MYSQL_ROWS)),
        ("lengths", POINTER(c_ulong)),
        ("handle", POINTER(MYSQL)),
        ("methods", POINTER(MYSQL_METHODS)),
        ("row", MYSQL_ROW),
        ("current_row", MYSQL_ROW),
        ("field_alloc", MEM_ROOT),
        ("field_count", c_ulong),
        ("current_field", c_ulong),
        ("eof", c_bool),
        ("unbuffered_fetch_cancelled", c_bool),
        ("metadata", enum_resultset_metadata),
        ("extension", POINTER(c_void_p))        
    ]
