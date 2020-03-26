"""
Example code for creating and visualizing
cluster of county-based cancer risk data

Note that you must download the file
http://www.codeskulptor.org/#alg_clusters_matplotlib.py
to use the matplotlib version of this code
"""

# Flavor of Python - desktop or CodeSkulptor
DESKTOP = True

import math
import alg_cluster
import urllib.request
import random


# conditional imports
if DESKTOP:
    # import alg_project3_solution      # desktop project solution
    import alg_clusters_matplotlib
else:
    #import userXX_XXXXXXXX as alg_project3_solution   # CodeSkulptor project solution
    import alg_clusters_simplegui
    import codeskulptor
    codeskulptor.set_timeout(300)


###################################################
# Code to load data tables

# URLs for cancer risk data tables of various sizes
# Numbers indicate number of counties in data table

DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"


def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)
    Brute  Force Closest Pair
    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    dist = pair_distance(cluster_list, 0, 1)
    
    for idx1 in range(len( cluster_list)):
        for idx2 in range(idx1+1, len(cluster_list)):
            tup = pair_distance(cluster_list, idx1, idx2)     
            if tup[0]<dist[0]:
                dist = tup            
    return dist



def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    if len(cluster_list) <= 3:
        return slow_closest_pair(cluster_list)
    
    mid = len(cluster_list) // 2
    p_left = cluster_list[:mid]
    p_right = cluster_list[mid:]
    tup1 = fast_closest_pair(p_left)
    tup2 = fast_closest_pair(p_right)
    
    dist, idx1, idx2 = min(tup1, (tup2[0], tup2[1]+mid, tup2[2]+mid))
    
    center_strip = (cluster_list[mid].horiz_center() + cluster_list[mid-1].horiz_center()) / 2
    
    tup3 = closest_pair_strip(cluster_list, center_strip, dist)
    return min((dist, idx1, idx2), tup3)


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    
    http://www.codeskulptor.org/#user47_R6H62ajuans3znA_0.py
    """
    indexes = list()
    for index in range(len(cluster_list)):
        if (horiz_center - half_width) <= cluster_list[index].horiz_center() <= (horiz_center + half_width):
            indexes.append(index)
    
    indexes.sort(key = lambda x:cluster_list[x].vert_center())
    
    dist = (float('inf'), -1, -1)
    for ith in range(0, len(indexes)-2 + 1):
        for kth in range(ith+1, min(ith+4, len(indexes))):
            dist1 = pair_distance(cluster_list, indexes[ith], indexes[kth])
            if dist1[0] <= dist[0]:
                dist = dist1
    return dist
            
 
    
######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    
    
    while len(cluster_list) > num_clusters:
        cluster_list.sort(key = lambda x:x.horiz_center())
        dist = fast_closest_pair(cluster_list)
        
        cluster_list[dist[1]].merge_clusters(cluster_list[dist[2]])
        del cluster_list[dist[2]]
    return cluster_list


######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """

    # position initial clusters at the location of clusters with largest populations
    clusters = [cluster for cluster in cluster_list]
    clusters.sort(key = lambda x:x.total_population(), reverse=True)
    clusters = clusters[:num_clusters]
    
    for _ in range(num_iterations):
        # num_iterations == q
        # initalize num_clusters i.e k empty cluster
        empty_cluster = [alg_cluster.Cluster(set([]), 0, 0, 0, 0) for _ in range(num_clusters)]
        
        for jdx in range(len(cluster_list)):
            distance, merge_with = float('inf'), None
            for cluster in clusters:
                if cluster_list[jdx].distance(cluster) < distance:
                    distance, merge_with = cluster_list[jdx].distance(cluster), cluster
            
            empty_cluster[clusters.index(merge_with)].merge_clusters(cluster_list[jdx])
        # new_clusters[.index(closest_cluster_center)].merge_clusters(county)
        clusters = empty_cluster
    return clusters

#print kmeans_clustering([alg_cluster.Cluster(set([]), 0, 0, 1, 0), alg_cluster.Cluster(set([]), 1, 0, 1001, 0)], 4, 5)





def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib.request.urlopen(data_url)
    data = data_file.read()
    data_lines = data.decode().split('\n')
    print("Loaded", len(data_lines), "data points")
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]


############################################################
# Code to create sequential clustering
# Create alphabetical clusters for county data

def sequential_clustering(singleton_list, num_clusters):
    """
    Take a data table and create a list of clusters
    by partitioning the table into clusters based on its ordering
    
    Note that method may return num_clusters or num_clusters + 1 final clusters
    """
    
    cluster_list = []
    cluster_idx = 0
    total_clusters = len(singleton_list)
    cluster_size = float(total_clusters)  / num_clusters
    
    for cluster_idx in range(len(singleton_list)):
        new_cluster = singleton_list[cluster_idx]
        if math.floor(cluster_idx / cluster_size) != \
           math.floor((cluster_idx - 1) / cluster_size):
            cluster_list.append(new_cluster)
        else:
            cluster_list[-1] = cluster_list[-1].merge_clusters(new_cluster)
            
    return cluster_list
                

#####################################################################
# Code to load cancer data, compute a clustering and 
# visualize the results


def run_example():
    """
    Load a data table, compute a list of clusters and 
    plot a list of clusters

    Set DESKTOP = True/False to use either matplotlib or simplegui
    """
    data_table = load_data_table(DATA_3108_URL)
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
        
    cluster_list = hierarchical_clustering(singleton_list, 15)	
    print("Displaying", len(cluster_list), "sequential clusters")

    #cluster_list = alg_project3_solution.hierarchical_clustering(singleton_list, 9)
    #print "Displaying", len(cluster_list), "hierarchical clusters"

    #cluster_list = alg_project3_solution.kmeans_clustering(singleton_list, 9, 5)	
    #print "Displaying", len(cluster_list), "k-means clusters"

            
    # draw the clusters using matplotlib or simplegui
    if DESKTOP:
        alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)
        #alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)  #add cluster centers
    else:
        alg_clusters_simplegui.PlotClusters(data_table, cluster_list)   # use toggle in GUI to add cluster centers
    
run_example()


