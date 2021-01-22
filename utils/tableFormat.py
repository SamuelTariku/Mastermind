
class Table():
    def __init__(self, header, spacing=15):
        self.header = header
        self.spacing = spacing
        self.data = []
        self.isAutoSpacing = True
        self.auto_spacing = [0] * len(header)

        self.padding = 1
        self.padding_f = " " * self.padding

        self.header_f = self.padding_f + \
            (("{:>" + str(spacing) + "} ") * (len(header))) + self.padding_f
        self.row_f = self.padding_f + \
            ("{:>" + str(spacing) + "}|") * (len(header)) + self.padding_f

    def addRow(self, data):
        self.data.append(data)

    def setData(self, data):
        self.data = data

    def setPadding(self, padding=1):
        self.padding = padding
        self.padding_f = " " * self.padding

    def setAutoSpacing(self, isAutoSpacing=True):
        self.isAutoSpacing = isAutoSpacing

    def auto_header_sizing(self):
        for i in range(0, len(self.header)):
            if(len(self.header[i]) > self.auto_spacing[i]):
                self.auto_spacing[i] = len(self.header[i])

    def auto_header_format(self):
        headerFormat = []
        for i in range(0, len(self.header)):
            headerFormat.append(
                self.padding_f + ("{:>" + str(self.auto_spacing[i]) + "} ") + self.padding_f)

        self.header_f = "".join(headerFormat)

    def auto_data_sizing(self):
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data[i])):
                if(len(str(self.data[i][j])) > self.auto_spacing[j]):
                    self.auto_spacing[j] = len(str(self.data[i][j]))

    def auto_data_format(self):
        rowFormat = []
        for i in range(0, len(self.header)):
            rowFormat.append(self.padding_f +
                             "{:>" + str(self.auto_spacing[i]) + "}" + self.padding_f + "|")

        self.row_f = "".join(rowFormat)

    def __str__(self):
        rows = []

        if(self.isAutoSpacing):
            self.auto_header_sizing()
            self.auto_data_sizing()

            self.auto_data_format()
            self.auto_header_format()

        def sum(lst):
            sum = 0
            for i in range(0, len(lst)):
                sum += lst[i]
            return sum

        headerText = self.header_f.format(*self.header)

        rows.append("_" * len(headerText))
        rows.append(" ")
        rows.append(headerText)
        rows.append("_" * len(headerText))

        for row in self.data:
            formattedRow = []
            for obj in row:
                formattedRow.append(self.printFormat(obj))

            rows.append(self.row_f.format(*formattedRow))

        return "\n".join(rows)

    def printFormat(self, obj):
        if(isinstance(obj, str)):
            return obj
        elif(isinstance(obj, bool)):
            if(obj):
                return "YES"
            else:
                return "NO"
        elif(isinstance(obj, int)):
            return str(obj)
        elif(obj == None):
            return ' - '


def main():
    header = ["Name", "Age"]
    data = [['Terry', 21], ['Jacob', 31], ['Alex', 32]]

    t = Table(header)
    t.setData(data)
    print(t)

    data[0][1] = 22
    print(t)

    s = Table(header)
    s.setData(data)
    s.setPadding(5)
    print(s)


if __name__ == "__main__":
    main()
