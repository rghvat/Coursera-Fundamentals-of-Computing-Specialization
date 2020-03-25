'''
Algorithmn part 1
Project 1
Author Raghav Atreya
Email raghavatreya16@gmail.com
'''
import alg_module1_graphs

EX_GRAPH0 = {0: set([1, 2]),
             1: set(),
             2: set()
            }


EX_GRAPH1 = {0 : set([1, 4, 5]),
             1 : set([2, 6 ]),
             2 : set([3]),
             3 : set([0]),
             4 : set([1]),
             5 : set([2]),
             6 : set([])
            }


EX_GRAPH2 = {0 : set([1, 4, 5]),
             1 : set([2, 6]),
             2 : set([3, 7]),
             3 : set([7]),
             4 : set([1]),
             5 : set([2]),
             6 : set([]),
             7 : set([3]),
             8 : set([1, 2]),
             9 : set([0, 3, 4, 5, 6, 7])
            }





def make_complete_graph(num):
    '''
    This function resturns complete graph given a node
    '''
    graph = {}
    nodes = list(range(num))
    for ind in range(num):
        graph[ind] = set(list( nodes[:ind] + nodes[ind+1:]))
    return graph

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
        print()
        my_dict[value] = my_dict.get(value, 0) + 1
    
    return my_dict
    

GRAPH4 = {"dog": set(["cat"]),
          "cat": set(["dog"]),
          "monkey": set(["banana"]),
          "banana": set([])}

GRAPH10 = {0: set([]),
          1: set([0]),
          2: set([0]),
          3: set([0]),
          4: set([0])}

    
\