'''
Activity 3 - Lagrangian Heuristic for 2-TSP.

TwoTSP.py: A class for the 2-TSP problem.

2-TSP: find the 2 shortest hamiltonian cycles in a complete graph.

Subject:
    MC859/MO824 - Operational Research.
Authors:
	André Soranzzo Mota			- RA 166404
    Victor Ferreira Ferrari  	- RA 187890
    Gabriel Oliveira dos Santos - RA 197460

University of Campinas - UNICAMP - 2020

Last Modified: 15/10/2020
'''

from Problem import Problem

class TwoTSP(Problem):
	def __init__(instance, llbp, heu):
		super(instance)
		
		# TODO: maybe not the best way to do that. Just import the functions?
		self.llbp = llbp
		self.heu = heu
	
	def init_mult(value):
		return {k:value for k in self.ins.keys()}
	
	def lg_costs(mult):
		# TODO: implement
		return NotImplementedError
	
	def solve_llbp(lc):
		return self.llbp(self.ins, lc)
	
	def lg_heu(sol):
		return self.heu(self.ins, sol)
	
	def subgradients(mult):
		subgrad = {}
		sub_sum = 0
		
		# Calculate subgradients
		for k in self.ins.keys():
			# TODO: implement subgradient calculation
			#sub = subgradient(k, sol)
			subgrad[k] = 0 if sub < 0 and mult[k] == 0 else sub
			sub_sum += subgrad[k]*subgrad[k]
			
		return subgrad, sub_sum
		
	def update_mult(mult, subgrad, step):
		for k in self.ins.keys():
			mult[k] = max(0, mult[k] + step*subgrad[k])
		return mult

