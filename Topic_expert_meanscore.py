import time

from numpy.distutils.fcompiler import none

import readfile
import utility

delimeter = "\",\""
hashtag_network_list = []
hashtag_user_score_nesdict = {}
outputfilepath = 'C:\\Users\\Shazia\\Desktop\\SKORR\\v6\\r\\'
filename = 'C:\\Users\\Shazia\\Desktop\\SKORR\\v6\\posts_ordered.csv'
# global startdate
startdate = '2020-01-01'
tot_time = 0.0


def main():
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:  # reading posts file
        for line in f:
            # line = f.readline()
            # print(line)
            global startdate
            global tot_time
            splitline = line.split(delimeter)
            hash_column = splitline[8]
            if hash_column == 'hashTags' or len(hash_column) == 0:  # leave the rows which have no hashtags available
                continue
            else:
                hash_list = hash_column.split(',')
                postProfileID = splitline[5]
                start_time = time.process_time()
                like = float(splitline[12])
                comment = float(splitline[13])
                share = float(splitline[14][0:-2])  # remove \n
                total = (like * 0.2 + comment * 0.3 + share * 0.5) / 30
                tot_time = tot_time + (time.process_time() - start_time)
                date = splitline[2]
                date = date[0:10]  # extracting year and month
                # print(date)
                if startdate == date:
                    if len(hash_list) > 0:
                        # print(hash_column[1])
                        # creating hashtag network
                        for i in range(len(hash_list)):
                            for j in range(i + 1, len(hash_list)):
                                hashtag_network_list.append(hash_list[i] + "," + hash_list[j])
                                # print(hashtag_network_list)

                            if hash_list[i] in hashtag_user_score_nesdict.keys():
                                user_score_map = hashtag_user_score_nesdict.get(hash_list[i])
                                start_time = time.process_time()
                                if postProfileID in user_score_map:
                                    old_score = user_score_map.get(postProfileID)
                                    new_score = (old_score + total) / 2
                                    user_score_map[postProfileID] = new_score
                                    # adding to a map of map (nested map)
                                    hashtag_user_score_nesdict[hash_list[i]][postProfileID] = new_score
                                else:
                                    user_score_map[postProfileID] = total
                                    hashtag_user_score_nesdict[hash_list[i]][postProfileID] = total
                                    tot_time = tot_time + (time.process_time() - start_time)
                            else:
                                hashtag_user_score_nesdict[hash_list[i]] = {postProfileID: total}


                # hash_network = topic_experts.readpostfile('C:\\Users\\Shazia\\Desktop\\SKORR\\v4\\posts_sample.txt',
                # delimeter, hashtag_network_list)
                else:  # when the date change occurs
                    startdate = date
                    if len(hashtag_network_list) != 0:
                        # print(hashtag_network_list)  # print when t changes
                        # print(hashtag_user_score_nesdict)

                        communityID_hashtag_dict = utility.community_discovery(hashtag_network_list)
                        # for key, value in communityID_hashtag_dict.items():
                        # print(key, value)
                        utility.community_user_score_combine(communityID_hashtag_dict, hashtag_user_score_nesdict, date,
                                                             outputfilepath)
                    if len(hash_list) == 0:
                        continue
                    else:
                        hashtag_user_score_nesdict.clear()
                        hashtag_network_list.clear()
                        if len(hash_list) > 1:
                            for i in range(len(hash_list)):
                                for j in range(i + 1, len(hash_list)):
                                    hashtag_network_list.append(hash_list[i] + "," + hash_list[j])

                                if hash_list[i] in hashtag_user_score_nesdict.keys():
                                    user_score_map = hashtag_user_score_nesdict.get(hash_list[i])
                                    start_time = time.process_time()
                                    if postProfileID in user_score_map:
                                        old_score = user_score_map.get(postProfileID)
                                        new_score = (old_score + total) / 2
                                        user_score_map[postProfileID] = new_score
                                        hashtag_user_score_nesdict[hash_list[i]][postProfileID] = new_score
                                    else:
                                        user_score_map[postProfileID] = total
                                        hashtag_user_score_nesdict[hash_list[i]][postProfileID] = total
                                        tot_time = tot_time + (time.process_time() - start_time)
                                else:
                                    hashtag_user_score_nesdict[hash_list[i]] = {postProfileID: total}

    # print(hashtag_network_list)
    # print(hashtag_user_score_nesdict)
    communityID_hashtag_dict = utility.community_discovery(hashtag_network_list)
    # for key, value in communityID_hashtag_dict.items():
    # print(key, value)
    utility.community_user_score_combine(communityID_hashtag_dict, hashtag_user_score_nesdict, date, outputfilepath)
    print(tot_time)


if __name__ == "__main__":
    main()
