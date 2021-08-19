import networkx as nx
import networkx as degree_alg
import networkx as betweenness
import networkx as closeness
import time

folder = 'C:\\Users\\Shazia\\Desktop\\SKORR\\v6\\friendship_20201001_20210124.csv'
# filename = 'C:\\Users\\Shazia\\Desktop\\SKORR\\v5\\users.csv'
# profileID_userID_dist = {}

delimeter = "\",\""
# delimeter = ","


def main():
    start_time = time.process_time()
    d = readfriendshipfile(delimeter, folder)
    print(time.process_time() - start_time, "seconds")


def readfriendshipfile(delimeter1, filename):
    count = 0
    G = nx.Graph()
    with open(filename, 'r') as f:
        for line in f:
            # line = f.readline()
            splitline = line.split(delimeter1)
            source = splitline[0].replace('\"', '')
            target = splitline[1].replace('\"\n', '')

            # edges.insert(0, "source,target")
            G.add_edge(source, target)

    # degree = degree_alg.degree_centrality(G)
    # degree = nx.betweenness_centrality(G, k=None, normalized=True, weight=None, endpoints=False, seed=None)
    # degree = closeness.closeness_centrality(G, u=None, distance=None, wf_improved=True)
    degree = nx.eigenvector_centrality(G)

    # for key, value in degree.items():
    #    print(key, value)

    return degree


def readuserfile(profileID_userID_dist, userfile, delimeter1):
    with open(userfile, 'r') as f:
        for line in f:
            # line = f.readline()
            splitline = line.split(delimeter1)
            userID = splitline[0].replace('\"', '')
            profileID = splitline[2].replace('\"', '')

            profileID_userID_dist[profileID] = userID

    #          print(profileID_userID_dist[userID])

    # for key, value in profileID_userID_dist.items():
    #    print(key, value)

    return profileID_userID_dist


if __name__ == "__main__":
    main()
