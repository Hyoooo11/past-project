class TableBuilder:
    def __init__(self):
        self.table = "<table>"
        self.tr_open = "<tr>"
        self.td_open = "<td>"
        self.table_close = "</table>"
        self.tr_close = "</tr>"
        self.td_close = "</td>"
        self.table_rows = []
 
    def tr(self, user_input):
        return [self.tr_open] + user_input + [self.tr_close]
 
    def td(self, user_input):
        return self.tr([self.td_open + x + self.td_close for x in user_input])
 
    def add_row(self, user_input):
        result = self.td(user_input)
        self.table_rows.append(result)
 
    def remove_last_row(self):
        if self.table_rows:
            self.table_rows.pop()
 
    def build_table(self):
        output = [self.table]
        for row in self.table_rows:
            output.append("  " + row[0])
            for cell in row[1:-1]:
                output.append("    " + cell)
            output.append("  " + row[-1])
        output.append(self.table_close)
        return "\n".join(output)