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

from time import time

import pandas as pd

from generator import generate_instance
from lagrangian import lagrangian_relaxation
from tsp import optimize_2tsp_integer_linear_programming


def save_instance(filename, dists):
    with open(filename, 'w') as file:
        file.write('{')
        n = len(dists)
        for i, (k, v) in enumerate(dists.items()):
            file.write('({}, {}): {}'.format(k[0], k[1], v))
            if i != n - 1:
                file.write(', ')
        file.write('}')


def main():
    seed = 42
    limit = 1800.0

    dict_solutions = {'instance':[],
                      '2tsp_ilp_lower_bound':[],
                      '2tsp_ilp_upper_bound': [],
                      '2tsp_ilp_runtime':[],
                      'lagrangean_lower_bound':[],
                      'lagrangean_upper_bound': [],
                      'lagrangean_runtime': [],
                      'lagrangean_cost_value': []}

    for n in [100, 150, 200, 250, 300]:

        # Create instance and solve
        two_tsp = generate_instance(n, seed)
        save_instance(filename="instance_{}.lp".format(n), dists=two_tsp.ins)

        start = time()
        res, opt, lower_bound_list, upper_bound_list = lagrangian_relaxation(two_tsp, start, limit)
        end = time()

        runtime_lagrangean = end-start
        cost_value = res.primal
        lb = lower_bound_list[-1]
        ub = upper_bound_list[-1]

        lower_bound_ilp, upper_bound_ilp, runtime_pli = optimize_2tsp_integer_linear_programming(n, two_tsp.ins)

        dict_solutions['instance'].append(n)
        dict_solutions['2tsp_ilp_lower_bound'].append(lower_bound_ilp)
        dict_solutions['2tsp_ilp_upper_bound'].append(upper_bound_ilp)
        dict_solutions['2tsp_ilp_runtime'].append(runtime_pli)

        dict_solutions['lagrangean_lower_bound'].append(lb)
        dict_solutions['lagrangean_upper_bound'].append(ub)
        dict_solutions['lagrangean_runtime'].append(runtime_lagrangean)
        dict_solutions['lagrangean_cost_value'].append(cost_value)

    df_solutions = pd.DataFrame(dict_solutions)
    df_solutions.to_csv('2tsp_solutions.csv', sep=";")

if __name__ == '__main__':
    main()
