# !/usr/bin/env python3.7

# Copyright 2020, Gurobi Optimization, LLC

'''
Activity 3 - Lagrangian Heuristic for 2-TSP.

llbp_solver.py: MIP model to solve the Dual Problem

Subject:
    MC859/MO824 - Operational Research.
Authors:
    André Soranzzo Mota         - RA 166404
    Victor Ferreira Ferrari     - RA 187890
    Gabriel Oliveira dos Santos - RA 197460

University of Campinas - UNICAMP - 2020

Last Modified: 16/10/2020
'''

import sys
import math
import random
from itertools import combinations
import gurobipy as gp
from gurobipy import GRB, tupledict
import pandas as pd
import time


# Callback - use lazy constraints to eliminate sub-tours
def subtourelim(model, where):
    if where == GRB.Callback.MIPSOL:
        # make a list of edges selected in the solution
        variables, n_vertices = model._vars
        for x in variables:
            vals = model.cbGetSolution(x)
            selected = gp.tuplelist((i, j) for i, j in x.keys()
                                    if vals[i, j] > 0.5)
            # find the shortest cycle in the selected edge list
            tour = subtour(selected, n_vertices)
            if len(tour) < n_vertices:
                # add subtour elimination constr. for every pair of cities in tour
                model.cbLazy(gp.quicksum(x[i, j]
                                         for i, j in combinations(tour, 2))
                             <= len(tour) - 1)

            # Given a tuplelist of edges, find the shortest subtour


def subtour(edges, n_vertices):
    unvisited = list(range(n_vertices))
    cycle = range(n_vertices + 1)  # initial length has 1 more city
    while unvisited:  # true if list is non-empty
        thiscycle = []
        neighbors = unvisited
        while neighbors:
            current = neighbors[0]
            thiscycle.append(current)
            unvisited.remove(current)
            neighbors = [j for i, j in edges.select(current, '*')
                         if j in unvisited]
        if len(cycle) > len(thiscycle):
            cycle = thiscycle
    return cycle

def get_cycle(model, X):
    values = model.getAttr('x', X)
    selected = gp.tuplelist((i, j) for i, j in values.keys() if values[i, j] > 0.5)
    return  subtour(selected)

def optimize(n_vertices, lagrangean_costs, time_limit=1800.0):
    '''

    :param n_vertices: number of vertices
    :param lagrangean_costs: lagrangean costs, lagrangean_costs[(i,j)] = c_(i,j) + lambda_(i,j), where c_(i,j) is the
                            original cost and lambda_(i,j) is the lagrangean multiplier.
    :param time_limit: time limit
    :return: cost and solution
    '''
    model = gp.Model()

    # Create variables
    x1 = model.addVars(lagrangean_costs.keys(), obj=lagrangean_costs, vtype=GRB.BINARY, name='x1')
    for i, j in x1.keys():
        x1[j, i] = x1[i, j]  # edge in opposite direction

    x2 = model.addVars(lagrangean_costs.keys(), obj=lagrangean_costs, vtype=GRB.BINARY, name='x2')
    for i, j in x2.keys():
        x2[j, i] = x2[i, j]  # edge in opposite direction

    # Add degree-2 constraint
    model.addConstrs(x1.sum(i, '*') == 2 for i in range(n_vertices))
    model.addConstrs(x2.sum(i, '*') == 2 for i in range(n_vertices))

    # Optimize model
    model._vars = ([x1, x2], n_vertices)
    model.Params.lazyConstraints = 1

    model.setParam(GRB.Param.TimeLimit, time_limit)
    model.optimize(subtourelim)

    solution = [get_cycle(model, x1), get_cycle(model, x2)]

    return model.objVal, solution
