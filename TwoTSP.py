'''
Activity 3 - Lagrangian Heuristic for 2-TSP.

TwoTSP.py: A class for the 2-TSP problem.

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

from math import inf

from Problem import Problem
from tsp import optimize

class TwoTSP(Problem):
    def __init__(self, instance, n_vertices):
        super().__init__(instance)
        self.n_vertices = n_vertices
        self.solution = None
    
    def init_mult(self, value):
        return {k:value for k in self.ins.keys()}
    
    def solve_llbp(self, mult, max_time):
        # Calculating lagrangian costs
        lc = {k : self.ins[k]+mult[k] for k in self.ins.keys()}

        # Solve LLBP and subtract linear term from cost
        cost, solution = optimize(n_vertices=self.n_vertices,
                                  costs=lc, 
                                  time_limit=max_time)
        cost *= 2
        cost -= sum(mult.values())
        return cost, solution
    
    def check_viability(self, sol):
        # The dual will never be viable for 2-TSP.
        return False

    def lg_heu(self, sol, max_time):
        new_ins = self.ins.copy()
        
        # Removing cycle from graph.
        for v in range(-1, len(sol)-1):
            edge = sol[v], sol[v+1]
            edge = sol[v+1], sol[v] if edge not in new_ins else edge
            new_ins[edge] = inf
        
        # Solving TSP without first cycle.
        cost, primal_sol = optimize(n_vertices=self.n_vertices,
                                    costs=new_ins,
                                    time_limit=max_time)
        
        return cost+self.dual, [sol, primal_sol]
    
    def subgradients(self, mult, sol):
        subgrad = {}
        sub_sum = 0
        x = {k:0 for k in self.ins.keys()}
        
        # Calculate X variables
        for v in range(-1, len(sol)-1):
            edge = sol[v], sol[v+1]
            edge = sol[v+1], sol[v] if edge not in x else edge
            x[edge] = 1
        
        # Calculate subgradients
        # g_k = x_1[k] + x_2[k] - 1
        for k in self.ins.keys():
            sub = 2*x[k] - 1
            subgrad[k] = 0 if sub < 0 and mult[k] == 0 else sub
            sub_sum += subgrad[k]*subgrad[k]
            
        return subgrad, sub_sum
        
    def update_mult(self, mult, subgrad, step):
        new_mult = lambda k : max(0, mult[k] + step*subgrad[k])
        return {k : new_mult(k) for k in self.ins.keys()}
