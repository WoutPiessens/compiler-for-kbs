# This part of the compiler is responsible for parsing the input IDPZ3 program. It is identical to first_method_parsing.py
# It returns a ParsedIDPZ3Program object that contains all the essential information to continue with the next steps.

# To create a first abstract syntax tree, tree-sitter-fodot is used (https://gitlab.com/sli-lib/tree-sitter-fodot)
# Next, all the necessary information is extracted from this AST and converted to a ParsedIDPZ3Program object.

# More details about this part of the compiler can be found in the thesis text, in section 4.3.1.
# This code is the same as the first method, except for some small differences regarding interpreted predicates in a structure.

from tree_sitter import Language, Parser, Tree, Node

class ParsedIDPZ3Program:
    def __init__(self, types, predicates, functions, interpreted_predicates, rules):
        self.types = types
        self.predicates = predicates
        self.functions = functions
        self.interpreted_predicates = interpreted_predicates
        self.rules = rules

class Type:
    def __init__(self, name, domain):
        self.name = name
        self.domain = domain

class IntegerRange:
    def __init__(self, lb, ub):
        self.lb = lb
        self.ub = ub

class Predicate:
    def __init__(self, name, argtypes):
        self.name = name
        self.argtypes = argtypes.copy()

class PredicateInterpretation:
    def __init__(self, name, values):
        self.name = name
        self.values = values.copy()

class Function:
    def __init__(self, name, argtypes, scopetype):
        self.name = name
        self.argtypes = argtypes.copy()
        self.scopetype = scopetype

class FunctionInterpretation:
    def __init__(self, name, values):
        self.name = name
        self.values = values.copy()



class Exp:
    def __init__(self):
        pass


class Atom(Exp):
    def __init__(self, name, args=[]):
        self.name = name
        self.args = args

    def clone(self):
        return Atom(self.name)

    def equals(self, atom):
        return self.name == atom.name

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

class Term(Exp):
    def __init__(self, name):
        self.name = name
class Not(Exp):
    def __init__(self, exp):
        self.exp = exp


class And(Exp):
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2

class Or(Exp):
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2

class Implies(Exp):
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2

class Equivalent(Exp):
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2


class UniversalQuantifier(Exp):
    def __init__(self, var_list, subexp):
        self.var_list = var_list.copy()
        self.subexp = subexp

class ExistentialQuantifier(Exp):
    def __init__(self, var_list, subexp):
        self.var_list = var_list.copy()
        self.subexp = subexp

class Variable(Exp):
    def __init__(self, name, type):
        self.name = name
        self.type = type

# Helper function to get a subtree labeled with a given type from a given AST.
def get_subtree_from_tree(node, type, avoid_types=[]):
    if node.type == type:
        return node
    if node.type in avoid_types:
        return None
    else:
        return_list = []
        for child in node.children:
            return_list.append(get_subtree_from_tree(child, type, avoid_types))
        for elem in return_list:
            if isinstance(elem, Node):
                return elem
        return None

# Helper function to get all relevant children from an AST labeled with the given type(s).
def get_relevant_children(node, type="formula",type_list=[]):
    potential_rules = node.children
    rules = []
    if len(type_list) == 0:
        for potential_rule in potential_rules:
            if potential_rule.type == type:
                rules.append(potential_rule)
    else:
        for potential_rule in potential_rules:
            if potential_rule.type in type_list:
                rules.append(potential_rule)

    return rules

# Helper function to transform a type, function or predicate declaration in the vocabulary of an IDP program to a self-defined data type.
def transform_declaration(node):
    if node.type == "declaration":
        return transform_declaration(node.children[0])
    if node.type == "type_declaration":
        symbol_name = get_relevant_children(node, "symbol_name")[0]
        possible_symbol_interpretation = get_relevant_children(node, "symbol_interpretation")
        if len(possible_symbol_interpretation) == 0:
            return None
        else:
            symbol_interpretation = possible_symbol_interpretation[0]
            for child in symbol_interpretation.children:
                if child.type == "element_enumeration":
                    elements = get_relevant_children(child, "type_element")
                    element_names = set()
                    for elem in elements:
                        decoded_elem = elem.text.decode('utf-8')
                        if decoded_elem.isdigit():
                            element_names.add(int(decoded_elem))
                        else:
                            element_names.add(decoded_elem)
                    return Type(symbol_name.text.decode('utf-8'), element_names)
                if child.type == "range_enumeration":
                    elements = get_relevant_children(child, "type_element")
                    return Type(symbol_name.text.decode('utf-8'),
                                IntegerRange(int(elements[0].text.decode('utf-8')), int(elements[1].text.decode('utf-8'))))


    if node.type == "prop_declaration":
        symbol_name = get_relevant_children(node, "", ["symbol_name", "builtin_type"])[0]
        return Predicate(symbol_name.text.decode('utf-8'), [])

    if node.type == "predicate_declaration":
        symbol_names = get_relevant_children(node, "", ["symbol_name", "builtin_type"])
        decoded_names = []
        for symbol_name in symbol_names:
            decoded_names.append(symbol_name.text.decode('utf-8'))
        return Predicate(decoded_names[0], decoded_names[1:])

    if node.type == "constant_declaration":
        symbol_names = get_relevant_children(node, "", ["symbol_name", "builtin_type"])  #builtin_type!
        decoded_names = []
        for symbol_name in symbol_names:
            decoded_names.append(symbol_name.text.decode('utf-8'))
        return Function(decoded_names[0], [], decoded_names[-1])

    if node.type == "function_declaration":
        symbol_names = get_relevant_children(node, "",["symbol_name", "builtin_type"])
        decoded_names = []
        for symbol_name in symbol_names:
            decoded_names.append(symbol_name.text.decode('utf-8'))
        return Function(decoded_names[0], decoded_names[1:-1], decoded_names[-1])


# Helper function to transform a type, predicate or function interpretation in the structure of an IDP program to a self-defined data type.
def transform_interpretation(node):
    if node.type == "structure_interpretation":
        name = get_relevant_children(node, "symbol_name")[0].text.decode('utf-8')
        interpretation = get_relevant_children(node, "symbol_interpretation")[0]

        for child in interpretation.children:
            if child.type == "element_enumeration":
                elements = get_relevant_children(child, "type_element")
                element_names = set()
                for elem in elements:
                    decoded_elem = elem.text.decode('utf-8')
                    if decoded_elem.isdigit():
                        element_names.add(int(decoded_elem))
                    else:
                        element_names.add(decoded_elem)
                return Type(name, element_names)
            if child.type == "range_enumeration":
                elements = get_relevant_children(child, "type_element")
                return Type(name,
                            IntegerRange(int(elements[0].text.decode('utf-8')), int(elements[1].text.decode('utf-8'))))
            if child.type == "function_enumeration":
                elem_enum = get_relevant_children(child, "element_enumeration")
                results = get_relevant_children(child, "type_element")
                assignments = {}
                all_arg_names = []
                for i in range(len(elem_enum)):
                    arg = get_relevant_children(elem_enum[i], "type_element")
                    arg_names = []
                    for elem in arg:
                        arg_name = elem.text.decode('utf-8')
                        if arg_name.isdigit():
                            arg_names.append(int(arg_name))
                        else:
                            arg_names.append(arg_name)
                    all_arg_names.append(arg_names)
                for i in range(len(elem_enum)):
                    res = results[i].text.decode('utf-8')
                    if res.isdigit():
                        assignments[tuple(all_arg_names[i])] = int(res)
                    else:
                        assignments[tuple(all_arg_names[i])] = res

                return FunctionInterpretation(name, assignments)
            if child.type == "predicate_enumeration":
                elem_enum = get_relevant_children(child, "element_enumeration")

                all_arg_names = []
                for i in range(len(elem_enum)):
                    arg = get_relevant_children(elem_enum[i], "type_element")
                    arg_names = []
                    for elem in arg:
                        arg_name = elem.text.decode('utf-8')
                        if arg_name.isdigit():
                            arg_names.append(int(arg_name))
                        else:
                            arg_names.append(arg_name)
                    all_arg_names.append(tuple(arg_names))

                return PredicateInterpretation(name, all_arg_names)

    return None

# Helper function to transform a rule in the theory of an IDP program to a self-defined data type.
def transform_rule(node):
    if node.type == "symbol_name":
        return node.text.decode('utf-8')
    if node.type == "type_element":
        arg_name = node.text.decode('utf-8')
        if arg_name.isdigit():
            return Term(int(arg_name))
        else:
            return Term(arg_name)

    if node.type == "applied_symbol":
        children = get_relevant_children(node, "symbol_name")
        children_args = get_relevant_children(node, "formula")
        arguments = []
        if len(children_args) > 0:
            for child in children_args:
                arguments.append(transform_rule(child))
        return Atom(transform_rule(children[0]), arguments)
    if node.type == "formula":
        if len(node.children) > 1:
            children = get_relevant_children(node, "formula")
            return transform_rule(children[0])
        return transform_rule(node.children[0])
    if node.type == "neg":
        children = get_relevant_children(node)
        return Not(transform_rule(children[0]))
    if node.type == "land" or node.type == "rand":
        children = get_relevant_children(node)
        return And(transform_rule(children[0]), transform_rule(children[1]))
    if node.type == "lor" or node.type == "ror":
        children = get_relevant_children(node)
        return Or(transform_rule(children[0]), transform_rule(children[1]))
    if node.type == "limplication" or node.type == "rimplication":
        children = get_relevant_children(node)
        return Implies(transform_rule(children[0]), transform_rule(children[1]))
    if node.type == "equivalence":
        children = get_relevant_children(node)
        return Equivalent(transform_rule(children[0]), transform_rule(children[1]))
    if node.type == "le":
        children = get_relevant_children(node)
        return Atom("_LE", [transform_rule(children[0]), transform_rule(children[1])])
    if node.type == "leq":
        children = get_relevant_children(node)
        return Atom("_LEQ", [transform_rule(children[0]), transform_rule(children[1])])
    if node.type == "ge":
        children = get_relevant_children(node)
        return Atom("_GE", [transform_rule(children[0]), transform_rule(children[1])])
    if node.type == "geq":
        children = get_relevant_children(node)
        return Atom("_GEQ", [transform_rule(children[0]), transform_rule(children[1])])
    if node.type == "equality":
        children = get_relevant_children(node)
        return Atom(";EQ", [transform_rule(children[0]), transform_rule(children[1])])
    if node.type == 'inequality':
        children = get_relevant_children(node)
        return Atom("_NEQ", [transform_rule(children[0]), transform_rule(children[1])])

    if node.type == "universal":
        quantification = get_relevant_children(node, "quantification")[0]
        nested_formula = get_relevant_children(node, "formula")[0]
        variables = get_relevant_children(quantification, "variable")
        variable_range = get_relevant_children(quantification, "symbol_name")[0]
        variable_list = []
        for var in variables:
            variable_list.append(Variable(var.text.decode("utf-8"), variable_range.text.decode("utf-8")))
        return UniversalQuantifier(variable_list,
                                   transform_rule(nested_formula))
    if node.type == "existential":
        quantification = get_relevant_children(node, "quantification")[0]
        nested_formula = get_relevant_children(node, "formula")[0]
        variables = get_relevant_children(quantification, "variable")
        variable_range = get_relevant_children(quantification, "symbol_name")[0]
        variable_list = []
        for var in variables:
            variable_list.append(Variable(var.text.decode("utf-8"), variable_range.text.decode("utf-8")))
        return ExistentialQuantifier(variable_list,
                                   transform_rule(nested_formula))




# Helper function to transform the parse tree (generated by tree-sitter-fodot) for the vocabulary of the given IDP-program to a list of declarations.
def transform_vocabulary(parse_tree):
    transformed_declarations = []
    vocabulary = get_subtree_from_tree(parse_tree.root_node, "vocabulary", ["theory, structure"])
    if vocabulary is not None:
        declarations = get_relevant_children(vocabulary.next_named_sibling, "declaration")

        for decl in declarations:
            transformed_decl = transform_declaration(decl)
            if transformed_decl is not None:
                transformed_declarations.append(transformed_decl)

    return transformed_declarations

# Helper function to transform the parse tree (generated by tree-sitter-fodot) for the structure of the given IDP-program to a list of interpretations.
def transform_structure(parse_tree):
    transformed_interpretations = []
    structure = get_subtree_from_tree(parse_tree.root_node, "structure", ["vocabulary", "theory"])

    if structure is not None:
        interpretations = get_relevant_children(structure.next_named_sibling, "structure_interpretation")

        for interpretation in interpretations:
            transformed_interpretations.append(transform_interpretation(interpretation))
    return transformed_interpretations

# Helper function to transform the parse tree (generated by tree-sitter-fodot) for the theory of the given IDP-program to a list of rules.
def transform_theory(parse_tree):
    transformed_rules = []

    theory = get_subtree_from_tree(parse_tree.root_node, "theory", ["vocabulary", "structure"])
    if theory is not None:
        rules = get_relevant_children(theory.next_named_sibling)

        for rule in rules:
            transformed_rules.append(transform_rule(rule))
    return transformed_rules


# Helper function to create a list of Term objects.
def make_into_terms(li):
    new_li = []
    for elem in li:
        new_li.append(Term(elem))
    return new_li


# Function that turns interpretations in a structure into rules in a theory.
def get_structure_rules(interpretation):
    structure_rules = []
    if type(interpretation) == FunctionInterpretation:
        for key, val in interpretation.values.items():
            structure_rules.append(Atom(";p;" + interpretation.name, make_into_terms(list(key) + [val])))
    if type(interpretation) == PredicateInterpretation:
        for t in interpretation.values:
            structure_rules.append(Atom(interpretation.name, make_into_terms(list(t))))
    return structure_rules



# This function first parses the input IDP program using tree-sitter-fodot.
# Next, the vocabulary, the structure, and the theory of the IDP program are separately transformed into self-defined data types.
# This is done in a way so that only the essential information is preserved:
#  - types, with their domain
#  - predicates, with their type signature
#  - functions, with their type signature
#  - total interpretations of predicates/functions in a structure
#  - rules, containing predicates/functions with all their arguments
# The function returns a ParsedIDPZ3Program object that contains all this information.

def parse(idp_program):
    Language.build_library(
        'build/fodot.so',
        ['./tree-sitter-fodot/']
    )

    FODOT = Language('./build/fodot.so', 'fodot')

    parser = Parser()
    parser.set_language(FODOT)
    original_parse_tree = parser.parse(bytes(idp_program, 'utf8'))

    transformed_declarations = transform_vocabulary(original_parse_tree)

    types = []
    predicates = []
    functions = []
    for tdecl in transformed_declarations:
        if isinstance(tdecl, Type):
            types.append(tdecl)
        elif isinstance(tdecl, Predicate):
            predicates.append(tdecl)
        elif isinstance(tdecl, Function):
            functions.append(tdecl)
            predicates.append(Predicate(';p;' + tdecl.name, tdecl.argtypes + [tdecl.scopetype]))

    transformed_interpretations = transform_structure(original_parse_tree)

    structure_rules = []
    interpreted_predicates = set()

    for transformed_interp in transformed_interpretations:
        if type(transformed_interp) == Type:
            types.append(transformed_interp)
        else:
            structure_rules.extend(get_structure_rules(transformed_interp))
            if type(transformed_interp) == PredicateInterpretation:
                interpreted_predicates.add(transformed_interp.name)
            elif type(transformed_interp) == FunctionInterpretation:
                interpreted_predicates.add(';p;' + transformed_interp.name)

    transformed_rules = transform_theory(original_parse_tree)
    transformed_rules.extend(structure_rules)


    return ParsedIDPZ3Program(types, predicates, functions, interpreted_predicates, transformed_rules)

