

def readdata(file, types) :
        data = []

        for row in file.readlines() :
            r = []
            for val in row.split("\t") :
                i = 0
                r.append(types[i](val))
                i = i + 1

            data.append(r)

        return data
