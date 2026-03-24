

MAX = 2**15
class Triangle:

    table: list[int] = []
    def __init__(self, table_len: int = 512):
        for i in range(int(table_len/2)):
            self.table.append(int(MAX*2*i/table_len))
        for i in range(int(table_len/2)):
            self.table.append(int(MAX*(2*i/table_len-1)))
