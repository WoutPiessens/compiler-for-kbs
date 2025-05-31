# This part of the compiler is responsible for grounding the ENF-rules, in other words, removing the universal and existential quantifiers.
# This is done in two steps:
# - First:
#     Rules of type ∀x: L(x) ⇔ ∀y: L’(x,y) are converted to rules of type ∀x: L(x) ⇔ L1(x) ∧ … ∧ Ln(x)
#     Rules of type ∀x: L(x) ⇔ ∃y: L’(x,y) are converted to rules of type ∀x: L(x) ⇔ L1(x) ∨ … ∨ Ln(x)
# - Second:
#     Quantifiers over the entire ENF-rules are removed, and all possible assignments of domain values to variables are filled in.
#     This way, one ENF-rule is converted to multiple grounded ENF-rules.

# More details about this part of the compiler can be found in the thesis text, in section 4.3.5.


from first_method.first_method_parsing import Term, Atom, IntegerRange
from first_method.first_method_nnf import Literal
from first_method.first_method_enf import ENFUniversal, ENFExistential, ENFDisjunctive, ENFConjunctive, AssertLiteral
from itertools import product


# Helper function to fill in domain values for variables in the first step.
def get_new_junct(exp, assignment):
    new_args = []
    for arg in exp.atom.args:
        if arg.name in assignment.keys():
            new_args.append(Term(assignment[arg.name]))
        else:
            new_args.append(Term(arg.name))
    return Literal(Atom(exp.atom.name, new_args), exp.pos)

# Helper function that implements the first step of grounding:
#    Rules of type ∀x: L(x) ⇔ ∀y: L’(x,y) are converted to rules of type ∀x: L(x) ⇔ L1(x) ∧ … ∧ Ln(x)
#    Rules of type ∀x: L(x) ⇔ ∃y: L’(x,y) are converted to rules of type ∀x: L(x) ⇔ L1(x) ∨ … ∨ Ln(x)
def remove_quantifier(enf, types):
    var_domain = IntegerRange(1,10) #temp
    new_binding_domains = dict()
    for var in enf.new_binding:
        for t in types:
            if var.type == t.name:
                var_domain = t.domain
        if type(var_domain) == IntegerRange:
            full_domain = list(range(var_domain.lb, var_domain.ub+1))
        else:
            full_domain = list(var_domain)

        new_binding_domains.update({var.name : full_domain})

    junction = []

    for combination in product(*new_binding_domains.values()):
        assignment = dict(zip(new_binding_domains.keys(), combination))
        junct = get_new_junct(enf.right, assignment)
        junction.append(junct)

    if type(enf) == ENFUniversal:
        return ENFConjunctive(enf.bindings, enf.left, junction)

    if type(enf) == ENFExistential:
        return ENFDisjunctive(enf.bindings, enf.left, junction)


# Helper function to fill in domain values for variables in the second step.
def fill_in_assignment(enf, assignment):

    left_atom = enf.left.atom
    left_atom_name = left_atom.name
    for argument in left_atom.args:
        if argument.name in assignment.keys():
            left_atom_name = left_atom_name + "_" + str(assignment[argument.name])
        else:
            left_atom_name = left_atom_name + "_" + str(argument.name)

    right_literals = []
    for right_lit in enf.right:
        right_atom = right_lit.atom
        new_atom_name = right_atom.name
        for argument in right_atom.args:
            if argument.name in assignment.keys():
                new_atom_name = new_atom_name + "_" + str(assignment[argument.name])
            else:
                new_atom_name = new_atom_name + "_" + str(argument.name)
        right_literals.append(Literal(new_atom_name, right_lit.pos))

    if type(enf) == ENFConjunctive:
        return ENFConjunctive([], Literal(left_atom_name, enf.left.pos), right_literals)
    if type(enf) == ENFDisjunctive:
        return ENFDisjunctive([], Literal(left_atom_name, enf.left.pos), right_literals)


# Helper function to rewrite an atom that is already grounded.

def rewrite_grounded_atom(name, args):
    new_name = name
    for arg in args:
        new_name += '_' + str(arg.name)
    return new_name



# Main grounding function that performs both grounding steps.

def ground_ENF(enf, types):
    if type(enf) != AssertLiteral:
        if type(enf) == ENFUniversal or type(enf) == ENFExistential:
            current_enf = remove_quantifier(enf, types)

        else:
            current_enf = enf
        full_domains = dict()
        var_domain = IntegerRange(1,10) #temp
        for var in enf.bindings:
            for t in types:
                if var.type == t.name:
                    var_domain = t.domain
            if type(var_domain) == IntegerRange: #{1..100}
                full_domain = list(range(var_domain.lb, var_domain.ub+1))
            else:
                full_domain = list(var_domain)

            full_domains.update({var.name : full_domain})

        grounded_enfs = []

        for combination in product(*full_domains.values()):
            assignment = dict(zip(full_domains.keys(), combination))
            grounded_enfs.append(fill_in_assignment(current_enf, assignment))
        return grounded_enfs
    else:
        return [AssertLiteral(Literal(rewrite_grounded_atom(enf.literal.atom.name, enf.literal.atom.args), enf.literal.pos))]


# Helper function to check if a grounded (in)equality atom (e.g. 1 == 2, 2 < 3) evaluates to true or false.
def evaluate_truth_value(name):
    parts_unfiltered = name.split("_")
    parts = [part for part in parts_unfiltered if part != '']
    if len(parts) < 3:
        return False
    if parts[0] == ';EQ':
        return parts[1] == parts[2]
    if parts[0] == 'NEQ':
        return parts[1] != parts[2]
    if parts[0] == 'LEQ':
        return parts[1] <= parts[2]
    if parts[0] == 'LE':
        return parts[1] < parts[2]
    if parts[0] == 'GEQ':
        return parts[1] >= parts[2]
    if parts[0] == 'GE':
        return parts[1] > parts[2]

# Function that removes (in)equality atoms from the ENF rules after the grounding step, since they can be evaluated to true or false.
def remove_equality_rules(enf):
    equality_predicates = (';EQ_', '_NEQ', '_GEQ', '_GE', '_LEQ', '_LE')
    if type(enf) == AssertLiteral:
        return enf
    else:
        if type(enf) == ENFConjunctive:
            new_right = []
            for lit in enf.right:
                if type(lit) == Literal and lit.atom.startswith(equality_predicates):
                    if not evaluate_truth_value(lit.atom):
                        return AssertLiteral(Literal(enf.left.atom, not enf.left.pos))
                else:
                    new_right.append(lit)
            return ENFConjunctive([], enf.left, new_right)
        if type(enf) == ENFDisjunctive:
            new_right = []
            for lit in enf.right:
                if type(lit) == Literal and lit.atom.startswith(equality_predicates):
                    if evaluate_truth_value(lit.atom):
                        return AssertLiteral(Literal(enf.left.atom, enf.left.pos))
                else:
                    new_right.append(lit)
            return ENFDisjunctive([], enf.left, new_right)
        if type(enf) == AssertLiteral:

            if type(enf.literal) == Literal and enf.literal.atom.startswith(equality_predicates):
                if not evaluate_truth_value(enf.literal.atom):
                    raise Exception("unsat")
                else:
                    return None
            else:
                return enf


# Main function grounding and reducing the ENF rules by calling ground_ENF() and remove_equality_rules().
def ground(enfs, types):
    grounded_enfs = [ground_ENF(enf, types) for enf in enfs]
    grounded_enfs_flat = [item for sublist in grounded_enfs for item in sublist]
    grounded_enfs_no_equality_rules = [remove_equality_rules(enf) for enf in grounded_enfs_flat]
    grounded_enfs_no_equality_rules_filter = [item for item in grounded_enfs_no_equality_rules if item is not None]
    return grounded_enfs_no_equality_rules_filter
