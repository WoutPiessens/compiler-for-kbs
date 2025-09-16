
import math
import random
import time
import pickle
from enum import Enum
from itertools import product
import xarray as xr
import numpy as np
from dash import Dash, html, dcc, State, Input, Output, ALL, callback_context

class EB(Enum):
    TRUE = 1
    FALSE = 2
    UNKNOWN = 0
    INCONSISTENT = (- 1)
    NONE = (- 2)

class Change():

    def __init__(self, name, true_slicing, false_slicing):
        self.name = name
        self.true_slicing = true_slicing
        self.false_slicing = false_slicing

class LiteralCollection():

    def __init__(self, name, slicing, b):
        self.name = name
        self.slicing = slicing
        self.b = b

class PropagateResult():

    def __init__(self, truth, position=0):
        self.truth = truth
        self.position = position
predicates = [xr.DataArray(np.full((31, 31, 31), EB.UNKNOWN), name='phi', dims=('x0', 'x1', 'x2'), coords={'x0': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x1': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x2': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]}), xr.DataArray(np.full((31, 31), EB.UNKNOWN), name='edge', dims=('x0', 'x1'), coords={'x0': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x1': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]}), xr.DataArray(np.full((31, 31, 31), EB.UNKNOWN), name='_X1', dims=('x0', 'x1', 'x2'), coords={'x0': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x1': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x2': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]}), xr.DataArray(np.full((31, 31, 31), EB.UNKNOWN), name='_X2', dims=('x0', 'x1', 'x2'), coords={'x0': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x1': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x2': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]}), xr.DataArray(np.full((31, 31, 31), EB.UNKNOWN), name='_X3', dims=('x0', 'x1', 'x2'), coords={'x0': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x1': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x2': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]}), xr.DataArray(np.full((31, 31, 31), EB.UNKNOWN), name='_X4', dims=('x0', 'x1', 'x2'), coords={'x0': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x1': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x2': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]}), xr.DataArray(np.full((31, 31, 31), EB.UNKNOWN), name='_X5', dims=('x0', 'x1', 'x2'), coords={'x0': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x1': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x2': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]}), xr.DataArray(np.full((31, 31, 31), EB.UNKNOWN), name='_X6', dims=('x0', 'x1', 'x2'), coords={'x0': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x1': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x2': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]}), xr.DataArray(np.full((31, 31, 31), EB.UNKNOWN), name='_X7', dims=('x0', 'x1', 'x2'), coords={'x0': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x1': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x2': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]}), xr.DataArray(np.full((31, 31, 31), EB.UNKNOWN), name='_X8', dims=('x0', 'x1', 'x2'), coords={'x0': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x1': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x2': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]}), xr.DataArray(np.full((31, 31, 31), EB.UNKNOWN), name='_X9', dims=('x0', 'x1', 'x2'), coords={'x0': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x1': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x2': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]}), xr.DataArray(np.full((31, 31, 31), EB.UNKNOWN), name='_X10', dims=('x0', 'x1', 'x2'), coords={'x0': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x1': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x2': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]}), xr.DataArray(np.full((31, 31, 31), EB.UNKNOWN), name='_X11', dims=('x0', 'x1', 'x2'), coords={'x0': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x1': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x2': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]}), xr.DataArray(np.full((31, 31, 31), EB.UNKNOWN), name='_X12', dims=('x0', 'x1', 'x2'), coords={'x0': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x1': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x2': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]}), xr.DataArray(np.full((31, 31, 31), EB.UNKNOWN), name='_X13', dims=('x0', 'x1', 'x2'), coords={'x0': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x1': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 'x2': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]}), xr.DataArray(np.array(EB.UNKNOWN), name='_X14')]
predicate_dict = {pred.name: pred for pred in predicates}
true_list = ['_X13', '_X5', '_X12']
unknown_list = [pred.name for pred in predicates]

def conditional_propagate(args):
    mask = (args != EB.TRUE)
    s = mask.sum()
    if (s == 1):
        index = np.where(mask)[0][0]
        if (args[index] == EB.UNKNOWN):
            return PropagateResult(EB.TRUE, index.item())
        return PropagateResult(EB.NONE)
    if (s == 0):
        return PropagateResult(EB.INCONSISTENT)
    return PropagateResult(EB.NONE)

def unconditional_propagate(args):
    mapping = {EB.UNKNOWN: EB.TRUE, EB.TRUE: EB.NONE, EB.FALSE: EB.INCONSISTENT}
    return [mapping.get(arg, arg) for arg in args]

def get_from_data_array(data_array, slices, threshold=100):
    if (len(slices) > threshold):
        vals = data_array.stack(points=data_array.dims).loc[slices].values
    else:
        index_list = [dict(zip(data_array.dims, t)) for t in slices]
        vals = [data_array.loc[i].values.item() for i in index_list]
    return vals

def inverse(x):
    if (x == EB.TRUE):
        return EB.FALSE
    if (x == EB.FALSE):
        return EB.TRUE
    return x

def append_changes(old, new):
    global unknown_list
    for key in new.keys():
        if (key in old.keys()):
            old[key].true_slicing.extend(new[key].true_slicing)
            old[key].false_slicing.extend(new[key].false_slicing)
        else:
            old[key] = Change(key, new[key].true_slicing, new[key].false_slicing)
    unknown_list = [elem for elem in unknown_list if (elem not in new.keys())]

def get_from_data_array_wrap(name, slice, bool):
    if (name == ';EQ'):
        temp_result = [(EB.TRUE if (s[0] == s[1]) else EB.FALSE) for s in slice]
    elif (name == '_NEQ'):
        temp_result = [(EB.TRUE if (s[0] != s[1]) else EB.FALSE) for s in slice]
    elif (name == '_LEQ'):
        temp_result = [(EB.TRUE if (s[0] <= s[1]) else EB.FALSE) for s in slice]
    elif (name == '_LE'):
        temp_result = [(EB.TRUE if (s[0] < s[1]) else EB.FALSE) for s in slice]
    elif (name == '_GE'):
        temp_result = [(EB.TRUE if (s[0] > s[1]) else EB.FALSE) for s in slice]
    elif (name == '_GEQ'):
        temp_result = [(EB.TRUE if (s[0] >= s[1]) else EB.FALSE) for s in slice]
    elif (name in true_list):
        temp_result = [EB.TRUE for _ in slice]
    elif (name in unknown_list):
        return [EB.UNKNOWN for _ in slice]
    else:
        temp_result = get_from_data_array(predicate_dict[name], slice)
    if bool:
        return temp_result
    else:
        return np.vectorize(inverse)(temp_result)

def write_to_data_array(slice_dict):
    new_changes = {}
    for p in slice_dict.keys():
        if (len(slice_dict[p]) > 100):
            da = predicate_dict[p.name]
            stacked = predicate_dict[p.name].stack(points=da.dims)
            if p.b:
                stacked.loc[slice_dict[p]] = EB.FALSE
                append_changes(new_changes, {p.name: Change(p.name, [], slice_dict[p])})
            else:
                stacked.loc[slice_dict[p]] = EB.TRUE
                append_changes(new_changes, {p.name: Change(p.name, slice_dict[p], [])})
            predicate_dict[p.name] = stacked.unstack()
        elif p.b:
            for s in slice_dict[p]:
                predicate_dict[p.name].loc[s] = EB.FALSE
            append_changes(new_changes, {p.name: Change(p.name, [], slice_dict[p])})
        else:
            for s in slice_dict[p]:
                predicate_dict[p.name].loc[s] = EB.TRUE
            append_changes(new_changes, {p.name: Change(p.name, slice_dict[p], [])})
    return new_changes

def handle_conditional_propagate_results(rule, result_list):
    incons_indices = np.where([(res.truth == EB.INCONSISTENT) for res in result_list])[0]
    if (len(incons_indices) > 0):
        raise Exception(('Inconsistency error in: ' + rule[0].name))
    true_indices = np.where([(res.truth == EB.TRUE) for res in result_list])[0]
    if (len(true_indices) > 0):
        changed_slices = [rule[result_list[i].position].slicing[i] for i in true_indices]
        changed_lcs = [rule[result_list[i].position] for i in true_indices]
        slices_per_lc = {}
        for (s, p) in zip(changed_slices, changed_lcs):
            if (p not in slices_per_lc.keys()):
                slices_per_lc[p] = [s]
            else:
                slices_per_lc[p].append(s)
        return write_to_data_array(slices_per_lc)
    return {}

def normal_propagation(rule):
    truth_list = [get_from_data_array_wrap(r.name, r.slicing, r.b) for r in rule]
    result_list = np.apply_along_axis(conditional_propagate, axis=0, arr=np.array(truth_list))
    try:
        new_changes = handle_conditional_propagate_results(rule, result_list)
        return new_changes
    except Exception as e:
        raise Exception(e)

def handle_unconditional_propagate_results(name, slices, result_list, bool_value):
    incons_indices = np.where((result_list == EB.INCONSISTENT))[0]
    if (len(incons_indices) > 0):
        raise Exception(('Inconsistency error in: ' + name))
    true_indices = np.where((result_list == EB.TRUE))[0]
    if (len(true_indices) > 0):
        changed_slices = [slices[i] for i in true_indices]
        slices_per_lc = {LiteralCollection(name, slices, (not bool_value)): changed_slices}
        return write_to_data_array(slices_per_lc)
    return {}

def unconditional_propagate_wrap(big_array, big_slices, bool_value):
    args = get_from_data_array_wrap(big_array.name, big_slices, bool_value)
    result_list = np.array(unconditional_propagate(np.array(args)))
    try:
        new_changes = handle_unconditional_propagate_results(big_array.name, big_slices, result_list, bool_value)
        return new_changes
    except Exception as e:
        raise Exception(e)

def calculate_first_coordinate(small_coordinate, data_array, changing_dims):
    new_coordinate = tuple(small_coordinate)
    index = 0
    for dim in data_array.dims:
        if (dim in changing_dims):
            new_coordinate = ((new_coordinate[:index] + (data_array.coords[dim][0].item(),)) + new_coordinate[index:])
        index += 1
    return new_coordinate

def calculate_next_coordinate(coordinate, data_array, changing_dims):
    next_coordinate = tuple(coordinate)
    index = 0
    for dim in data_array.dims:
        if (dim in changing_dims):
            current_value = coordinate[index]
            current_coords = data_array.coords[dim].values
            current_index = np.where((current_coords == current_value))[0][0]
            if (current_index < (len(current_coords) - 1)):
                if (index < (len(data_array.dims) - 1)):
                    next_coordinate = ((next_coordinate[:index] + (data_array.coords[dim][(current_index + 1)].item(),)) + next_coordinate[(index + 1):])
                else:
                    next_coordinate = (next_coordinate[:index] + (data_array.coords[dim][(current_index + 1)].item(),))
                return next_coordinate
            elif (index < (len(data_array.dims) - 1)):
                next_coordinate = ((next_coordinate[:index] + (data_array.coords[dim][0].item(),)) + next_coordinate[(index + 1):])
            else:
                return None
        index += 1

def incremental_propagate(data_array, small_coordinates, changing_dims, b, unknown_coordinates_list=None, boolean_list=None, small_array=None):
    continue_list = [True for _ in range(len(small_coordinates))]
    if (unknown_coordinates_list is None):
        unknown_coordinates_list = [[] for _ in range(len(small_coordinates))]
    coordinates = [calculate_first_coordinate(small_coordinate, data_array, changing_dims) for small_coordinate in small_coordinates]
    while (any(continue_list) and (None not in coordinates)):
        results = get_from_data_array_wrap(data_array.name, coordinates, b)
        unknown_coordinates_list = [((unknown_coordinates_list[i] + [coordinates[i]]) if ((results[i] == EB.UNKNOWN) and (len(unknown_coordinates_list[i]) <= 1)) else unknown_coordinates_list[i]) for i in range(len(small_coordinates))]
        continue_list = [(((results[i] == EB.TRUE) or (results[i] == EB.UNKNOWN)) and (len(unknown_coordinates_list[i]) <= 1) and continue_list[i]) for i in range(len(results))]
        coordinates = [(calculate_next_coordinate(coordinates[i], data_array, changing_dims) if continue_list[i] else coordinates[i]) for i in range(len(coordinates))]
    new_changes = {}
    for (i, coord_list) in enumerate(unknown_coordinates_list):
        if ((len(coord_list) == 1) and continue_list[i]):
            coord = coord_list[0]
            if ((boolean_list is not None) and boolean_list[i]):
                if b:
                    small_array.loc[coord] = EB.TRUE
                    append_changes(new_changes, {small_array.name: Change(small_array.name, [coord], [])})
                else:
                    small_array.loc[coord] = EB.FALSE
                    append_changes(new_changes, {small_array.name: Change(small_array.name, [], [coord])})
            elif b:
                data_array.loc[coord] = EB.FALSE
                append_changes(new_changes, {data_array.name: Change(data_array.name, [], [coord])})
            else:
                data_array.loc[coord] = EB.TRUE
                append_changes(new_changes, {data_array.name: Change(data_array.name, [coord], [])})
        if ((len(coord_list) == 0) and continue_list[i]):
            raise Exception(('Inconsistency error in: ' + data_array.name))
    return new_changes

def incremental_propagate_wrap(big_array, small_array, small_coordinates, changing_dims, b):
    results = get_from_data_array_wrap(small_array.name, small_coordinates, (not b))
    used_small_coordinates = []
    unknown_coordinates_list = []
    boolean_list = []
    for (i, res) in enumerate(results):
        if (res == EB.TRUE):
            used_small_coordinates.append(small_coordinates[i])
            unknown_coordinates_list.append([])
            boolean_list.append(False)
        if (res == EB.UNKNOWN):
            used_small_coordinates.append(small_coordinates[i])
            unknown_coordinates_list.append([small_coordinates[i]])
            boolean_list.append(True)
    if (len(used_small_coordinates) > 0):
        return incremental_propagate(big_array, used_small_coordinates, changing_dims, b, unknown_coordinates_list, boolean_list, small_array)
    return {}

def map_indices(index, binding1, binding2):
    match_with_index = {}
    for (i, bind1) in enumerate(binding1):
        match_with_index[bind1] = index[i]
    new_index = tuple()
    for bind2 in binding2:
        if (bind2 in match_with_index.keys()):
            new_index += (match_with_index[bind2],)
        else:
            new_index += (bind2,)
    return new_index

def is_valid_index(s, argument, quantified_var):
    var_mapping = {}
    for (i, elem) in enumerate(s):
        if (argument[i] not in quantified_var):
            if (elem != argument[i]):
                return False
        else:
            arg = argument[i]
            if (arg in var_mapping.keys()):
                if (elem != var_mapping[arg]):
                    return False
            else:
                var_mapping[arg] = elem
    return True

def map_indices_wrap(argument_dict, changed_var, slicing, quantified_var):
    if (len(slicing) == 0):
        return None
    slicing_dict = {}
    valid_slicing = [s for s in slicing if is_valid_index(s, argument_dict[changed_var], quantified_var)]
    slicing_dict[changed_var] = valid_slicing
    for (key, val) in argument_dict.items():
        if (val != argument_dict[changed_var]):
            new_slicing = [map_indices(index, argument_dict[changed_var], argument_dict[key]) for index in slicing_dict[changed_var]]
            slicing_dict[key] = new_slicing
        else:
            slicing_dict[key] = valid_slicing
    return slicing_dict

def add_dims(slicing, new, extra_dims):
    new_slicing = []
    new_slicing.append(slicing.copy())
    new_domains = [new.coords[dim].values for dim in extra_dims]
    for comb in product(*new_domains):
        new_slice = slicing.copy()
        index = 0
        c_index = 0
        for dim in new.dims:
            if (dim in extra_dims):
                new_slice = [((elem[:index] + (comb[c_index].item(),)) + elem[index:]) for elem in new_slice]
                c_index += 1
            index += 1
        new_slicing.append(new_slice)
    big_slices = [list(val) for (key, val) in zip(new_slicing[0], zip(*new_slicing[1:]))]
    return [item for sublist in big_slices for item in sublist]

def reduce_dims(slicing, old, extra_dims):
    indices = np.array([i for (i, value) in enumerate(old.dims) if (value not in extra_dims)])
    new_slicing = {tuple((tup[i] for i in indices)) for tup in slicing}
    return new_slicing

def specifying_propagation(big, true_slices, false_slices, new_dims, universal):
    big_array = predicate_dict[big]
    new_changes = {}
    if (len(true_slices) > 0):
        if universal:
            big_slices = add_dims(true_slices, big_array, new_dims)
            if (big in true_list):
                detected_changes = {big: Change(big, big_slices, [])}
            else:
                try:
                    detected_changes = unconditional_propagate_wrap(big_array, big_slices, True)
                except Exception as e:
                    raise Exception(e)
            append_changes(new_changes, detected_changes)
        else:
            try:
                detected_changes = incremental_propagate(big_array, true_slices, new_dims, False)
            except Exception as e:
                raise Exception(e)
            append_changes(new_changes, detected_changes)
    if (len(false_slices) > 0):
        if universal:
            try:
                detected_changes = incremental_propagate(big_array, false_slices, new_dims, True)
            except Exception as e:
                raise Exception(e)
            append_changes(new_changes, detected_changes)
        else:
            big_slices = add_dims(false_slices, big_array, new_dims)
            try:
                detected_changes = unconditional_propagate_wrap(big_array, big_slices, False)
            except Exception as e:
                raise Exception(e)
            append_changes(new_changes, detected_changes)
    return new_changes

def generalizing_propagation(big, small, true_slices, false_slices, old_dims, universal):
    small_array = predicate_dict[small]
    big_array = predicate_dict[big]
    new_changes = {}
    if (len(true_slices) > 0):
        small_slices = reduce_dims(true_slices, big_array, old_dims)
        if universal:
            try:
                detected_changes = incremental_propagate_wrap(big_array, small_array, list(small_slices), old_dims, True)
                append_changes(new_changes, detected_changes)
            except Exception as e:
                raise Exception(e)
        else:
            try:
                detected_changes = unconditional_propagate_wrap(small_array, list(small_slices), True)
                append_changes(new_changes, detected_changes)
            except Exception as e:
                raise Exception(e)
    if (len(false_slices) > 0):
        small_slices = reduce_dims(false_slices, big_array, old_dims)
        if universal:
            try:
                detected_changes = unconditional_propagate_wrap(small_array, list(small_slices), False)
                append_changes(new_changes, detected_changes)
            except Exception as e:
                raise Exception(e)
        else:
            try:
                detected_changes = incremental_propagate_wrap(big_array, small_array, list(small_slices), old_dims, False)
                append_changes(new_changes, detected_changes)
            except Exception as e:
                raise Exception(e)
    return new_changes

def add_all_function_outputs(data_array, slice):
    all_outputs = []
    scope = data_array.coords[data_array.dims[(- 1)]].values
    for elem in scope:
        if (elem != slice[(- 1)]):
            all_outputs.append((slice[:(- 1)] + (elem.item(),)))
    return all_outputs

def function_propagation(name, true_slices, false_slices):
    new_changes = {}
    data_array = predicate_dict[name]
    if (len(true_slices) > 0):
        corresponding_function_slices = [add_all_function_outputs(data_array, slice) for slice in true_slices]
        corresponding_function_slices_flat = [item for sublist in corresponding_function_slices for item in sublist]
        try:
            detected_changes = unconditional_propagate_wrap(data_array, corresponding_function_slices_flat, False)
        except Exception as e:
            raise Exception(e)
        append_changes(new_changes, detected_changes)
    if (len(false_slices) > 0):
        last_dim = predicate_dict[name].dims[(- 1)]
        reduced_slices = reduce_dims(false_slices, data_array, [last_dim])
        try:
            detected_changes = incremental_propagate(predicate_dict[name], list(reduced_slices), [last_dim], False)
        except Exception as e:
            raise Exception(e)
        append_changes(new_changes, detected_changes)
    return new_changes

def propagate(changes):
    new_changes = {}
    for change in changes.values():
        if (change.name == '_X1'):
            try:
                old_dims = ['x2']
                detected_changes = generalizing_propagation('_X1', 'edge', change.true_slicing, change.false_slicing, old_dims, False)
                append_changes(new_changes, detected_changes)
            except Exception as e:
                raise Exception(e)
            if (len(change.false_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X1': ['x', 'y', 'z'], '_X4': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X1']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X1', slicing_dict['_X1'], False), LiteralCollection('_X4', slicing_dict['_X4'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.true_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X1': ['x', 'y', 'z'], '_X2': ['x', 'y', 'z'], '_X3': ['x', 'y', 'z'], '_X4': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X1']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X1', slicing_dict['_X1'], True), LiteralCollection('_X2', slicing_dict['_X2'], True), LiteralCollection('_X3', slicing_dict['_X3'], True), LiteralCollection('_X4', slicing_dict['_X4'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
        if (change.name == 'edge'):
            try:
                new_dims = ['x2']
                detected_changes = specifying_propagation('_X1', change.true_slicing, change.false_slicing, new_dims, False)
                append_changes(new_changes, detected_changes)
            except Exception as e:
                raise Exception(e)
            try:
                new_dims = ['x0']
                detected_changes = specifying_propagation('_X2', change.true_slicing, change.false_slicing, new_dims, False)
                append_changes(new_changes, detected_changes)
            except Exception as e:
                raise Exception(e)
            try:
                new_dims = ['x1']
                detected_changes = specifying_propagation('_X3', change.true_slicing, change.false_slicing, new_dims, False)
                append_changes(new_changes, detected_changes)
            except Exception as e:
                raise Exception(e)
            try:
                new_dims = ['x2']
                detected_changes = specifying_propagation('_X7', change.true_slicing, change.false_slicing, new_dims, True)
                append_changes(new_changes, detected_changes)
            except Exception as e:
                raise Exception(e)
            try:
                new_dims = ['x0']
                detected_changes = specifying_propagation('_X9', change.true_slicing, change.false_slicing, new_dims, True)
                append_changes(new_changes, detected_changes)
            except Exception as e:
                raise Exception(e)
            try:
                new_dims = ['x1']
                detected_changes = specifying_propagation('_X11', change.true_slicing, change.false_slicing, new_dims, True)
                append_changes(new_changes, detected_changes)
            except Exception as e:
                raise Exception(e)
        if (change.name == '_X2'):
            try:
                old_dims = ['x0']
                detected_changes = generalizing_propagation('_X2', 'edge', change.true_slicing, change.false_slicing, old_dims, False)
                append_changes(new_changes, detected_changes)
            except Exception as e:
                raise Exception(e)
            if (len(change.false_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X2': ['x', 'y', 'z'], '_X4': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X2']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X2', slicing_dict['_X2'], False), LiteralCollection('_X4', slicing_dict['_X4'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.true_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X2': ['x', 'y', 'z'], '_X1': ['x', 'y', 'z'], '_X3': ['x', 'y', 'z'], '_X4': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X2']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X2', slicing_dict['_X2'], True), LiteralCollection('_X1', slicing_dict['_X1'], True), LiteralCollection('_X3', slicing_dict['_X3'], True), LiteralCollection('_X4', slicing_dict['_X4'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
        if (change.name == '_X3'):
            try:
                old_dims = ['x1']
                detected_changes = generalizing_propagation('_X3', 'edge', change.true_slicing, change.false_slicing, old_dims, False)
                append_changes(new_changes, detected_changes)
            except Exception as e:
                raise Exception(e)
            if (len(change.false_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X3': ['x', 'y', 'z'], '_X4': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X3']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X3', slicing_dict['_X3'], False), LiteralCollection('_X4', slicing_dict['_X4'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.true_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X3': ['x', 'y', 'z'], '_X1': ['x', 'y', 'z'], '_X2': ['x', 'y', 'z'], '_X4': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X3']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X3', slicing_dict['_X3'], True), LiteralCollection('_X1', slicing_dict['_X1'], True), LiteralCollection('_X2', slicing_dict['_X2'], True), LiteralCollection('_X4', slicing_dict['_X4'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
        if (change.name == '_X4'):
            if (len(change.true_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X4': ['x', 'y', 'z'], '_X1': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X4']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X4', slicing_dict['_X4'], True), LiteralCollection('_X1', slicing_dict['_X1'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.true_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X4': ['x', 'y', 'z'], '_X2': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X4']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X4', slicing_dict['_X4'], True), LiteralCollection('_X2', slicing_dict['_X2'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.true_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X4': ['x', 'y', 'z'], '_X3': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X4']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X4', slicing_dict['_X4'], True), LiteralCollection('_X3', slicing_dict['_X3'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.false_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X4': ['x', 'y', 'z'], '_X1': ['x', 'y', 'z'], '_X2': ['x', 'y', 'z'], '_X3': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X4']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X4', slicing_dict['_X4'], False), LiteralCollection('_X1', slicing_dict['_X1'], True), LiteralCollection('_X2', slicing_dict['_X2'], True), LiteralCollection('_X3', slicing_dict['_X3'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.true_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X4': ['x', 'y', 'z'], '_X5': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X4']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X4', slicing_dict['_X4'], True), LiteralCollection('_X5', slicing_dict['_X5'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.false_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X4': ['x', 'y', 'z'], 'phi': ['x', 'y', 'z'], '_X5': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X4']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X4', slicing_dict['_X4'], False), LiteralCollection('phi', slicing_dict['phi'], True), LiteralCollection('_X5', slicing_dict['_X5'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
        if (change.name == '_X5'):
            if (len(change.false_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X5': ['x', 'y', 'z'], 'phi': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X5']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X5', slicing_dict['_X5'], False), LiteralCollection('phi', slicing_dict['phi'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.false_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X5': ['x', 'y', 'z'], '_X4': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X5']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X5', slicing_dict['_X5'], False), LiteralCollection('_X4', slicing_dict['_X4'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.true_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X5': ['x', 'y', 'z'], 'phi': ['x', 'y', 'z'], '_X4': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X5']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X5', slicing_dict['_X5'], True), LiteralCollection('phi', slicing_dict['phi'], True), LiteralCollection('_X4', slicing_dict['_X4'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.false_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X5': ['x', 'y', 'z'], '_X13': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X5']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X5', slicing_dict['_X5'], False), LiteralCollection('_X13', slicing_dict['_X13'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.true_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X5': ['x', 'y', 'z'], '_X12': ['x', 'y', 'z'], '_X13': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X5']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X5', slicing_dict['_X5'], True), LiteralCollection('_X12', slicing_dict['_X12'], True), LiteralCollection('_X13', slicing_dict['_X13'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
        if (change.name == 'phi'):
            if (len(change.false_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'phi': ['x', 'y', 'z'], '_X5': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['phi']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('phi', slicing_dict['phi'], False), LiteralCollection('_X5', slicing_dict['_X5'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.true_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'phi': ['x', 'y', 'z'], '_X4': ['x', 'y', 'z'], '_X5': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['phi']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('phi', slicing_dict['phi'], True), LiteralCollection('_X4', slicing_dict['_X4'], False), LiteralCollection('_X5', slicing_dict['_X5'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.true_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'phi': ['x', 'y', 'z'], '_X12': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['phi']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('phi', slicing_dict['phi'], True), LiteralCollection('_X12', slicing_dict['_X12'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.false_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'phi': ['x', 'y', 'z'], '_X6': ['x', 'y', 'z'], '_X8': ['x', 'y', 'z'], '_X10': ['x', 'y', 'z'], '_X12': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['phi']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('phi', slicing_dict['phi'], False), LiteralCollection('_X6', slicing_dict['_X6'], False), LiteralCollection('_X8', slicing_dict['_X8'], False), LiteralCollection('_X10', slicing_dict['_X10'], False), LiteralCollection('_X12', slicing_dict['_X12'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
        if (change.name == '_X6'):
            if (len(change.true_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X6': ['x', 'y', 'z'], '_X7': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X6']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X6', slicing_dict['_X6'], True), LiteralCollection('_X7', slicing_dict['_X7'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.false_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X6': ['x', 'y', 'z'], '_X7': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X6']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X6', slicing_dict['_X6'], False), LiteralCollection('_X7', slicing_dict['_X7'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.true_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X6': ['x', 'y', 'z'], '_X12': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X6']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X6', slicing_dict['_X6'], True), LiteralCollection('_X12', slicing_dict['_X12'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.false_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X6': ['x', 'y', 'z'], '_X8': ['x', 'y', 'z'], '_X10': ['x', 'y', 'z'], 'phi': ['x', 'y', 'z'], '_X12': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X6']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X6', slicing_dict['_X6'], False), LiteralCollection('_X8', slicing_dict['_X8'], False), LiteralCollection('_X10', slicing_dict['_X10'], False), LiteralCollection('phi', slicing_dict['phi'], False), LiteralCollection('_X12', slicing_dict['_X12'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
        if (change.name == '_X7'):
            if (len(change.true_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X7': ['x', 'y', 'z'], '_X6': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X7']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X7', slicing_dict['_X7'], True), LiteralCollection('_X6', slicing_dict['_X6'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.false_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X7': ['x', 'y', 'z'], '_X6': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X7']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X7', slicing_dict['_X7'], False), LiteralCollection('_X6', slicing_dict['_X6'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            try:
                old_dims = ['x2']
                detected_changes = generalizing_propagation('_X7', 'edge', change.true_slicing, change.false_slicing, old_dims, True)
                append_changes(new_changes, detected_changes)
            except Exception as e:
                raise Exception(e)
        if (change.name == '_X8'):
            if (len(change.true_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X8': ['x', 'y', 'z'], '_X9': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X8']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X8', slicing_dict['_X8'], True), LiteralCollection('_X9', slicing_dict['_X9'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.false_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X8': ['x', 'y', 'z'], '_X9': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X8']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X8', slicing_dict['_X8'], False), LiteralCollection('_X9', slicing_dict['_X9'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.true_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X8': ['x', 'y', 'z'], '_X12': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X8']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X8', slicing_dict['_X8'], True), LiteralCollection('_X12', slicing_dict['_X12'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.false_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X8': ['x', 'y', 'z'], '_X6': ['x', 'y', 'z'], '_X10': ['x', 'y', 'z'], 'phi': ['x', 'y', 'z'], '_X12': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X8']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X8', slicing_dict['_X8'], False), LiteralCollection('_X6', slicing_dict['_X6'], False), LiteralCollection('_X10', slicing_dict['_X10'], False), LiteralCollection('phi', slicing_dict['phi'], False), LiteralCollection('_X12', slicing_dict['_X12'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
        if (change.name == '_X9'):
            if (len(change.true_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X9': ['x', 'y', 'z'], '_X8': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X9']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X9', slicing_dict['_X9'], True), LiteralCollection('_X8', slicing_dict['_X8'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.false_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X9': ['x', 'y', 'z'], '_X8': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X9']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X9', slicing_dict['_X9'], False), LiteralCollection('_X8', slicing_dict['_X8'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            try:
                old_dims = ['x0']
                detected_changes = generalizing_propagation('_X9', 'edge', change.true_slicing, change.false_slicing, old_dims, True)
                append_changes(new_changes, detected_changes)
            except Exception as e:
                raise Exception(e)
        if (change.name == '_X10'):
            if (len(change.true_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X10': ['x', 'y', 'z'], '_X11': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X10']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X10', slicing_dict['_X10'], True), LiteralCollection('_X11', slicing_dict['_X11'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.false_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X10': ['x', 'y', 'z'], '_X11': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X10']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X10', slicing_dict['_X10'], False), LiteralCollection('_X11', slicing_dict['_X11'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.true_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X10': ['x', 'y', 'z'], '_X12': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X10']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X10', slicing_dict['_X10'], True), LiteralCollection('_X12', slicing_dict['_X12'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.false_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X10': ['x', 'y', 'z'], '_X6': ['x', 'y', 'z'], '_X8': ['x', 'y', 'z'], 'phi': ['x', 'y', 'z'], '_X12': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X10']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X10', slicing_dict['_X10'], False), LiteralCollection('_X6', slicing_dict['_X6'], False), LiteralCollection('_X8', slicing_dict['_X8'], False), LiteralCollection('phi', slicing_dict['phi'], False), LiteralCollection('_X12', slicing_dict['_X12'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
        if (change.name == '_X11'):
            if (len(change.true_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X11': ['x', 'y', 'z'], '_X10': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X11']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X11', slicing_dict['_X11'], True), LiteralCollection('_X10', slicing_dict['_X10'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.false_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X11': ['x', 'y', 'z'], '_X10': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X11']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X11', slicing_dict['_X11'], False), LiteralCollection('_X10', slicing_dict['_X10'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            try:
                old_dims = ['x1']
                detected_changes = generalizing_propagation('_X11', 'edge', change.true_slicing, change.false_slicing, old_dims, True)
                append_changes(new_changes, detected_changes)
            except Exception as e:
                raise Exception(e)
        if (change.name == '_X12'):
            if (len(change.false_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X12': ['x', 'y', 'z'], '_X6': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X12']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X12', slicing_dict['_X12'], False), LiteralCollection('_X6', slicing_dict['_X6'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.false_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X12': ['x', 'y', 'z'], '_X8': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X12']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X12', slicing_dict['_X12'], False), LiteralCollection('_X8', slicing_dict['_X8'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.false_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X12': ['x', 'y', 'z'], '_X10': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X12']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X12', slicing_dict['_X12'], False), LiteralCollection('_X10', slicing_dict['_X10'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.false_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X12': ['x', 'y', 'z'], 'phi': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X12']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X12', slicing_dict['_X12'], False), LiteralCollection('phi', slicing_dict['phi'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.true_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X12': ['x', 'y', 'z'], '_X6': ['x', 'y', 'z'], '_X8': ['x', 'y', 'z'], '_X10': ['x', 'y', 'z'], 'phi': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X12']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X12', slicing_dict['_X12'], True), LiteralCollection('_X6', slicing_dict['_X6'], False), LiteralCollection('_X8', slicing_dict['_X8'], False), LiteralCollection('_X10', slicing_dict['_X10'], False), LiteralCollection('phi', slicing_dict['phi'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.false_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X12': ['x', 'y', 'z'], '_X13': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X12']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X12', slicing_dict['_X12'], False), LiteralCollection('_X13', slicing_dict['_X13'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.true_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X12': ['x', 'y', 'z'], '_X5': ['x', 'y', 'z'], '_X13': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X12']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X12', slicing_dict['_X12'], True), LiteralCollection('_X5', slicing_dict['_X5'], True), LiteralCollection('_X13', slicing_dict['_X13'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
        if (change.name == '_X13'):
            if (len(change.true_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X13': ['x', 'y', 'z'], '_X5': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X13']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X13', slicing_dict['_X13'], True), LiteralCollection('_X5', slicing_dict['_X5'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.true_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X13': ['x', 'y', 'z'], '_X12': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X13']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X13', slicing_dict['_X13'], True), LiteralCollection('_X12', slicing_dict['_X12'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.false_slicing) > 0):
                quantified_var = ['x', 'y', 'z']
                argument_dict = {'_X13': ['x', 'y', 'z'], '_X5': ['x', 'y', 'z'], '_X12': ['x', 'y', 'z']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X13']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X13', slicing_dict['_X13'], False), LiteralCollection('_X5', slicing_dict['_X5'], True), LiteralCollection('_X12', slicing_dict['_X12'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            try:
                old_dims = ['x0', 'x1', 'x2']
                detected_changes = generalizing_propagation('_X13', '_X14', change.true_slicing, change.false_slicing, old_dims, True)
                append_changes(new_changes, detected_changes)
            except Exception as e:
                raise Exception(e)
        if (change.name == '_X14'):
            try:
                new_dims = ['x0', 'x1', 'x2']
                detected_changes = specifying_propagation('_X13', change.true_slicing, change.false_slicing, new_dims, True)
                append_changes(new_changes, detected_changes)
            except Exception as e:
                raise Exception(e)
    return new_changes

def propagate_full(changes):
    while (len(changes) != 0):
        changes = propagate(changes)

def fill_in_interpreted_domain(predicate_list):
    changes = {}
    for pred in predicate_list:
        data_array = predicate_dict[pred]
        mask = (data_array != EB.TRUE)
        data_array.values[mask] = EB.FALSE
        index_tuples = np.argwhere(mask.values)
        false_indices = [tuple((data_array[d].values[i] for (d, i) in zip(data_array.dims, idx))) for idx in index_tuples]
        append_changes(changes, {pred: Change(pred, [], false_indices)})
    return changes

def get_changes_for_comparison_operators(operator_list, domain):
    changes = {}
    if ((';EQ' in operator_list) or ('_NEQ' in operator_list)):
        equal_pairs = [(elem, elem) for elem in domain]
        unequal_pairs = [(elem1, elem2) for elem1 in domain for elem2 in domain if (elem1 != elem2)]
        if (';EQ' in operator_list):
            append_changes(changes, {';EQ': Change(';EQ', equal_pairs, unequal_pairs)})
        if ('_NEQ' in operator_list):
            append_changes(changes, {'_NEQ': Change('_NEQ', unequal_pairs, equal_pairs)})
    if (('_LEQ' in operator_list) or ('_LE' in operator_list) or ('_GEQ' in operator_list) or ('_GE' in operator_list)):
        integer_domain = {elem for elem in domain if (type(elem) == int)}
        integer_pairs = [(elem1, elem2) for elem1 in integer_domain for elem2 in integer_domain]
        integer_equal_pairs = [(elem, elem) for elem in integer_domain]
        integer_gt_pairs = [(elem1, elem2) for elem1 in integer_domain for elem2 in integer_domain if (elem1 > elem2)]
        if ('_LEQ' in operator_list):
            append_changes(changes, {'_LEQ': Change('_LEQ', [pair for pair in integer_pairs if (pair not in integer_gt_pairs)], integer_gt_pairs)})
        if ('_LE' in operator_list):
            append_changes(changes, {'_LE': Change('_LE', [pair for pair in integer_pairs if ((pair not in integer_gt_pairs) and (pair not in integer_equal_pairs))], (integer_gt_pairs + integer_equal_pairs))})
        if ('_GE' in operator_list):
            append_changes(changes, {'_GE': Change('_GE', integer_gt_pairs, [pair for pair in integer_pairs if (pair not in integer_gt_pairs)])})
        if ('_GEQ' in operator_list):
            append_changes(changes, {'_GEQ': Change('_GEQ', (integer_gt_pairs + integer_equal_pairs), [pair for pair in integer_pairs if ((pair not in integer_gt_pairs) and (pair not in integer_equal_pairs))])})
    return changes

def initial_propagation():
    asserted_literals = [('edge', (0, 1), EB.TRUE), ('edge', (0, 2), EB.TRUE), ('edge', (0, 3), EB.TRUE), ('edge', (1, 2), EB.TRUE), ('edge', (1, 3), EB.TRUE), ('edge', (1, 4), EB.TRUE), ('edge', (2, 3), EB.TRUE), ('edge', (2, 4), EB.TRUE), ('edge', (2, 5), EB.TRUE), ('edge', (3, 4), EB.TRUE), ('edge', (3, 5), EB.TRUE), ('edge', (3, 6), EB.TRUE), ('edge', (4, 5), EB.TRUE), ('edge', (4, 6), EB.TRUE), ('edge', (4, 7), EB.TRUE), ('edge', (5, 6), EB.TRUE), ('edge', (5, 7), EB.TRUE), ('edge', (5, 8), EB.TRUE), ('edge', (6, 7), EB.TRUE), ('edge', (6, 8), EB.TRUE), ('edge', (6, 9), EB.TRUE), ('edge', (7, 8), EB.TRUE), ('edge', (7, 9), EB.TRUE), ('edge', (7, 10), EB.TRUE), ('edge', (8, 9), EB.TRUE), ('edge', (8, 10), EB.TRUE), ('edge', (8, 11), EB.TRUE), ('edge', (9, 10), EB.TRUE), ('edge', (9, 11), EB.TRUE), ('edge', (9, 12), EB.TRUE), ('edge', (10, 11), EB.TRUE), ('edge', (10, 12), EB.TRUE), ('edge', (10, 13), EB.TRUE), ('edge', (11, 12), EB.TRUE), ('edge', (11, 13), EB.TRUE), ('edge', (11, 14), EB.TRUE), ('edge', (12, 13), EB.TRUE), ('edge', (12, 14), EB.TRUE), ('edge', (12, 15), EB.TRUE), ('edge', (13, 14), EB.TRUE), ('edge', (13, 15), EB.TRUE), ('edge', (13, 16), EB.TRUE), ('edge', (14, 15), EB.TRUE), ('edge', (14, 16), EB.TRUE), ('edge', (14, 17), EB.TRUE), ('edge', (15, 16), EB.TRUE), ('edge', (15, 17), EB.TRUE), ('edge', (15, 18), EB.TRUE), ('edge', (16, 17), EB.TRUE), ('edge', (16, 18), EB.TRUE), ('edge', (16, 19), EB.TRUE), ('edge', (17, 18), EB.TRUE), ('edge', (17, 19), EB.TRUE), ('edge', (17, 20), EB.TRUE), ('edge', (18, 19), EB.TRUE), ('edge', (18, 20), EB.TRUE), ('edge', (18, 21), EB.TRUE), ('edge', (19, 20), EB.TRUE), ('edge', (19, 21), EB.TRUE), ('edge', (19, 22), EB.TRUE), ('edge', (20, 21), EB.TRUE), ('edge', (20, 22), EB.TRUE), ('edge', (20, 23), EB.TRUE), ('edge', (21, 22), EB.TRUE), ('edge', (21, 23), EB.TRUE), ('edge', (21, 24), EB.TRUE), ('edge', (22, 23), EB.TRUE), ('edge', (22, 24), EB.TRUE), ('edge', (22, 25), EB.TRUE), ('edge', (23, 24), EB.TRUE), ('edge', (23, 25), EB.TRUE), ('edge', (23, 26), EB.TRUE), ('edge', (24, 25), EB.TRUE), ('edge', (24, 26), EB.TRUE), ('edge', (24, 27), EB.TRUE), ('edge', (25, 26), EB.TRUE), ('edge', (25, 27), EB.TRUE), ('edge', (25, 28), EB.TRUE), ('edge', (26, 27), EB.TRUE), ('edge', (26, 28), EB.TRUE), ('edge', (26, 29), EB.TRUE), ('edge', (27, 28), EB.TRUE), ('edge', (27, 29), EB.TRUE), ('edge', (28, 29), EB.TRUE), ('_X14', (), EB.TRUE)]
    changes = {}
    for asserted_lit in asserted_literals:
        predicate_dict[asserted_lit[0]].loc[asserted_lit[1]] = asserted_lit[2]
        if (asserted_lit[2] == EB.TRUE):
            append_changes(changes, {asserted_lit[0]: Change(asserted_lit[0], [asserted_lit[1]], [])})
        elif (asserted_lit[2] == EB.FALSE):
            append_changes(changes, {asserted_lit[0]: Change(asserted_lit[0], [], [asserted_lit[1]])})
    append_changes(changes, fill_in_interpreted_domain(['edge']))
    operator_list = []
    domain = []
    comparison_changes = get_changes_for_comparison_operators(operator_list, domain)
    append_changes(changes, comparison_changes)
    propagate_full(changes)

def get_grounded_atom_name(name, comb):
    atom_name = name
    for elem in comb:
        atom_name += ('_' + str(elem.item()))
    return atom_name

def get_grounded_atoms_for_display(atom_name):
    ground_atoms = {}
    data_array = predicate_dict[atom_name]
    name = data_array.name
    new_domains = [data_array.coords[dim].values for dim in data_array.dims]
    for comb in product(*new_domains):
        ground_atom_name = get_grounded_atom_name(name, comb)
        ground_atoms[ground_atom_name] = data_array.loc[comb].values.item()
    return ground_atoms

def test_on_user_input():
    current_var = ''
    start = time.time()
    initial_propagation()
    end = time.time()
    print('Initial propagation: ', (end - start))
    for var_name in predicate_dict.keys():
        if (not var_name.startswith('_')):
            print('__________________________')
            grounded_var = get_grounded_atoms_for_display(var_name)
            for (key, val) in grounded_var.items():
                print(((key + ': ') + str(val)))
            print('__________________________')
    while (current_var.lower() != 'stop'):
        current_var = input('Give the name of the variable\n')
        if (current_var not in predicate_dict.keys()):
            print("Try again, this variable doesn't exist")
            continue
        args = []
        for i in range(len(predicate_dict[current_var].dims)):
            new_arg = input(f'''Give argument number {(i + 1)}:
''')
            if new_arg.isdigit():
                args.append(int(new_arg))
            else:
                args.append(new_arg)
        b = input('True (1) or false (0)?\n')
        if (b != '0'):
            b_val = EB.TRUE
        else:
            b_val = EB.FALSE
        current_array = predicate_dict[current_var]
        if (current_array.loc[(*args,)] == EB.UNKNOWN):
            current_array.loc[(*args,)] = b_val
        else:
            print('Sorry, this variable is already assigned a value')
            continue
        change = {}
        if (b_val == EB.TRUE):
            append_changes(change, {current_var: Change(current_var, [tuple(args)], [])})
        else:
            append_changes(change, {current_var: Change(current_var, [], [tuple(args)])})
        start = time.time()
        propagate_full(change)
        end = time.time()
        for var_name in predicate_dict.keys():
            if (not var_name.startswith('_')):
                print('__________________________')
                grounded_var = get_grounded_atoms_for_display(var_name)
                for (key, val) in grounded_var.items():
                    print(((key + ': ') + str(val)))
                print('__________________________')
        print('Time to propagate: ', (end - start))
test_on_user_input()
