import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def plot_bounds_graph(lower_bound_list, upper_bound_list):
    n=len(lower_bound_list)
    plt.plot(list(range(n)), lower_bound_list, label='Lower Bound', color='blue')
    plt.plot(list(range(n)), upper_bound_list, label='Upper Bound', color='red')
    plt.xlabel('Iterations')
    plt.ylabel('Values')
    plt.legend()
    plt.show()
    #plt.savefig(figure_path, bbox_inches='tight')


# Ignore esta função por enquanto
def plot_graphic(solution1, solution2):
    G = nx.Graph()
    # Solution 1
    edges = []
    for i in range(1, len(solution1)):
        edges.append([solution1[i-1],solution1[i]])
    edges.append([solution1[i],solution1[0]])
    G.add_edges_from(edges, color='blue')
    # Solution 2
    edges = []
    for i in range(1, len(solution2)):
        edges.append([solution2[i-1],solution2[i]])
    edges.append([solution2[i],solution2[0]])
    G.add_edges_from(edges, color='red')
    print(G)
    nx.draw(G)
    plt.show()

#plot_lower_bound_graph([1, 2.3, 5.7, 16.9],[50, 20, 19, 18])
#plot_graphic([0, 4, 9, 3, 1, 6, 5, 2, 7, 8], [0, 2, 8, 3, 5, 1, 9, 6, 4, 7])
