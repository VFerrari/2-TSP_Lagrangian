'''
Activity 3 - Lagrangian Heuristic for 2-TSP.

subgradient.py: Implements the subgradient method for solving the dual lagrangian problem.

2-TSP: find the 2 shortest hamiltonian cycles in a complete graph.

Subject:
    MC859/MO824 - Operational Research.
Authors:
    André Soranzzo Mota         - RA 166404
    Victor Ferreira Ferrari     - RA 187890
    Gabriel Oliveira dos Santos - RA 197460

University of Campinas - UNICAMP - 2020

Last Modified: 16/10/2020
'''

from time import time

# Constants
INIT_PI = 2
MIN_PI = 0.005
MAX_ITER_PI = 30
INIT_MULT_VAL = 0
EPS = 0.0005

'''
 Generic subgradient method function for a MINIMIZATION problem.
 Solutions and dual bounds acquired through Lagrangian Relaxation.
 Takes Problem instance, execution time limit (in seconds).
 Returns the best solution and dual bound found within time "max_time".
'''
def subgradient_method(problem, max_time):
    
    # 1 - Initialize lagrange multipliers and other important values/functions.
    pi, n_iter = INIT_PI, 0
    curr_time = lambda x: time() - x
    mult = problem.init_mult(INIT_MULT_VAL)
    
    # End conditions: pi too small, too much time elapsed and optimum found.
    while pi > MIN_PI and curr_time(start_time) < max_time and problem.gap() >= 1:
        
        # 2 - Calculate lagrangian costs
        lc = problem.lg_costs(mult)
        
        # 3 - Solve LLBP
        dual, sol = problem.solve_llbp(lc)

        # TODO: unify steps 2 and 3?

        # 4 - Update best dual if possible
        n_iter += 1
        if dual > problem.dual:
            problem.dual = dual
            n_iter = 0
        
        # 4.5 - Half pi after MAX_ITER_PI iterations without improvement.
        elif n_iter == MAX_ITER_PI:
            pi /= 2
            n_iter = 0
        
        # 5 - Generate primal with lagrangian heuristic, and update.
        problem.primal = min(problem.primal, problem.lg_heu(sol))
        
        # 6 - Calculate subgradients.
        subgrad, sub_sum = problem.update_mult(mult)
    
        # 6.5 - Early stopping.
        # Finish execution if Gi=0 for every i.
        # If solution is viable, it's the optimum.
        if sub_sum == 0:
            # TODO: check viability
            break
    
        # 7 - Update lagrange multipliers
        step = pi*((1+EPS)*problem.primal - problem.dual)/sub_sum
        mult = problem.update_mult(mult, subgrad, sub_sum)
    
    return problem
