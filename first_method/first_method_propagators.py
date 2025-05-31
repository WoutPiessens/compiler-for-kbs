# This part of the compiler is responsible for converting UNSAT-sets to grounded propagators.
# This happens by means of the following rule.
# Given an UNSAT-set U, take two elements x and y from U so that x != y.
# Then a DerivedPropagator object (corresponding to a grounded propagator) can be constructed as follows: DerivedPropagator(x, U\{x,y}, ~y)
# If an UNSAT-set only has one element, than that element must necessarily be false.

# Class representing a propagator: if the left literal evaluates to true,
# and the middle literals all evaluate to true too,
# then the right literal must also evaluate to true.

# More details about this part of the compiler can be found in the thesis text, in section 4.3.7.


class DerivedPropagator:
    def __init__(self, left, middle, right):
        if left == None:
            self.left = None
        else:
            self.left = left.clone()
        self.middle = [lit.clone() for lit in middle]
        self.right = right.clone()

# Function calculating the derived propagators from an UNSAT-set.
def derive_propagators_for_unsat_set(unsat_set):
    derived_propagators = set()
    if len(unsat_set) > 1:
        for start_literal in unsat_set:
            for end_literal in unsat_set:
                if (type(start_literal) != type(end_literal)) or not start_literal.equals(end_literal):
                    derived_propagators.add(DerivedPropagator(start_literal, unsat_set - {start_literal, end_literal}, end_literal.negate()))

    else:
        literal = unsat_set.pop()
        derived_propagators.add(DerivedPropagator(None, [], literal.negate()))
    return derived_propagators


# Main function, calling the function that does the transformation.

def derive_propagators(unsat_sets):
    props = [derive_propagators_for_unsat_set(unsat_set) for unsat_set in unsat_sets]
    props_flat = [item for sublist in props for item in sublist]
    return props_flat
