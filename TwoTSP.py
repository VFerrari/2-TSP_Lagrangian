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

Last Modified: 16/10/2020
'''

from Problem import Problem

class TwoTSP(Problem):
    def __init__(self, instance, llbp, heu):
        super(instance)
        
        # TODO: maybe not the best way to do that. Just import the functions?
        self.llbp = llbp
        self.heu = heu
    
    def init_mult(self, value):
        return {k:value for k in self.ins.keys()}
    
    def solve_llbp(self, mult, max_time):
		# Calculating lagrangian costs
		lc = {k : self.ins[k]+mult[k] for k in self.ins.keys()}
        
        # Solve LLBP and subtract linear term from cost.
        cost, solution = self.llbp(lc, max_time)
        cost -= sum(mult.values())
        
        return cost, solution
    
    def check_viability(self, sol):
		# TODO: implement
		raise NotImplementedError
    
    def lg_heu(self, sol):
        return self.heu(self.ins, sol)
    
    def subgradients(self, mult, sol):
        subgrad = {}
        sub_sum = 0
        
        # Calculate subgradients
        for k in self.ins.keys():
            # TODO: implement subgradient calculation from solution.
            #sub = subgradient(k, sol)
            subgrad[k] = 0 if sub < 0 and mult[k] == 0 else sub
            sub_sum += subgrad[k]*subgrad[k]
            
        return subgrad, sub_sum
        
    def update_mult(self, mult, subgrad, step):
		new_mult = lambda k : max(0, mult[k] + step*subgrad[k])
        return {k : new_mult(k) for k in self.ins.keys()}

