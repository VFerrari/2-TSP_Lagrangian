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
from tsp import optimize_2tsp, optimize_tsp


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
        cost, solution = optimize_2tsp(n_vertices=self.n_vertices,
                                       costs=lc,
                                       time_limit=max_time)
        cost -= sum(mult.values())
        return cost, solution
    
    def check_viability(self, sol):
        cycle_list = []
        
        # Calculate edges for every cycle.
        for cycle in sol:
            e_list = []
            
            for v in range(-1, len(cycle)-1):
                edge = cycle[v], cycle[v+1]
                if edge not in self.ins.keys():
                    edge = cycle[v + 1], cycle[v]

                e_list.append(edge)
            cycle_list.append(x)
        
        # Check if edge sets are disjoint.
        # If no edges repeat, the union size is the sum of all sizes.
        union = set().union(*cycle_list)
        n = sum(len(u) for u in cycle_list)
        return n == len(union)

    def compute_cost(self, cycle):
        total_cost = 0
        for v in range(-1, len(cycle)-1):
            edge = cycle[v], cycle[v+1]
            if edge not in self.ins.keys():
                edge = cycle[v+1], cycle[v]

            total_cost += self.ins[edge]

        return total_cost

    def lg_heu(self, sol, max_time):
        new_ins = self.ins.copy()

        # Compute individual costs.
        cost1 = self.compute_cost(sol[0])
        cost2 = self.compute_cost(sol[1])
        
        # Choose least cost cycle to remove.
        if cost1 < cost2:
            cycle = sol[0]
            cost = cost1
        else:
            cycle = sol[1]
            cost = cost2

        # Removing cycle from graph.
        for v in range(-1, len(cycle)-1):
            edge = cycle[v], cycle[v+1]
            if edge not in new_ins.keys():
                edge = cycle[v + 1], cycle[v]

            new_ins[edge] = inf
        
        # Solving TSP without first cycle.
        primal_cost, primal_sol = optimize_tsp(n_vertices=self.n_vertices,
                                                 costs=new_ins,
                                                 time_limit=max_time)
        
        return cost + primal_cost, [cycle, primal_sol]
    
    def subgradients(self, mult, sol):
        subgrad = {}
        sub_sum = 0
        x_list = []
        
        # Calculate X variables for every cycle.
        for cycle in sol:
            x = {k: 0 for k in self.ins.keys()}
        
            for v in range(-1, len(cycle)-1):
                edge = cycle[v], cycle[v+1]
                if edge not in x.keys():
                    edge = cycle[v + 1], cycle[v]

                x[edge] = 1
            x_list.append(x)
        
        # Calculate subgradients
        # g_k = x_1[k] + x_2[k] - 1
        for k in self.ins.keys():
            sub = sum(x[k] for x in x_list)
            sub -= 1
            subgrad[k] = 0 if sub < 0 and mult[k] == 0 else sub
            sub_sum += subgrad[k]*subgrad[k]
            
        return subgrad, sub_sum
        
    def update_mult(self, mult, subgrad, step):
        new_mult = lambda k : max(0, mult[k] + step*subgrad[k])
        return {k : new_mult(k) for k in self.ins.keys()}
