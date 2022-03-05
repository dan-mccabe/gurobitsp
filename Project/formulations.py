import gurobipy as gp
from gurobipy import GRB
import sys
import numpy as np
import pandas as pd


def solve_f0(c_ij, **kwargs):
    n_cities = np.shape(c_ij)[0]
    cities = np.arange(n_cities)
    model = gp.Model("F0")
    arcs = [(i, j) for i in cities for j in cities]
    ii_arcs = [(i, i) for i in cities]
    x = model.addVars(arcs, vtype=GRB.BINARY, name='x')

    model.addConstrs((sum(x[i, j] for j in cities) == 1.0 for i in cities),
                     name='sum_j')
    model.addConstrs((sum(x[i, j] for i in cities) == 1.0 for j in cities),
                     name='sum_i')
    model.addConstrs((x[i, i] == 0 for (i, i) in ii_arcs), name='ii')
    model.setObjective(sum(x[i, j] * c_ij[i, j] for (i, j) in arcs),
                       GRB.MINIMIZE)

    # Optimize
    for k in kwargs:
        model.setParam(k, kwargs[k])
    if 'TimeLimit' not in kwargs:
        model.setParam('TimeLimit', 3600)
    model.optimize()

    # Status checking
    status = model.getAttr(GRB.Attr.Status)

    if status in (GRB.INF_OR_UNBD, GRB.INFEASIBLE, GRB.UNBOUNDED):
        print("The model cannot be solved because it is infeasible or "
              "unbounded")
        sys.exit(1)

    if status != GRB.OPTIMAL and status != GRB.TIME_LIMIT:
        print("Optimization was stopped with status ", status)
        sys.exit(1)

    # Print result
    objval = model.getAttr(GRB.Attr.ObjVal)


def solve_f2(c_ij, fname=None, **kwargs):
    n_cities = np.shape(c_ij)[0]
    cities = np.arange(n_cities)
    city0 = 0
    non0cities = np.array([i for i in cities if i != city0])
    arcs = [(i, j) for i in cities for j in cities]
    ii_arcs = [(i, i) for i in cities]

    model = gp.Model("F0")
    x = model.addVars(arcs, vtype=GRB.BINARY, name='x')
    u = model.addVars(cities, lb=1, ub=n_cities, name='u')

    # Assignment constraints
    model.addConstrs((sum(x[i, j] for j in cities) == 1.0 for i in cities),
                     name='sum_j')
    model.addConstrs((sum(x[i, j] for i in cities) == 1.0 for j in cities),
                     name='sum_i')
    model.addConstrs((x[i, i] == 0 for (i, i) in ii_arcs), name='ii')

    # Additional MTZ constraints
    model.addConstrs((u[i] - u[j] + 1 <= n_cities * (1 - x[i, j])
                      for i in non0cities for j in non0cities),
                     name='mtz_order')
    model.addConstr(u[city0] == 1, name='mtz_first')

    # Objective
    model.setObjective(sum(x[i, j] * c_ij[i, j] for (i, j) in arcs),
                       GRB.MINIMIZE)

    # Optimize
    for k in kwargs:
        model.setParam(k, kwargs[k])
    if 'TimeLimit' not in kwargs:
        model.setParam('TimeLimit', 3600)
    model.optimize()

    # Status checking
    status = model.getAttr(GRB.Attr.Status)

    if status in (GRB.INF_OR_UNBD, GRB.INFEASIBLE, GRB.UNBOUNDED):
        print("The model cannot be solved because it is infeasible or "
              "unbounded")
        sys.exit(1)

    if status != GRB.OPTIMAL and status != GRB.TIME_LIMIT:
        print("Optimization was stopped with status ", status)
        sys.exit(1)

    # Print result
    model.getAttr(GRB.Attr.ObjVal)
    if fname:
        model.write(fname)


def solve_f3(c_ij, **kwargs):
    n_cities = np.shape(c_ij)[0]
    cities = np.arange(n_cities)
    city0 = 0
    r = city0
    non0cities = np.array([i for i in cities if i != city0])
    arcs = [(i, j) for i in cities for j in cities]
    ii_arcs = [(i, i) for i in cities]

    model = gp.Model("F0")
    x = model.addVars(arcs, vtype=GRB.BINARY, name='x')
    f = model.addVars(cities, arcs, vtype=GRB.BINARY, name='f')

    # Assignment constraints
    model.addConstrs((sum(x[i, j] for j in cities) == 1.0 for i in cities),
                     name='sum_j')
    model.addConstrs((sum(x[i, j] for i in cities) == 1.0 for j in cities),
                     name='sum_i')
    model.addConstrs((x[i, i] == 0 for (i, i) in ii_arcs), name='ii')

    # Additional MCF constraints
    model.addConstrs((sum(f[v, r, j] for j in non0cities)
                      - sum(f[v, j, r] for j in non0cities) == 1
                      for v in non0cities), name='root_flow')
    model.addConstrs((sum(f[v, i, j] for j in cities if j != i)
                      - sum(f[v, j, i] for j in cities if j != i) == 0 \
                      for i in non0cities for v in non0cities if v != i),
                     name='flow_cons')
    model.addConstrs(
        (f[v, i, j] <= x[i, j] for (i, j) in arcs for v in non0cities),
        name='f_leq_x')

    # Objective
    model.setObjective(sum(x[i, j] * c_ij[i, j] for (i, j) in arcs),
                       GRB.MINIMIZE)

    # Optimize
    for k in kwargs:
        model.setParam(k, kwargs[k])
    if 'TimeLimit' not in kwargs:
        model.setParam('TimeLimit', 3600)
    model.optimize()

    # Status checking
    status = model.getAttr(GRB.Attr.Status)

    if status in (GRB.INF_OR_UNBD, GRB.INFEASIBLE, GRB.UNBOUNDED):
        print("The model cannot be solved because it is infeasible or "
              "unbounded")
        sys.exit(1)

    if status != GRB.OPTIMAL and status != GRB.TIME_LIMIT:
        print("Optimization was stopped with status ", status)
        sys.exit(1)

    # Print result
    objval = model.getAttr(GRB.Attr.ObjVal)


def load_instances():
    bays = pd.read_csv(
        'bays29.txt', sep='\t', index_col=False, header=None, skiprows=1)
    bays_np = bays.to_numpy()

    dantzig = pd.read_csv(
        'dantzig42.txt', sep='\t', index_col=False, header=None, skiprows=1)
    dantzig_np = dantzig.to_numpy()

    pr = pd.read_csv(
        'pr76.txt', sep='\t', index_col=False, header=None, skiprows=1)
    pr_np = pr.to_numpy()

    rat = pd.read_csv(
        'rat99.txt', sep='\t', index_col=False, header=None, skiprows=1)
    rat_np = rat.to_numpy()

    return [bays_np, dantzig_np, pr_np, rat_np]

