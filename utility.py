import csv
import time

import community as community_louvain
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx
from networkx import Graph
from networkx.tests.test_convert_pandas import pd


def community_discovery(edges):  # parameter is list with source,target
    hashtag_community_dict = {}
    delete_list = []
    G = nx.Graph()
    # edges.insert(0, "source,target")

    # create grpah data structure and populate with edges
    for i in range(len(edges)):
        splitLine = edges[i].split(",")
        G.add_edge(splitLine[0], splitLine[1])

    # G = nx.from_pandas_edgelist(edges, 'source', 'target')
    # print(G)
    start_time = time.process_time()

    # compute the best partition
    partition = community_louvain.best_partition(G, resolution=1.0)
    print(time.process_time() - start_time, "seconds")

    for key, value in partition.items():
        # print(key, value)
        # interchange key,value (hashtag,communityID) to value,key (communityID,hashtag1,hashtag2...) and write in map
        if value in hashtag_community_dict.keys():
            hashtag_community_dict[value] = hashtag_community_dict[value] + "," + key
        else:
            hashtag_community_dict[value] = key

    for k, v in hashtag_community_dict.items():
        splitLine = v.split(",")
        if len(splitLine) < 20:
            delete_list.append(k)

    for d in delete_list:
        del hashtag_community_dict[d]

    return hashtag_community_dict


'''for key, value in partition.items():
        # print(key, value)
        # interchange key,value (hashtag,communityID) to value,key(communityID,hashtag) and write in map
        if value in hashtag_community_dict.keys():
            hashtag_community_dict[value].append(key)
        else:
            value_list = [key]
            hashtag_community_dict[value] = value_list'''

''' # draw the graph
    pos = nx.spring_layout(G)
    # color the nodes according to their partition
    cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
    nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40,
                           cmap=cmap, node_color=list(partition.values()))
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    plt.show()'''


def community_user_score_combine(communityID_hashtag_dict, hashtag_user_score_nesdict, date, outputfilepath):
    key_list = []
    value_list = []
    k_list = []
    v_list = []
    result_dict = {}
    for key, value in communityID_hashtag_dict.items():
        hash_row = value.split(',')
        for i in range(len(hash_row)):
            if hash_row[i] in hashtag_user_score_nesdict:
                user_score_dict = hashtag_user_score_nesdict.get(hash_row[i])
                for k, v in user_score_dict.items():
                    key_list.append(key)
                    value_list.append(value)
                    k_list.append(k)
                    v_list.append(v)
    result_dict = {'CommunityID': key_list, 'Hashtags': value_list, 'ProfileID': k_list, 'Score': v_list}
    df = pd.DataFrame(result_dict)
    group = df.groupby(['CommunityID', 'ProfileID'])['Score'].mean().reset_index()
    # print(group)
    writetofile(group, date, outputfilepath, communityID_hashtag_dict)

    # print('yes')


def writetofile(group, date, outputfilepath, communityID_hashtag_dict):
    with open(outputfilepath + date, 'a', encoding='utf-8', errors='ignore') as f:
        f.write(group.to_csv(sep='\t', index=False, line_terminator='\n'))
    with open(outputfilepath + date + "community-hashtag", 'a', encoding='utf-8', errors='ignore') as f2:
        writer = csv.writer(f2, delimiter='\t')
        for key, value in communityID_hashtag_dict.items():
            writer.writerow([key, value])

        # writer.writerow([[item] for item in communityID_hashtag_dict.items()])

    print('wrote')

