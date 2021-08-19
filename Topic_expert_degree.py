from numpy.distutils.fcompiler import none

import friendship_measures
import readfile
import utility

delimeter = "\",\""
hashtag_network_list = []
hashtag_user_score_nesdict = {}
profileID_userID_dist = {}
outputfilepath = 'C:\\Users\\Shazia\\Desktop\\SKORR\\v5\\results2\\'
filename = 'C:\\Users\\Shazia\\Desktop\\SKORR\\v5\\posts_orderbydate.csv'
userfile = 'C:\\Users\\Shazia\\Desktop\\SKORR\\v5\\users.csv'
friendshipfile = 'C:\\Users\\Shazia\\Desktop\\SKORR\\v5\\friendship.csv'
# global startdate
startdate = '2020-01-01'


def main():
    profileID_userID_map = friendship_measures.readuserfile(profileID_userID_dist, userfile, delimeter)
    userID_cent_dist = friendship_measures.readfriendshipfile(delimeter, friendshipfile)
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:  # reading posts file
        for line in f:
            # line = f.readline()
            # print(line)
            global startdate
            splitline = line.split(delimeter)
            hash_column = splitline[8]
            if hash_column == 'hashTags' or len(hash_column) == 0:  # leave the rows which have no hashtags available
                continue
            else:
                hash_list = hash_column.split(',')
                postProfileID = splitline[5]

                like = float(splitline[12])
                comment = float(splitline[13])
                share = float(splitline[14][0:-2])  # remove \n
                total = (like * 0.2 + comment * 0.3 + share * 0.5) / 30
                date = splitline[2]
                date = date[0:10]  # extracting year and month
                for postProfileID in profileID_userID_map.keys():
                    userID = profileID_userID_map[postProfileID]
                    score = userID_cent_dist.get(userID)
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
                                    user_score_map[userID] = userID_cent_dist.get(userID)

                                else:
                                    hashtag_user_score_nesdict[hash_list[i]] = {userID: score}

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
                                        user_score_map[userID] = userID_cent_dist.get(userID)

                                    else:
                                        hashtag_user_score_nesdict[hash_list[i]] = {userID: score}

    # print(hashtag_network_list)
    # print(hashtag_user_score_nesdict)
    communityID_hashtag_dict = utility.community_discovery(hashtag_network_list)
    # for key, value in communityID_hashtag_dict.items():
    # print(key, value)
    utility.community_user_score_combine(communityID_hashtag_dict, hashtag_user_score_nesdict, date, outputfilepath)


if __name__ == "__main__":
    main()
