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


# This data structure contains, for every possible grounded atom, the truth values that are still possible.
# Before the program is executed, both true and false are possible for any atom.
# An initial propagation step will already eliminate certain options.
structure = {'mu_5': {True, False}, 'mu_3': {True, False}, 'mu_0': {True, False}, '_X1_3': {True, False}, '_X2': {True, False}, 'mu_2': {True, False}, 'mu_4': {True, False}, 'tau_5': {True, False}, 'phi_3': {True, False}, 'phi_0': {True, False}, 'phi_4': {True, False}, '_X1_5': {True, False}, 'tau_2': {True, False}, '_X1_0': {True, False}, 'tau_1': {True, False}, '_X1_4': {True, False}, 'tau_0': {True, False}, 'mu_1': {True, False}, 'tau_4': {True, False}, 'phi_5': {True, False}, '_X1_2': {True, False}, 'phi_1': {True, False}, 'tau_3': {True, False}, 'phi_2': {True, False}, '_X1_1': {True, False}, '_X1_0': {False, True}, 'phi_0': {False, True}, 'mu_0': {False, True}, 'tau_0': {False, True}, '_X1_1': {False, True}, 'phi_1': {False, True}, 'mu_1': {False, True}, 'tau_1': {False, True}, '_X1_2': {False, True}, 'phi_2': {False, True}, 'mu_2': {False, True}, 'tau_2': {False, True}, '_X1_3': {False, True}, 'phi_3': {False, True}, 'mu_3': {False, True}, 'tau_3': {False, True}, '_X1_4': {False, True}, 'phi_4': {False, True}, 'mu_4': {False, True}, 'tau_4': {False, True}, '_X1_5': {False, True}, 'phi_5': {False, True}, 'mu_5': {False, True}, 'tau_5': {False, True}, '_X2': {False, True}}

# Helper function to update the structure.
def update_structure(changes):
    for (key, value) in changes.items():
        structure[key] = value

# Helper function to print the structure.
def print_structure():
    for key in structure.keys():
        if (not key.startswith('_')):
            print(key, end='')
            print(':  ', end='')
            print(structure[key])
            print()

# Helper function to check if any grounded atoms are unsatisfiable, in other words, if there are no more possible truth values to be assigned.
def check_unsat_fields(changes):
    unsat_fields = set()
    for key in changes.keys():
        if (len(changes[key]) == 0):
            unsat_fields.add(key)
    return unsat_fields

# Helper function to fuse together different changes that were detected.
def intersect_changes(changes):
    intersected_changes = {}
    for key in changes.keys():
        if (len(changes[key]) > 0):
            intersected_changes[key] = changes[key].pop()
            while (len(changes[key]) > 0):
                intersected_changes[key] = intersected_changes[key].intersection(changes[key].pop())
            if (intersected_changes[key] == structure[key]):
                del intersected_changes[key]
    return intersected_changes

# Propagate function: this function implements all the grounded propagators which were derived in the compiler,
# by checking the condition in the structure, and adding the consequence to changes if the condition holds.
def propagate(changes):
    new_changes = {key: [] for key in structure.keys()}
    for (key, value) in changes.items():
        if (not all(((elem == True) for elem in structure['_X2']))):
            new_changes['_X2'].append({elem for elem in structure['_X2'] if (elem == True)})
        if (key == 'phi_0'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_0']))):
                    new_changes['_X1_0'].append({elem for elem in structure['_X1_0'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['tau_0']))):
                    if (all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == False) for elem in structure['mu_0']))):
                        new_changes['tau_0'].append({elem for elem in structure['tau_0'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['mu_0']))):
                    if (all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == False) for elem in structure['tau_0']))):
                        new_changes['mu_0'].append({elem for elem in structure['mu_0'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_0']))):
                    if (all(((elem == False) for elem in structure['mu_0'])) and all(((elem == False) for elem in structure['tau_0']))):
                        new_changes['_X1_0'].append({elem for elem in structure['_X1_0'] if (elem == False)})
        if (key == '_X1_0'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_5']))):
                    if (all(((elem == True) for elem in structure['_X1_1'])) and all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X1_5'].append({elem for elem in structure['_X1_5'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X1_4']))):
                    if (all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_1']))):
                        new_changes['_X1_4'].append({elem for elem in structure['_X1_4'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X1_1']))):
                    if (all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X1_1'].append({elem for elem in structure['_X1_1'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['mu_0']))):
                    if (all(((elem == False) for elem in structure['phi_0'])) and all(((elem == False) for elem in structure['tau_0']))):
                        new_changes['mu_0'].append({elem for elem in structure['mu_0'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_3']))):
                    if (all(((elem == True) for elem in structure['_X1_1'])) and all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X1_3'].append({elem for elem in structure['_X1_3'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X2']))):
                    if (all(((elem == True) for elem in structure['_X1_1'])) and all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X2'].append({elem for elem in structure['_X2'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['phi_0']))):
                    if (all(((elem == False) for elem in structure['mu_0'])) and all(((elem == False) for elem in structure['tau_0']))):
                        new_changes['phi_0'].append({elem for elem in structure['phi_0'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_2']))):
                    if (all(((elem == True) for elem in structure['_X1_1'])) and all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X1_2'].append({elem for elem in structure['_X1_2'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['tau_0']))):
                    if (all(((elem == False) for elem in structure['phi_0'])) and all(((elem == False) for elem in structure['mu_0']))):
                        new_changes['tau_0'].append({elem for elem in structure['tau_0'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['mu_0']))):
                    new_changes['mu_0'].append({elem for elem in structure['mu_0'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['phi_0']))):
                    new_changes['phi_0'].append({elem for elem in structure['phi_0'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['tau_0']))):
                    new_changes['tau_0'].append({elem for elem in structure['tau_0'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X2']))):
                    new_changes['_X2'].append({elem for elem in structure['_X2'] if (elem == False)})
        if (key == 'mu_0'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_0']))):
                    new_changes['_X1_0'].append({elem for elem in structure['_X1_0'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['phi_0']))):
                    if (all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == False) for elem in structure['tau_0']))):
                        new_changes['phi_0'].append({elem for elem in structure['phi_0'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['tau_0']))):
                    if (all(((elem == False) for elem in structure['phi_0'])) and all(((elem == True) for elem in structure['_X1_0']))):
                        new_changes['tau_0'].append({elem for elem in structure['tau_0'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_0']))):
                    if (all(((elem == False) for elem in structure['phi_0'])) and all(((elem == False) for elem in structure['tau_0']))):
                        new_changes['_X1_0'].append({elem for elem in structure['_X1_0'] if (elem == False)})
        if (key == 'tau_0'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_0']))):
                    new_changes['_X1_0'].append({elem for elem in structure['_X1_0'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_0']))):
                    if (all(((elem == False) for elem in structure['phi_0'])) and all(((elem == False) for elem in structure['mu_0']))):
                        new_changes['_X1_0'].append({elem for elem in structure['_X1_0'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['mu_0']))):
                    if (all(((elem == False) for elem in structure['phi_0'])) and all(((elem == True) for elem in structure['_X1_0']))):
                        new_changes['mu_0'].append({elem for elem in structure['mu_0'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['phi_0']))):
                    if (all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == False) for elem in structure['mu_0']))):
                        new_changes['phi_0'].append({elem for elem in structure['phi_0'] if (elem == True)})
        if (key == '_X1_1'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_5']))):
                    if (all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X1_5'].append({elem for elem in structure['_X1_5'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['phi_1']))):
                    if (all(((elem == False) for elem in structure['mu_1'])) and all(((elem == False) for elem in structure['tau_1']))):
                        new_changes['phi_1'].append({elem for elem in structure['phi_1'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_0']))):
                    if (all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X1_0'].append({elem for elem in structure['_X1_0'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X1_3']))):
                    if (all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X1_3'].append({elem for elem in structure['_X1_3'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X1_4']))):
                    if (all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_0']))):
                        new_changes['_X1_4'].append({elem for elem in structure['_X1_4'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['tau_1']))):
                    if (all(((elem == False) for elem in structure['phi_1'])) and all(((elem == False) for elem in structure['mu_1']))):
                        new_changes['tau_1'].append({elem for elem in structure['tau_1'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X2']))):
                    if (all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X2'].append({elem for elem in structure['_X2'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['mu_1']))):
                    if (all(((elem == False) for elem in structure['phi_1'])) and all(((elem == False) for elem in structure['tau_1']))):
                        new_changes['mu_1'].append({elem for elem in structure['mu_1'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_2']))):
                    if (all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X1_2'].append({elem for elem in structure['_X1_2'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['tau_1']))):
                    new_changes['tau_1'].append({elem for elem in structure['tau_1'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['phi_1']))):
                    new_changes['phi_1'].append({elem for elem in structure['phi_1'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['mu_1']))):
                    new_changes['mu_1'].append({elem for elem in structure['mu_1'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X2']))):
                    new_changes['_X2'].append({elem for elem in structure['_X2'] if (elem == False)})
        if (key == 'phi_1'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_1']))):
                    new_changes['_X1_1'].append({elem for elem in structure['_X1_1'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_1']))):
                    if (all(((elem == False) for elem in structure['mu_1'])) and all(((elem == False) for elem in structure['tau_1']))):
                        new_changes['_X1_1'].append({elem for elem in structure['_X1_1'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['tau_1']))):
                    if (all(((elem == False) for elem in structure['mu_1'])) and all(((elem == True) for elem in structure['_X1_1']))):
                        new_changes['tau_1'].append({elem for elem in structure['tau_1'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['mu_1']))):
                    if (all(((elem == True) for elem in structure['_X1_1'])) and all(((elem == False) for elem in structure['tau_1']))):
                        new_changes['mu_1'].append({elem for elem in structure['mu_1'] if (elem == True)})
        if (key == 'mu_1'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_1']))):
                    new_changes['_X1_1'].append({elem for elem in structure['_X1_1'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['phi_1']))):
                    if (all(((elem == True) for elem in structure['_X1_1'])) and all(((elem == False) for elem in structure['tau_1']))):
                        new_changes['phi_1'].append({elem for elem in structure['phi_1'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_1']))):
                    if (all(((elem == False) for elem in structure['phi_1'])) and all(((elem == False) for elem in structure['tau_1']))):
                        new_changes['_X1_1'].append({elem for elem in structure['_X1_1'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['tau_1']))):
                    if (all(((elem == False) for elem in structure['phi_1'])) and all(((elem == True) for elem in structure['_X1_1']))):
                        new_changes['tau_1'].append({elem for elem in structure['tau_1'] if (elem == True)})
        if (key == 'tau_1'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_1']))):
                    new_changes['_X1_1'].append({elem for elem in structure['_X1_1'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['mu_1']))):
                    if (all(((elem == False) for elem in structure['phi_1'])) and all(((elem == True) for elem in structure['_X1_1']))):
                        new_changes['mu_1'].append({elem for elem in structure['mu_1'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['phi_1']))):
                    if (all(((elem == False) for elem in structure['mu_1'])) and all(((elem == True) for elem in structure['_X1_1']))):
                        new_changes['phi_1'].append({elem for elem in structure['phi_1'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_1']))):
                    if (all(((elem == False) for elem in structure['phi_1'])) and all(((elem == False) for elem in structure['mu_1']))):
                        new_changes['_X1_1'].append({elem for elem in structure['_X1_1'] if (elem == False)})
        if (key == '_X1_2'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['tau_2']))):
                    if (all(((elem == False) for elem in structure['phi_2'])) and all(((elem == False) for elem in structure['mu_2']))):
                        new_changes['tau_2'].append({elem for elem in structure['tau_2'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_1']))):
                    if (all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X1_1'].append({elem for elem in structure['_X1_1'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X1_0']))):
                    if (all(((elem == True) for elem in structure['_X1_1'])) and all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X1_0'].append({elem for elem in structure['_X1_0'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['phi_2']))):
                    if (all(((elem == False) for elem in structure['tau_2'])) and all(((elem == False) for elem in structure['mu_2']))):
                        new_changes['phi_2'].append({elem for elem in structure['phi_2'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_5']))):
                    if (all(((elem == True) for elem in structure['_X1_1'])) and all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X1_5'].append({elem for elem in structure['_X1_5'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X1_4']))):
                    if (all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_1']))):
                        new_changes['_X1_4'].append({elem for elem in structure['_X1_4'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['mu_2']))):
                    if (all(((elem == False) for elem in structure['phi_2'])) and all(((elem == False) for elem in structure['tau_2']))):
                        new_changes['mu_2'].append({elem for elem in structure['mu_2'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_3']))):
                    if (all(((elem == True) for elem in structure['_X1_1'])) and all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X1_3'].append({elem for elem in structure['_X1_3'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X2']))):
                    if (all(((elem == True) for elem in structure['_X1_1'])) and all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X2'].append({elem for elem in structure['_X2'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X2']))):
                    new_changes['_X2'].append({elem for elem in structure['_X2'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['phi_2']))):
                    new_changes['phi_2'].append({elem for elem in structure['phi_2'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['tau_2']))):
                    new_changes['tau_2'].append({elem for elem in structure['tau_2'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['mu_2']))):
                    new_changes['mu_2'].append({elem for elem in structure['mu_2'] if (elem == False)})
        if (key == 'phi_2'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_2']))):
                    new_changes['_X1_2'].append({elem for elem in structure['_X1_2'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_2']))):
                    if (all(((elem == False) for elem in structure['tau_2'])) and all(((elem == False) for elem in structure['mu_2']))):
                        new_changes['_X1_2'].append({elem for elem in structure['_X1_2'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['mu_2']))):
                    if (all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == False) for elem in structure['tau_2']))):
                        new_changes['mu_2'].append({elem for elem in structure['mu_2'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['tau_2']))):
                    if (all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == False) for elem in structure['mu_2']))):
                        new_changes['tau_2'].append({elem for elem in structure['tau_2'] if (elem == True)})
        if (key == 'mu_2'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_2']))):
                    new_changes['_X1_2'].append({elem for elem in structure['_X1_2'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_2']))):
                    if (all(((elem == False) for elem in structure['phi_2'])) and all(((elem == False) for elem in structure['tau_2']))):
                        new_changes['_X1_2'].append({elem for elem in structure['_X1_2'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['tau_2']))):
                    if (all(((elem == False) for elem in structure['phi_2'])) and all(((elem == True) for elem in structure['_X1_2']))):
                        new_changes['tau_2'].append({elem for elem in structure['tau_2'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['phi_2']))):
                    if (all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == False) for elem in structure['tau_2']))):
                        new_changes['phi_2'].append({elem for elem in structure['phi_2'] if (elem == True)})
        if (key == 'tau_2'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_2']))):
                    new_changes['_X1_2'].append({elem for elem in structure['_X1_2'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['phi_2']))):
                    if (all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == False) for elem in structure['mu_2']))):
                        new_changes['phi_2'].append({elem for elem in structure['phi_2'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_2']))):
                    if (all(((elem == False) for elem in structure['phi_2'])) and all(((elem == False) for elem in structure['mu_2']))):
                        new_changes['_X1_2'].append({elem for elem in structure['_X1_2'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['mu_2']))):
                    if (all(((elem == False) for elem in structure['phi_2'])) and all(((elem == True) for elem in structure['_X1_2']))):
                        new_changes['mu_2'].append({elem for elem in structure['mu_2'] if (elem == True)})
        if (key == 'phi_3'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_3']))):
                    new_changes['_X1_3'].append({elem for elem in structure['_X1_3'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_3']))):
                    if (all(((elem == False) for elem in structure['tau_3'])) and all(((elem == False) for elem in structure['mu_3']))):
                        new_changes['_X1_3'].append({elem for elem in structure['_X1_3'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['mu_3']))):
                    if (all(((elem == False) for elem in structure['tau_3'])) and all(((elem == True) for elem in structure['_X1_3']))):
                        new_changes['mu_3'].append({elem for elem in structure['mu_3'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['tau_3']))):
                    if (all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == False) for elem in structure['mu_3']))):
                        new_changes['tau_3'].append({elem for elem in structure['tau_3'] if (elem == True)})
        if (key == '_X1_3'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['phi_3']))):
                    if (all(((elem == False) for elem in structure['tau_3'])) and all(((elem == False) for elem in structure['mu_3']))):
                        new_changes['phi_3'].append({elem for elem in structure['phi_3'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_1']))):
                    if (all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X1_1'].append({elem for elem in structure['_X1_1'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X1_0']))):
                    if (all(((elem == True) for elem in structure['_X1_1'])) and all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X1_0'].append({elem for elem in structure['_X1_0'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['mu_3']))):
                    if (all(((elem == False) for elem in structure['phi_3'])) and all(((elem == False) for elem in structure['tau_3']))):
                        new_changes['mu_3'].append({elem for elem in structure['mu_3'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_5']))):
                    if (all(((elem == True) for elem in structure['_X1_1'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X1_5'].append({elem for elem in structure['_X1_5'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X1_4']))):
                    if (all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_1']))):
                        new_changes['_X1_4'].append({elem for elem in structure['_X1_4'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['tau_3']))):
                    if (all(((elem == False) for elem in structure['phi_3'])) and all(((elem == False) for elem in structure['mu_3']))):
                        new_changes['tau_3'].append({elem for elem in structure['tau_3'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X2']))):
                    if (all(((elem == True) for elem in structure['_X1_1'])) and all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X2'].append({elem for elem in structure['_X2'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_2']))):
                    if (all(((elem == True) for elem in structure['_X1_1'])) and all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X1_2'].append({elem for elem in structure['_X1_2'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['tau_3']))):
                    new_changes['tau_3'].append({elem for elem in structure['tau_3'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X2']))):
                    new_changes['_X2'].append({elem for elem in structure['_X2'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['phi_3']))):
                    new_changes['phi_3'].append({elem for elem in structure['phi_3'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['mu_3']))):
                    new_changes['mu_3'].append({elem for elem in structure['mu_3'] if (elem == False)})
        if (key == 'mu_3'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_3']))):
                    new_changes['_X1_3'].append({elem for elem in structure['_X1_3'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['phi_3']))):
                    if (all(((elem == False) for elem in structure['tau_3'])) and all(((elem == True) for elem in structure['_X1_3']))):
                        new_changes['phi_3'].append({elem for elem in structure['phi_3'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_3']))):
                    if (all(((elem == False) for elem in structure['phi_3'])) and all(((elem == False) for elem in structure['tau_3']))):
                        new_changes['_X1_3'].append({elem for elem in structure['_X1_3'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['tau_3']))):
                    if (all(((elem == False) for elem in structure['phi_3'])) and all(((elem == True) for elem in structure['_X1_3']))):
                        new_changes['tau_3'].append({elem for elem in structure['tau_3'] if (elem == True)})
        if (key == 'tau_3'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_3']))):
                    new_changes['_X1_3'].append({elem for elem in structure['_X1_3'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_3']))):
                    if (all(((elem == False) for elem in structure['phi_3'])) and all(((elem == False) for elem in structure['mu_3']))):
                        new_changes['_X1_3'].append({elem for elem in structure['_X1_3'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['mu_3']))):
                    if (all(((elem == False) for elem in structure['phi_3'])) and all(((elem == True) for elem in structure['_X1_3']))):
                        new_changes['mu_3'].append({elem for elem in structure['mu_3'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['phi_3']))):
                    if (all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == False) for elem in structure['mu_3']))):
                        new_changes['phi_3'].append({elem for elem in structure['phi_3'] if (elem == True)})
        if (key == '_X1_4'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X2']))):
                    if (all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_1']))):
                        new_changes['_X2'].append({elem for elem in structure['_X2'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_2']))):
                    if (all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_1']))):
                        new_changes['_X1_2'].append({elem for elem in structure['_X1_2'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['mu_4']))):
                    if (all(((elem == False) for elem in structure['tau_4'])) and all(((elem == False) for elem in structure['phi_4']))):
                        new_changes['mu_4'].append({elem for elem in structure['mu_4'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_3']))):
                    if (all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_1']))):
                        new_changes['_X1_3'].append({elem for elem in structure['_X1_3'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X1_1']))):
                    if (all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_0']))):
                        new_changes['_X1_1'].append({elem for elem in structure['_X1_1'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['phi_4']))):
                    if (all(((elem == False) for elem in structure['tau_4'])) and all(((elem == False) for elem in structure['mu_4']))):
                        new_changes['phi_4'].append({elem for elem in structure['phi_4'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_5']))):
                    if (all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_1']))):
                        new_changes['_X1_5'].append({elem for elem in structure['_X1_5'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X1_0']))):
                    if (all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_1']))):
                        new_changes['_X1_0'].append({elem for elem in structure['_X1_0'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['tau_4']))):
                    if (all(((elem == False) for elem in structure['phi_4'])) and all(((elem == False) for elem in structure['mu_4']))):
                        new_changes['tau_4'].append({elem for elem in structure['tau_4'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['tau_4']))):
                    new_changes['tau_4'].append({elem for elem in structure['tau_4'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['phi_4']))):
                    new_changes['phi_4'].append({elem for elem in structure['phi_4'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X2']))):
                    new_changes['_X2'].append({elem for elem in structure['_X2'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['mu_4']))):
                    new_changes['mu_4'].append({elem for elem in structure['mu_4'] if (elem == False)})
        if (key == 'phi_4'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_4']))):
                    new_changes['_X1_4'].append({elem for elem in structure['_X1_4'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['mu_4']))):
                    if (all(((elem == False) for elem in structure['tau_4'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['mu_4'].append({elem for elem in structure['mu_4'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['tau_4']))):
                    if (all(((elem == False) for elem in structure['mu_4'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['tau_4'].append({elem for elem in structure['tau_4'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_4']))):
                    if (all(((elem == False) for elem in structure['tau_4'])) and all(((elem == False) for elem in structure['mu_4']))):
                        new_changes['_X1_4'].append({elem for elem in structure['_X1_4'] if (elem == False)})
        if (key == 'mu_4'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_4']))):
                    new_changes['_X1_4'].append({elem for elem in structure['_X1_4'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_4']))):
                    if (all(((elem == False) for elem in structure['tau_4'])) and all(((elem == False) for elem in structure['phi_4']))):
                        new_changes['_X1_4'].append({elem for elem in structure['_X1_4'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['tau_4']))):
                    if (all(((elem == False) for elem in structure['phi_4'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['tau_4'].append({elem for elem in structure['tau_4'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['phi_4']))):
                    if (all(((elem == False) for elem in structure['tau_4'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['phi_4'].append({elem for elem in structure['phi_4'] if (elem == True)})
        if (key == 'tau_4'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_4']))):
                    new_changes['_X1_4'].append({elem for elem in structure['_X1_4'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['phi_4']))):
                    if (all(((elem == False) for elem in structure['mu_4'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['phi_4'].append({elem for elem in structure['phi_4'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_4']))):
                    if (all(((elem == False) for elem in structure['phi_4'])) and all(((elem == False) for elem in structure['mu_4']))):
                        new_changes['_X1_4'].append({elem for elem in structure['_X1_4'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['mu_4']))):
                    if (all(((elem == False) for elem in structure['phi_4'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['mu_4'].append({elem for elem in structure['mu_4'] if (elem == True)})
        if (key == 'phi_5'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_5']))):
                    new_changes['_X1_5'].append({elem for elem in structure['_X1_5'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['mu_5']))):
                    if (all(((elem == False) for elem in structure['tau_5'])) and all(((elem == True) for elem in structure['_X1_5']))):
                        new_changes['mu_5'].append({elem for elem in structure['mu_5'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['tau_5']))):
                    if (all(((elem == False) for elem in structure['mu_5'])) and all(((elem == True) for elem in structure['_X1_5']))):
                        new_changes['tau_5'].append({elem for elem in structure['tau_5'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_5']))):
                    if (all(((elem == False) for elem in structure['mu_5'])) and all(((elem == False) for elem in structure['tau_5']))):
                        new_changes['_X1_5'].append({elem for elem in structure['_X1_5'] if (elem == False)})
        if (key == '_X1_5'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X2']))):
                    if (all(((elem == True) for elem in structure['_X1_1'])) and all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X2'].append({elem for elem in structure['_X2'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['tau_5']))):
                    if (all(((elem == False) for elem in structure['phi_5'])) and all(((elem == False) for elem in structure['mu_5']))):
                        new_changes['tau_5'].append({elem for elem in structure['tau_5'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_2']))):
                    if (all(((elem == True) for elem in structure['_X1_1'])) and all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X1_2'].append({elem for elem in structure['_X1_2'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['mu_5']))):
                    if (all(((elem == False) for elem in structure['phi_5'])) and all(((elem == False) for elem in structure['tau_5']))):
                        new_changes['mu_5'].append({elem for elem in structure['mu_5'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_4']))):
                    if (all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_1']))):
                        new_changes['_X1_4'].append({elem for elem in structure['_X1_4'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X1_1']))):
                    if (all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X1_1'].append({elem for elem in structure['_X1_1'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X1_0']))):
                    if (all(((elem == True) for elem in structure['_X1_1'])) and all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X1_0'].append({elem for elem in structure['_X1_0'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['phi_5']))):
                    if (all(((elem == False) for elem in structure['mu_5'])) and all(((elem == False) for elem in structure['tau_5']))):
                        new_changes['phi_5'].append({elem for elem in structure['phi_5'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_3']))):
                    if (all(((elem == True) for elem in structure['_X1_1'])) and all(((elem == False) for elem in structure['_X2'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X1_3'].append({elem for elem in structure['_X1_3'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X2']))):
                    new_changes['_X2'].append({elem for elem in structure['_X2'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['phi_5']))):
                    new_changes['phi_5'].append({elem for elem in structure['phi_5'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['mu_5']))):
                    new_changes['mu_5'].append({elem for elem in structure['mu_5'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['tau_5']))):
                    new_changes['tau_5'].append({elem for elem in structure['tau_5'] if (elem == False)})
        if (key == 'mu_5'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_5']))):
                    new_changes['_X1_5'].append({elem for elem in structure['_X1_5'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_5']))):
                    if (all(((elem == False) for elem in structure['phi_5'])) and all(((elem == False) for elem in structure['tau_5']))):
                        new_changes['_X1_5'].append({elem for elem in structure['_X1_5'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['tau_5']))):
                    if (all(((elem == False) for elem in structure['phi_5'])) and all(((elem == True) for elem in structure['_X1_5']))):
                        new_changes['tau_5'].append({elem for elem in structure['tau_5'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['phi_5']))):
                    if (all(((elem == False) for elem in structure['tau_5'])) and all(((elem == True) for elem in structure['_X1_5']))):
                        new_changes['phi_5'].append({elem for elem in structure['phi_5'] if (elem == True)})
        if (key == 'tau_5'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_5']))):
                    new_changes['_X1_5'].append({elem for elem in structure['_X1_5'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_5']))):
                    if (all(((elem == False) for elem in structure['phi_5'])) and all(((elem == False) for elem in structure['mu_5']))):
                        new_changes['_X1_5'].append({elem for elem in structure['_X1_5'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['mu_5']))):
                    if (all(((elem == False) for elem in structure['phi_5'])) and all(((elem == True) for elem in structure['_X1_5']))):
                        new_changes['mu_5'].append({elem for elem in structure['mu_5'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['phi_5']))):
                    if (all(((elem == False) for elem in structure['mu_5'])) and all(((elem == True) for elem in structure['_X1_5']))):
                        new_changes['phi_5'].append({elem for elem in structure['phi_5'] if (elem == True)})
        if (key == '_X2'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_4']))):
                    new_changes['_X1_4'].append({elem for elem in structure['_X1_4'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X1_1']))):
                    new_changes['_X1_1'].append({elem for elem in structure['_X1_1'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X1_5']))):
                    new_changes['_X1_5'].append({elem for elem in structure['_X1_5'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X1_2']))):
                    new_changes['_X1_2'].append({elem for elem in structure['_X1_2'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X1_0']))):
                    new_changes['_X1_0'].append({elem for elem in structure['_X1_0'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X1_3']))):
                    new_changes['_X1_3'].append({elem for elem in structure['_X1_3'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_3']))):
                    if (all(((elem == True) for elem in structure['_X1_1'])) and all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X1_3'].append({elem for elem in structure['_X1_3'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X1_5']))):
                    if (all(((elem == True) for elem in structure['_X1_1'])) and all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X1_5'].append({elem for elem in structure['_X1_5'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X1_2']))):
                    if (all(((elem == True) for elem in structure['_X1_1'])) and all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X1_2'].append({elem for elem in structure['_X1_2'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X1_0']))):
                    if (all(((elem == True) for elem in structure['_X1_1'])) and all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X1_0'].append({elem for elem in structure['_X1_0'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X1_1']))):
                    if (all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X1_1'].append({elem for elem in structure['_X1_1'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X1_4']))):
                    if (all(((elem == True) for elem in structure['_X1_5'])) and all(((elem == True) for elem in structure['_X1_3'])) and all(((elem == True) for elem in structure['_X1_2'])) and all(((elem == True) for elem in structure['_X1_0'])) and all(((elem == True) for elem in structure['_X1_1']))):
                        new_changes['_X1_4'].append({elem for elem in structure['_X1_4'] if (elem == False)})
    return intersect_changes(new_changes)

# This function calls the propagate() function repeatedly, until either
# - an inconsistency is detected
# - no new changes are detected
# The function also updates the 'structure' data structure with newly detected changes.

def propagation_loop(changes):
    unsat_fields = check_unsat_fields(changes)
    while ((len(changes) != 0) and (len(unsat_fields) == 0)):
        old_changes = changes
        changes = propagate(changes)
        update_structure(old_changes)
        unsat_fields = check_unsat_fields(changes)
    return unsat_fields


# Code to enable interaction with the user through the terminal.

quit = False
unsat_fields = propagation_loop(structure)
if (len(unsat_fields) > 0):
    print('The initial problem is unsatisfiable: in particular, the following fields are unsatisfiable')
    for field in unsat_fields:
        print(field)
    quit = True
else:
    print('Initial domains')
    print_structure()
while (not quit):
    field = input('What field do you want to change\n')
    value = input('Enter the value\n')
    if ((field == 'quit') or (value == 'quit')):
        quit = True
    else:
        if (value.lower() == 'true'):
            value = structure[field].intersection({True})
        elif (value.lower() == 'false'):
            value = structure[field].intersection({False})
        else:
            value = structure[field].intersection({int(value)})
        changes = {field: value}
        unsat_fields = propagation_loop(changes)
        if (len(unsat_fields) > 0):
            print('The following fields have become unsatisfiable')
            for field in unsat_fields:
                print(field)
            quit = True
        else:
            print_structure()
