

class BufferParser:

    @staticmethod
    def get_content(buffer, num: int):
        return buffer.raw.decode().split("\x00")[0:num]


class TableParser:

    def __init__(self, headers: [str], rows: [[str]]):
        self.headers = headers
        self.rows = rows

    @classmethod
    def from_buffers(cls, headers_buffer_dict, content_buffer_dict):
        headers = BufferParser.get_content(headers_buffer_dict["buffer"], headers_buffer_dict["num_of_results"])
        content = BufferParser.get_content(content_buffer_dict["buffer"], content_buffer_dict["num_of_results"])
        rows = [content[i:i + len(headers)] for i in range(0, len(content), len(headers))]
        return cls(headers, rows)

    def to_dict(self):
        return self.__dict__
