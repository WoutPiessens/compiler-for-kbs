# This part of the compiler is responsible for transforming functions into predicates in an equivalence-preserving way.
# This happens as described in Wittocx et. al.
# (Wittocx, J., Denecker, M., Bruynooghe, M. 2012. Constraint propagation for first-order logic and inductive definitions ACM Trans. Comput. Logic V, N, Article A (January 2012), 44 pages.)

# Nested functions are rewritten through iterated application of the following rewrite rule:
# P (..., f(t), ...) −→ ∀x(f(t) = x ⇒ P (..., x, ...))
#
# Moreover, all atoms of the form f(x) = y are replaced by P(x,y).

# More details about this part of the compiler can be found in the thesis text, in section 4.3.2.
# This part is identical in the second method, except that the following sentences are not added to the theory:
# # ∀x: ∃y: P(x, y)
# # ∀x: ∀y1: ∀y2: (P(x, y1) ∧ P(x, y2) ⇒ y1 = y2)
# The alternative for adding these rules is adding function propagators (in a later step), this is discussed in section 4.4.3.4.


from second_method_parsing import Equivalent, Implies, And, Or, Not, UniversalQuantifier, ExistentialQuantifier, Atom, Term, Variable

# Helper function to find the predicate corresponding to a certain name.
# This is done in order to get relevant information regarding the type signature.
def get_predicate(exp, predicates):
    for pred in predicates:
        if pred.name == exp.name or ';p;' + pred.name == exp.name or ';p;' + exp.name == pred.name:
            return pred
    return None

# Helper function that constructs variables with their domain types from a predicate.
# Used for constructing universal quantifiers to substitute nested functions.
def construct_variables(pred, new_vars):
    var_list = []
    for i in range(len(new_vars)):
        if new_vars[i] != None:
            #if func == None:
            #    var_list.append(Variable(new_vars[i], None))
            if pred != None:
                var_list.append(Variable(new_vars[i], pred.argtypes[i]))

    return var_list

# Helper function to construct the arguments to a predicate (that was previously a function).
# This is done in such a way that nested functions are substituted by new variables.
def construct_arguments(exp, new_vars):
    new_args = []
    for i in range(len(exp.args)):
        if new_vars[i] == None:
            new_args.append(exp.args[i])
        else:
            new_args.append(Term(new_vars[i]))
    return new_args

# Helper function to construct the necessary conditions for the following substitution
# P (..., f(t), ...) −→ ∀x(f(t) = x ⇒ P (..., x, ...))
def construct_condition(args):

    if len(args) == 0:
        return None
    if len(args) == 1:
        return args[0]
    if len(args) == 2:
        return And(args[0], args[1])
    else:
        return And(args[0], construct_condition(args[1:]))


class TemporarySubexpression:
    def __init__(self, result, substituted_var):
        self.result = result
        self.substituted_var = substituted_var


# Main function transformation function, rewriting nested functions and substituting all functions with predicates.
function_count = 0
def function_transformer(exp, predicates, inside_function=False):
    global function_count
    if type(exp) == Implies:
        return Implies(function_transformer(exp.exp1, predicates), function_transformer(exp.exp2, predicates))
    elif type(exp) == Equivalent:
        return Equivalent(function_transformer(exp.exp1, predicates), function_transformer(exp.exp2, predicates))
    elif type(exp) == And:
        return And(function_transformer(exp.exp1, predicates), function_transformer(exp.exp2, predicates))
    elif type(exp) == Or:
        return Or(function_transformer(exp.exp1, predicates), function_transformer(exp.exp2, predicates))
    elif type(exp) == Not:
        return Not(function_transformer(exp.exp, predicates))

    elif type(exp) == UniversalQuantifier:
        return UniversalQuantifier(exp.var_list, function_transformer(exp.subexp, predicates))
    elif type(exp) == ExistentialQuantifier:
        return ExistentialQuantifier(exp.var_list, function_transformer(exp.subexp, predicates))

    elif type(exp) == Term:
        return TemporarySubexpression(exp, None)
    elif type(exp) == Atom:
        if not inside_function and all(type(arg) != Atom for arg in exp.args):
            return exp
        if exp.name == ";EQ":
            left = exp.args[0]
            right = exp.args[1]
            return function_transformer(Atom(";p;" + left.name, left.args + [right]), predicates, inside_function)
        new_args = []
        new_vars_in_arg = []
        for arg in exp.args:
            transformed_subexpression = function_transformer(arg, predicates, inside_function=True)
            new_args.append(transformed_subexpression.result)
            new_vars_in_arg.append(transformed_subexpression.substituted_var)

        func = get_predicate(exp, predicates)
        variables = construct_variables(func, new_vars_in_arg)
        arguments = construct_arguments(exp, new_vars_in_arg)
        true_args = []
        for arg in new_args:
            if type(arg) != Term:
                true_args.append(arg)
        condition = construct_condition(true_args)

        if inside_function:
            function_count = function_count + 1
            if condition == None:
                return TemporarySubexpression(Atom(";p;" + exp.name, arguments + [Term(f"_q{function_count}")]), f"_q{function_count}")
            else:
                return TemporarySubexpression(UniversalQuantifier(variables,
                                           Implies(condition, Atom(";p;" + exp.name, arguments + [Term(f"_q{function_count}")]))), f"_q{function_count}")
        else:
            return UniversalQuantifier(variables,
                                       Implies(condition, Atom(exp.name, arguments)))


    else:
        raise Exception("type unrecognized")


# Function for adding the new sentences:
# ∀x: ∃y: P(x, y)
# ∀x: ∀y1: ∀y2: (P(x, y1) ∧ P(x, y2) ⇒ y1 = y2)
# They express the property that for every x in the domain, there is exactly one y so that f(x) = y.
# For every function, these rules are added to the corresponding predicates.
# This function is not used by default in the second method.
'''def add_new_function_rules(functions):
    new_function_rules = []

    for func in functions:
        name = func.name
        c = 0
        argument_variables = []
        terms = []
        for argtype in func.argtypes:
            c = c + 1
            argument_variables.append(Variable(f"_Y{c}", argtype))
            terms.append(Term(f"_Y{c}"))

        scope_variable = Variable(f"_Z", func.scopetype)


        scope_variable1 = Variable(f"_Z1", func.scopetype)
        scope_variable2 = Variable(f"_Z2", func.scopetype)

        rule1 = UniversalQuantifier(argument_variables, ExistentialQuantifier([scope_variable],
                                                                              Atom(";p;" + name, terms + [Term(f"_Z")])))
        rule2 = UniversalQuantifier(argument_variables + [scope_variable1] + [scope_variable2],
                                    Implies(And(Atom(";p;" + name, terms + [Term(f"_Z1")]),
                                                Atom(";p;" + name, terms + [Term(f"_Z2")])),
                                            Atom(";EQ", [Term(f"_Z1"), Term(f"_Z2")])))
        new_function_rules.append(rule1)
        new_function_rules.append(rule2)
    return new_function_rules'''


# Main function, calling the functions implementing the function transformation.
def transform_functions(rules, functions, predicates):
    new_rules = [function_transformer(rule, predicates) for rule in rules]
    #new_rules.extend(add_new_function_rules(functions))
    return new_rules
