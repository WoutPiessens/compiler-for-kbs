# An example of the generated Python code resulting from the following IDP-program:

# vocabulary V{
#     type node := {0..5}
#     phi: node -> Bool
#     mu: node -> Bool
#     tau: node -> Bool
# }
#
# theory T:V{
#     !x in node: phi(x) | mu(x) | tau(x).
# }
#
# structure S:V{}


import math
import time
from enum import Enum
from itertools import product
import xarray as xr
import numpy as np
from dash import Dash, html, dcc, State, Input, Output, ALL, callback_context

# Possible truth values that can be derived during propagation. NONE indicates that nothing new was derived.
class EB(Enum):
    TRUE = 1
    FALSE = 2
    UNKNOWN = 0
    INCONSISTENT = (- 1)
    NONE = (- 2)

# Objects of this class indicate a change to a certain predicate.
# The name of the predicate is given, and the arguments for which the predicate now evaluates to true/false are given too.
# This class is equivalent to a literal collection (LC), as described in Definition 6 of section 4.4.2 of the thesis text.
class Change():
    def __init__(self, name, true_slicing, false_slicing):
        self.name = name
        self.true_slicing = true_slicing
        self.false_slicing = false_slicing

# Objects of this class indicate a literal collection, as described in Definition 6 of section 4.4.2.
class LiteralCollection():

    def __init__(self, name, slicing, b):
        self.name = name
        self.slicing = slicing
        self.b = b

# Objects of this class indicate the result of propagation:
# - the truth value that is derived
# - the position in the list of atoms for which it is derived
class PropagateResult():

    def __init__(self, truth, position=0):
        self.truth = truth
        self.position = position

# These data structures contain all predicates in the IDP program (including functions that were transformed to predicates), and all auxiliary predicates.
# Each argument position has a unique dimension name, and the possible values are enumerated.
# The information stored here is described in section 4.4.1.
predicates = [xr.DataArray(np.full((6,), EB.UNKNOWN), name='phi', dims=('x0',), coords={'x0': [0, 1, 2, 3, 4, 5]}), xr.DataArray(np.full((6,), EB.UNKNOWN), name='mu', dims=('x0',), coords={'x0': [0, 1, 2, 3, 4, 5]}), xr.DataArray(np.full((6,), EB.UNKNOWN), name='tau', dims=('x0',), coords={'x0': [0, 1, 2, 3, 4, 5]}), xr.DataArray(np.full((6,), EB.UNKNOWN), name='_X1', dims=('x0',), coords={'x0': [0, 1, 2, 3, 4, 5]}), xr.DataArray(np.array(EB.UNKNOWN), name='_X2')]
predicate_dict = {pred.name: pred for pred in predicates}

# The following two lists are used for caching, as described in section 4.4.5.1.

# This list indicates predicates that necessarily evaluate to TRUE for all arguments.
true_list = ['_X1']
# This list indicates predicates that have not yet been changed by the propagate() function, and therefore evaluate to UNKNOWN for all arguments.
# Initially, this is every predicate. After initial propagation and further propagation this list will shrink.
unknown_list = [pred.name for pred in predicates]

# The blueprint for conditional propagation, which is closely related to UNSAT-sets (see 'voorwaardelijke propagatie' in section 4.4.4):
# - if all arguments evaluate to true, an inconsistency is derived
# - if all arguments evaluate to true except one, that one must evaluate to false
# - otherwise, no consequences can be derived
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

# The blueprint for unconditional propagation (see 'onvoorwaardelijke propagatie' in section 4.4.4)
#  - If a certain argument evaluates to unknown, it must become true.
#  - If a certain argument evaluates to true, it stays like that.
#  - If a certain argument evaluates to false, an inconsistency is derived.
def unconditional_propagate(args):
    mapping = {EB.UNKNOWN: EB.TRUE, EB.TRUE: EB.NONE, EB.FALSE: EB.INCONSISTENT}
    return [mapping.get(arg, arg) for arg in args]

# Method to retrieve a list of coordinates (arguments to a predicate) from a DataArray object.
# This is done differently depending on the length of the list of coordinates, for time efficiency reasons.
def get_from_data_array(data_array, slices, threshold=100):
    if (len(slices) > threshold):
        vals = data_array.stack(points=data_array.dims).loc[slices].values
    else:
        index_list = [dict(zip(data_array.dims, t)) for t in slices]
        vals = [data_array.loc[i].values.item() for i in index_list]
    return vals

# Calculates the inverse of a truth value. UNKNOWN and INCONSISTENT stay the same.
def inverse(x):
    if (x == EB.TRUE):
        return EB.FALSE
    if (x == EB.FALSE):
        return EB.TRUE
    return x

# Helper function to concatenate two dictionaries of changes, where the keys are predicate names and the values are lists of Change objects.
# Since all new changes pass through this function, this is also where changed predicate names are removed from the unknown_list.
def append_changes(old, new):
    global unknown_list
    for key in new.keys():
        if (key in old.keys()):
            old[key].true_slicing.extend(new[key].true_slicing)
            old[key].false_slicing.extend(new[key].false_slicing)
        else:
            old[key] = Change(key, new[key].true_slicing, new[key].false_slicing)
    unknown_list = [elem for elem in unknown_list if (elem not in new.keys())]

# Helper function to wrap around DataArray requests.
#  - in case the predicate is a mathematical operator (=, !=, <, <=, >, >=), the truth value for all coordinates can be calculated.
#  - in case the predicate is in the true_list or unknown_list, the truth values are always true/unknown and do not need to be looked up.
#  - Otherwise, a lookup is needed.
# In case an inverse operation is needed, this is also done here.
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

# Helper function to write derived consequences to the correct DataArray.
# To achieve this, changes are grouped by the literal collections representing the part of the rule that was enforced (led to a consequence being derived).
# This grouping is done for time efficiency reasons.
# Also, depending on the amount of changed coordinates per literal collection, a different writing method is used, also for time efficiency reasons.
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


# Helper function to consider three different cases for conditional propagation.
# An inconsistency is derived -> an exception is thrown.
# (A) logical consequence(s) is/are derived -> consequences are grouped by the enforced literal collection, and write_to_data_array() is called.
# Nothing is derived -> the empty dictionary of changes is returned
def handle_conditional_propagate_results(rule, result_list):
    incons_indices = np.where((result_list == PropagateResult(EB.INCONSISTENT)))[0]
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

# Function implementing normal propagation as described in Definition 8 of section 4.4.3.1.
# This also matches with conditional propagation ('voorwaardelijke propagatie') as described in section 4.4.4.
# There are three important steps:
#   - Retrieving the truth values from the DataArrays.
#   - Doing the necessary calculations by calling conditional_propagate() elementwise.
#   - Writing consequences to the DataArrays and gathering them in a dictionary with Change objects for further propagation.
def normal_propagation(rule):
    truth_list = [get_from_data_array_wrap(r.name, r.slicing, r.b) for r in rule]
    result_list = np.apply_along_axis(conditional_propagate, axis=0, arr=np.array(truth_list))
    try:
        new_changes = handle_conditional_propagate_results(rule, result_list)
        return new_changes
    except Exception as e:
        raise Exception(e)

# Helper function to consider three different cases for unconditional propagation ('onvoorwaardelijke propagatie' in section 4.4.4).
# An inconsistency is derived -> an exception is thrown.
# (A) logical consequence(s) is/are derived -> consequences are grouped by the enforced literal collection, and write_to_data_array() is called.
# Nothing is derived -> the empty dictionary of changes is returned
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


# Function implementing unconditional propagation as described in section 4.4.4.
# There are three important steps:
#   - Retrieving the truth values from the DataArrays.
#   - Doing the necessary calculations by calling unconditional_propagate() on the truth values.
#   - Writing consequences to the DataArrays and gathering them in a dictionary with Change objects for further propagation.
def unconditional_propagate_wrap(big_array, big_slices, bool_value):
    args = get_from_data_array_wrap(big_array.name, big_slices, bool_value)
    result_list = np.array(unconditional_propagate(np.array(args)))
    try:
        new_changes = handle_unconditional_propagate_results(big_array.name, big_slices, result_list, bool_value)
        return new_changes
    except Exception as e:
        raise Exception(e)

# Helper function for incremental propagation, as described in section 4.4.4. ('incrementele propagatie')
# Given a 'small' coordinate, for which the values stay the same (e.g. (0,2)).
# Given a DataArray object.
# Given the dimensions that should be added to get a 'big' coordinate.
# Then this information is used together to add the new dimensions, for all possible values in the domain of these dimensions.
# For example: if small_coordinate = (0,2), dims = ['x1', 'x3'] (the second and fourth dimension), with both domains [0,1,2,3] in the DataArray object.
# The first coordinate will be (0,0,2,0)
# The next coordinate will be (0,1,2,0), (0,2,2,0), (0,3,2,0), (0,0,2,1) ...

def calculate_first_coordinate(small_coordinate, data_array, changing_dims):
    new_coordinate = tuple(small_coordinate)
    index = 0
    for dim in data_array.dims:
        if (dim in changing_dims):
            new_coordinate = ((new_coordinate[:index] + (data_array.coords[dim][0].item(),)) + new_coordinate[index:])
        index += 1
    return new_coordinate


# See explanation under calculate_first_coordinate()
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

# Function implementing incremental propagation, as described in section 4.4.4.
# This is done as follows:
# All coordinates that need to be checked are generated incrementally, with calculate_first_coordinate() and calculate_next_coordinate().
# The algorithm can stop when it knows it cannot derive anything anymore. For this, the following conditions are checked.
# If for a certain small coordinate, one coordinate evaluates to false, the algorithm can stop for that small coordinate. No consequences can be derived (analogous to conditional propagation)
# If for a certain small coordinate, more than one coordinate evaluates to unknown, the algorithm can stop for that small coordinate. No consequences can be derived (analogous to conditional propagation)
# If the algorithm does finish for a certain small coordinate, the following conditions are checked:
# If for a certain small coordinate, exactly one coordinate evaluates to unknown, this coordinate is set to true (or false in case inversion is needed)
# If for a certain small coordinate, all coordinates evaluate to true, an inconsistency is derived.
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


# Wrapper function for incremental propagation that also checks the truth value for the small coordinate. This is needed for generalizing propagation.
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

# Helper function that matches a coordinate of one predicate to a coordinate of another predicate. This is used in normal propagation.
# For example, if a propagation rule is derived between A(x,y) and B(y,x), and a change is detected for A(3,4), than consequences possibly need to be derived for B(4,3).
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

# Helper function that checks if a certain coordinate can be filled in a certain argument 'template' with quantified variables.
# For example
#   - (2,3) can be filled in in (x,y), x = 2 and y = 3
#   - (2,2) can be filled in in (x,x), x = 2
#   - (2,3) cannot be filled in in (x,x)
#   - (2,3) can be filled in in (x,3), x = 2
#   - (2,3) cannot be filled in in (x,4)
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

# Function that maps coordinates to each other in order to perform normal propagation.
# It corresponds to the coords function described in Algorithm 1 of section 4.4.3.1.
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

# Function that adds values to coordinates, coming from the domain of newly added dimensions.
# Corresponds with the increase function from Algorithm 2 of section 4.4.3.2.
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

# Function that removes values from coordinates for removed dimensions.
# Corresponds with the decrease function from Algorithm 3 of section 4.4.3.3.
def reduce_dims(slicing, old, extra_dims):
    indices = np.array([i for (i, value) in enumerate(old.dims) if (value not in extra_dims)])
    new_slicing = {tuple((tup[i] for i in indices)) for tup in slicing}
    return new_slicing

# Function implementing specifying propagation, making a case distinction between 4 cases.
# This is analogous to Definition 9 in section 4.4.3.2.
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


# Function implementing generalizing propagation, making a case distinction between 4 cases.
# This is analogous to Definition 10 in section 4.4.3.3.
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

# Helper function that, for a given predicate that was previously a function, and for a given coordinate, gives all possible other outputs to that former function.
# In other words, for the last argument of the coordinates, all other values in the domain are iterated over.
# e.g. (0,1) and the second dimension has domain [0,1,2,3] -> output: (0,0), (0,2), (0,3)
# Corresponds to the function 'codomain' in Algorithm 4 of section 4.4.3.4.
def add_all_function_outputs(data_array, slice):
    all_outputs = []
    scope = data_array.coords[data_array.dims[(- 1)]].values
    for elem in scope:
        if (elem != slice[(- 1)]):
            all_outputs.append((slice[:(- 1)] + (elem.item(),)))
    return all_outputs

# Function implementing function propagation, making a case distinction between 2 cases.
# This is analogous to Definition 11 in section 4.4.3.4.
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


# Main propagate function.
# For every predicate name (including auxiliary predicates),
# the corresponding propagators (in other words, propagators that can be activated by a change to that predicate)
# are grouped together under the if-statement for that predicate name.
def propagate(changes):
    new_changes = {}
    for change in changes.values():
        if (change.name == '_X1'):
            if (len(change.false_slicing) > 0):
                quantified_var = ['x']
                argument_dict = {'_X1': ['x'], 'phi': ['x']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X1']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X1', slicing_dict['_X1'], False), LiteralCollection('phi', slicing_dict['phi'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.false_slicing) > 0):
                quantified_var = ['x']
                argument_dict = {'_X1': ['x'], 'mu': ['x']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X1']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X1', slicing_dict['_X1'], False), LiteralCollection('mu', slicing_dict['mu'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.false_slicing) > 0):
                quantified_var = ['x']
                argument_dict = {'_X1': ['x'], 'tau': ['x']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X1']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X1', slicing_dict['_X1'], False), LiteralCollection('tau', slicing_dict['tau'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.true_slicing) > 0):
                quantified_var = ['x']
                argument_dict = {'_X1': ['x'], 'phi': ['x'], 'mu': ['x'], 'tau': ['x']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['_X1']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('_X1', slicing_dict['_X1'], True), LiteralCollection('phi', slicing_dict['phi'], False), LiteralCollection('mu', slicing_dict['mu'], False), LiteralCollection('tau', slicing_dict['tau'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            try:
                old_dims = ['x0']
                detected_changes = generalizing_propagation('_X1', '_X2', change.true_slicing, change.false_slicing, old_dims, True)
                append_changes(new_changes, detected_changes)
            except Exception as e:
                raise Exception(e)
        if (change.name == 'phi'):
            if (len(change.true_slicing) > 0):
                quantified_var = ['x']
                argument_dict = {'phi': ['x'], '_X1': ['x']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['phi']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('phi', slicing_dict['phi'], True), LiteralCollection('_X1', slicing_dict['_X1'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.false_slicing) > 0):
                quantified_var = ['x']
                argument_dict = {'phi': ['x'], 'mu': ['x'], 'tau': ['x'], '_X1': ['x']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['phi']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('phi', slicing_dict['phi'], False), LiteralCollection('mu', slicing_dict['mu'], False), LiteralCollection('tau', slicing_dict['tau'], False), LiteralCollection('_X1', slicing_dict['_X1'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
        if (change.name == 'mu'):
            if (len(change.true_slicing) > 0):
                quantified_var = ['x']
                argument_dict = {'mu': ['x'], '_X1': ['x']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['mu']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('mu', slicing_dict['mu'], True), LiteralCollection('_X1', slicing_dict['_X1'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.false_slicing) > 0):
                quantified_var = ['x']
                argument_dict = {'mu': ['x'], 'phi': ['x'], 'tau': ['x'], '_X1': ['x']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['mu']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('mu', slicing_dict['mu'], False), LiteralCollection('phi', slicing_dict['phi'], False), LiteralCollection('tau', slicing_dict['tau'], False), LiteralCollection('_X1', slicing_dict['_X1'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
        if (change.name == 'tau'):
            if (len(change.true_slicing) > 0):
                quantified_var = ['x']
                argument_dict = {'tau': ['x'], '_X1': ['x']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.true_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['tau']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('tau', slicing_dict['tau'], True), LiteralCollection('_X1', slicing_dict['_X1'], False)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
            if (len(change.false_slicing) > 0):
                quantified_var = ['x']
                argument_dict = {'tau': ['x'], 'phi': ['x'], 'mu': ['x'], '_X1': ['x']}
                slicing_dict = map_indices_wrap(argument_dict, change.name, change.false_slicing, quantified_var)
                if ((slicing_dict is not None) and (len(slicing_dict['tau']) > 0)):
                    try:
                        detected_changes = normal_propagation([LiteralCollection('tau', slicing_dict['tau'], False), LiteralCollection('phi', slicing_dict['phi'], False), LiteralCollection('mu', slicing_dict['mu'], False), LiteralCollection('_X1', slicing_dict['_X1'], True)])
                        append_changes(new_changes, detected_changes)
                    except Exception as e:
                        raise Exception(e)
        if (change.name == '_X2'):
            try:
                new_dims = ['x0']
                detected_changes = specifying_propagation('_X1', change.true_slicing, change.false_slicing, new_dims, True)
                append_changes(new_changes, detected_changes)
            except Exception as e:
                raise Exception(e)
    return new_changes

# This function keeps calling propagate() until no more changes are detected.
def propagate_full(changes):
    while (len(changes) != 0):
        changes = propagate(changes)

# This function fills in all truth values of a predicate that has an interpretation in the structure of the original IDP-program.
# We follow IDP-Z3: an interpretation of a predicate/function in a structure is total, so the arguments that are not mentioned evaluate to FALSE.
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


# This function initializes all knowledge regarding mathematical comparison operators (=, !=, <, <=, >, >=).
# It takes a list of all comparison operators that are used, and all domain elements that are compared.
# Then it propagates the knowledge that follows from the mathematical definition of the operators, for all pairs of domain elements.
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

# This function calls propagate() when the program is run initially.
# First, it derives the following knowledge:
#    - propositional auxiliary symbols (derived in the ENF algorithm) that represent a rule must evaluate to true. They are of the type AssertLiteral
#    - interpreted predicates/functions should be true for the mentioned values and false for all others
#    - knowledge about comparison operators (see get_changes_for_comparison_operators())
# Then it calls propagate() with those changes and derives further consequences
def initial_propagation():
    asserted_literals = [('_X2', (), EB.TRUE)]
    changes = {}
    for asserted_lit in asserted_literals:
        predicate_dict[asserted_lit[0]].loc[asserted_lit[1]] = asserted_lit[2]
        if (asserted_lit[2] == EB.TRUE):
            append_changes(changes, {asserted_lit[0]: Change(asserted_lit[0], [asserted_lit[1]], [])})
        elif (asserted_lit[2] == EB.FALSE):
            append_changes(changes, {asserted_lit[0]: Change(asserted_lit[0], [], [asserted_lit[1]])})
    append_changes(changes, fill_in_interpreted_domain([]))
    operator_list = []
    domain = []
    comparison_changes = get_changes_for_comparison_operators(operator_list, domain)
    append_changes(changes, comparison_changes)
    propagate_full(changes)

# Auxiliary function to get the unique name of a grounded atom, given the name of the predicate and the arguments
def get_grounded_atom_name(name, comb):
    atom_name = name
    for elem in comb:
        atom_name += ('_' + str(elem.item()))
    return atom_name

# Auxiliary function to help display grounded atoms and their truth values to the user
def get_grounded_atoms_for_display(atom_name):
    ground_atoms = {}
    data_array = predicate_dict[atom_name]
    name = data_array.name
    new_domains = [data_array.coords[dim].values for dim in data_array.dims]
    for comb in product(*new_domains):
        ground_atom_name = get_grounded_atom_name(name, comb)
        ground_atoms[ground_atom_name] = data_array.loc[comb].values.item()
    return ground_atoms

# Auxiliary function to support user input and interaction through the terminal
# This can also be an interactive application (Dash application), if this option is chosen in second_method_main.py
# Logical consequences of initial propagation can also be written to a .pkl file, if this option is chosen in second_method_main.py
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
