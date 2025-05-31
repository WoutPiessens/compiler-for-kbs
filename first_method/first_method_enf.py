# This part of the compiler is responsible for converting Negation Normal Form-rules to Equivalence Normal Form-rules.
# This transformation is based on the work of Wittocx. et. al.
# (Wittocx, J., Denecker, M., Bruynooghe, M. 2012. Constraint propagation for first-order logic and inductive definitions ACM Trans. Comput. Logic V, N, Article A (January 2012), 44 pages.)
# In short: subexpressions are substituted for auxiliary variables in a recursive way.
# This results in a list of ENF-expressions for every NNF-expression.
# There are 5 types of ENF-expressions, as described in the thesis text (section 4.3.4.).

# More details about this part of the compiler can be found in the thesis text, in section 4.3.4.


from first_method_parsing import Term, Atom, UniversalQuantifier, ExistentialQuantifier
from first_method_nnf import Literal, And_mul, Or_mul

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

# Represents the result of a recursive call to the derive_ENFs function:
# - the literal representing the subexpression on which derive_ENFs was called
# - and the current ENF-rules that have been derived
class TemporaryENF:
    def __init__(self, lit, expressions):
        self.lit = lit
        self.expressions = expressions.copy()


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
            return TemporaryENF(exp, [])
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
            var_names = {var.name for var in new_bindings}
            arg_names = {arg.name for arg in subexp_enf.lit.atom.args}
            if not subexp_enf.lit.pos or var_names != arg_names:
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
            var_names = {var.name for var in new_bindings}
            arg_names = {arg.name for arg in subexp_enf.lit.atom.args}
            if not subexp_enf.lit.pos or var_names != arg_names:
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


# Main function, which transforms each NNF-rule to ENF.
def transform_to_enf(rules):
    enf_rules = [derive_ENFs(rule, []) for rule in rules]
    enf_rules_flat = [item for sublist in enf_rules for item in sublist]
    return enf_rules_flat

