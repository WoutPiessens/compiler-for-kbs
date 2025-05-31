
structure = {'_X1_5': {True, False}, '_X2_10': {True, False}, 'A_1': {True, False}, '_X1_4': {True, False}, '_X2_1': {True, False}, '_X3_2': {True, False}, 'A_3': {True, False}, '_X3_9': {True, False}, '_X2_3': {True, False}, '_X1_9': {True, False}, '_X1_7': {True, False}, '_X2_9': {True, False}, 'B_3': {True, False}, 'B_5': {True, False}, '_X1_10': {True, False}, '_X2_8': {True, False}, '_X2_6': {True, False}, 'B_10': {True, False}, 'A_2': {True, False}, '_X3_1': {True, False}, '_X1_3': {True, False}, '_X1_1': {True, False}, '_X3_8': {True, False}, 'B_8': {True, False}, '_X2_5': {True, False}, 'B_2': {True, False}, '_X1_6': {True, False}, '_X4': {True, False}, 'B_4': {True, False}, 'A_5': {True, False}, '_X1_2': {True, False}, '_X2_2': {True, False}, 'B_7': {True, False}, 'A_7': {True, False}, '_X3_5': {True, False}, 'A_6': {True, False}, '_X3_4': {True, False}, 'A_8': {True, False}, 'B_1': {True, False}, '_X2_4': {True, False}, '_X3_7': {True, False}, '_X3_3': {True, False}, 'B_9': {True, False}, '_X2_7': {True, False}, 'A_4': {True, False}, 'A_9': {True, False}, '_X1_8': {True, False}, '_X3_10': {True, False}, '_X3_6': {True, False}, 'B_6': {True, False}, 'A_10': {True, False}, '_X1_1': {False, True}, 'A_1': {False, True}, 'B_1': {False, True}, '_X1_2': {False, True}, 'A_2': {False, True}, 'B_2': {False, True}, '_X1_3': {False, True}, 'A_3': {False, True}, 'B_3': {False, True}, '_X1_4': {False, True}, 'A_4': {False, True}, 'B_4': {False, True}, '_X1_5': {False, True}, 'A_5': {False, True}, 'B_5': {False, True}, '_X1_6': {False, True}, 'A_6': {False, True}, 'B_6': {False, True}, '_X1_7': {False, True}, 'A_7': {False, True}, 'B_7': {False, True}, '_X1_8': {False, True}, 'A_8': {False, True}, 'B_8': {False, True}, '_X1_9': {False, True}, 'A_9': {False, True}, 'B_9': {False, True}, '_X1_10': {False, True}, 'A_10': {False, True}, 'B_10': {False, True}, '_X2_1': {False, True}, '_X2_2': {False, True}, '_X2_3': {False, True}, '_X2_4': {False, True}, '_X2_5': {False, True}, '_X2_6': {False, True}, '_X2_7': {False, True}, '_X2_8': {False, True}, '_X2_9': {False, True}, '_X2_10': {False, True}, '_X3_1': {False, True}, '_X3_2': {False, True}, '_X3_3': {False, True}, '_X3_4': {False, True}, '_X3_5': {False, True}, '_X3_6': {False, True}, '_X3_7': {False, True}, '_X3_8': {False, True}, '_X3_9': {False, True}, '_X3_10': {False, True}, '_X4': {False, True}}

def update_structure(changes):
    for (key, value) in changes.items():
        structure[key] = value

def print_structure():
    for key in structure.keys():
        if (not key.startswith('_')):
            print(key, end='')
            print(':  ', end='')
            print(structure[key])
            print()

def check_unsat_fields(changes):
    unsat_fields = set()
    for key in changes.keys():
        if (len(changes[key]) == 0):
            unsat_fields.add(key)
    return unsat_fields

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

def propagate(changes):
    new_changes = {key: [] for key in structure.keys()}
    for (key, value) in changes.items():
        if (not all(((elem == True) for elem in structure['A_5']))):
            new_changes['A_5'].append({elem for elem in structure['A_5'] if (elem == True)})
        if (not all(((elem == False) for elem in structure['B_4']))):
            new_changes['B_4'].append({elem for elem in structure['B_4'] if (elem == False)})
        if (not all(((elem == True) for elem in structure['_X4']))):
            new_changes['_X4'].append({elem for elem in structure['_X4'] if (elem == True)})
        if (key == 'A_1'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X2_1']))):
                    new_changes['_X2_1'].append({elem for elem in structure['_X2_1'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['B_1']))):
                    if (all(((elem == True) for elem in structure['_X1_1']))):
                        new_changes['B_1'].append({elem for elem in structure['B_1'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X1_1']))):
                    if (all(((elem == True) for elem in structure['B_1']))):
                        new_changes['_X1_1'].append({elem for elem in structure['_X1_1'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_1']))):
                    new_changes['_X1_1'].append({elem for elem in structure['_X1_1'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X2_1']))):
                    if (all(((elem == False) for elem in structure['B_1']))):
                        new_changes['_X2_1'].append({elem for elem in structure['_X2_1'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['B_1']))):
                    if (all(((elem == True) for elem in structure['_X2_1']))):
                        new_changes['B_1'].append({elem for elem in structure['B_1'] if (elem == True)})
        if (key == '_X1_1'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X3_1']))):
                    if (all(((elem == True) for elem in structure['_X2_1']))):
                        new_changes['_X3_1'].append({elem for elem in structure['_X3_1'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['B_1']))):
                    if (all(((elem == True) for elem in structure['A_1']))):
                        new_changes['B_1'].append({elem for elem in structure['B_1'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X2_1']))):
                    if (all(((elem == False) for elem in structure['_X3_1']))):
                        new_changes['_X2_1'].append({elem for elem in structure['_X2_1'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['A_1']))):
                    if (all(((elem == True) for elem in structure['B_1']))):
                        new_changes['A_1'].append({elem for elem in structure['A_1'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['B_1']))):
                    new_changes['B_1'].append({elem for elem in structure['B_1'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['A_1']))):
                    new_changes['A_1'].append({elem for elem in structure['A_1'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_1']))):
                    new_changes['_X3_1'].append({elem for elem in structure['_X3_1'] if (elem == False)})
        if (key == 'B_1'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X2_1']))):
                    new_changes['_X2_1'].append({elem for elem in structure['_X2_1'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['A_1']))):
                    if (all(((elem == True) for elem in structure['_X1_1']))):
                        new_changes['A_1'].append({elem for elem in structure['A_1'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X1_1']))):
                    if (all(((elem == True) for elem in structure['A_1']))):
                        new_changes['_X1_1'].append({elem for elem in structure['_X1_1'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['A_1']))):
                    if (all(((elem == True) for elem in structure['_X2_1']))):
                        new_changes['A_1'].append({elem for elem in structure['A_1'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X2_1']))):
                    if (all(((elem == False) for elem in structure['A_1']))):
                        new_changes['_X2_1'].append({elem for elem in structure['_X2_1'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X1_1']))):
                    new_changes['_X1_1'].append({elem for elem in structure['_X1_1'] if (elem == True)})
        if (key == 'A_2'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['B_2']))):
                    if (all(((elem == True) for elem in structure['_X1_2']))):
                        new_changes['B_2'].append({elem for elem in structure['B_2'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X2_2']))):
                    new_changes['_X2_2'].append({elem for elem in structure['_X2_2'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_2']))):
                    if (all(((elem == True) for elem in structure['B_2']))):
                        new_changes['_X1_2'].append({elem for elem in structure['_X1_2'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_2']))):
                    new_changes['_X1_2'].append({elem for elem in structure['_X1_2'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['B_2']))):
                    if (all(((elem == True) for elem in structure['_X2_2']))):
                        new_changes['B_2'].append({elem for elem in structure['B_2'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X2_2']))):
                    if (all(((elem == False) for elem in structure['B_2']))):
                        new_changes['_X2_2'].append({elem for elem in structure['_X2_2'] if (elem == False)})
        if (key == '_X1_2'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['B_2']))):
                    if (all(((elem == True) for elem in structure['A_2']))):
                        new_changes['B_2'].append({elem for elem in structure['B_2'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['A_2']))):
                    if (all(((elem == True) for elem in structure['B_2']))):
                        new_changes['A_2'].append({elem for elem in structure['A_2'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X2_2']))):
                    if (all(((elem == False) for elem in structure['_X3_2']))):
                        new_changes['_X2_2'].append({elem for elem in structure['_X2_2'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X3_2']))):
                    if (all(((elem == True) for elem in structure['_X2_2']))):
                        new_changes['_X3_2'].append({elem for elem in structure['_X3_2'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['B_2']))):
                    new_changes['B_2'].append({elem for elem in structure['B_2'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_2']))):
                    new_changes['_X3_2'].append({elem for elem in structure['_X3_2'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['A_2']))):
                    new_changes['A_2'].append({elem for elem in structure['A_2'] if (elem == True)})
        if (key == 'B_2'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['A_2']))):
                    if (all(((elem == True) for elem in structure['_X1_2']))):
                        new_changes['A_2'].append({elem for elem in structure['A_2'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X2_2']))):
                    new_changes['_X2_2'].append({elem for elem in structure['_X2_2'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_2']))):
                    if (all(((elem == True) for elem in structure['A_2']))):
                        new_changes['_X1_2'].append({elem for elem in structure['_X1_2'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X2_2']))):
                    if (all(((elem == False) for elem in structure['A_2']))):
                        new_changes['_X2_2'].append({elem for elem in structure['_X2_2'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['A_2']))):
                    if (all(((elem == True) for elem in structure['_X2_2']))):
                        new_changes['A_2'].append({elem for elem in structure['A_2'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X1_2']))):
                    new_changes['_X1_2'].append({elem for elem in structure['_X1_2'] if (elem == True)})
        if (key == '_X1_3'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X3_3']))):
                    if (all(((elem == True) for elem in structure['_X2_3']))):
                        new_changes['_X3_3'].append({elem for elem in structure['_X3_3'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X2_3']))):
                    if (all(((elem == False) for elem in structure['_X3_3']))):
                        new_changes['_X2_3'].append({elem for elem in structure['_X2_3'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['A_3']))):
                    if (all(((elem == True) for elem in structure['B_3']))):
                        new_changes['A_3'].append({elem for elem in structure['A_3'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['B_3']))):
                    if (all(((elem == True) for elem in structure['A_3']))):
                        new_changes['B_3'].append({elem for elem in structure['B_3'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['A_3']))):
                    new_changes['A_3'].append({elem for elem in structure['A_3'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_3']))):
                    new_changes['_X3_3'].append({elem for elem in structure['_X3_3'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['B_3']))):
                    new_changes['B_3'].append({elem for elem in structure['B_3'] if (elem == True)})
        if (key == 'A_3'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X2_3']))):
                    new_changes['_X2_3'].append({elem for elem in structure['_X2_3'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_3']))):
                    if (all(((elem == True) for elem in structure['B_3']))):
                        new_changes['_X1_3'].append({elem for elem in structure['_X1_3'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['B_3']))):
                    if (all(((elem == True) for elem in structure['_X1_3']))):
                        new_changes['B_3'].append({elem for elem in structure['B_3'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X2_3']))):
                    if (all(((elem == False) for elem in structure['B_3']))):
                        new_changes['_X2_3'].append({elem for elem in structure['_X2_3'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['B_3']))):
                    if (all(((elem == True) for elem in structure['_X2_3']))):
                        new_changes['B_3'].append({elem for elem in structure['B_3'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X1_3']))):
                    new_changes['_X1_3'].append({elem for elem in structure['_X1_3'] if (elem == True)})
        if (key == 'B_3'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X2_3']))):
                    new_changes['_X2_3'].append({elem for elem in structure['_X2_3'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['A_3']))):
                    if (all(((elem == True) for elem in structure['_X1_3']))):
                        new_changes['A_3'].append({elem for elem in structure['A_3'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X1_3']))):
                    if (all(((elem == True) for elem in structure['A_3']))):
                        new_changes['_X1_3'].append({elem for elem in structure['_X1_3'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_3']))):
                    new_changes['_X1_3'].append({elem for elem in structure['_X1_3'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X2_3']))):
                    if (all(((elem == False) for elem in structure['A_3']))):
                        new_changes['_X2_3'].append({elem for elem in structure['_X2_3'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['A_3']))):
                    if (all(((elem == True) for elem in structure['_X2_3']))):
                        new_changes['A_3'].append({elem for elem in structure['A_3'] if (elem == True)})
        if (key == '_X1_4'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['B_4']))):
                    if (all(((elem == True) for elem in structure['A_4']))):
                        new_changes['B_4'].append({elem for elem in structure['B_4'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X3_4']))):
                    if (all(((elem == True) for elem in structure['_X2_4']))):
                        new_changes['_X3_4'].append({elem for elem in structure['_X3_4'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['A_4']))):
                    if (all(((elem == True) for elem in structure['B_4']))):
                        new_changes['A_4'].append({elem for elem in structure['A_4'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X2_4']))):
                    if (all(((elem == False) for elem in structure['_X3_4']))):
                        new_changes['_X2_4'].append({elem for elem in structure['_X2_4'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X3_4']))):
                    new_changes['_X3_4'].append({elem for elem in structure['_X3_4'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['A_4']))):
                    new_changes['A_4'].append({elem for elem in structure['A_4'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['B_4']))):
                    new_changes['B_4'].append({elem for elem in structure['B_4'] if (elem == True)})
        if (key == 'A_4'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['B_4']))):
                    if (all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['B_4'].append({elem for elem in structure['B_4'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X1_4']))):
                    if (all(((elem == True) for elem in structure['B_4']))):
                        new_changes['_X1_4'].append({elem for elem in structure['_X1_4'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X2_4']))):
                    new_changes['_X2_4'].append({elem for elem in structure['_X2_4'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X2_4']))):
                    if (all(((elem == False) for elem in structure['B_4']))):
                        new_changes['_X2_4'].append({elem for elem in structure['_X2_4'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X1_4']))):
                    new_changes['_X1_4'].append({elem for elem in structure['_X1_4'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['B_4']))):
                    if (all(((elem == True) for elem in structure['_X2_4']))):
                        new_changes['B_4'].append({elem for elem in structure['B_4'] if (elem == True)})
        if (key == 'B_4'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_4']))):
                    if (all(((elem == True) for elem in structure['A_4']))):
                        new_changes['_X1_4'].append({elem for elem in structure['_X1_4'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['A_4']))):
                    if (all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['A_4'].append({elem for elem in structure['A_4'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X2_4']))):
                    new_changes['_X2_4'].append({elem for elem in structure['_X2_4'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['A_4']))):
                    if (all(((elem == True) for elem in structure['_X2_4']))):
                        new_changes['A_4'].append({elem for elem in structure['A_4'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X1_4']))):
                    new_changes['_X1_4'].append({elem for elem in structure['_X1_4'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X2_4']))):
                    if (all(((elem == False) for elem in structure['A_4']))):
                        new_changes['_X2_4'].append({elem for elem in structure['_X2_4'] if (elem == False)})
        if (key == '_X1_5'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X2_5']))):
                    if (all(((elem == False) for elem in structure['_X3_5']))):
                        new_changes['_X2_5'].append({elem for elem in structure['_X2_5'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['B_5']))):
                    if (all(((elem == True) for elem in structure['A_5']))):
                        new_changes['B_5'].append({elem for elem in structure['B_5'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X3_5']))):
                    if (all(((elem == True) for elem in structure['_X2_5']))):
                        new_changes['_X3_5'].append({elem for elem in structure['_X3_5'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['A_5']))):
                    if (all(((elem == True) for elem in structure['B_5']))):
                        new_changes['A_5'].append({elem for elem in structure['A_5'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['A_5']))):
                    new_changes['A_5'].append({elem for elem in structure['A_5'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_5']))):
                    new_changes['_X3_5'].append({elem for elem in structure['_X3_5'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['B_5']))):
                    new_changes['B_5'].append({elem for elem in structure['B_5'] if (elem == True)})
        if (key == 'A_5'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_5']))):
                    if (all(((elem == True) for elem in structure['B_5']))):
                        new_changes['_X1_5'].append({elem for elem in structure['_X1_5'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['B_5']))):
                    if (all(((elem == True) for elem in structure['_X1_5']))):
                        new_changes['B_5'].append({elem for elem in structure['B_5'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X2_5']))):
                    new_changes['_X2_5'].append({elem for elem in structure['_X2_5'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['B_5']))):
                    if (all(((elem == True) for elem in structure['_X2_5']))):
                        new_changes['B_5'].append({elem for elem in structure['B_5'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X2_5']))):
                    if (all(((elem == False) for elem in structure['B_5']))):
                        new_changes['_X2_5'].append({elem for elem in structure['_X2_5'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X1_5']))):
                    new_changes['_X1_5'].append({elem for elem in structure['_X1_5'] if (elem == True)})
        if (key == 'B_5'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['A_5']))):
                    if (all(((elem == True) for elem in structure['_X1_5']))):
                        new_changes['A_5'].append({elem for elem in structure['A_5'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X1_5']))):
                    if (all(((elem == True) for elem in structure['A_5']))):
                        new_changes['_X1_5'].append({elem for elem in structure['_X1_5'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X2_5']))):
                    new_changes['_X2_5'].append({elem for elem in structure['_X2_5'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['A_5']))):
                    if (all(((elem == True) for elem in structure['_X2_5']))):
                        new_changes['A_5'].append({elem for elem in structure['A_5'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X2_5']))):
                    if (all(((elem == False) for elem in structure['A_5']))):
                        new_changes['_X2_5'].append({elem for elem in structure['_X2_5'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X1_5']))):
                    new_changes['_X1_5'].append({elem for elem in structure['_X1_5'] if (elem == True)})
        if (key == '_X1_6'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X2_6']))):
                    if (all(((elem == False) for elem in structure['_X3_6']))):
                        new_changes['_X2_6'].append({elem for elem in structure['_X2_6'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['B_6']))):
                    if (all(((elem == True) for elem in structure['A_6']))):
                        new_changes['B_6'].append({elem for elem in structure['B_6'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X3_6']))):
                    if (all(((elem == True) for elem in structure['_X2_6']))):
                        new_changes['_X3_6'].append({elem for elem in structure['_X3_6'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['A_6']))):
                    if (all(((elem == True) for elem in structure['B_6']))):
                        new_changes['A_6'].append({elem for elem in structure['A_6'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['A_6']))):
                    new_changes['A_6'].append({elem for elem in structure['A_6'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['B_6']))):
                    new_changes['B_6'].append({elem for elem in structure['B_6'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_6']))):
                    new_changes['_X3_6'].append({elem for elem in structure['_X3_6'] if (elem == False)})
        if (key == 'A_6'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_6']))):
                    if (all(((elem == True) for elem in structure['B_6']))):
                        new_changes['_X1_6'].append({elem for elem in structure['_X1_6'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['B_6']))):
                    if (all(((elem == True) for elem in structure['_X1_6']))):
                        new_changes['B_6'].append({elem for elem in structure['B_6'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X2_6']))):
                    new_changes['_X2_6'].append({elem for elem in structure['_X2_6'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['B_6']))):
                    if (all(((elem == True) for elem in structure['_X2_6']))):
                        new_changes['B_6'].append({elem for elem in structure['B_6'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X1_6']))):
                    new_changes['_X1_6'].append({elem for elem in structure['_X1_6'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X2_6']))):
                    if (all(((elem == False) for elem in structure['B_6']))):
                        new_changes['_X2_6'].append({elem for elem in structure['_X2_6'] if (elem == False)})
        if (key == 'B_6'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_6']))):
                    if (all(((elem == True) for elem in structure['A_6']))):
                        new_changes['_X1_6'].append({elem for elem in structure['_X1_6'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['A_6']))):
                    if (all(((elem == True) for elem in structure['_X1_6']))):
                        new_changes['A_6'].append({elem for elem in structure['A_6'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X2_6']))):
                    new_changes['_X2_6'].append({elem for elem in structure['_X2_6'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X2_6']))):
                    if (all(((elem == False) for elem in structure['A_6']))):
                        new_changes['_X2_6'].append({elem for elem in structure['_X2_6'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X1_6']))):
                    new_changes['_X1_6'].append({elem for elem in structure['_X1_6'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['A_6']))):
                    if (all(((elem == True) for elem in structure['_X2_6']))):
                        new_changes['A_6'].append({elem for elem in structure['A_6'] if (elem == True)})
        if (key == 'A_7'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['B_7']))):
                    if (all(((elem == True) for elem in structure['_X1_7']))):
                        new_changes['B_7'].append({elem for elem in structure['B_7'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X1_7']))):
                    if (all(((elem == True) for elem in structure['B_7']))):
                        new_changes['_X1_7'].append({elem for elem in structure['_X1_7'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X2_7']))):
                    new_changes['_X2_7'].append({elem for elem in structure['_X2_7'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_7']))):
                    new_changes['_X1_7'].append({elem for elem in structure['_X1_7'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['B_7']))):
                    if (all(((elem == True) for elem in structure['_X2_7']))):
                        new_changes['B_7'].append({elem for elem in structure['B_7'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X2_7']))):
                    if (all(((elem == False) for elem in structure['B_7']))):
                        new_changes['_X2_7'].append({elem for elem in structure['_X2_7'] if (elem == False)})
        if (key == '_X1_7'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['B_7']))):
                    if (all(((elem == True) for elem in structure['A_7']))):
                        new_changes['B_7'].append({elem for elem in structure['B_7'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['A_7']))):
                    if (all(((elem == True) for elem in structure['B_7']))):
                        new_changes['A_7'].append({elem for elem in structure['A_7'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X2_7']))):
                    if (all(((elem == False) for elem in structure['_X3_7']))):
                        new_changes['_X2_7'].append({elem for elem in structure['_X2_7'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X3_7']))):
                    if (all(((elem == True) for elem in structure['_X2_7']))):
                        new_changes['_X3_7'].append({elem for elem in structure['_X3_7'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['B_7']))):
                    new_changes['B_7'].append({elem for elem in structure['B_7'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_7']))):
                    new_changes['_X3_7'].append({elem for elem in structure['_X3_7'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['A_7']))):
                    new_changes['A_7'].append({elem for elem in structure['A_7'] if (elem == True)})
        if (key == 'B_7'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_7']))):
                    if (all(((elem == True) for elem in structure['A_7']))):
                        new_changes['_X1_7'].append({elem for elem in structure['_X1_7'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['A_7']))):
                    if (all(((elem == True) for elem in structure['_X1_7']))):
                        new_changes['A_7'].append({elem for elem in structure['A_7'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X2_7']))):
                    new_changes['_X2_7'].append({elem for elem in structure['_X2_7'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_7']))):
                    new_changes['_X1_7'].append({elem for elem in structure['_X1_7'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['A_7']))):
                    if (all(((elem == True) for elem in structure['_X2_7']))):
                        new_changes['A_7'].append({elem for elem in structure['A_7'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X2_7']))):
                    if (all(((elem == False) for elem in structure['A_7']))):
                        new_changes['_X2_7'].append({elem for elem in structure['_X2_7'] if (elem == False)})
        if (key == '_X1_8'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['B_8']))):
                    if (all(((elem == True) for elem in structure['A_8']))):
                        new_changes['B_8'].append({elem for elem in structure['B_8'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X3_8']))):
                    if (all(((elem == True) for elem in structure['_X2_8']))):
                        new_changes['_X3_8'].append({elem for elem in structure['_X3_8'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['A_8']))):
                    if (all(((elem == True) for elem in structure['B_8']))):
                        new_changes['A_8'].append({elem for elem in structure['A_8'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X2_8']))):
                    if (all(((elem == False) for elem in structure['_X3_8']))):
                        new_changes['_X2_8'].append({elem for elem in structure['_X2_8'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['A_8']))):
                    new_changes['A_8'].append({elem for elem in structure['A_8'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_8']))):
                    new_changes['_X3_8'].append({elem for elem in structure['_X3_8'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['B_8']))):
                    new_changes['B_8'].append({elem for elem in structure['B_8'] if (elem == True)})
        if (key == 'A_8'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['B_8']))):
                    if (all(((elem == True) for elem in structure['_X1_8']))):
                        new_changes['B_8'].append({elem for elem in structure['B_8'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X2_8']))):
                    new_changes['_X2_8'].append({elem for elem in structure['_X2_8'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_8']))):
                    if (all(((elem == True) for elem in structure['B_8']))):
                        new_changes['_X1_8'].append({elem for elem in structure['_X1_8'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['B_8']))):
                    if (all(((elem == True) for elem in structure['_X2_8']))):
                        new_changes['B_8'].append({elem for elem in structure['B_8'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X2_8']))):
                    if (all(((elem == False) for elem in structure['B_8']))):
                        new_changes['_X2_8'].append({elem for elem in structure['_X2_8'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X1_8']))):
                    new_changes['_X1_8'].append({elem for elem in structure['_X1_8'] if (elem == True)})
        if (key == 'B_8'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_8']))):
                    if (all(((elem == True) for elem in structure['A_8']))):
                        new_changes['_X1_8'].append({elem for elem in structure['_X1_8'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['A_8']))):
                    if (all(((elem == True) for elem in structure['_X1_8']))):
                        new_changes['A_8'].append({elem for elem in structure['A_8'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X2_8']))):
                    new_changes['_X2_8'].append({elem for elem in structure['_X2_8'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['A_8']))):
                    if (all(((elem == True) for elem in structure['_X2_8']))):
                        new_changes['A_8'].append({elem for elem in structure['A_8'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X2_8']))):
                    if (all(((elem == False) for elem in structure['A_8']))):
                        new_changes['_X2_8'].append({elem for elem in structure['_X2_8'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X1_8']))):
                    new_changes['_X1_8'].append({elem for elem in structure['_X1_8'] if (elem == True)})
        if (key == '_X1_9'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X2_9']))):
                    if (all(((elem == False) for elem in structure['_X3_9']))):
                        new_changes['_X2_9'].append({elem for elem in structure['_X2_9'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['B_9']))):
                    if (all(((elem == True) for elem in structure['A_9']))):
                        new_changes['B_9'].append({elem for elem in structure['B_9'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X3_9']))):
                    if (all(((elem == True) for elem in structure['_X2_9']))):
                        new_changes['_X3_9'].append({elem for elem in structure['_X3_9'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['A_9']))):
                    if (all(((elem == True) for elem in structure['B_9']))):
                        new_changes['A_9'].append({elem for elem in structure['A_9'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['A_9']))):
                    new_changes['A_9'].append({elem for elem in structure['A_9'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['B_9']))):
                    new_changes['B_9'].append({elem for elem in structure['B_9'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_9']))):
                    new_changes['_X3_9'].append({elem for elem in structure['_X3_9'] if (elem == False)})
        if (key == 'A_9'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X2_9']))):
                    new_changes['_X2_9'].append({elem for elem in structure['_X2_9'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['B_9']))):
                    if (all(((elem == True) for elem in structure['_X1_9']))):
                        new_changes['B_9'].append({elem for elem in structure['B_9'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X1_9']))):
                    if (all(((elem == True) for elem in structure['B_9']))):
                        new_changes['_X1_9'].append({elem for elem in structure['_X1_9'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_9']))):
                    new_changes['_X1_9'].append({elem for elem in structure['_X1_9'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X2_9']))):
                    if (all(((elem == False) for elem in structure['B_9']))):
                        new_changes['_X2_9'].append({elem for elem in structure['_X2_9'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['B_9']))):
                    if (all(((elem == True) for elem in structure['_X2_9']))):
                        new_changes['B_9'].append({elem for elem in structure['B_9'] if (elem == True)})
        if (key == 'B_9'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_9']))):
                    if (all(((elem == True) for elem in structure['A_9']))):
                        new_changes['_X1_9'].append({elem for elem in structure['_X1_9'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['A_9']))):
                    if (all(((elem == True) for elem in structure['_X1_9']))):
                        new_changes['A_9'].append({elem for elem in structure['A_9'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X2_9']))):
                    new_changes['_X2_9'].append({elem for elem in structure['_X2_9'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X2_9']))):
                    if (all(((elem == False) for elem in structure['A_9']))):
                        new_changes['_X2_9'].append({elem for elem in structure['_X2_9'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X1_9']))):
                    new_changes['_X1_9'].append({elem for elem in structure['_X1_9'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['A_9']))):
                    if (all(((elem == True) for elem in structure['_X2_9']))):
                        new_changes['A_9'].append({elem for elem in structure['A_9'] if (elem == True)})
        if (key == '_X1_10'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X2_10']))):
                    if (all(((elem == False) for elem in structure['_X3_10']))):
                        new_changes['_X2_10'].append({elem for elem in structure['_X2_10'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['B_10']))):
                    if (all(((elem == True) for elem in structure['A_10']))):
                        new_changes['B_10'].append({elem for elem in structure['B_10'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X3_10']))):
                    if (all(((elem == True) for elem in structure['_X2_10']))):
                        new_changes['_X3_10'].append({elem for elem in structure['_X3_10'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['A_10']))):
                    if (all(((elem == True) for elem in structure['B_10']))):
                        new_changes['A_10'].append({elem for elem in structure['A_10'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['A_10']))):
                    new_changes['A_10'].append({elem for elem in structure['A_10'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_10']))):
                    new_changes['_X3_10'].append({elem for elem in structure['_X3_10'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['B_10']))):
                    new_changes['B_10'].append({elem for elem in structure['B_10'] if (elem == True)})
        if (key == 'A_10'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_10']))):
                    if (all(((elem == True) for elem in structure['B_10']))):
                        new_changes['_X1_10'].append({elem for elem in structure['_X1_10'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X2_10']))):
                    new_changes['_X2_10'].append({elem for elem in structure['_X2_10'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['B_10']))):
                    if (all(((elem == True) for elem in structure['_X1_10']))):
                        new_changes['B_10'].append({elem for elem in structure['B_10'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_10']))):
                    new_changes['_X1_10'].append({elem for elem in structure['_X1_10'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['B_10']))):
                    if (all(((elem == True) for elem in structure['_X2_10']))):
                        new_changes['B_10'].append({elem for elem in structure['B_10'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X2_10']))):
                    if (all(((elem == False) for elem in structure['B_10']))):
                        new_changes['_X2_10'].append({elem for elem in structure['_X2_10'] if (elem == False)})
        if (key == 'B_10'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_10']))):
                    if (all(((elem == True) for elem in structure['A_10']))):
                        new_changes['_X1_10'].append({elem for elem in structure['_X1_10'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X2_10']))):
                    new_changes['_X2_10'].append({elem for elem in structure['_X2_10'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['A_10']))):
                    if (all(((elem == True) for elem in structure['_X1_10']))):
                        new_changes['A_10'].append({elem for elem in structure['A_10'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_10']))):
                    new_changes['_X1_10'].append({elem for elem in structure['_X1_10'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X2_10']))):
                    if (all(((elem == False) for elem in structure['A_10']))):
                        new_changes['_X2_10'].append({elem for elem in structure['_X2_10'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['A_10']))):
                    if (all(((elem == True) for elem in structure['_X2_10']))):
                        new_changes['A_10'].append({elem for elem in structure['A_10'] if (elem == True)})
        if (key == '_X2_1'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['B_1']))):
                    if (all(((elem == False) for elem in structure['A_1']))):
                        new_changes['B_1'].append({elem for elem in structure['B_1'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_1']))):
                    if (all(((elem == False) for elem in structure['_X3_1']))):
                        new_changes['_X1_1'].append({elem for elem in structure['_X1_1'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['A_1']))):
                    if (all(((elem == False) for elem in structure['B_1']))):
                        new_changes['A_1'].append({elem for elem in structure['A_1'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X3_1']))):
                    if (all(((elem == True) for elem in structure['_X1_1']))):
                        new_changes['_X3_1'].append({elem for elem in structure['_X3_1'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['B_1']))):
                    new_changes['B_1'].append({elem for elem in structure['B_1'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['A_1']))):
                    new_changes['A_1'].append({elem for elem in structure['A_1'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_1']))):
                    new_changes['_X3_1'].append({elem for elem in structure['_X3_1'] if (elem == False)})
        if (key == '_X2_2'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X3_2']))):
                    if (all(((elem == True) for elem in structure['_X1_2']))):
                        new_changes['_X3_2'].append({elem for elem in structure['_X3_2'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['B_2']))):
                    if (all(((elem == False) for elem in structure['A_2']))):
                        new_changes['B_2'].append({elem for elem in structure['B_2'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['A_2']))):
                    if (all(((elem == False) for elem in structure['B_2']))):
                        new_changes['A_2'].append({elem for elem in structure['A_2'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_2']))):
                    if (all(((elem == False) for elem in structure['_X3_2']))):
                        new_changes['_X1_2'].append({elem for elem in structure['_X1_2'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['B_2']))):
                    new_changes['B_2'].append({elem for elem in structure['B_2'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['A_2']))):
                    new_changes['A_2'].append({elem for elem in structure['A_2'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_2']))):
                    new_changes['_X3_2'].append({elem for elem in structure['_X3_2'] if (elem == False)})
        if (key == '_X2_3'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['B_3']))):
                    if (all(((elem == False) for elem in structure['A_3']))):
                        new_changes['B_3'].append({elem for elem in structure['B_3'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X3_3']))):
                    if (all(((elem == True) for elem in structure['_X1_3']))):
                        new_changes['_X3_3'].append({elem for elem in structure['_X3_3'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['A_3']))):
                    if (all(((elem == False) for elem in structure['B_3']))):
                        new_changes['A_3'].append({elem for elem in structure['A_3'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_3']))):
                    if (all(((elem == False) for elem in structure['_X3_3']))):
                        new_changes['_X1_3'].append({elem for elem in structure['_X1_3'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['B_3']))):
                    new_changes['B_3'].append({elem for elem in structure['B_3'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_3']))):
                    new_changes['_X3_3'].append({elem for elem in structure['_X3_3'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['A_3']))):
                    new_changes['A_3'].append({elem for elem in structure['A_3'] if (elem == False)})
        if (key == '_X2_4'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_4']))):
                    if (all(((elem == False) for elem in structure['_X3_4']))):
                        new_changes['_X1_4'].append({elem for elem in structure['_X1_4'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['A_4']))):
                    if (all(((elem == False) for elem in structure['B_4']))):
                        new_changes['A_4'].append({elem for elem in structure['A_4'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X3_4']))):
                    if (all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X3_4'].append({elem for elem in structure['_X3_4'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['B_4']))):
                    if (all(((elem == False) for elem in structure['A_4']))):
                        new_changes['B_4'].append({elem for elem in structure['B_4'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X3_4']))):
                    new_changes['_X3_4'].append({elem for elem in structure['_X3_4'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['A_4']))):
                    new_changes['A_4'].append({elem for elem in structure['A_4'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['B_4']))):
                    new_changes['B_4'].append({elem for elem in structure['B_4'] if (elem == False)})
        if (key == '_X2_5'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['A_5']))):
                    if (all(((elem == False) for elem in structure['B_5']))):
                        new_changes['A_5'].append({elem for elem in structure['A_5'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X3_5']))):
                    if (all(((elem == True) for elem in structure['_X1_5']))):
                        new_changes['_X3_5'].append({elem for elem in structure['_X3_5'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['B_5']))):
                    if (all(((elem == False) for elem in structure['A_5']))):
                        new_changes['B_5'].append({elem for elem in structure['B_5'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_5']))):
                    if (all(((elem == False) for elem in structure['_X3_5']))):
                        new_changes['_X1_5'].append({elem for elem in structure['_X1_5'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['A_5']))):
                    new_changes['A_5'].append({elem for elem in structure['A_5'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_5']))):
                    new_changes['_X3_5'].append({elem for elem in structure['_X3_5'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['B_5']))):
                    new_changes['B_5'].append({elem for elem in structure['B_5'] if (elem == False)})
        if (key == '_X2_6'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['A_6']))):
                    if (all(((elem == False) for elem in structure['B_6']))):
                        new_changes['A_6'].append({elem for elem in structure['A_6'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X3_6']))):
                    if (all(((elem == True) for elem in structure['_X1_6']))):
                        new_changes['_X3_6'].append({elem for elem in structure['_X3_6'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['B_6']))):
                    if (all(((elem == False) for elem in structure['A_6']))):
                        new_changes['B_6'].append({elem for elem in structure['B_6'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_6']))):
                    if (all(((elem == False) for elem in structure['_X3_6']))):
                        new_changes['_X1_6'].append({elem for elem in structure['_X1_6'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X3_6']))):
                    new_changes['_X3_6'].append({elem for elem in structure['_X3_6'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['B_6']))):
                    new_changes['B_6'].append({elem for elem in structure['B_6'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['A_6']))):
                    new_changes['A_6'].append({elem for elem in structure['A_6'] if (elem == False)})
        if (key == '_X2_7'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['A_7']))):
                    if (all(((elem == False) for elem in structure['B_7']))):
                        new_changes['A_7'].append({elem for elem in structure['A_7'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_7']))):
                    if (all(((elem == False) for elem in structure['_X3_7']))):
                        new_changes['_X1_7'].append({elem for elem in structure['_X1_7'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['B_7']))):
                    if (all(((elem == False) for elem in structure['A_7']))):
                        new_changes['B_7'].append({elem for elem in structure['B_7'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X3_7']))):
                    if (all(((elem == True) for elem in structure['_X1_7']))):
                        new_changes['_X3_7'].append({elem for elem in structure['_X3_7'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['A_7']))):
                    new_changes['A_7'].append({elem for elem in structure['A_7'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['B_7']))):
                    new_changes['B_7'].append({elem for elem in structure['B_7'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_7']))):
                    new_changes['_X3_7'].append({elem for elem in structure['_X3_7'] if (elem == False)})
        if (key == '_X2_8'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['B_8']))):
                    if (all(((elem == False) for elem in structure['A_8']))):
                        new_changes['B_8'].append({elem for elem in structure['B_8'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_8']))):
                    if (all(((elem == False) for elem in structure['_X3_8']))):
                        new_changes['_X1_8'].append({elem for elem in structure['_X1_8'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X3_8']))):
                    if (all(((elem == True) for elem in structure['_X1_8']))):
                        new_changes['_X3_8'].append({elem for elem in structure['_X3_8'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['A_8']))):
                    if (all(((elem == False) for elem in structure['B_8']))):
                        new_changes['A_8'].append({elem for elem in structure['A_8'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['A_8']))):
                    new_changes['A_8'].append({elem for elem in structure['A_8'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_8']))):
                    new_changes['_X3_8'].append({elem for elem in structure['_X3_8'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['B_8']))):
                    new_changes['B_8'].append({elem for elem in structure['B_8'] if (elem == False)})
        if (key == '_X2_9'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['B_9']))):
                    if (all(((elem == False) for elem in structure['A_9']))):
                        new_changes['B_9'].append({elem for elem in structure['B_9'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_9']))):
                    if (all(((elem == False) for elem in structure['_X3_9']))):
                        new_changes['_X1_9'].append({elem for elem in structure['_X1_9'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X3_9']))):
                    if (all(((elem == True) for elem in structure['_X1_9']))):
                        new_changes['_X3_9'].append({elem for elem in structure['_X3_9'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['A_9']))):
                    if (all(((elem == False) for elem in structure['B_9']))):
                        new_changes['A_9'].append({elem for elem in structure['A_9'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X3_9']))):
                    new_changes['_X3_9'].append({elem for elem in structure['_X3_9'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['B_9']))):
                    new_changes['B_9'].append({elem for elem in structure['B_9'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['A_9']))):
                    new_changes['A_9'].append({elem for elem in structure['A_9'] if (elem == False)})
        if (key == '_X2_10'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['B_10']))):
                    if (all(((elem == False) for elem in structure['A_10']))):
                        new_changes['B_10'].append({elem for elem in structure['B_10'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X3_10']))):
                    if (all(((elem == True) for elem in structure['_X1_10']))):
                        new_changes['_X3_10'].append({elem for elem in structure['_X3_10'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X1_10']))):
                    if (all(((elem == False) for elem in structure['_X3_10']))):
                        new_changes['_X1_10'].append({elem for elem in structure['_X1_10'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['A_10']))):
                    if (all(((elem == False) for elem in structure['B_10']))):
                        new_changes['A_10'].append({elem for elem in structure['A_10'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['B_10']))):
                    new_changes['B_10'].append({elem for elem in structure['B_10'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['A_10']))):
                    new_changes['A_10'].append({elem for elem in structure['A_10'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_10']))):
                    new_changes['_X3_10'].append({elem for elem in structure['_X3_10'] if (elem == False)})
        if (key == '_X3_1'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X4']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X4'].append({elem for elem in structure['_X4'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_6']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_6'].append({elem for elem in structure['_X3_6'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_5']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_5'].append({elem for elem in structure['_X3_5'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X2_1']))):
                    new_changes['_X2_1'].append({elem for elem in structure['_X2_1'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_7']))):
                    if (all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_7'].append({elem for elem in structure['_X3_7'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_8']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4']))):
                        new_changes['_X3_8'].append({elem for elem in structure['_X3_8'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_3']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_3'].append({elem for elem in structure['_X3_3'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_10']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_10'].append({elem for elem in structure['_X3_10'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_2']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_2'].append({elem for elem in structure['_X3_2'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_4']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_4'].append({elem for elem in structure['_X3_4'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X1_1']))):
                    new_changes['_X1_1'].append({elem for elem in structure['_X1_1'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_9']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_9'].append({elem for elem in structure['_X3_9'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X4']))):
                    new_changes['_X4'].append({elem for elem in structure['_X4'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X1_1']))):
                    if (all(((elem == True) for elem in structure['_X2_1']))):
                        new_changes['_X1_1'].append({elem for elem in structure['_X1_1'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X2_1']))):
                    if (all(((elem == True) for elem in structure['_X1_1']))):
                        new_changes['_X2_1'].append({elem for elem in structure['_X2_1'] if (elem == False)})
        if (key == '_X3_2'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X1_2']))):
                    new_changes['_X1_2'].append({elem for elem in structure['_X1_2'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X2_2']))):
                    new_changes['_X2_2'].append({elem for elem in structure['_X2_2'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_5']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_5'].append({elem for elem in structure['_X3_5'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_3']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_3'].append({elem for elem in structure['_X3_3'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_8']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4']))):
                        new_changes['_X3_8'].append({elem for elem in structure['_X3_8'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_10']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_10'].append({elem for elem in structure['_X3_10'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_1']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_1'].append({elem for elem in structure['_X3_1'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_7']))):
                    if (all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_7'].append({elem for elem in structure['_X3_7'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_4']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_4'].append({elem for elem in structure['_X3_4'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_9']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_9'].append({elem for elem in structure['_X3_9'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X4']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X4'].append({elem for elem in structure['_X4'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_6']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_6'].append({elem for elem in structure['_X3_6'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_2']))):
                    if (all(((elem == True) for elem in structure['_X2_2']))):
                        new_changes['_X1_2'].append({elem for elem in structure['_X1_2'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X2_2']))):
                    if (all(((elem == True) for elem in structure['_X1_2']))):
                        new_changes['_X2_2'].append({elem for elem in structure['_X2_2'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X4']))):
                    new_changes['_X4'].append({elem for elem in structure['_X4'] if (elem == False)})
        if (key == '_X3_3'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X3_9']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_9'].append({elem for elem in structure['_X3_9'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_2']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_2'].append({elem for elem in structure['_X3_2'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X1_3']))):
                    new_changes['_X1_3'].append({elem for elem in structure['_X1_3'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X2_3']))):
                    new_changes['_X2_3'].append({elem for elem in structure['_X2_3'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_6']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_6'].append({elem for elem in structure['_X3_6'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_5']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_5'].append({elem for elem in structure['_X3_5'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X4']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X4'].append({elem for elem in structure['_X4'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_8']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4']))):
                        new_changes['_X3_8'].append({elem for elem in structure['_X3_8'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_10']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_10'].append({elem for elem in structure['_X3_10'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_7']))):
                    if (all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_7'].append({elem for elem in structure['_X3_7'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_1']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_1'].append({elem for elem in structure['_X3_1'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_4']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_4'].append({elem for elem in structure['_X3_4'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_3']))):
                    if (all(((elem == True) for elem in structure['_X2_3']))):
                        new_changes['_X1_3'].append({elem for elem in structure['_X1_3'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X4']))):
                    new_changes['_X4'].append({elem for elem in structure['_X4'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X2_3']))):
                    if (all(((elem == True) for elem in structure['_X1_3']))):
                        new_changes['_X2_3'].append({elem for elem in structure['_X2_3'] if (elem == False)})
        if (key == '_X3_4'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X3_8']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6']))):
                        new_changes['_X3_8'].append({elem for elem in structure['_X3_8'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_9']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_9'].append({elem for elem in structure['_X3_9'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_2']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_2'].append({elem for elem in structure['_X3_2'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_7']))):
                    if (all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_7'].append({elem for elem in structure['_X3_7'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_6']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_6'].append({elem for elem in structure['_X3_6'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X2_4']))):
                    new_changes['_X2_4'].append({elem for elem in structure['_X2_4'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X1_4']))):
                    new_changes['_X1_4'].append({elem for elem in structure['_X1_4'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_5']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_5'].append({elem for elem in structure['_X3_5'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_3']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_3'].append({elem for elem in structure['_X3_3'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X4']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X4'].append({elem for elem in structure['_X4'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_10']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_10'].append({elem for elem in structure['_X3_10'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_1']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_1'].append({elem for elem in structure['_X3_1'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_4']))):
                    if (all(((elem == True) for elem in structure['_X2_4']))):
                        new_changes['_X1_4'].append({elem for elem in structure['_X1_4'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X4']))):
                    new_changes['_X4'].append({elem for elem in structure['_X4'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X2_4']))):
                    if (all(((elem == True) for elem in structure['_X1_4']))):
                        new_changes['_X2_4'].append({elem for elem in structure['_X2_4'] if (elem == False)})
        if (key == '_X3_5'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X3_2']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_2'].append({elem for elem in structure['_X3_2'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_7']))):
                    if (all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_7'].append({elem for elem in structure['_X3_7'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_4']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_4'].append({elem for elem in structure['_X3_4'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_9']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_9'].append({elem for elem in structure['_X3_9'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_8']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4']))):
                        new_changes['_X3_8'].append({elem for elem in structure['_X3_8'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X4']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X4'].append({elem for elem in structure['_X4'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_6']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_6'].append({elem for elem in structure['_X3_6'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_1']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_1'].append({elem for elem in structure['_X3_1'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_3']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_3'].append({elem for elem in structure['_X3_3'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_10']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_10'].append({elem for elem in structure['_X3_10'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X1_5']))):
                    new_changes['_X1_5'].append({elem for elem in structure['_X1_5'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X2_5']))):
                    new_changes['_X2_5'].append({elem for elem in structure['_X2_5'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X2_5']))):
                    if (all(((elem == True) for elem in structure['_X1_5']))):
                        new_changes['_X2_5'].append({elem for elem in structure['_X2_5'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X4']))):
                    new_changes['_X4'].append({elem for elem in structure['_X4'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X1_5']))):
                    if (all(((elem == True) for elem in structure['_X2_5']))):
                        new_changes['_X1_5'].append({elem for elem in structure['_X1_5'] if (elem == False)})
        if (key == '_X3_6'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X3_4']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_4'].append({elem for elem in structure['_X3_4'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_7']))):
                    if (all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_7'].append({elem for elem in structure['_X3_7'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X2_6']))):
                    new_changes['_X2_6'].append({elem for elem in structure['_X2_6'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X1_6']))):
                    new_changes['_X1_6'].append({elem for elem in structure['_X1_6'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_5']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_5'].append({elem for elem in structure['_X3_5'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X4']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X4'].append({elem for elem in structure['_X4'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_10']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_10'].append({elem for elem in structure['_X3_10'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_1']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_1'].append({elem for elem in structure['_X3_1'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_8']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_4']))):
                        new_changes['_X3_8'].append({elem for elem in structure['_X3_8'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_3']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_3'].append({elem for elem in structure['_X3_3'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_9']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_9'].append({elem for elem in structure['_X3_9'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_2']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_2'].append({elem for elem in structure['_X3_2'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_6']))):
                    if (all(((elem == True) for elem in structure['_X2_6']))):
                        new_changes['_X1_6'].append({elem for elem in structure['_X1_6'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X4']))):
                    new_changes['_X4'].append({elem for elem in structure['_X4'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X2_6']))):
                    if (all(((elem == True) for elem in structure['_X1_6']))):
                        new_changes['_X2_6'].append({elem for elem in structure['_X2_6'] if (elem == False)})
        if (key == '_X3_7'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X3_5']))):
                    if (all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_5'].append({elem for elem in structure['_X3_5'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_3']))):
                    if (all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_3'].append({elem for elem in structure['_X3_3'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_8']))):
                    if (all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4']))):
                        new_changes['_X3_8'].append({elem for elem in structure['_X3_8'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X4']))):
                    if (all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X4'].append({elem for elem in structure['_X4'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_10']))):
                    if (all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_10'].append({elem for elem in structure['_X3_10'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_1']))):
                    if (all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_1'].append({elem for elem in structure['_X3_1'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X1_7']))):
                    new_changes['_X1_7'].append({elem for elem in structure['_X1_7'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X2_7']))):
                    new_changes['_X2_7'].append({elem for elem in structure['_X2_7'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_4']))):
                    if (all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_4'].append({elem for elem in structure['_X3_4'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_9']))):
                    if (all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_9'].append({elem for elem in structure['_X3_9'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_2']))):
                    if (all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_2'].append({elem for elem in structure['_X3_2'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_6']))):
                    if (all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_6'].append({elem for elem in structure['_X3_6'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_7']))):
                    if (all(((elem == True) for elem in structure['_X2_7']))):
                        new_changes['_X1_7'].append({elem for elem in structure['_X1_7'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X2_7']))):
                    if (all(((elem == True) for elem in structure['_X1_7']))):
                        new_changes['_X2_7'].append({elem for elem in structure['_X2_7'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X4']))):
                    new_changes['_X4'].append({elem for elem in structure['_X4'] if (elem == False)})
        if (key == '_X3_8'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X3_10']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4']))):
                        new_changes['_X3_10'].append({elem for elem in structure['_X3_10'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X2_8']))):
                    new_changes['_X2_8'].append({elem for elem in structure['_X2_8'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_1']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4']))):
                        new_changes['_X3_1'].append({elem for elem in structure['_X3_1'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_3']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4']))):
                        new_changes['_X3_3'].append({elem for elem in structure['_X3_3'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_4']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6']))):
                        new_changes['_X3_4'].append({elem for elem in structure['_X3_4'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_9']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4']))):
                        new_changes['_X3_9'].append({elem for elem in structure['_X3_9'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_2']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4']))):
                        new_changes['_X3_2'].append({elem for elem in structure['_X3_2'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X1_8']))):
                    new_changes['_X1_8'].append({elem for elem in structure['_X1_8'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_6']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_4']))):
                        new_changes['_X3_6'].append({elem for elem in structure['_X3_6'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_7']))):
                    if (all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4']))):
                        new_changes['_X3_7'].append({elem for elem in structure['_X3_7'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_5']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4']))):
                        new_changes['_X3_5'].append({elem for elem in structure['_X3_5'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X4']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4']))):
                        new_changes['_X4'].append({elem for elem in structure['_X4'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_8']))):
                    if (all(((elem == True) for elem in structure['_X2_8']))):
                        new_changes['_X1_8'].append({elem for elem in structure['_X1_8'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X2_8']))):
                    if (all(((elem == True) for elem in structure['_X1_8']))):
                        new_changes['_X2_8'].append({elem for elem in structure['_X2_8'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X4']))):
                    new_changes['_X4'].append({elem for elem in structure['_X4'] if (elem == False)})
        if (key == '_X3_9'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X3_8']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4']))):
                        new_changes['_X3_8'].append({elem for elem in structure['_X3_8'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_3']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_3'].append({elem for elem in structure['_X3_3'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_10']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_10'].append({elem for elem in structure['_X3_10'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_2']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_2'].append({elem for elem in structure['_X3_2'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X2_9']))):
                    new_changes['_X2_9'].append({elem for elem in structure['_X2_9'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X1_9']))):
                    new_changes['_X1_9'].append({elem for elem in structure['_X1_9'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_4']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_4'].append({elem for elem in structure['_X3_4'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_7']))):
                    if (all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_7'].append({elem for elem in structure['_X3_7'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_5']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_5'].append({elem for elem in structure['_X3_5'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X4']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X4'].append({elem for elem in structure['_X4'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_6']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_6'].append({elem for elem in structure['_X3_6'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_1']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_1'].append({elem for elem in structure['_X3_1'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X4']))):
                    new_changes['_X4'].append({elem for elem in structure['_X4'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X2_9']))):
                    if (all(((elem == True) for elem in structure['_X1_9']))):
                        new_changes['_X2_9'].append({elem for elem in structure['_X2_9'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X1_9']))):
                    if (all(((elem == True) for elem in structure['_X2_9']))):
                        new_changes['_X1_9'].append({elem for elem in structure['_X1_9'] if (elem == False)})
        if (key == '_X3_10'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X4']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X4'].append({elem for elem in structure['_X4'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_6']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_6'].append({elem for elem in structure['_X3_6'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_1']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_1'].append({elem for elem in structure['_X3_1'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_3']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_3'].append({elem for elem in structure['_X3_3'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_8']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4']))):
                        new_changes['_X3_8'].append({elem for elem in structure['_X3_8'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_9']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_9'].append({elem for elem in structure['_X3_9'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_2']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_2'].append({elem for elem in structure['_X3_2'] if (elem == False)})
                if (not all(((elem == True) for elem in structure['_X1_10']))):
                    new_changes['_X1_10'].append({elem for elem in structure['_X1_10'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X2_10']))):
                    new_changes['_X2_10'].append({elem for elem in structure['_X2_10'] if (elem == True)})
                if (not all(((elem == False) for elem in structure['_X3_7']))):
                    if (all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_7'].append({elem for elem in structure['_X3_7'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_4']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_4'].append({elem for elem in structure['_X3_4'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_5']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == False) for elem in structure['_X4'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_5'].append({elem for elem in structure['_X3_5'] if (elem == False)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X1_10']))):
                    if (all(((elem == True) for elem in structure['_X2_10']))):
                        new_changes['_X1_10'].append({elem for elem in structure['_X1_10'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X2_10']))):
                    if (all(((elem == True) for elem in structure['_X1_10']))):
                        new_changes['_X2_10'].append({elem for elem in structure['_X2_10'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X4']))):
                    new_changes['_X4'].append({elem for elem in structure['_X4'] if (elem == False)})
        if (key == '_X4'):
            if all(((elem == True) for elem in value)):
                if (not all(((elem == True) for elem in structure['_X3_1']))):
                    new_changes['_X3_1'].append({elem for elem in structure['_X3_1'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X3_3']))):
                    new_changes['_X3_3'].append({elem for elem in structure['_X3_3'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X3_4']))):
                    new_changes['_X3_4'].append({elem for elem in structure['_X3_4'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X3_5']))):
                    new_changes['_X3_5'].append({elem for elem in structure['_X3_5'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X3_2']))):
                    new_changes['_X3_2'].append({elem for elem in structure['_X3_2'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X3_6']))):
                    new_changes['_X3_6'].append({elem for elem in structure['_X3_6'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X3_7']))):
                    new_changes['_X3_7'].append({elem for elem in structure['_X3_7'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X3_8']))):
                    new_changes['_X3_8'].append({elem for elem in structure['_X3_8'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X3_9']))):
                    new_changes['_X3_9'].append({elem for elem in structure['_X3_9'] if (elem == True)})
                if (not all(((elem == True) for elem in structure['_X3_10']))):
                    new_changes['_X3_10'].append({elem for elem in structure['_X3_10'] if (elem == True)})
            elif all(((elem == False) for elem in value)):
                if (not all(((elem == False) for elem in structure['_X3_1']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_1'].append({elem for elem in structure['_X3_1'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_4']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_4'].append({elem for elem in structure['_X3_4'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_7']))):
                    if (all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_7'].append({elem for elem in structure['_X3_7'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_9']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_9'].append({elem for elem in structure['_X3_9'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_3']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_3'].append({elem for elem in structure['_X3_3'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_2']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_2'].append({elem for elem in structure['_X3_2'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_6']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_6'].append({elem for elem in structure['_X3_6'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_5']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_5'].append({elem for elem in structure['_X3_5'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_8']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_10'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4']))):
                        new_changes['_X3_8'].append({elem for elem in structure['_X3_8'] if (elem == False)})
                if (not all(((elem == False) for elem in structure['_X3_10']))):
                    if (all(((elem == True) for elem in structure['_X3_7'])) and all(((elem == True) for elem in structure['_X3_3'])) and all(((elem == True) for elem in structure['_X3_2'])) and all(((elem == True) for elem in structure['_X3_1'])) and all(((elem == True) for elem in structure['_X3_5'])) and all(((elem == True) for elem in structure['_X3_9'])) and all(((elem == True) for elem in structure['_X3_6'])) and all(((elem == True) for elem in structure['_X3_4'])) and all(((elem == True) for elem in structure['_X3_8']))):
                        new_changes['_X3_10'].append({elem for elem in structure['_X3_10'] if (elem == False)})
    return intersect_changes(new_changes)

def propagation_loop(changes):
    unsat_fields = check_unsat_fields(changes)
    while ((len(changes) != 0) and (len(unsat_fields) == 0)):
        old_changes = changes
        changes = propagate(changes)
        update_structure(old_changes)
        unsat_fields = check_unsat_fields(changes)
    return unsat_fields
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
