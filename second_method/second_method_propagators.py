# This part of the compiler is responsible for converting ENF-rules to high-level propagators, as discussed in sections 4.4.2 and 4.4.3 of the thesis text.
# In short:
#   - rules of type ENFConjunctive and ENFDisjunctive are converted to normal propagators, represented by general UNSAT-sets.
#   - rules of type ENFExistential, ENFUniversal and ENFReductive are converted to both a generalizing propagator and a specifying propagator.
#   - for every function in the original IDP-program, a function propagator is added.


from second_method_enf import AssertLiteral, ENFConjunctive, ENFDisjunctive, ENFUniversal, ENFExistential, ENFReductive

# This class represents normal propagators, as mentioned in section 4.4.3.1.
class NormalPropagator:
    def __init__(self, unsat, bindings):
        self.unsat = unsat.copy()
        self.bindings = bindings.copy()

# This class represents specifying propagators, as mentioned in section 4.4.3.2.
class SpecifyingPropagator:
    def __init__(self, general, specific, bindings, new_binding, universal):
        self.general = general
        self.specific = specific
        self.bindings = bindings.copy()
        self.new_binding = new_binding
        self.universal = universal

# This class represents generalizing propagators, as mentioned in 4.4.3.3.
class GeneralizingPropagator:
    def __init__(self, specific, general, bindings, new_binding, universal):
        self.specific = specific
        self.general = general
        self.bindings = bindings.copy()
        self.new_binding = new_binding
        self.universal = universal

# This class represents function propagators, as mentioned in section 4.4.3.4.
class FunctionPropagator:
    def __init__(self, name):
        self.name = name


# This function performs the transformation from ENF-rules to high-level propagators, as discussed in section 4.4.3.
def get_propagators(enf, position):
    propagators = []
    if type(enf) == ENFConjunctive:
        if position == 0:
            for lit in enf.right:
                propagators.append(NormalPropagator([enf.left] + [lit.negate()], enf.bindings))
            propagators.append(NormalPropagator([enf.left.negate()] + enf.right, enf.bindings))
        else:
            propagators.append(NormalPropagator([enf.right[position-1].negate()] + [enf.left], enf.bindings))
            propagators.append(NormalPropagator([enf.right[position-1]] + enf.right[:(position-1)] + enf.right[position:] + [enf.left.negate()], enf.bindings))
    if type(enf) == ENFDisjunctive:
        if position == 0:
            for lit in enf.right:
                    propagators.append(NormalPropagator([enf.left.negate()] + [lit], enf.bindings))
            propagators.append(NormalPropagator([enf.left] + [lit.negate() for lit in enf.right], enf.bindings))
        else:
            propagators.append(NormalPropagator([enf.right[position-1]] + [enf.left.negate()], enf.bindings))
            propagators.append(NormalPropagator([enf.right[position-1].negate()] + [lit.negate() for lit in enf.right[:(position-1)]] + [lit.negate() for lit in enf.right[position:]] + [enf.left], enf.bindings))
    if type(enf) == ENFUniversal:
        if position == 0:
            propagators.append(SpecifyingPropagator(enf.left, enf.right, enf.bindings, enf.new_binding, True))
        if position == 1:
            propagators.append(GeneralizingPropagator(enf.right, enf.left, enf.bindings, enf.new_binding, True))
    if type(enf) == ENFExistential:
        if position == 0:
            propagators.append(SpecifyingPropagator(enf.left, enf.right, enf.bindings, enf.new_binding, False))
        if position == 1:
            propagators.append(GeneralizingPropagator(enf.right, enf.left, enf.bindings, enf.new_binding, False))
    if type(enf) == ENFReductive: #!x,y: A(x,y) <=> B(x)
        if position == 0:
            propagators.append(GeneralizingPropagator(enf.left, enf.right, enf.bindings, enf.old_binding,enf.b))
        if position == 1:
            propagators.append(SpecifyingPropagator(enf.right, enf.left, enf.bindings, enf.old_binding, enf.b))
    return propagators



# Auxiliary function to easily add an element with a given key to a dictionary.
def add_to_dict(d, k, elem):
    if k in d.keys():
        d[k].extend(elem)
    else:
        d[k] = elem

# This function gets as input all generated ENF rules.
# The function goes over all literals (positions) in the rules and calls get_propagators() for every position.
# Next, the new propagators are grouped based on the name of the atom.
# Moreover, for every function in the original IDP program, a function propagator is added to the grouped propagators.
def group_propagators(enf_rules, functions):
    #full_predicates = [predicate.name for predicate in predicates] + [";p_" + function.name for function in functions] # + hulpvariabelen!
    grouped_propagators = {}

    for enf_rule in enf_rules:
        if type(enf_rule) == AssertLiteral:
            add_to_dict(grouped_propagators, enf_rule.literal.atom.name, [AssertLiteral(enf_rule.literal)])
        if type(enf_rule) == ENFConjunctive or type(enf_rule) == ENFDisjunctive:
            add_to_dict(grouped_propagators, enf_rule.left.atom.name, get_propagators(enf_rule, 0))
            for i, lit in enumerate(enf_rule.right):
                add_to_dict(grouped_propagators, lit.atom.name, get_propagators(enf_rule, i+1))
        if type(enf_rule) == ENFUniversal or type(enf_rule) == ENFExistential or type(enf_rule) == ENFReductive:
            add_to_dict(grouped_propagators, enf_rule.left.atom.name, get_propagators(enf_rule, 0))
            add_to_dict(grouped_propagators, enf_rule.right.atom.name, get_propagators(enf_rule, 1))

    for func in functions:
        add_to_dict(grouped_propagators, ';p;' + func.name, [FunctionPropagator(';p;' + func.name)])

    return grouped_propagators