"""
Algorithmic Thinking part 1
Week 2 Applicaiton 1

Author : Raghav
Email. : raghavpushkalatreya@gmail.com
Imports physics citation graph 
"""

# general imports
import urllib.request as url
import matplotlib.pyplot as plt
import math
import random


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = url.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.decode().split('\n')
    graph_lines = graph_lines[ : -1]
    
    print("Loaded graph with {} nodes".format(len(graph_lines)))
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

citation_graph = load_graph(CITATION_URL)
print('citation_graph Loaded')

def compute_in_degrees(digraph):
    '''
    Input : graph representation using dict
    Output : dict with key as node and value as in degree of node
    '''
    my_dict = {}
    for index in digraph:
        my_dict[index] = 0
    
    for node in digraph:
        for value in digraph[node]:
            my_dict[value] = my_dict.get(value, 0) + 1
    
    return my_dict


def in_degree_distribution(diagraph):
    '''
    Input : Graph as dict
    Output : dict
    '''
    my_dict = {}
    for value in compute_in_degrees(diagraph).values():
        my_dict[value] = my_dict.get(value, 0) + 1
    return my_dict

def normalize_diagraph(diagraph):
    total = sum(diagraph.values())
    
    for ele in diagraph:
        diagraph[ele] = (diagraph[ele]* 1.0 ) / total
    
    return diagraph

def plot_question1():
    
    degree_distribution = in_degree_distribution(citation_graph)
    normalize = normalize_diagraph(degree_distribution)
    print(normalize)
    '''
    lst = []
    for ele in graph:
        if ele == 0 or graph[ele] == 0:
            continue
        lst.append((math.log(ele, 10), math.log(graph[ele], 10)))
    '''
    #simpleplot.plot_scatter('Normalize degree distribution', 800, 600, 'no of paper', 'distribution of citation', [lst], ['lst'])
    plt.loglog(list(normalize.keys()), list(normalize.values()), 'o', color='Red')
    plt.xlabel('Number of Nodes')
    plt.ylabel('Normalized in degree distribution')
    plt.savefig('Question 1 solution')
    plt.show()
    
# plot_question1()



######################################Q2
'''
modified (ER) random directed graphs: For every ordered pair of distinct nodes (i,j)
the modified algorithm adds the directed edge from i to j with probability p

your task is to consider the shape of the in-degree distribution for an ER graph 
and compare its shape to that of the physics citation graph
'''
def generate_er_graph(node, probablity = .5):
    er_graph = {}
    for ith in range(0, node):
        er_graph[ith] = set()
        for jth in range(0, node):
            if random.randint(0, 10) / 10 >= probablity and jth != ith:
                er_graph[ith].add(jth)
    print('Graph generated')
    in_degree_er = in_degree_distribution(er_graph)
    in_degree_cit = in_degree_distribution(citation_graph)
    node = max(node, len(in_degree_er))
    
    plt.plot(list(range(node)), list(in_degree_er.values()), 'o', color='Green')
    plt.plot(list(range(node)), list(in_degree_cit.values()), 'o', color='Red')
    plt.xlabel('Number of Nodes')
    plt.ylabel('Normalized in degree distribution')
    plt.savefig('Question 2 solution')
    plt.show()
generate_er_graph(5000, probablity = .2)
    
