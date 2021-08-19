def readpostfile(filename, delimeter, hashtag_network_list):
    count = 0
    with open(filename, 'r') as f:
        for line in f:
            count = count + 1
            print(count)
            # line = f.readline()
            splitline = line.split(delimeter)
            hash_column = splitline[7]
            date = splitline[2]
            hash_column = hash_column.split(',')
            if len(hash_column) > 0:
                print(hash_column[0])
                print(len(hash_column))
                for i in range(len(hash_column)):
                    for j in range(i + 1, len(hash_column)):
                        hashtag_network_list.append(hash_column[i] + "," + hash_column[j] + "," + date)
    return hashtag_network_list
