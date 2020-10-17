'''
Activity 3 - Lagrangian Heuristic for 2-TSP.

Problem.py: An abstract class for problems to be used in lg. relaxation.

Subject:
    MC859/MO824 - Operational Research.
Authors:
    André Soranzzo Mota         - RA 166404
    Victor Ferreira Ferrari     - RA 187890
    Gabriel Oliveira dos Santos - RA 197460

University of Campinas - UNICAMP - 2020

Last Modified: 16/10/2020
'''

from math import inf

# Should NOT be instantiated!
class Problem(object):
    def __init__(self, instance):
        self.ins = instance
        self.primal = inf
        self.dual = 0
    
    def gap(self):
        return abs(self.primal - self.dual)
    
    # Initializes lagrange multipliers with value `value`.
    def init_mult(self, value):
        raise NotImplementedError
    
    # Solves the Lagrangian Primal Problem, returns solution and its cost.
    def solve_llbp(self, mult, max_time):
        raise NotImplementedError
    
    # Check viability of solution for the original problem.
    def check_viability(self, sol):
        raise NotImplementedError
    
    # Lagrangian Heuristic to viabilize dual solution.
    def lg_heu(self, sol):
        raise NotImplementedError
    
    # Subgradient calculation method.
    def subgradients(self, mult, sol):
        raise NotImplementedError
    
    # Multiplier update method.
    def update_mult(self, mult, subgrad, step):
        raise NotImplementedError
