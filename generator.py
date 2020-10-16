'''
Activity 3 - Lagrangian Heuristic for 2-TSP.

generator.py: generates 2-TSP instance.

2-TSP: find the 2 shortest hamiltonian cycles in a complete graph.
Based on Gurobi's `tsp.py` example.

Subject:
    MC859/MO824 - Operational Research.
Authors:
    André Soranzzo Mota         - RA 166404
    Victor Ferreira Ferrari     - RA 187890
    Gabriel Oliveira dos Santos - RA 197460

University of Campinas - UNICAMP - 2020

Last Modified: 15/10/2020
'''

import random
from math import sqrt
from TwoTSP import TwoTSP

def generate_instance(n_points, seed_value):

    # Create n random points
    random.seed(seed_value)
    points = [(random.uniform(0, 1), random.uniform(0, 1)) for i in range(n_points)]
    
    # Dictionary of Euclidean distance between each pair of points
    dist = {(i, j):
            sqrt(sum((points[i][k]-points[j][k])**2 for k in range(2)))
            for i in range(n_points) for j in range(i)}
    
    # TODO: not sure if this works.
    for i,j in dist.keys():
        dist[j,i] = dist[i,j]
    
    return TwoTSP(dist, None, None)

