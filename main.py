'''
Activity 3 - Lagrangian Heuristic for 2-TSP.

main.py: Front-end for 2-TSP lagrangian heuristic.

2-TSP: find the 2 shortest hamiltonian cycles in a complete graph.

Subject:
    MC859/MO824 - Operational Research.
Authors:
    André Soranzzo Mota         - RA 166404
    Victor Ferreira Ferrari     - RA 187890
    Gabriel Oliveira dos Santos - RA 197460

University of Campinas - UNICAMP - 2020

Last Modified: 18/10/2020
'''

from sys import argv, exit
from time import time
from generator import generate_instance
from lagrangian import lagrangian_relaxation
import graphic

def main():
            
    # Parse arguments
    if len(argv) < 4:
    	print('Usage: main.py <n_points> <seed_value> <time_limit>')
    	exit(1)
    n = int(argv[1])
    print(f"n = {n}")
    
    seed = int(argv[2])
    print(f"seed = {seed}")
    
    limit = int(argv[3])
    print(f"limit = {limit}s")
    
    # Create instance and solve
    start = time()
    ins = generate_instance(n, seed)
    res, opt, lower_bound_list, upper_bound_list = lagrangian_relaxation(ins, start, limit)
    graphic.plot_bounds_graph(lower_bound_list, upper_bound_list)
    # Output 
    print('')
    if opt:
        print("Optimal solution found!")
    print(f'Best dual: {res.dual}')
    print(f'Best primal: {res.primal}')
    print(f'First tour: {res.solution[0]}')
    print(f'Second tour: {res.solution[1]}')
    print('')
    

if __name__ == '__main__':
    main()
