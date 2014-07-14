

def readdata(file, types) :
        data = []

        for row in file.readlines() :
            r = []

	    i = 0
            for val in row.split("\t") :

		try:
		    value = types[i](val.strip())

		except ValueError:
		    value = val

                r.append(value)
                i = i + 1

            data.append(r)

        return data
