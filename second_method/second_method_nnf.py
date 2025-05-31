# This part of the compiler is responsible for converting rules in FO(.) to Negation Normal Form.
# This means:
#   - Logical implications and equivalences are rewritten in function of logical conjunctions and disjunctions
#   - Logical negations can only appear in front of an atom
# Additionally, I perform the following steps on the FO(.)-rules:
#   - Joining multiple quantifiers into one quantifier where possible (this will save auxiliary variables in a later step)
#   - Joining multiple logical conjunctions/disjunctions into one where possible (analogously)

# More details about this part of the compiler can be found in the thesis text, in section 4.3.3.
# This part is identical in the second method.



from second_method.second_method_parsing import Exp, Equivalent, Implies, And, Or, Not, UniversalQuantifier, ExistentialQuantifier, Atom, Term, Variable


class Literal(Exp):
    def __init__(self, atom, pos):
        self.atom = atom
        self.pos = pos

    def clone(self):
        return Literal(self.atom, self.pos)
    def negate(self):
        return Literal(self.atom, not self.pos)

    def equals(self, lit):
        return self.atom == lit.atom and self.pos == lit.pos

    def __eq__(self, other):
        if isinstance(other, Literal):
            return self.atom == other.atom and self.pos == other.pos
        return False

    def __hash__(self):
        return hash(self.atom)

class And_mul(Exp):
    def __init__(self, exp_list):
        self.exp_list = exp_list.copy()


class Or_mul(Exp):
    def __init__(self, exp_list):
        self.exp_list = exp_list.copy()

# Rewrites logical implication and equivalence in function of logical conjunction and disjunction
# A => B is equivalent with ~A ∨ B
# A <=> B is equivalent with (~A ∨ B) ∧ (~B ∨ A)
def impl_and_eq_transformer(exp):
    if type(exp) == Implies:
        return Or(Not(impl_and_eq_transformer(exp.exp1)), impl_and_eq_transformer(exp.exp2))
    elif type(exp) == Equivalent:
        return And(Or(Not(impl_and_eq_transformer(exp.exp1)), impl_and_eq_transformer(exp.exp2)), Or(Not(impl_and_eq_transformer(exp.exp2)), impl_and_eq_transformer(exp.exp1)))
    elif type(exp) == And:
        return And(impl_and_eq_transformer(exp.exp1), impl_and_eq_transformer(exp.exp2))
    elif type(exp) == Or:
        return Or(impl_and_eq_transformer(exp.exp1), impl_and_eq_transformer(exp.exp2))
    elif type(exp) == Not:
        return Not(impl_and_eq_transformer(exp.exp))
    elif type(exp) == Atom:
        return exp
    elif type(exp) == UniversalQuantifier:
        return UniversalQuantifier(exp.var_list, impl_and_eq_transformer(exp.subexp))
    elif type(exp) == ExistentialQuantifier:
        return ExistentialQuantifier(exp.var_list, impl_and_eq_transformer(exp.subexp))
    else:
        print(type(exp))
        raise Exception("type unrecognized")

# Pushes negations inside the logical expression, following De Morgan's laws
# ~(A ∧ B) is equivalent with ~A ∨ ~B
# ~(A ∨ B) is equivalent with ~A ∧ ~B
def negation_push_transformer(exp, active=False):
    if type(exp) == And:
        if active:
            return Or(negation_push_transformer(exp.exp1, active), negation_push_transformer(exp.exp2, active))
        else:
            return And(negation_push_transformer(exp.exp1, active), negation_push_transformer(exp.exp2, active))
    elif type(exp) == Or:
        if active:
            return And(negation_push_transformer(exp.exp1, active), negation_push_transformer(exp.exp2, active))
        else:
            return Or(negation_push_transformer(exp.exp1, active), negation_push_transformer(exp.exp2, active))
    elif type(exp) == Not:
        return negation_push_transformer(exp.exp, not active)
    elif type(exp) == Atom:
        if active:
            if exp.name in ["_LE", "_LEQ", "_GE", "_GEQ", ";EQ", "_NEQ"]:
                equation_negate_map = {";EQ" : "_NEQ", "_NEQ" : ";EQ", "_LE" : "_GEQ", "_LEQ" : "_GE",
                                       "_GE" : "_LEQ", "_GEQ" : "_LE"}
                return Literal(Atom(equation_negate_map[exp.name], exp.args.copy()), True)
            return Literal(exp, False)
        else:
            return Literal(exp, True)
    elif type(exp) == UniversalQuantifier:
        if active:
            return ExistentialQuantifier(exp.var_list, negation_push_transformer(exp.subexp, active))
        else:
            return UniversalQuantifier(exp.var_list, negation_push_transformer(exp.subexp, active))

    elif type(exp) == ExistentialQuantifier:
        if active:
            return UniversalQuantifier(exp.var_list, negation_push_transformer(exp.subexp, active))
        else:
            return ExistentialQuantifier(exp.var_list, negation_push_transformer(exp.subexp, active))
    else:
        raise Exception("type unrecognized")



# Groups quantifiers together where possible
# It is only possible to group two quantifiers together when they are the same type
# e.g. !x in {1,2,3}, !y in {1,2,3}: A(x,y) can become !x,y in {1,2,3}: A(x,y)
# but, !x in {1,2,3}, ?y in {1,2,3}: A(x,y) cannot be transformed, because the order of the quantifiers matters
def quantifier_transformer(exp):
    if type(exp) == Literal:
        return exp
    if type(exp) == And:
        return And(quantifier_transformer(exp.exp1), quantifier_transformer(exp.exp2))
    if type(exp) == Or:
        return Or(quantifier_transformer(exp.exp1), quantifier_transformer(exp.exp2))
    if type(exp) == UniversalQuantifier:
        current_exp = exp
        var_list = []
        while type(current_exp) == UniversalQuantifier:
            var_list.extend(current_exp.var_list)
            current_exp = current_exp.subexp
        return UniversalQuantifier(var_list, quantifier_transformer(current_exp))
    if type(exp) == ExistentialQuantifier:
        current_exp = exp
        var_list = []
        while type(current_exp) == ExistentialQuantifier:
            var_list.extend(current_exp.var_list)
            current_exp = current_exp.subexp
        return ExistentialQuantifier(var_list, quantifier_transformer(current_exp))


# Helper function for and_or_transformer(), retrieving all the arguments of a logical conjunction or disjunction (possibly nested)
def and_or_auxiliary(exp, t):
    args = []
    first_exp = exp.exp1
    second_exp = exp.exp2
    if type(first_exp) == t:
        args.extend(and_or_auxiliary(first_exp, t))
    else:
        args.append(first_exp)
    if type(second_exp) == t:
        args.extend(and_or_auxiliary(second_exp, t))
    else:
        args.append(second_exp)
    return args


# Transforms binary logical ∧ and ∨ into equivalent operators that can take multiple operands (where possible)
def and_or_transformer(exp):
    if type(exp) == Literal:
        return exp
    if type(exp) == UniversalQuantifier:
        return UniversalQuantifier(exp.var_list, and_or_transformer(exp.subexp))
    if type(exp) == ExistentialQuantifier:
        return ExistentialQuantifier(exp.var_list, and_or_transformer(exp.subexp))
    if type(exp) == And:
        args = and_or_auxiliary(exp, And)
        evaluated_args = [and_or_transformer(arg) for arg in args]
        return And_mul(evaluated_args)
    if type(exp) == Or:
        args = and_or_auxiliary(exp, Or)
        evaluated_args = [and_or_transformer(arg) for arg in args]
        return Or_mul(evaluated_args)

# This function goes through all the steps to transform an FO(.)-rule to NNF.
def pipeline(rule):
    transformed_rule1 = impl_and_eq_transformer(rule)
    transformed_rule2 = negation_push_transformer(transformed_rule1)
    transformed_rule3 = quantifier_transformer(transformed_rule2)
    transformed_rule4 = and_or_transformer(transformed_rule3)
    return transformed_rule4

# Main function, calling the pipeline() function on every rule
def transform_to_nnf(rules):
    return [pipeline(rule) for rule in rules]
