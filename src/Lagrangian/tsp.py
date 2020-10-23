# !/usr/bin/env python3.7

# Copyright 2020, Gurobi Optimization, LLC

'''
Activity 3 - Lagrangian Heuristic for 2-TSP.

tsp.py: MIP model to solve LLBP for 2-TSP: simple TSP.

Subject:
    MC859/MO824 - Operational Research.
Authors:
    André Soranzzo Mota         - RA 166404
    Victor Ferreira Ferrari     - RA 187890
    Gabriel Oliveira dos Santos - RA 197460

University of Campinas - UNICAMP - 2020

Last Modified: 19/10/2020
'''

import gurobipy as gp
from gurobipy import GRB
from itertools import combinations
from math import inf

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

def get_cycle(model, X, n_vertices):
    values = model.getAttr('x', X)
    selected = gp.tuplelist((i, j) for i, j in values.keys() if values[i, j] > 0.5)
    return subtour(selected, n_vertices)

def optimize_tsp(n_vertices, costs, time_limit=1800.0):
    model = gp.Model()

    # Create variables
    x = model.addVars(costs.keys(), obj=costs, vtype=GRB.BINARY, name='e')
    for i, j in x.keys():
        x[j, i] = x[i, j]  # edge in opposite direction

    # Add degree-2 constraint
    model.addConstrs(x.sum(i, '*') == 2 for i in range(n_vertices))

    # Optimize model
    model._vars = ([x], n_vertices)
    model.Params.lazyConstraints = 1
    
    # Set time limit
    model.setParam('TimeLimit', max(time_limit,0))
    #model.setParam('OutputFlag', 0)
    model.optimize(subtourelim)

    if model.status == GRB.Status.OPTIMAL:
        solution = get_cycle(model, x, n_vertices)
        cost = model.objVal
    elif model.status == GRB.Status.TIME_LIMIT:
        solution = None
        cost = inf
    else:
        print("Panic! Shouldn't be here, something went wrong.")

    return cost, solution

def optimize_2tsp(n_vertices, costs, time_limit=1800.0):
    '''
    :param n_vertices: number of vertices
    :param costs: costs of the edges from a graph., given in dict format.
                  can be lagrangean costs:
                  costs[(i,j)] = c_(i,j) + lambda_(i,j), where c_(i,j) is the
                            original cost and lambda_(i,j) is the lagrangean multiplier.
    :param time_limit: time limit
    :return: cost and solution
    '''
    model = gp.Model()

    # Create variables
    x1 = model.addVars(costs.keys(), obj=costs, vtype=GRB.BINARY, name='x1')
    x2 = model.addVars(costs.keys(), obj=costs, vtype=GRB.BINARY, name='x2')

    for i, j in x1.keys():
        x1[j, i] = x1[i, j]  # edge in opposite direction

    for i, j in x2.keys():
        x2[j, i] = x2[i, j]  # edge in opposite direction

    # Add degree-2 constraint
    model.addConstrs(x1.sum(i, '*') == 2 for i in range(n_vertices))
    model.addConstrs(x2.sum(i, '*') == 2 for i in range(n_vertices))

    # Optimize model
    model._vars = ([x1, x2], n_vertices)
    model.Params.lazyConstraints = 1

    model.setParam('TimeLimit', max(time_limit,0))
    #model.setParam('OutputFlag', 0)
    model.optimize(subtourelim)

    if model.status == GRB.Status.OPTIMAL:
        solution1 = get_cycle(model, x1, n_vertices)
        solution2 = get_cycle(model, x2, n_vertices)
        cost = model.objVal
    elif model.status == GRB.Status.TIME_LIMIT:
        solution1 = None
        solution2 = None
        cost = inf
    else:
        print("Panic! Shouldn't be here, something went wrong.")
        
    return cost, [solution1, solution2]


def optimize_2tsp_integer_linear_programming(n_vertices, dist):
    model = gp.Model()

    # Create variables
    x1 = model.addVars(dist.keys(), obj=dist, vtype=GRB.BINARY, name='x1')
    for i, j in x1.keys():
        x1[j, i] = x1[i, j]  # edge in opposite direction

    x2 = model.addVars(dist.keys(), obj=dist, vtype=GRB.BINARY, name='x2')
    for i, j in x2.keys():
        x2[j, i] = x2[i, j]  # edge in opposite direction

    # Add degree-2 constraint
    model.addConstrs(x1.sum(i, '*') == 2 for i in range(n_vertices))
    model.addConstrs(x2.sum(i, '*') == 2 for i in range(n_vertices))

    for i, j in x2.keys():
        model.addConstr((x1[i, j] + x2[i, j]) <= 1, "c{}_{}".format(i, j))

    # Optimize model
    model._vars = ([x1, x2], n_vertices)
    model.Params.lazyConstraints = 1
    
    # set time limit to 30 minutes (1800 s)
    model.setParam('TimeLimit', 1800.0)
    model.optimize(subtourelim)

    # solution1 = get_cycle(model, x1, n_vertices)
    # solution2 = get_cycle(model, x2, n_vertices)

    return model.objVal, model.ObjBound, model.Runtime
