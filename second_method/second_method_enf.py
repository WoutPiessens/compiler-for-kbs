# This part of the compiler is responsible for converting Negation Normal Form-rules to Equivalence Normal Form-rules.
# This transformation is based on the work of Wittocx. et. al.
# (Wittocx, J., Denecker, M., Bruynooghe, M. 2012. Constraint propagation for first-order logic and inductive definitions ACM Trans. Comput. Logic V, N, Article A (January 2012), 44 pages.)
# In short: subexpressions are substituted for auxiliary variables in a recursive way.
# This results in a list of ENF-expressions for every NNF-expression.
# There are 5 types of ENF-expressions, as described in the thesis text (section 4.3.4.).

# More details about this part of the compiler can be found in the thesis text, in section 4.3.4.
# The second method makes some changes compared to the first, to support high-level propagators in later steps:
#   - More precise rules regarding when a predicate has to be substituted with an auxiliary predicate.
#     This is done so that ENFUniversal and ENFExistential rules have no constant or repeated arguments,
#     and so that the order of arguments in the left and the right predicate (apart from the new quantified variables) is the same)
#   - Introduction of ENFReductive rules, originating from predicates that don't have all quantified variables as arguments.
#     They reduce to the same propagators as ENFUniversal and ENFExistential rules in later steps.
#   - Handling duplicate names in the same ENF rule.
#   - Code for adding new auxiliary predicates to the list of predicates (important for later steps, more precisely the generation of DataArrays)

from second_method_parsing import Term, Atom, UniversalQuantifier, ExistentialQuantifier, Predicate
from second_method_nnf import Literal, And_mul, Or_mul

# Represents rules of the following type: true <=> _X1
class AssertLiteral:
    def __init__(self, literal):
        self.literal = literal.clone()


# Represents rules of the following type: ∀x: L(x) ⇔ L1(x) ∨ … ∨ Ln(x)
class ENFDisjunctive:
    def __init__(self, bindings, left, right):
        self.bindings = bindings.copy()
        self.left = left.clone()
        self.right = [lit.clone() for lit in right]

# Represents rules of the following type: ∀x: L(x) ⇔ L1(x) ∧ … ∧ Ln(x)
class ENFConjunctive:
    def __init__(self, bindings, left, right):
        self.bindings = bindings.copy()
        self.left = left.clone()
        self.right = [lit.clone() for lit in right]

# Represents rules of the following type: ∀x: L(x) ⇔ ∀y: L’(x,y)
class ENFUniversal:
    def __init__(self, bindings, left, new_binding, right):
        self.bindings = bindings.copy()
        self.left = left.clone()
        self.new_binding = new_binding
        self.right = right.clone()

# Represents rules of the following type: ∀x: L(x) ⇔ ∃y: L’(x,y)
class ENFExistential:
    def __init__(self, bindings, left, new_binding, right):
        self.bindings = bindings.copy()
        self.left = left.clone()
        self.new_binding = new_binding
        self.right = right.clone()

# Represents rules of the following type: ∀x,y: L(x,y) ⇔ L'(x)
# These rules reduce to ENFUniversal and ENFExistential rules in a later step.

class ENFReductive:
    def __init__(self, bindings, left, old_binding, right, b):
        self.bindings = bindings.copy()
        self.left = left.clone()
        self.old_binding = old_binding
        self.right = right.clone()
        self.b = b

# Represents the result of a recursive call to the derive_ENFs function:
# - the literal representing the subexpression on which derive_ENFs was called
# - and the current ENF-rules that have been derived
class TemporaryENF:
    def __init__(self, lit, expressions):
        self.lit = lit
        self.expressions = expressions.copy()


# Helper function that checks if one list is a subsequence of another list.
# This means that all elements in list1 have to occur in list2, in the same order.
def is_subseq(list1, list2):
    idx = -1
    for elem in list1:
        if idx == len(list2) - 1:
            return False
        elif elem in list2[(idx+1):]:
            idx = list2.index(elem)
        else:
            return False
    return True

# Helper function that creates auxiliary variables with a unique name to substitute a certain subexpression.
count = 0
def create_auxiliary_literal(bindings):
    global count
    count += 1
    args = []
    for var in bindings:
        args.append(Term(var.name))
    return Literal(Atom(f'_X{count}', args), True)

# Function implementing the conversion algorithm from NNF to ENF.
# The additions that are described in the beginning of this file, are taken care of in this function.
def derive_ENFs(exp, bindings, nested=False):
    if type(exp) == Literal:
        if exp.atom.name in [';EQ', '_NEQ', '_GE', '_GEQ', '_LE', '_LEQ']:
            arg_names = [arg.name for arg in exp.atom.args]
            quantified_var = [var.name for var in bindings]
            small_bindings = [var for var in bindings if var.name in arg_names]
            if quantified_var != small_bindings:
                aux_lit1 = create_auxiliary_literal(small_bindings)
                temp = derive_ENFs(aux_lit1, bindings, True)
                if nested:
                    return TemporaryENF(temp.lit, temp.expressions + [ENFConjunctive(small_bindings, aux_lit1, [exp])])
                else:
                    return [AssertLiteral(temp.lit), temp.expressions + [ENFConjunctive(small_bindings, aux_lit1, [exp])]]

            else:
                aux_lit = create_auxiliary_literal(bindings)
                if nested:
                    return TemporaryENF(aux_lit, [ENFConjunctive(bindings, aux_lit, [exp])])
                else:
                    return [AssertLiteral(aux_lit), ENFConjunctive(bindings, aux_lit, [exp])]
        if nested:
            arg_names = [arg.name for arg in exp.atom.args]
            quantified_var = [var.name for var in bindings]
            arg_names_set = set(arg_names)
            quantified_var_set = set(quantified_var)
            if arg_names == quantified_var:
                #print("i: ", exp.atom.name)
                return TemporaryENF(exp, [])
            elif quantified_var_set.issubset(arg_names_set):
                aux_lit = create_auxiliary_literal(bindings)
                return TemporaryENF(aux_lit, [ENFConjunctive(bindings.copy(), aux_lit, [exp])])
            else:
                aux_lit = create_auxiliary_literal(bindings)
                old_binding = [var for var in bindings if var.name in quantified_var_set.difference(arg_names_set)]
                if exp.pos:

                    if arg_names_set.issubset(quantified_var_set) and is_subseq(arg_names, quantified_var):
                        return TemporaryENF(aux_lit, [ENFReductive(bindings.copy(), aux_lit, old_binding, exp, False)])
                    else:
                        reduced_bindings = [var for var in bindings if var.name in arg_names_set]
                        aux_lit2 = create_auxiliary_literal(reduced_bindings)
                        return TemporaryENF(aux_lit, [ENFReductive(bindings.copy(), aux_lit, old_binding, aux_lit2, False)] +
                                            [ENFConjunctive(reduced_bindings.copy(), aux_lit2, [exp])])
                else:
                    if arg_names_set.issubset(quantified_var_set) and is_subseq(arg_names, quantified_var):
                        aux_lit2 = create_auxiliary_literal(bindings)
                        return TemporaryENF(aux_lit, [ENFConjunctive(bindings.copy(), aux_lit, [aux_lit2.negate()])] +
                                            [ENFReductive(bindings.copy(), aux_lit2, old_binding, exp.negate(), True)])
                    else:
                        reduced_bindings = [var for var in bindings if var.name in arg_names_set]
                        aux_lit2 = create_auxiliary_literal(bindings)
                        aux_lit3 = create_auxiliary_literal(reduced_bindings)
                        return TemporaryENF(aux_lit, [ENFConjunctive(bindings.copy(), aux_lit, [aux_lit2.negate()])] +
                                            [ENFReductive(bindings.copy(), aux_lit2, old_binding, aux_lit3, True)] +
                                            [ENFConjunctive(reduced_bindings.copy(), aux_lit3, [exp.negate()])]) #??

        else:
            return [AssertLiteral(exp)]
            #if len(exp.atom.args) == 0:
            #    return [AssertLiteral(exp)]
            #else:
            #    aux_lit = create_auxiliary_literal(bindings)
            #    return [AssertLiteral(aux_lit)] + [ENFConjunctive(bindings, aux_lit, [exp])]
    if type(exp) == And_mul:
        literals = []
        enfs = []
        for subexp in exp.exp_list:
            temp_enf = derive_ENFs(subexp, bindings, True)
            literals.append(temp_enf.lit)
            enfs.extend(temp_enf.expressions)
        aux_lit = create_auxiliary_literal(bindings)
        if nested:
            return TemporaryENF(aux_lit ,enfs + [ENFConjunctive(bindings, aux_lit, literals)])
        else:
            return enfs + [ENFConjunctive(bindings, aux_lit, literals)] + [AssertLiteral(aux_lit)]
    if type(exp) == Or_mul:
        literals = []
        enfs = []
        for subexp in exp.exp_list:
            temp_enf = derive_ENFs(subexp, bindings, True)
            literals.append(temp_enf.lit)
            enfs.extend(temp_enf.expressions)
        aux_lit = create_auxiliary_literal(bindings)
        if nested:
            return TemporaryENF(aux_lit, enfs + [ENFDisjunctive(bindings, aux_lit, literals)])
        else:
            return enfs + [ENFDisjunctive(bindings, aux_lit, literals)] + [AssertLiteral(aux_lit)]
    if type(exp) == UniversalQuantifier:
        new_bindings = bindings.copy()
        new_bindings.extend(exp.var_list)
        subexp_enf = derive_ENFs(exp.subexp, new_bindings, True)
        if len(subexp_enf.expressions) == 0 or not subexp_enf.lit.pos:
            #var_names = {var.name for var in new_bindings}
            #arg_names = {arg.name for arg in subexp_enf.lit.atom.args}
            if not subexp_enf.lit.atom.name.startswith('_'):
                aux_lit1 = create_auxiliary_literal(bindings)
                aux_lit2 = create_auxiliary_literal(new_bindings)
                if nested:
                    return TemporaryENF(aux_lit1, subexp_enf.expressions + [ENFUniversal(bindings.copy(), aux_lit1, exp.var_list, aux_lit2)] + [ENFConjunctive(new_bindings.copy(), aux_lit2, [subexp_enf.lit])])
                else:
                    return subexp_enf.expressions + [ENFUniversal(bindings.copy(), aux_lit1, exp.var_list, aux_lit2)] + [ENFConjunctive(new_bindings.copy(), aux_lit2, [subexp_enf.lit])] + [AssertLiteral(aux_lit1)]
        aux_lit = create_auxiliary_literal(bindings)
        if nested:
            return TemporaryENF(aux_lit, subexp_enf.expressions + [ENFUniversal(bindings.copy(), aux_lit, exp.var_list, subexp_enf.lit)])
        else:
            return subexp_enf.expressions + [ENFUniversal(bindings.copy(), aux_lit, exp.var_list, subexp_enf.lit)] + [AssertLiteral(aux_lit)]

    if type(exp) == ExistentialQuantifier:
        new_bindings = bindings.copy()
        new_bindings.extend(exp.var_list)
        subexp_enf = derive_ENFs(exp.subexp, new_bindings, True)
        if len(subexp_enf.expressions) == 0 or not subexp_enf.lit.pos:
            #var_names = {var.name for var in new_bindings}
            #arg_names = {arg.name for arg in subexp_enf.lit.atom.args}
            if not subexp_enf.lit.atom.name.startswith('_'):
                aux_lit1 = create_auxiliary_literal(bindings)
                aux_lit2 = create_auxiliary_literal(new_bindings)
                if nested:
                    return TemporaryENF(aux_lit1, subexp_enf.expressions + [ENFExistential(bindings.copy(), aux_lit1, exp.var_list, aux_lit2)] + [ENFConjunctive(new_bindings.copy(), aux_lit2, [subexp_enf.lit])])
                else:
                    return subexp_enf.expressions + [ENFExistential(bindings.copy(), aux_lit1, exp.var_list, aux_lit2)] + [ENFConjunctive(new_bindings.copy(), aux_lit2, [subexp_enf.lit])] + [AssertLiteral(aux_lit1)]
        aux_lit = create_auxiliary_literal(bindings)
        if nested:
            return TemporaryENF(aux_lit, subexp_enf.expressions + [ENFExistential(bindings.copy(), aux_lit, exp.var_list, subexp_enf.lit)])
        else:
            return subexp_enf.expressions + [ENFExistential(bindings.copy(), aux_lit, exp.var_list, subexp_enf.lit)]


# Helper function creating a replacement literal starting with '_R[' to handle the same literal appearing multiple times in the same ENF rules.
# This was not necessary for the first method due to grounding.
def create_replacement_literal(old_literal, repl_count):
    args = []
    for arg in old_literal.atom.args:
        args.append(Term(arg.name))
    return Literal(Atom(f'_R[{old_literal.atom.name}[{repl_count}', args), old_literal.pos)

# Helper function substituting a literal with a replacement literal.
def substitute_literal(enf, pos, replacement_count):
    aux_lit = create_replacement_literal(enf.right[pos], replacement_count)
    t = type(enf)
    return t(enf.bindings, enf.left, enf.right[:pos] + [aux_lit] + enf.right[(pos+1):]), ENFConjunctive(enf.bindings, aux_lit, [enf.right[pos]])

# Function that replaces all duplicate predicates in an ENF-rule with replacements.
def remove_duplicate_predicates_from_ENF(enf):
    if type(enf) == ENFConjunctive or type(enf) == ENFDisjunctive:
        names = [enf.left.atom.name] + [lit.atom.name for lit in enf.right]
        if len(names) == len(set(names)):
            return [enf]
        seen = {enf.left.atom.name}
        new_enfs = []
        current_enf = enf
        replacement_count = 1
        for i, lit in enumerate(enf.right):
            if lit.atom.name in seen:
                substituted_enf, new_enf = substitute_literal(current_enf, i, replacement_count)
                current_enf = substituted_enf
                new_enfs.append(new_enf)
            seen.add(lit.atom.name)
            replacement_count += 1
        return [current_enf] + new_enfs
    return [enf]

# Helper function to get text between brackets when adding replacement predicates to the list of predicates.
def get_text_between_brackets(text):
    parts = text.split('[')
    return parts[1] if len(parts) > 2 else ''

# Helper function to add all auxiliary predicates that were generated in the ENF algorithm to the list of predicates.
# This step is necessary in the second method (unlike the first method).
# This is because we need to store all truth values for all predicates in a data structure (list of DataArrays) that allows for querying.
def get_new_predicates(enf_rule, predicates):
    predicate_dict = {pred.name : pred for pred in predicates}
    if type(enf_rule) == AssertLiteral:
        return None
    new_lit = enf_rule.left
    if new_lit.atom.name.startswith('_R'):
        corresponding_pred = predicate_dict[get_text_between_brackets(new_lit.atom.name)]
        return Predicate(new_lit.atom.name, corresponding_pred.argtypes)
    new_bind = {b.name : b.type for b in enf_rule.bindings}
    argtypes = [new_bind[arg.name] for arg in new_lit.atom.args]
    return Predicate(new_lit.atom.name, argtypes)







# Main function, which transforms each NNF-rule to ENF.
# It also adds the new auxiliary predicates to the list of predicates.
def transform_to_enf(rules, predicates):
    enf_rules = [derive_ENFs(rule, []) for rule in rules]
    enf_rules_flat = [item for sublist in enf_rules for item in sublist]
    enf_rules_no_dupl = [remove_duplicate_predicates_from_ENF(enf_rule) for enf_rule in
                         enf_rules_flat]
    enf_rules_no_dupl_flat = [item for sublist in enf_rules_no_dupl for item in sublist]

    new_preds = [get_new_predicates(enf_rule, predicates) for enf_rule in
                 enf_rules_no_dupl_flat]
    predicates.extend([new_pred for new_pred in new_preds if new_pred is not None])
    return enf_rules_flat, predicates
