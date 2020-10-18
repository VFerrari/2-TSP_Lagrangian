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

Last Modified: 18/10/2020
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
 
 Some optimizations are described in the "Lagrangian Relaxation" article
 by J.E. Beasley, in the "Modern Heuristic Techniques for Combinatorial
 Problems" book, pages 243-303, 1993.
'''
def subgradient_method(problem, start_time, max_time):
    
    # 1 - Initialize lagrange multipliers and other important values/functions.
    pi, n_iter = INIT_PI, 0
    curr_time = lambda x: time() - x
    mult = problem.init_mult(INIT_MULT_VAL)
    
    # End conditions: pi too small, too much time elapsed and optimum found.
    while pi > MIN_PI and curr_time(start_time) < max_time and problem.gap() >= 1:
        
        # 2 - Solve LLBP with lagrangian costs.
        dual, dual_sol = problem.solve_llbp(mult, max_time-curr_time(start_time))

        # 3 - Update best dual if possible
        n_iter += 1
        if dual > problem.dual:
            problem.dual = dual
            n_iter = 0
        
        # 3.5 - Half pi after MAX_ITER_PI iterations without improvement.
        elif n_iter == MAX_ITER_PI:
            pi /= 2
            n_iter = 0
        
        # 4 - Generate primal with lagrangian heuristic, and update.
        primal, primal_sol = problem.lg_heu(dual_sol, max_time-curr_time(start_time))
        if primal < problem.primal: 
            problem.primal = primal
            problem.solution = primal_sol
        
        # 5 - Calculate subgradients.
        subgrad, sub_sum = problem.subgradients(mult, dual_sol)
    
        # 5.5 - Early stopping.
        # Finish execution if Gi=0 for every i.
        # If solution is viable, it's the optimum.
        if sub_sum == 0:
            if problem.check_viability(dual_sol): 
                problem.primal = dual
                problem.solution = dual_sol
            break
    
        # 6 - Update lagrange multipliers
        step = pi*((1+EPS)*problem.primal - problem.dual)/sub_sum
        mult = problem.update_mult(mult, subgrad, step)
    
    return problem
