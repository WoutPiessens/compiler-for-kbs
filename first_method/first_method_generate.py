# This part of the compiler builds up an abstract syntax tree, using:
# - all the propagators that were derived
# - the names of all the grounded atoms
# - abstract syntax trees of helper functions or functions that implement functionality such as an interactive application
# When the full AST is generated, it is converted to Python-code using astunparse.

# More details about this part of the compiler can be found in the thesis text, in section 4.3.8.

import ast
import time
from enum import Enum

import astunparse

from first_method_enf import ENFConjunctive, ENFDisjunctive, AssertLiteral, Literal




class Operator(Enum):
    EQ = 1
    NEQ = 2
    LEQ = 3
    LT = 4
    GEQ = 5
    GT = 6


# AST for a helper function

def generate_dash_imports():
    return ast.ImportFrom(
         module='dash',
         names=[
            ast.alias(name='Dash'),
            ast.alias(name='html'),
            ast.alias(name='dcc'),
            ast.alias(name='State'),
            ast.alias(name='Input'),
            ast.alias(name='Output'),
            ast.alias(name='ALL'),
            ast.alias(name='callback_context')],
         level=0)

# Helper function to create an AST for a set of values.
def derive_syntax_tree_for_set(set_of_values):
    elements = []
    for elem in set_of_values:
        elements.append(ast.Constant(value=elem))
    return elements

# Function that creates the initial 'structure' data structure, representing all grounded atoms and their truth values.
def generate_initial_structure(enf_rules, domain_rules, name='structure'):
    set_of_bool_var = set()

    for enf_rule in enf_rules:
        if type(enf_rule) == ENFDisjunctive or type(enf_rule) == ENFConjunctive:
            set_of_bool_var.add(enf_rule.left.atom)
            for exp in enf_rule.right:
                if type(exp) == Literal:
                    set_of_bool_var.add(exp.atom)

        else:
             if type(enf_rule.literal) == Literal:
                 set_of_bool_var.add(enf_rule.literal.atom)

    list_of_atoms = []
    for atom in set_of_bool_var:
        list_of_atoms.append(ast.Constant(value=atom))
    list_of_values = []
    for i in range(len(set_of_bool_var)):
        list_of_values.append(ast.Set(
                  elts=[
                     ast.Constant(value=True),
                     ast.Constant(value=False)]))

    for key in domain_rules.keys():
        list_of_atoms.append(ast.Constant(value=key))
        list_of_values.append(ast.Set(elts=derive_syntax_tree_for_set(domain_rules[key])))




    return ast.Assign(
         targets=[
            ast.Name(id=name, ctx=ast.Store())],
         value=ast.Dict(
            keys=list_of_atoms,
            values=list_of_values))



# Generates AST for a helper function
def generate_update_structure():
    return ast.FunctionDef(
        name='update_structure',
        args=ast.arguments(
            posonlyargs=[],
            args=[
                ast.arg(arg='changes')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
        body=[
            ast.For(
                target=ast.Tuple(
                    elts=[
                        ast.Name(id='key', ctx=ast.Store()),
                        ast.Name(id='value', ctx=ast.Store())],
                    ctx=ast.Store()),
                iter=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id='changes', ctx=ast.Load()),
                        attr='items',
                        ctx=ast.Load()),
                    args=[],
                    keywords=[]),
                body=[
                    ast.Assign(
                        targets=[
                            ast.Subscript(
                                value=ast.Name(id='structure', ctx=ast.Load()),
                                slice=ast.Name(id='key', ctx=ast.Load()),
                                ctx=ast.Store())],
                        value=ast.Name(id='value', ctx=ast.Load()))],
                orelse=[])],
        decorator_list=[])

# Generates AST for a helper function
def generate_handle_reset():
    return ast.FunctionDef(
         name='handle_reset',
         args=ast.arguments(
            posonlyargs=[],
            args=[],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            ast.For(
               target=ast.Tuple(
                  elts=[
                     ast.Name(id='key', ctx=ast.Store()),
                     ast.Name(id='value', ctx=ast.Store())],
                  ctx=ast.Store()),
               iter=ast.Call(
                  func=ast.Attribute(
                     value=ast.Name(id='initial_structure', ctx=ast.Load()),
                     attr='items',
                     ctx=ast.Load()),
                  args=[],
                  keywords=[]),
               body=[
                  ast.Assign(
                     targets=[
                        ast.Subscript(
                           value=ast.Name(id='structure', ctx=ast.Load()),
                           slice=ast.Name(id='key', ctx=ast.Load()),
                           ctx=ast.Store())],
                     value=ast.Subscript(
                        value=ast.Name(id='initial_structure', ctx=ast.Load()),
                        slice=ast.Name(id='key', ctx=ast.Load()),
                        ctx=ast.Load()))],
               orelse=[])],
         decorator_list=[])

# Generates AST for a helper function
def generate_print_structure():
    return ast.FunctionDef(
         name='print_structure',
         args=ast.arguments(
            posonlyargs=[],
            args=[],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            ast.For(
               target=ast.Name(id='key', ctx=ast.Store()),
               iter=ast.Call(
                  func=ast.Attribute(
                     value=ast.Name(id='structure', ctx=ast.Load()),
                     attr='keys',
                     ctx=ast.Load()),
                  args=[],
                  keywords=[]),
               body=[
                  ast.If(
                     test=ast.UnaryOp(
                        op=ast.Not(),
                        operand=ast.Call(
                           func=ast.Attribute(
                              value=ast.Name(id='key', ctx=ast.Load()),
                              attr='startswith',
                              ctx=ast.Load()),
                           args=[
                              ast.Constant(value='_')],
                           keywords=[])),
                     body=[
                        ast.Expr(
                           value=ast.Call(
                              func=ast.Name(id='print', ctx=ast.Load()),
                              args=[
                                 ast.Name(id='key', ctx=ast.Load())],
                              keywords=[
                                 ast.keyword(
                                    arg='end',
                                    value=ast.Constant(value=''))])),
                        ast.Expr(
                           value=ast.Call(
                              func=ast.Name(id='print', ctx=ast.Load()),
                              args=[
                                 ast.Constant(value=':  ')],
                              keywords=[
                                 ast.keyword(
                                    arg='end',
                                    value=ast.Constant(value=''))])),
                        ast.Expr(
                           value=ast.Call(
                              func=ast.Name(id='print', ctx=ast.Load()),
                              args=[
                                 ast.Subscript(
                                    value=ast.Name(id='structure', ctx=ast.Load()),
                                    slice=ast.Name(id='key', ctx=ast.Load()),
                                    ctx=ast.Load())],
                              keywords=[])),
                        ast.Expr(
                           value=ast.Call(
                              func=ast.Name(id='print', ctx=ast.Load()),
                              args=[],
                              keywords=[]))],
                     orelse=[])],
               orelse=[])],
         decorator_list=[])

# Generates AST for a helper function
def generate_check_unsat_fields():
    return ast.FunctionDef(
         name='check_unsat_fields',
         args=ast.arguments(
            posonlyargs=[],
            args=[
               ast.arg(arg='changes')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            ast.Assign(
               targets=[
                  ast.Name(id='unsat_fields', ctx=ast.Store())],
               value=ast.Call(
                  func=ast.Name(id='set', ctx=ast.Load()),
                  args=[],
                  keywords=[])),
            ast.For(
               target=ast.Name(id='key', ctx=ast.Store()),
               iter=ast.Call(
                  func=ast.Attribute(
                     value=ast.Name(id='changes', ctx=ast.Load()),
                     attr='keys',
                     ctx=ast.Load()),
                  args=[],
                  keywords=[]),
               body=[
                  ast.If(
                     test=ast.Compare(
                        left=ast.Call(
                           func=ast.Name(id='len', ctx=ast.Load()),
                           args=[
                              ast.Subscript(
                                 value=ast.Name(id='changes', ctx=ast.Load()),
                                 slice=ast.Name(id='key', ctx=ast.Load()),
                                 ctx=ast.Load())],
                           keywords=[]),
                        ops=[
                           ast.Eq()],
                        comparators=[
                           ast.Constant(value=0)]),
                     body=[
                        ast.Expr(
                           value=ast.Call(
                              func=ast.Attribute(
                                 value=ast.Name(id='unsat_fields', ctx=ast.Load()),
                                 attr='add',
                                 ctx=ast.Load()),
                              args=[
                                 ast.Name(id='key', ctx=ast.Load())],
                              keywords=[]))],
                     orelse=[])],
               orelse=[]),
            ast.Return(
               value=ast.Name(id='unsat_fields', ctx=ast.Load()))],
         decorator_list=[])

# Generates AST for a helper function
def generate_intersect_changes():
    return ast.FunctionDef(
         name='intersect_changes',
         args=ast.arguments(
            posonlyargs=[],
            args=[
               ast.arg(arg='changes')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            ast.Assign(
               targets=[
                  ast.Name(id='intersected_changes', ctx=ast.Store())],
               value=ast.Dict(keys=[], values=[])),
            ast.For(
               target=ast.Name(id='key', ctx=ast.Store()),
               iter=ast.Call(
                  func=ast.Attribute(
                     value=ast.Name(id='changes', ctx=ast.Load()),
                     attr='keys',
                     ctx=ast.Load()),
                  args=[],
                  keywords=[]),
               body=[
                  ast.If(
                     test=ast.Compare(
                        left=ast.Call(
                           func=ast.Name(id='len', ctx=ast.Load()),
                           args=[
                              ast.Subscript(
                                 value=ast.Name(id='changes', ctx=ast.Load()),
                                 slice=ast.Name(id='key', ctx=ast.Load()),
                                 ctx=ast.Load())],
                           keywords=[]),
                        ops=[
                           ast.Gt()],
                        comparators=[
                           ast.Constant(value=0)]),
                     body=[
                        ast.Assign(
                           targets=[
                              ast.Subscript(
                                 value=ast.Name(id='intersected_changes', ctx=ast.Load()),
                                 slice=ast.Name(id='key', ctx=ast.Load()),
                                 ctx=ast.Store())],
                           value=ast.Call(
                              func=ast.Attribute(
                                 value=ast.Subscript(
                                    value=ast.Name(id='changes', ctx=ast.Load()),
                                    slice=ast.Name(id='key', ctx=ast.Load()),
                                    ctx=ast.Load()),
                                 attr='pop',
                                 ctx=ast.Load()),
                              args=[],
                              keywords=[])),
                        ast.While(
                           test=ast.Compare(
                              left=ast.Call(
                                 func=ast.Name(id='len', ctx=ast.Load()),
                                 args=[
                                    ast.Subscript(
                                       value=ast.Name(id='changes', ctx=ast.Load()),
                                       slice=ast.Name(id='key', ctx=ast.Load()),
                                       ctx=ast.Load())],
                                 keywords=[]),
                              ops=[
                                 ast.Gt()],
                              comparators=[
                                 ast.Constant(value=0)]),
                           body=[
                              ast.Assign(
                                 targets=[
                                    ast.Subscript(
                                       value=ast.Name(id='intersected_changes', ctx=ast.Load()),
                                       slice=ast.Name(id='key', ctx=ast.Load()),
                                       ctx=ast.Store())],
                                 value=ast.Call(
                                    func=ast.Attribute(
                                       value=ast.Subscript(
                                          value=ast.Name(id='intersected_changes', ctx=ast.Load()),
                                          slice=ast.Name(id='key', ctx=ast.Load()),
                                          ctx=ast.Load()),
                                       attr='intersection',
                                       ctx=ast.Load()),
                                    args=[
                                       ast.Call(
                                          func=ast.Attribute(
                                             value=ast.Subscript(
                                                value=ast.Name(id='changes', ctx=ast.Load()),
                                                slice=ast.Name(id='key', ctx=ast.Load()),
                                                ctx=ast.Load()),
                                             attr='pop',
                                             ctx=ast.Load()),
                                          args=[],
                                          keywords=[])],
                                    keywords=[]))],
                           orelse=[]),
                        ast.If(
                           test=ast.Compare(
                              left=ast.Subscript(
                                 value=ast.Name(id='intersected_changes', ctx=ast.Load()),
                                 slice=ast.Name(id='key', ctx=ast.Load()),
                                 ctx=ast.Load()),
                              ops=[
                                 ast.Eq()],
                              comparators=[
                                 ast.Subscript(
                                    value=ast.Name(id='structure', ctx=ast.Load()),
                                    slice=ast.Name(id='key', ctx=ast.Load()),
                                    ctx=ast.Load())]),
                           body=[
                              ast.Delete(
                                 targets=[
                                    ast.Subscript(
                                       value=ast.Name(id='intersected_changes', ctx=ast.Load()),
                                       slice=ast.Name(id='key', ctx=ast.Load()),
                                       ctx=ast.Del())])],
                           orelse=[])],
                     orelse=[])],
               orelse=[]),
            ast.Return(
               value=ast.Name(id='intersected_changes', ctx=ast.Load()))],
         decorator_list=[])

# Generates AST for a helper function
def generate_feedback_loop_with_contradiction_check():
    return ast.Module(
   body=[
      ast.Assign(
         targets=[
            ast.Name(id='quit', ctx=ast.Store())],
         value=ast.Constant(value=False)),
      ast.Assign(
         targets=[
            ast.Name(id='unsat_fields', ctx=ast.Store())],
         value=ast.Call(
            func=ast.Name(id='propagation_loop', ctx=ast.Load()),
            args=[
               ast.Name(id='structure', ctx=ast.Load())],
            keywords=[])),
      ast.If(
         test=ast.Compare(
            left=ast.Call(
               func=ast.Name(id='len', ctx=ast.Load()),
               args=[
                  ast.Name(id='unsat_fields', ctx=ast.Load())],
               keywords=[]),
            ops=[
               ast.Gt()],
            comparators=[
               ast.Constant(value=0)]),
         body=[
            ast.Expr(
               value=ast.Call(
                  func=ast.Name(id='print', ctx=ast.Load()),
                  args=[
                     ast.Constant(value='The initial problem is unsatisfiable: in particular, the following fields are unsatisfiable')],
                  keywords=[])),
            ast.For(
               target=ast.Name(id='field', ctx=ast.Store()),
               iter=ast.Name(id='unsat_fields', ctx=ast.Load()),
               body=[
                  ast.Expr(
                     value=ast.Call(
                        func=ast.Name(id='print', ctx=ast.Load()),
                        args=[
                           ast.Name(id='field', ctx=ast.Load())],
                        keywords=[]))],
               orelse=[]),
            ast.Assign(
               targets=[
                  ast.Name(id='quit', ctx=ast.Store())],
               value=ast.Constant(value=True))],
         orelse=[
            ast.Expr(
               value=ast.Call(
                  func=ast.Name(id='print', ctx=ast.Load()),
                  args=[
                     ast.Constant(value='Initial domains')],
                  keywords=[])),
            ast.Expr(
               value=ast.Call(
                  func=ast.Name(id='print_structure', ctx=ast.Load()),
                  args=[],
                  keywords=[]))]),
      ast.While(
         test=ast.UnaryOp(
            op=ast.Not(),
            operand=ast.Name(id='quit', ctx=ast.Load())),
         body=[
            ast.Assign(
               targets=[
                  ast.Name(id='field', ctx=ast.Store())],
               value=ast.Call(
                  func=ast.Name(id='input', ctx=ast.Load()),
                  args=[
                     ast.Constant(value='What field do you want to change\n')],
                  keywords=[])),
            ast.Assign(
               targets=[
                  ast.Name(id='value', ctx=ast.Store())],
               value=ast.Call(
                  func=ast.Name(id='input', ctx=ast.Load()),
                  args=[
                     ast.Constant(value='Enter the value\n')],
                  keywords=[])),
            ast.If(
               test=ast.BoolOp(
                  op=ast.Or(),
                  values=[
                     ast.Compare(
                        left=ast.Name(id='field', ctx=ast.Load()),
                        ops=[
                           ast.Eq()],
                        comparators=[
                           ast.Constant(value='quit')]),
                     ast.Compare(
                        left=ast.Name(id='value', ctx=ast.Load()),
                        ops=[
                           ast.Eq()],
                        comparators=[
                           ast.Constant(value='quit')])]),
               body=[
                  ast.Assign(
                     targets=[
                        ast.Name(id='quit', ctx=ast.Store())],
                     value=ast.Constant(value=True))],
               orelse=[
                  ast.If(
                     test=ast.Compare(
                        left=ast.Call(
                           func=ast.Attribute(
                              value=ast.Name(id='value', ctx=ast.Load()),
                              attr='lower',
                              ctx=ast.Load()),
                           args=[],
                           keywords=[]),
                        ops=[
                           ast.Eq()],
                        comparators=[
                           ast.Constant(value='true')]),
                     body=[
                        ast.Assign(
                           targets=[
                              ast.Name(id='value', ctx=ast.Store())],
                           value=ast.Call(
                              func=ast.Attribute(
                                 value=ast.Subscript(
                                    value=ast.Name(id='structure', ctx=ast.Load()),
                                    slice=ast.Name(id='field', ctx=ast.Load()),
                                    ctx=ast.Load()),
                                 attr='intersection',
                                 ctx=ast.Load()),
                              args=[
                                 ast.Set(
                                    elts=[
                                       ast.Constant(value=True)])],
                              keywords=[]))],
                     orelse=[
                        ast.If(
                           test=ast.Compare(
                              left=ast.Call(
                                 func=ast.Attribute(
                                    value=ast.Name(id='value', ctx=ast.Load()),
                                    attr='lower',
                                    ctx=ast.Load()),
                                 args=[],
                                 keywords=[]),
                              ops=[
                                 ast.Eq()],
                              comparators=[
                                 ast.Constant(value='false')]),
                           body=[
                              ast.Assign(
                                 targets=[
                                    ast.Name(id='value', ctx=ast.Store())],
                                 value=ast.Call(
                                    func=ast.Attribute(
                                       value=ast.Subscript(
                                          value=ast.Name(id='structure', ctx=ast.Load()),
                                          slice=ast.Name(id='field', ctx=ast.Load()),
                                          ctx=ast.Load()),
                                       attr='intersection',
                                       ctx=ast.Load()),
                                    args=[
                                       ast.Set(
                                          elts=[
                                             ast.Constant(value=False)])],
                                    keywords=[]))],
                           orelse=[
                              ast.Assign(
                                 targets=[
                                    ast.Name(id='value', ctx=ast.Store())],
                                 value=ast.Call(
                                    func=ast.Attribute(
                                       value=ast.Subscript(
                                          value=ast.Name(id='structure', ctx=ast.Load()),
                                          slice=ast.Name(id='field', ctx=ast.Load()),
                                          ctx=ast.Load()),
                                       attr='intersection',
                                       ctx=ast.Load()),
                                    args=[
                                       ast.Set(
                                          elts=[
                                             ast.Call(
                                                func=ast.Name(id='int', ctx=ast.Load()),
                                                args=[
                                                   ast.Name(id='value', ctx=ast.Load())],
                                                keywords=[])])],
                                    keywords=[]))])]),
                  ast.Assign(
                     targets=[
                        ast.Name(id='changes', ctx=ast.Store())],
                     value=ast.Dict(
                        keys=[
                           ast.Name(id='field', ctx=ast.Load())],
                        values=[
                           ast.Name(id='value', ctx=ast.Load())])),
                  ast.Assign(
                     targets=[
                        ast.Name(id='unsat_fields', ctx=ast.Store())],
                     value=ast.Call(
                        func=ast.Name(id='propagation_loop', ctx=ast.Load()),
                        args=[
                           ast.Name(id='changes', ctx=ast.Load())],
                        keywords=[])),
                  ast.If(
                     test=ast.Compare(
                        left=ast.Call(
                           func=ast.Name(id='len', ctx=ast.Load()),
                           args=[
                              ast.Name(id='unsat_fields', ctx=ast.Load())],
                           keywords=[]),
                        ops=[
                           ast.Gt()],
                        comparators=[
                           ast.Constant(value=0)]),
                     body=[
                        ast.Expr(
                           value=ast.Call(
                              func=ast.Name(id='print', ctx=ast.Load()),
                              args=[
                                 ast.Constant(value='The following fields have become unsatisfiable')],
                              keywords=[])),
                        ast.For(
                           target=ast.Name(id='field', ctx=ast.Store()),
                           iter=ast.Name(id='unsat_fields', ctx=ast.Load()),
                           body=[
                              ast.Expr(
                                 value=ast.Call(
                                    func=ast.Name(id='print', ctx=ast.Load()),
                                    args=[
                                       ast.Name(id='field', ctx=ast.Load())],
                                    keywords=[]))],
                           orelse=[]),
                        ast.Assign(
                           targets=[
                              ast.Name(id='quit', ctx=ast.Store())],
                           value=ast.Constant(value=True))],
                     orelse=[
                        ast.Expr(
                           value=ast.Call(
                              func=ast.Name(id='print_structure', ctx=ast.Load()),
                              args=[],
                              keywords=[]))])])],
         orelse=[])],
   type_ignores=[])

# Generates AST for a helper function
def generate_feedback_loop():
    return ast.Module(
   body=[
      ast.Assign(
         targets=[
            ast.Name(id='quit', ctx=ast.Store())],
         value=ast.Constant(value=False)),
      ast.While(
         test=ast.UnaryOp(
            op=ast.Not(),
            operand=ast.Name(id='quit', ctx=ast.Load())),
         body=[
            ast.Assign(
               targets=[
                  ast.Name(id='field', ctx=ast.Store())],
               value=ast.Call(
                  func=ast.Name(id='input', ctx=ast.Load()),
                  args=[
                     ast.Constant(value='What field do you want to change\n')],
                  keywords=[])),
            ast.Assign(
               targets=[
                  ast.Name(id='value', ctx=ast.Store())],
               value=ast.Call(
                  func=ast.Name(id='input', ctx=ast.Load()),
                  args=[
                     ast.Constant(value='Enter the value\n')],
                  keywords=[])),
            ast.If(
               test=ast.BoolOp(
                  op=ast.Or(),
                  values=[
                     ast.Compare(
                        left=ast.Name(id='field', ctx=ast.Load()),
                        ops=[
                           ast.Eq()],
                        comparators=[
                           ast.Constant(value='quit')]),
                     ast.Compare(
                        left=ast.Name(id='value', ctx=ast.Load()),
                        ops=[
                           ast.Eq()],
                        comparators=[
                           ast.Constant(value='quit')])]),
               body=[
                  ast.Assign(
                     targets=[
                        ast.Name(id='quit', ctx=ast.Store())],
                     value=ast.Constant(value=True))],
               orelse=[
                  ast.If(
                     test=ast.Compare(
                        left=ast.Call(
                           func=ast.Attribute(
                              value=ast.Name(id='value', ctx=ast.Load()),
                              attr='lower',
                              ctx=ast.Load()),
                           args=[],
                           keywords=[]),
                        ops=[
                           ast.Eq()],
                        comparators=[
                           ast.Constant(value='true')]),
                     body=[
                        ast.Assign(
                           targets=[
                              ast.Name(id='value', ctx=ast.Store())],
                           value=ast.Constant(value=True))],
                     orelse=[ast.If(
                     test=ast.Compare(
                        left=ast.Call(
                           func=ast.Attribute(
                              value=ast.Name(id='value', ctx=ast.Load()),
                              attr='lower',
                              ctx=ast.Load()),
                           args=[],
                           keywords=[]),
                        ops=[
                           ast.Eq()],
                        comparators=[
                           ast.Constant(value='false')]),
                     body=[
                        ast.Assign(
                           targets=[
                              ast.Name(id='value', ctx=ast.Store())],
                           value=ast.Constant(value=False))],
                     orelse=[
                        ast.Assign(
                           targets=[
                              ast.Name(id='value', ctx=ast.Store())],
                           value=ast.Set(
                              elts=[
                                 ast.Call(
                                    func=ast.Name(id='int', ctx=ast.Load()),
                                    args=[
                                       ast.Name(id='value', ctx=ast.Load())],
                                    keywords=[])]))])]),
                  ast.Assign(
                     targets=[
                        ast.Name(id='changes', ctx=ast.Store())],
                     value=ast.Dict(
                        keys=[
                           ast.Name(id='field', ctx=ast.Load())],
                        values=[
                           ast.Name(id='value', ctx=ast.Load())])),
                  ast.While(
                     test=ast.Compare(
                        left=ast.Call(
                           func=ast.Name(id='len', ctx=ast.Load()),
                           args=[
                              ast.Name(id='changes', ctx=ast.Load())],
                           keywords=[]),
                        ops=[
                           ast.NotEq()],
                        comparators=[
                           ast.Constant(value=0)]),
                     body=[
                        ast.Assign(
                           targets=[
                              ast.Name(id='old_changes', ctx=ast.Store())],
                           value=ast.Name(id='changes', ctx=ast.Load())),
                        ast.Assign(
                           targets=[
                              ast.Name(id='changes', ctx=ast.Store())],
                           value=ast.Call(
                              func=ast.Name(id='propagate', ctx=ast.Load()),
                              args=[
                                 ast.Name(id='changes', ctx=ast.Load())],
                              keywords=[])),
                        ast.Expr(
                           value=ast.Call(
                              func=ast.Name(id='update_structure', ctx=ast.Load()),
                              args=[
                                 ast.Name(id='old_changes', ctx=ast.Load())],
                              keywords=[]))],
                     orelse=[]),
                  ast.Expr(
                     value=ast.Call(
                        func=ast.Name(id='print_structure', ctx=ast.Load()),
                        args=[],
                        keywords=[]))])],
         orelse=[])],
   type_ignores=[])





# Generates AST for an if-statement in the main propagate() function
def generate_if_statement(derived_propagator):
    if len(derived_propagator.middle) == 0:
        if type(derived_propagator.right) == Literal:
            return ast.If(
         test=ast.UnaryOp(
            op=ast.Not(),
            operand=ast.Call(
               func=ast.Name(id='all', ctx=ast.Load()),
               args=[
                  ast.GeneratorExp(
                     elt=ast.Compare(
                        left=ast.Name(id='elem', ctx=ast.Load()),
                        ops=[
                           ast.Eq()],
                        comparators=[
                           ast.Constant(value=derived_propagator.right.pos)]),
                     generators=[
                        ast.comprehension(
                           target=ast.Name(id='elem', ctx=ast.Store()),
                           iter=ast.Subscript(
                              value=ast.Name(id='structure', ctx=ast.Load()),
                              slice=ast.Constant(value=derived_propagator.right.atom),
                              ctx=ast.Load()),
                           ifs=[],
                           is_async=0)])],
               keywords=[])),
         body=[
             ast.Expr(
                 value=ast.Call(
                     func=ast.Attribute(
                         value=ast.Subscript(
                             value=ast.Name(id='new_changes', ctx=ast.Load()),
                             slice=ast.Constant(value=derived_propagator.right.atom),
                             ctx=ast.Load()),
                         attr='append',
                         ctx=ast.Load()),
                     args=[ast.SetComp(
                  elt=ast.Name(id='elem', ctx=ast.Load()),
                  generators=[
                     ast.comprehension(
                        target=ast.Name(id='elem', ctx=ast.Store()),
                        iter=ast.Subscript(
                           value=ast.Name(id='structure', ctx=ast.Load()),
                           slice=ast.Constant(value=derived_propagator.right.atom),
                           ctx=ast.Load()),
                        ifs=[
                           ast.Compare(
                              left=ast.Name(id='elem', ctx=ast.Load()),
                              ops=[
                                 ast.Eq()],
                              comparators=[
                                 ast.Constant(value=derived_propagator.right.pos)])],
                        is_async=0)])],
                     keywords=[]))],
            orelse = [])


    else:
        if type(derived_propagator.right) == Literal:
            and_list = []
            for literal in derived_propagator.middle:
                and_list.append(ast.Call(
            func=ast.Name(id='all', ctx=ast.Load()),
            args=[
               ast.GeneratorExp(
                  elt=ast.Compare(
                     left=ast.Name(id='elem', ctx=ast.Load()),
                     ops=[
                        ast.Eq()],
                     comparators=[
                        ast.Constant(value=literal.pos)]),
                  generators=[
                     ast.comprehension(
                        target=ast.Name(id='elem', ctx=ast.Store()),
                        iter=ast.Subscript(
                           value=ast.Name(id='structure', ctx=ast.Load()),
                           slice=ast.Constant(value=literal.atom),
                           ctx=ast.Load()),
                        ifs=[],
                        is_async=0)])],
            keywords=[]))
            return ast.If(
             test=ast.UnaryOp(
            op=ast.Not(),
            operand=ast.Call(
               func=ast.Name(id='all', ctx=ast.Load()),
               args=[
                  ast.GeneratorExp(
                     elt=ast.Compare(
                        left=ast.Name(id='elem', ctx=ast.Load()),
                        ops=[
                           ast.Eq()],
                        comparators=[
                           ast.Constant(value=derived_propagator.right.pos)]),
                     generators=[
                        ast.comprehension(
                           target=ast.Name(id='elem', ctx=ast.Store()),
                           iter=ast.Subscript(
                              value=ast.Name(id='structure', ctx=ast.Load()),
                              slice=ast.Constant(value=derived_propagator.right.atom),
                              ctx=ast.Load()),
                           ifs=[],
                           is_async=0)])],
               keywords=[])),
             body=[
                 ast.If(
                     test=ast.BoolOp(
                         op=ast.And(),
                         values=and_list),
                     body=[
                         ast.Expr(
                             value=ast.Call(
                                 func=ast.Attribute(
                                     value=ast.Subscript(
                                         value=ast.Name(id='new_changes', ctx=ast.Load()),
                                         slice=ast.Constant(value=derived_propagator.right.atom),
                                         ctx=ast.Load()),
                                     attr='append',
                                     ctx=ast.Load()),
                                 args=[ast.SetComp(
                                     elt=ast.Name(id='elem', ctx=ast.Load()),
                                     generators=[
                                         ast.comprehension(
                                             target=ast.Name(id='elem', ctx=ast.Store()),
                                             iter=ast.Subscript(
                                                 value=ast.Name(id='structure', ctx=ast.Load()),
                                                 slice=ast.Constant(value=derived_propagator.right.atom),
                                                 ctx=ast.Load()),
                                             ifs=[
                                                 ast.Compare(
                                                     left=ast.Name(id='elem', ctx=ast.Load()),
                                                     ops=[
                                                         ast.Eq()],
                                                     comparators=[
                                                         ast.Constant(value=derived_propagator.right.pos)])],
                                             is_async=0)])],
                                 keywords=[]))
                     ],
                     orelse=[])],
                orelse=[])




# Groups all DerivedPropagator-objects based on their left argument, and on the truth value of that argument.
# This is helpful in order to activate the correct propagators based on which atom (left argument) was changed to what value.
def group_derived_props(derived_props):
    grouped = {}
    for derived_prop in derived_props:
        if derived_prop.left == None:
            if None not in grouped.keys():
                grouped[None] = {derived_prop}
            else:
                grouped[None].add(derived_prop)
        if type(derived_prop.left) == Literal:
            if derived_prop.left.atom not in grouped.keys():
                grouped[derived_prop.left.atom] = {derived_prop.left.pos : {derived_prop}}
            else:
                if derived_prop.left.pos not in grouped[derived_prop.left.atom].keys():
                    grouped[derived_prop.left.atom][derived_prop.left.pos] = {derived_prop}
                else:
                    grouped[derived_prop.left.atom][derived_prop.left.pos].add(derived_prop)
        #elif type(derived_prop.left) == Equation:
        #    if derived_prop.left.exp1.name not in grouped.keys():
        #        grouped[derived_prop.left.exp1.name] = {(derived_prop.left.operator, derived_prop.left.exp2.name) : {derived_prop}}
        #    else:
        #        if (derived_prop.left.operator, derived_prop.left.exp2.name) not in grouped[derived_prop.left.exp1.name].keys():
        #            grouped[derived_prop.left.exp1.name][(derived_prop.left.operator, derived_prop.left.exp2.name)] = {derived_prop}
        #        else:
        #            grouped[derived_prop.left.exp1.name][(derived_prop.left.operator, derived_prop.left.exp2.name)].add(derived_prop)
        #elif type(derived_prop) == EquationPropagator:
        #    if derived_prop.left.name not in grouped.keys():
        #       grouped[derived_prop.left.name] = {(derived_prop.middle[0].atom, derived_prop.middle[0].pos): {derived_prop}}
        #    else:
        #        if (derived_prop.middle[0].atom, derived_prop.middle[0].pos) not in grouped[derived_prop.left.name].keys():
        #            grouped[derived_prop.left.name][(derived_prop.middle[0].atom, derived_prop.middle[0].pos)] = {derived_prop}
        #        else:
        #            grouped[derived_prop.left.name][(derived_prop.middle[0].atom, derived_prop.middle[0].pos)].add(derived_prop)



    return grouped






# Generates an AST for a propagator that is unconditional, in other words, that have a consequence that is always true.
def generate_unconditional_statement(propagator):
    if type(propagator.right) == Literal:
        return ast.If(
         test=ast.Compare(
            left=ast.Name(id='key', ctx=ast.Load()),
            ops=[
               ast.NotEq()],
            comparators=[
               ast.Constant(value=propagator.right.atom)]),
         body=[
            generate_if_statement(propagator)],
        orelse=[])


# Generates an AST for all the propagators that are activated by the given atom.
def generate_atom_tests(atom, propagators):
    true_if_statements = []
    false_if_statements = []
    if True in propagators.keys():
        for prop in propagators[True]:
            true_if_statements.append(generate_if_statement(prop))
    else:
        true_if_statements.append(ast.Pass())
    if False in propagators.keys():
        for prop in propagators[False]:
            false_if_statements.append(generate_if_statement(prop))
    else:
        false_if_statements.append(ast.Pass())

    return ast.If(
         test=ast.Compare(
            left=ast.Name(id='key', ctx=ast.Load()),
            ops=[
               ast.Eq()],
            comparators=[
               ast.Constant(value=atom)]),
         body=[
            ast.If(
               test=ast.Call(
                  func=ast.Name(id='all', ctx=ast.Load()),
                  args=[
                     ast.GeneratorExp(
                        elt=ast.Compare(
                           left=ast.Name(id='elem', ctx=ast.Load()),
                           ops=[
                              ast.Eq()],
                           comparators=[
                              ast.Constant(value=True)]),
                        generators=[
                           ast.comprehension(
                              target=ast.Name(id='elem', ctx=ast.Store()),
                              iter=ast.Name(id='value', ctx=ast.Load()),
                              ifs=[],
                              is_async=0)])],
                  keywords=[]),
               body=[
                  true_if_statements],
               orelse=[
                  ast.If(
                     test=ast.Call(
                        func=ast.Name(id='all', ctx=ast.Load()),
                        args=[
                           ast.GeneratorExp(
                              elt=ast.Compare(
                                 left=ast.Name(id='elem', ctx=ast.Load()),
                                 ops=[
                                    ast.Eq()],
                                 comparators=[
                                    ast.Constant(value=False)]),
                              generators=[
                                 ast.comprehension(
                                    target=ast.Name(id='elem', ctx=ast.Store()),
                                    iter=ast.Name(id='value', ctx=ast.Load()),
                                    ifs=[],
                                    is_async=0)])],
                        keywords=[]),
                     body=[
                        false_if_statements],
                     orelse=[])])],
         orelse=[])


# Generates the main propagate() function, performing the propagation inference task.
def generate_propagate(derived_props):
    if_statements = []
    unconditional_statements = []
    grouped = group_derived_props(derived_props)
    for atom in grouped.keys():
        if atom == None:
            for derived_prop in grouped[atom]:
                unconditional_statements.append(generate_if_statement(derived_prop))
        else:
            if True in grouped[atom].keys() or False in grouped[atom].keys():
                if_statements.append(generate_atom_tests(atom, grouped[atom]))

    return ast.FunctionDef(
         name='propagate',
         args=ast.arguments(
            posonlyargs=[],
            args=[
               ast.arg(arg='changes')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
             ast.Assign(
                 targets=[
                     ast.Name(id='new_changes', ctx=ast.Store())],
                 value=ast.DictComp(
                     key=ast.Name(id='key', ctx=ast.Load()),
                     value=ast.List(elts=[], ctx=ast.Load()),
                     generators=[
                         ast.comprehension(
                             target=ast.Name(id='key', ctx=ast.Store()),
                             iter=ast.Call(
                                 func=ast.Attribute(
                                     value=ast.Name(id='structure', ctx=ast.Load()),
                                     attr='keys',
                                     ctx=ast.Load()),
                                 args=[],
                                 keywords=[]),
                             ifs=[],
                             is_async=0)])),
            ast.For(
               target=ast.Tuple(
                  elts=[
                     ast.Name(id='key', ctx=ast.Store()),
                     ast.Name(id='value', ctx=ast.Store())],
                  ctx=ast.Store()),
               iter=ast.Call(
                  func=ast.Attribute(
                     value=ast.Name(id='changes', ctx=ast.Load()),
                     attr='items',
                     ctx=ast.Load()),
                  args=[],
                  keywords=[]),
               body=[unconditional_statements, if_statements],
                orelse=[]),
             ast.Return(
                 value=ast.Call(
                     func=ast.Name(id='intersect_changes', ctx=ast.Load()),
                     args=[
                         ast.Name(id='new_changes', ctx=ast.Load())],
                     keywords=[]))
         ],
        decorator_list=[])

# Generates AST for a helper function
def generate_propagation_loop_with_contradiction_check():
    return ast.FunctionDef(
         name='propagation_loop',
         args=ast.arguments(
            posonlyargs=[],
            args=[
               ast.arg(arg='changes')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            ast.Assign(
               targets=[
                  ast.Name(id='unsat_fields', ctx=ast.Store())],
               value=ast.Call(
                  func=ast.Name(id='check_unsat_fields', ctx=ast.Load()),
                  args=[
                     ast.Name(id='changes', ctx=ast.Load())],
                  keywords=[])),
            ast.While(
               test=ast.BoolOp(
                  op=ast.And(),
                  values=[
                     ast.Compare(
                        left=ast.Call(
                           func=ast.Name(id='len', ctx=ast.Load()),
                           args=[
                              ast.Name(id='changes', ctx=ast.Load())],
                           keywords=[]),
                        ops=[
                           ast.NotEq()],
                        comparators=[
                           ast.Constant(value=0)]),
                     ast.Compare(
                        left=ast.Call(
                           func=ast.Name(id='len', ctx=ast.Load()),
                           args=[
                              ast.Name(id='unsat_fields', ctx=ast.Load())],
                           keywords=[]),
                        ops=[
                           ast.Eq()],
                        comparators=[
                           ast.Constant(value=0)])]),
               body=[
                  ast.Assign(
                     targets=[
                        ast.Name(id='old_changes', ctx=ast.Store())],
                     value=ast.Name(id='changes', ctx=ast.Load())),
                  ast.Assign(
                     targets=[
                        ast.Name(id='changes', ctx=ast.Store())],
                     value=ast.Call(
                        func=ast.Name(id='propagate', ctx=ast.Load()),
                        args=[
                           ast.Name(id='changes', ctx=ast.Load())],
                        keywords=[])),
                  ast.Expr(
                     value=ast.Call(
                        func=ast.Name(id='update_structure', ctx=ast.Load()),
                        args=[
                           ast.Name(id='old_changes', ctx=ast.Load())],
                        keywords=[])),
                  ast.Assign(
                     targets=[
                        ast.Name(id='unsat_fields', ctx=ast.Store())],
                     value=ast.Call(
                        func=ast.Name(id='check_unsat_fields', ctx=ast.Load()),
                        args=[
                           ast.Name(id='changes', ctx=ast.Load())],
                        keywords=[]))],
               orelse=[]),
            ast.Return(
               value=ast.Name(id='unsat_fields', ctx=ast.Load()))],
         decorator_list=[])
# Generates AST for a helper function
def generate_propagate_loop():
    return ast.FunctionDef(
         name='propagate_loop',
         args=ast.arguments(
            posonlyargs=[],
            args=[
               ast.arg(arg='field'),
               ast.arg(arg='value')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            ast.Assign(
               targets=[
                  ast.Name(id='changes', ctx=ast.Store())],
               value=ast.Dict(
                  keys=[
                     ast.Name(id='field', ctx=ast.Load())],
                  values=[
                     ast.Name(id='value', ctx=ast.Load())])),
            ast.While(
               test=ast.Compare(
                  left=ast.Call(
                     func=ast.Name(id='len', ctx=ast.Load()),
                     args=[
                        ast.Name(id='changes', ctx=ast.Load())],
                     keywords=[]),
                  ops=[
                     ast.NotEq()],
                  comparators=[
                     ast.Constant(value=0)]),
               body=[
                  ast.Assign(
                     targets=[
                        ast.Name(id='old_changes', ctx=ast.Store())],
                     value=ast.Name(id='changes', ctx=ast.Load())),
                  ast.Assign(
                     targets=[
                        ast.Name(id='changes', ctx=ast.Store())],
                     value=ast.Call(
                        func=ast.Name(id='propagate', ctx=ast.Load()),
                        args=[
                           ast.Name(id='changes', ctx=ast.Load())],
                        keywords=[])),
                  ast.Expr(
                     value=ast.Call(
                        func=ast.Name(id='update_structure', ctx=ast.Load()),
                        args=[
                           ast.Name(id='old_changes', ctx=ast.Load())],
                        keywords=[]))],
               orelse=[])],
        decorator_list=[])


# Generates AST for a helper function
def generate_get_dropdown_options():
    return ast.FunctionDef(
        name='get_dropdown_options',
        args=ast.arguments(
            posonlyargs=[],
            args=[
                ast.arg(arg='integer_list')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
        body=[
            ast.Assign(
                targets=[
                    ast.Name(id='options_list', ctx=ast.Store())],
                value=ast.List(elts=[], ctx=ast.Load())),
            ast.For(
                target=ast.Name(id='i', ctx=ast.Store()),
                iter=ast.Name(id='integer_list', ctx=ast.Load()),
                body=[
                    ast.Expr(
                        value=ast.Call(
                            func=ast.Attribute(
                                value=ast.Name(id='options_list', ctx=ast.Load()),
                                attr='append',
                                ctx=ast.Load()),
                            args=[
                                ast.Dict(
                                    keys=[
                                        ast.Constant(value='label'),
                                        ast.Constant(value='value')],
                                    values=[
                                        ast.Call(
                                            func=ast.Name(id='str', ctx=ast.Load()),
                                            args=[
                                                ast.Name(id='i', ctx=ast.Load())],
                                            keywords=[]),
                                        ast.Name(id='i', ctx=ast.Load())])],
                            keywords=[]))],
                orelse=[]),
            ast.Return(
                value=ast.Name(id='options_list', ctx=ast.Load()))],
        decorator_list=[])

# Generates AST for a helper function
def generate_convert_to_ui():
    return ast.FunctionDef(
         name='convert_to_ui',
         args=ast.arguments(
            posonlyargs=[],
            args=[
               ast.arg(arg='values')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            ast.If(
               test=ast.Compare(
                  left=ast.Name(id='values', ctx=ast.Load()),
                  ops=[
                     ast.Eq()],
                  comparators=[
                     ast.Set(
                        elts=[
                           ast.Constant(value=True),
                           ast.Constant(value=False)])]),
               body=[
                  ast.Return(
                     value=ast.List(elts=[], ctx=ast.Load()))],
               orelse=[]),
            ast.If(
               test=ast.Compare(
                  left=ast.Name(id='values', ctx=ast.Load()),
                  ops=[
                     ast.Eq()],
                  comparators=[
                     ast.Set(
                        elts=[
                           ast.Constant(value=True)])]),
               body=[
                  ast.Return(
                     value=ast.List(
                        elts=[
                           ast.Constant(value=True)],
                        ctx=ast.Load()))],
               orelse=[]),
            ast.If(
               test=ast.Compare(
                  left=ast.Name(id='values', ctx=ast.Load()),
                  ops=[
                     ast.Eq()],
                  comparators=[
                     ast.Set(
                        elts=[
                           ast.Constant(value=False)])]),
               body=[
                  ast.Return(
                     value=ast.List(
                        elts=[
                           ast.Constant(value=False)],
                        ctx=ast.Load()))],
               orelse=[
                  ast.Return(
                     value=ast.Call(
                        func=ast.Name(id='get_dropdown_options', ctx=ast.Load()),
                        args=[
                           ast.Name(id='values', ctx=ast.Load())],
                        keywords=[]))])],
         decorator_list=[])


# Generates AST for a helper function
def generate_convert_from_ui():
    return ast.FunctionDef(
        name='convert_from_ui',
        args=ast.arguments(
            posonlyargs=[],
            args=[
                ast.arg(arg='values')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
        body=[
            ast.If(
                test=ast.BoolOp(
                    op=ast.Or(),
                    values=[
                        ast.Compare(
                            left=ast.Name(id='values', ctx=ast.Load()),
                            ops=[
                                ast.Eq()],
                            comparators=[
                                ast.List(
                                    elts=[
                                        ast.Constant(value=True),
                                        ast.Constant(value=False)],
                                    ctx=ast.Load())]),
                        ast.Compare(
                            left=ast.Name(id='values', ctx=ast.Load()),
                            ops=[
                                ast.Eq()],
                            comparators=[
                                ast.List(
                                    elts=[
                                        ast.Constant(value=False),
                                        ast.Constant(value=True)],
                                    ctx=ast.Load())])]),
                body=[
                    ast.Return(
                        value=ast.Call(
                            func=ast.Name(id='set', ctx=ast.Load()),
                            args=[],
                            keywords=[]))],
                orelse=[]),
            ast.If(
                test=ast.Compare(
                    left=ast.Name(id='values', ctx=ast.Load()),
                    ops=[
                        ast.Eq()],
                    comparators=[
                        ast.List(
                            elts=[
                                ast.Constant(value=True)],
                            ctx=ast.Load())]),
                body=[
                    ast.Return(
                        value=ast.Set(
                            elts=[
                                ast.Constant(value=True)]))],
                orelse=[]),
            ast.If(
                test=ast.Compare(
                    left=ast.Name(id='values', ctx=ast.Load()),
                    ops=[
                        ast.Eq()],
                    comparators=[
                        ast.List(
                            elts=[
                                ast.Constant(value=False)],
                            ctx=ast.Load())]),
                body=[
                    ast.Return(
                        value=ast.Set(
                            elts=[
                                ast.Constant(value=False)]))],
                orelse=[
                    ast.Return(
                        value=ast.Constant(value=None))])],
        decorator_list=[])

# Generates AST for a helper function
def generate_unsat_message():
    return ast.FunctionDef(
        name='unsat_message',
        args=ast.arguments(
            posonlyargs=[],
            args=[
                ast.arg(arg='unsat_values')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
        body=[
            ast.Assign(
                targets=[
                    ast.Name(id='unsat_str', ctx=ast.Store())],
                value=ast.Constant(value='UNSAT: inconsistencies were detected in the following fields: ')),
            ast.For(
                target=ast.Name(id='unsat_val', ctx=ast.Store()),
                iter=ast.Name(id='unsat_values', ctx=ast.Load()),
                body=[
                    ast.AugAssign(
                        target=ast.Name(id='unsat_str', ctx=ast.Store()),
                        op=ast.Add(),
                        value=ast.BinOp(
                            left=ast.Name(id='unsat_val', ctx=ast.Load()),
                            op=ast.Add(),
                            right=ast.Constant(value=' ')))],
                orelse=[]),
            ast.AugAssign(
                target=ast.Name(id='unsat_str', ctx=ast.Store()),
                op=ast.Add(),
                value=ast.Constant(value='. Please reset the application.')),
            ast.Return(
                value=ast.Name(id='unsat_str', ctx=ast.Load()))],
        decorator_list=[])

# Generates AST for a helper function
def generate_launch_dash_app():
    return ast.Module(
   body=[
      ast.FunctionDef(
         name='launch_dash_app',
         args=ast.arguments(
            posonlyargs=[],
            args=[],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            ast.Assign(
               targets=[
                  ast.Name(id='app', ctx=ast.Store())],
               value=ast.Call(
                  func=ast.Name(id='Dash', ctx=ast.Load()),
                  args=[
                     ast.Name(id='__name__', ctx=ast.Load())],
                  keywords=[])),
            ast.Assign(
               targets=[
                  ast.Name(id='boolean_variables', ctx=ast.Store())],
               value=ast.ListComp(
                  elt=ast.Name(id='var', ctx=ast.Load()),
                  generators=[
                     ast.comprehension(
                        target=ast.Name(id='var', ctx=ast.Store()),
                        iter=ast.Call(
                           func=ast.Attribute(
                              value=ast.Name(id='structure', ctx=ast.Load()),
                              attr='keys',
                              ctx=ast.Load()),
                           args=[],
                           keywords=[]),
                        ifs=[
                           ast.BoolOp(
                              op=ast.And(),
                              values=[
                                 ast.Compare(
                                    left=ast.Subscript(
                                       value=ast.Name(id='structure', ctx=ast.Load()),
                                       slice=ast.Name(id='var', ctx=ast.Load()),
                                       ctx=ast.Load()),
                                    ops=[
                                       ast.Eq()],
                                    comparators=[
                                       ast.Set(
                                          elts=[
                                             ast.Constant(value=True),
                                             ast.Constant(value=False)])]),
                                 ast.UnaryOp(
                                    op=ast.Not(),
                                    operand=ast.Call(
                                       func=ast.Attribute(
                                          value=ast.Name(id='var', ctx=ast.Load()),
                                          attr='startswith',
                                          ctx=ast.Load()),
                                       args=[
                                          ast.Constant(value='_')],
                                       keywords=[]))])],
                        is_async=0)])),
            ast.Expr(
                 value=ast.Call(
                     func=ast.Attribute(
                         value=ast.Name(id='boolean_variables', ctx=ast.Load()),
                         attr='sort',
                         ctx=ast.Load()),
                     args=[],
                     keywords=[])),
       ast.Assign(
               targets=[
                  ast.Name(id='integer_variables', ctx=ast.Store())],
               value=ast.ListComp(
                  elt=ast.Name(id='var', ctx=ast.Load()),
                  generators=[
                     ast.comprehension(
                        target=ast.Name(id='var', ctx=ast.Store()),
                        iter=ast.Call(
                           func=ast.Attribute(
                              value=ast.Name(id='structure', ctx=ast.Load()),
                              attr='keys',
                              ctx=ast.Load()),
                           args=[],
                           keywords=[]),
                        ifs=[
                           ast.Compare(
                              left=ast.Subscript(
                                 value=ast.Name(id='structure', ctx=ast.Load()),
                                 slice=ast.Name(id='var', ctx=ast.Load()),
                                 ctx=ast.Load()),
                              ops=[
                                 ast.NotEq()],
                              comparators=[
                                 ast.Set(
                                    elts=[
                                       ast.Constant(value=True),
                                       ast.Constant(value=False)])])],
                        is_async=0)])),
            ast.Assign(
               targets=[
                  ast.Attribute(
                     value=ast.Name(id='app', ctx=ast.Load()),
                     attr='layout',
                     ctx=ast.Store())],
               value=ast.Call(
                  func=ast.Attribute(
                     value=ast.Name(id='html', ctx=ast.Load()),
                     attr='Div',
                     ctx=ast.Load()),
                  args=[
                     ast.List(
                        elts=[
                           ast.Call(
                              func=ast.Attribute(
                                 value=ast.Name(id='html', ctx=ast.Load()),
                                 attr='H1',
                                 ctx=ast.Load()),
                              args=[
                                 ast.Constant(value='Interactive configuration')],
                              keywords=[]),
                           ast.Call(
                              func=ast.Attribute(
                                 value=ast.Name(id='html', ctx=ast.Load()),
                                 attr='Button',
                                 ctx=ast.Load()),
                              args=[
                                 ast.Constant(value='Reset')],
                              keywords=[
                                 ast.keyword(
                                    arg='id',
                                    value=ast.Constant(value='reset-button')),
                                 ast.keyword(
                                    arg='n_clicks',
                                    value=ast.Constant(value=0))]),
                           ast.Call(
                              func=ast.Attribute(
                                 value=ast.Name(id='html', ctx=ast.Load()),
                                 attr='Div',
                                 ctx=ast.Load()),
                              args=[
                                 ast.ListComp(
                                    elt=ast.Call(
                                       func=ast.Attribute(
                                          value=ast.Name(id='html', ctx=ast.Load()),
                                          attr='Div',
                                          ctx=ast.Load()),
                                       args=[
                                          ast.List(
                                             elts=[
                                                ast.Call(
                                                   func=ast.Attribute(
                                                      value=ast.Name(id='html', ctx=ast.Load()),
                                                      attr='Label',
                                                      ctx=ast.Load()),
                                                   args=[
                                                      ast.JoinedStr(
                                                         values=[
                                                            ast.FormattedValue(
                                                               value=ast.Name(id='var', ctx=ast.Load()),
                                                               conversion=-1),
                                                            ast.Constant(value=':')])],
                                                   keywords=[]),
                                                ast.Call(
                                                   func=ast.Attribute(
                                                      value=ast.Name(id='dcc', ctx=ast.Load()),
                                                      attr='Checklist',
                                                      ctx=ast.Load()),
                                                   args=[],
                                                   keywords=[
                                                      ast.keyword(
                                                         arg='id',
                                                         value=ast.Dict(
                                                            keys=[
                                                               ast.Constant(value='type'),
                                                               ast.Constant(value='index')],
                                                            values=[
                                                               ast.Constant(value='checkboxes'),
                                                               ast.Name(id='var', ctx=ast.Load())])),
                                                      ast.keyword(
                                                         arg='options',
                                                         value=ast.List(
                                                            elts=[
                                                               ast.Dict(
                                                                  keys=[
                                                                     ast.Constant(value='label'),
                                                                     ast.Constant(value='value')],
                                                                  values=[
                                                                     ast.Constant(value='True'),
                                                                     ast.Constant(value=True)]),
                                                               ast.Dict(
                                                                  keys=[
                                                                     ast.Constant(value='label'),
                                                                     ast.Constant(value='value')],
                                                                  values=[
                                                                     ast.Constant(value='False'),
                                                                     ast.Constant(value=False)])],
                                                            ctx=ast.Load())),
                                                      ast.keyword(
                                                         arg='value',
                                                         value=ast.List(elts=[], ctx=ast.Load())),
                                                      ast.keyword(
                                                         arg='inline',
                                                         value=ast.Constant(value=True))]),
                                                ast.Call(
                                                   func=ast.Attribute(
                                                      value=ast.Name(id='html', ctx=ast.Load()),
                                                      attr='Div',
                                                      ctx=ast.Load()),
                                                   args=[],
                                                   keywords=[
                                                      ast.keyword(
                                                         arg='id',
                                                         value=ast.Dict(
                                                            keys=[
                                                               ast.Constant(value='type'),
                                                               ast.Constant(value='index')],
                                                            values=[
                                                               ast.Constant(value='output'),
                                                               ast.Name(id='var', ctx=ast.Load())]))])],
                                             ctx=ast.Load())],
                                       keywords=[]),
                                    generators=[
                                       ast.comprehension(
                                          target=ast.Name(id='var', ctx=ast.Store()),
                                          iter=ast.Name(id='boolean_variables', ctx=ast.Load()),
                                          ifs=[],
                                          is_async=0)])],
                              keywords=[]),
                           ast.Call(
                              func=ast.Attribute(
                                 value=ast.Name(id='html', ctx=ast.Load()),
                                 attr='Div',
                                 ctx=ast.Load()),
                              args=[
                                 ast.ListComp(
                                    elt=ast.Call(
                                       func=ast.Attribute(
                                          value=ast.Name(id='html', ctx=ast.Load()),
                                          attr='Div',
                                          ctx=ast.Load()),
                                       args=[
                                          ast.List(
                                             elts=[
                                                ast.Call(
                                                   func=ast.Attribute(
                                                      value=ast.Name(id='html', ctx=ast.Load()),
                                                      attr='Label',
                                                      ctx=ast.Load()),
                                                   args=[
                                                      ast.JoinedStr(
                                                         values=[
                                                            ast.FormattedValue(
                                                               value=ast.Name(id='var', ctx=ast.Load()),
                                                               conversion=-1),
                                                            ast.Constant(value=':')])],
                                                   keywords=[]),
                                                ast.Call(
                                                   func=ast.Attribute(
                                                      value=ast.Name(id='dcc', ctx=ast.Load()),
                                                      attr='Dropdown',
                                                      ctx=ast.Load()),
                                                   args=[],
                                                   keywords=[
                                                      ast.keyword(
                                                         arg='id',
                                                         value=ast.Dict(
                                                            keys=[
                                                               ast.Constant(value='type'),
                                                               ast.Constant(value='index')],
                                                            values=[
                                                               ast.Constant(value='dropdown'),
                                                               ast.Name(id='var', ctx=ast.Load())])),
                                                      ast.keyword(
                                                         arg='options',
                                                         value=ast.Call(
                                                            func=ast.Name(id='get_dropdown_options', ctx=ast.Load()),
                                                            args=[
                                                               ast.Subscript(
                                                                  value=ast.Name(id='structure', ctx=ast.Load()),
                                                                  slice=ast.Name(id='var', ctx=ast.Load()),
                                                                  ctx=ast.Load())],
                                                            keywords=[])),
                                                      ast.keyword(
                                                         arg='placeholder',
                                                         value=ast.Constant(value='Select a number'))]),
                                                ast.Call(
                                                   func=ast.Attribute(
                                                      value=ast.Name(id='html', ctx=ast.Load()),
                                                      attr='Div',
                                                      ctx=ast.Load()),
                                                   args=[],
                                                   keywords=[
                                                      ast.keyword(
                                                         arg='id',
                                                         value=ast.Dict(
                                                            keys=[
                                                               ast.Constant(value='type'),
                                                               ast.Constant(value='index')],
                                                            values=[
                                                               ast.Constant(value='output'),
                                                               ast.Name(id='var', ctx=ast.Load())]))])],
                                             ctx=ast.Load())],
                                       keywords=[]),
                                    generators=[
                                       ast.comprehension(
                                          target=ast.Name(id='var', ctx=ast.Store()),
                                          iter=ast.Name(id='integer_variables', ctx=ast.Load()),
                                          ifs=[],
                                          is_async=0)])],
                              keywords=[]),
                           ast.Call(
                              func=ast.Attribute(
                                 value=ast.Name(id='html', ctx=ast.Load()),
                                 attr='Div',
                                 ctx=ast.Load()),
                              args=[
                                 ast.List(
                                    elts=[
                                       ast.Call(
                                          func=ast.Attribute(
                                             value=ast.Name(id='html', ctx=ast.Load()),
                                             attr='Div',
                                             ctx=ast.Load()),
                                          args=[],
                                          keywords=[
                                             ast.keyword(
                                                arg='id',
                                                value=ast.Dict(
                                                   keys=[
                                                      ast.Constant(value='type')],
                                                   values=[
                                                      ast.Constant(value='text-output')])),
                                             ast.keyword(
                                                arg='children',
                                                value=ast.Constant(value='No inconsistencies detected yet'))])],
                                    ctx=ast.Load())],
                              keywords=[])],
                        ctx=ast.Load())],
                  keywords=[])),
            ast.FunctionDef(
               name='handle_changes',
               args=ast.arguments(
                  posonlyargs=[],
                  args=[
                     ast.arg(arg='checkbox_values'),
                     ast.arg(arg='dropdown_values'),
                     ast.arg(arg='checkbox_ids'),
                     ast.arg(arg='dropdown_ids'),
                     ast.arg(arg='reset')],
                  kwonlyargs=[],
                  kw_defaults=[],
                  defaults=[]),
               body=[
                  ast.Assign(
                     targets=[
                        ast.Name(id='triggered', ctx=ast.Store())],
                     value=ast.Attribute(
                        value=ast.Name(id='callback_context', ctx=ast.Load()),
                        attr='triggered',
                        ctx=ast.Load())),
                  ast.If(
                     test=ast.Name(id='triggered', ctx=ast.Load()),
                     body=[
                        ast.Assign(
                           targets=[
                              ast.Name(id='changed_component', ctx=ast.Store())],
                           value=ast.Subscript(
                              value=ast.Call(
                                 func=ast.Attribute(
                                    value=ast.Subscript(
                                       value=ast.Subscript(
                                          value=ast.Name(id='triggered', ctx=ast.Load()),
                                          slice=ast.Constant(value=0),
                                          ctx=ast.Load()),
                                       slice=ast.Constant(value='prop_id'),
                                       ctx=ast.Load()),
                                    attr='split',
                                    ctx=ast.Load()),
                                 args=[
                                    ast.Constant(value='.')],
                                 keywords=[]),
                              slice=ast.Constant(value=0),
                              ctx=ast.Load())),
                        ast.Assign(
                           targets=[
                              ast.Name(id='changed_value', ctx=ast.Store())],
                           value=ast.Subscript(
                              value=ast.Subscript(
                                 value=ast.Name(id='triggered', ctx=ast.Load()),
                                 slice=ast.Constant(value=0),
                                 ctx=ast.Load()),
                              slice=ast.Constant(value='value'),
                              ctx=ast.Load())),
                        ast.If(
                           test=ast.Compare(
                              left=ast.Name(id='changed_component', ctx=ast.Load()),
                              ops=[
                                 ast.Eq()],
                              comparators=[
                                 ast.Constant(value='reset-button')]),
                           body=[
                              ast.Expr(
                                 value=ast.Call(
                                    func=ast.Name(id='handle_reset', ctx=ast.Load()),
                                    args=[],
                                    keywords=[])),
                              ast.Assign(
                                 targets=[
                                    ast.Name(id='checkbox_values', ctx=ast.Store())],
                                 value=ast.ListComp(
                                    elt=ast.List(elts=[], ctx=ast.Load()),
                                    generators=[
                                       ast.comprehension(
                                          target=ast.Name(id='_', ctx=ast.Store()),
                                          iter=ast.Name(id='boolean_variables', ctx=ast.Load()),
                                          ifs=[],
                                          is_async=0)])),
                              ast.Assign(
                                 targets=[
                                    ast.Name(id='dropdown_options', ctx=ast.Store())],
                                 value=ast.ListComp(
                                    elt=ast.Call(
                                       func=ast.Name(id='get_dropdown_options', ctx=ast.Load()),
                                       args=[
                                          ast.Subscript(
                                             value=ast.Name(id='structure', ctx=ast.Load()),
                                             slice=ast.Name(id='v', ctx=ast.Load()),
                                             ctx=ast.Load())],
                                       keywords=[]),
                                    generators=[
                                       ast.comprehension(
                                          target=ast.Name(id='v', ctx=ast.Store()),
                                          iter=ast.Name(id='integer_variables', ctx=ast.Load()),
                                          ifs=[],
                                          is_async=0)])),
                              ast.Return(
                                 value=ast.Tuple(
                                    elts=[
                                       ast.Name(id='checkbox_values', ctx=ast.Load()),
                                       ast.Name(id='dropdown_options', ctx=ast.Load()),
                                       ast.List(
                                          elts=[
                                             ast.Constant(value='No inconsistencies detected yet')],
                                          ctx=ast.Load())],
                                    ctx=ast.Load()))],
                           orelse=[]),
                        ast.Assign(
                           targets=[
                              ast.Name(id='changed_id', ctx=ast.Store())],
                           value=ast.Call(
                              func=ast.Name(id='eval', ctx=ast.Load()),
                              args=[
                                 ast.Name(id='changed_component', ctx=ast.Load())],
                              keywords=[])),
                        ast.If(
                           test=ast.Compare(
                              left=ast.Subscript(
                                 value=ast.Name(id='changed_id', ctx=ast.Load()),
                                 slice=ast.Constant(value='type'),
                                 ctx=ast.Load()),
                              ops=[
                                 ast.Eq()],
                              comparators=[
                                 ast.Constant(value='checkboxes')]),
                           body=[
                              ast.If(
                                 test=ast.Compare(
                                    left=ast.Call(
                                       func=ast.Name(id='len', ctx=ast.Load()),
                                       args=[
                                          ast.Name(id='changed_value', ctx=ast.Load())],
                                       keywords=[]),
                                    ops=[
                                       ast.Gt()],
                                    comparators=[
                                       ast.Constant(value=0)]),
                                 body=[
                                    ast.Assign(
                                       targets=[
                                          ast.Name(id='changes', ctx=ast.Store())],
                                       value=ast.Dict(
                                          keys=[
                                             ast.Subscript(
                                                value=ast.Name(id='changed_id', ctx=ast.Load()),
                                                slice=ast.Constant(value='index'),
                                                ctx=ast.Load())],
                                          values=[
                                             ast.Call(
                                                func=ast.Name(id='convert_from_ui', ctx=ast.Load()),
                                                args=[
                                                   ast.Name(id='changed_value', ctx=ast.Load())],
                                                keywords=[])])),
                                    ast.Assign(
                                       targets=[
                                          ast.Name(id='unsat_fields', ctx=ast.Store())],
                                       value=ast.Call(
                                          func=ast.Name(id='propagation_loop', ctx=ast.Load()),
                                          args=[
                                             ast.Name(id='changes', ctx=ast.Load())],
                                          keywords=[])),
                                    ast.If(
                                       test=ast.Compare(
                                          left=ast.Call(
                                             func=ast.Name(id='len', ctx=ast.Load()),
                                             args=[
                                                ast.Name(id='unsat_fields', ctx=ast.Load())],
                                             keywords=[]),
                                          ops=[
                                             ast.Eq()],
                                          comparators=[
                                             ast.Constant(value=0)]),
                                       body=[
                                          ast.Return(
                                             value=ast.Tuple(
                                                elts=[
                                                   ast.ListComp(
                                                      elt=ast.Call(
                                                         func=ast.Name(id='convert_to_ui', ctx=ast.Load()),
                                                         args=[
                                                            ast.Subscript(
                                                               value=ast.Name(id='structure', ctx=ast.Load()),
                                                               slice=ast.Name(id='v', ctx=ast.Load()),
                                                               ctx=ast.Load())],
                                                         keywords=[]),
                                                      generators=[
                                                         ast.comprehension(
                                                            target=ast.Name(id='v', ctx=ast.Store()),
                                                            iter=ast.Name(id='boolean_variables', ctx=ast.Load()),
                                                            ifs=[],
                                                            is_async=0)]),
                                                   ast.ListComp(
                                                      elt=ast.Call(
                                                         func=ast.Name(id='convert_to_ui', ctx=ast.Load()),
                                                         args=[
                                                            ast.Subscript(
                                                               value=ast.Name(id='structure', ctx=ast.Load()),
                                                               slice=ast.Name(id='v', ctx=ast.Load()),
                                                               ctx=ast.Load())],
                                                         keywords=[]),
                                                      generators=[
                                                         ast.comprehension(
                                                            target=ast.Name(id='v', ctx=ast.Store()),
                                                            iter=ast.Name(id='integer_variables', ctx=ast.Load()),
                                                            ifs=[],
                                                            is_async=0)]),
                                                   ast.List(
                                                      elts=[
                                                         ast.Constant(value='No inconsistencies detected yet')],
                                                      ctx=ast.Load())],
                                                ctx=ast.Load()))],
                                       orelse=[
                                          ast.Return(
                                             value=ast.Tuple(
                                                elts=[
                                                   ast.Name(id='checkbox_values', ctx=ast.Load()),
                                                   ast.ListComp(
                                                      elt=ast.Call(
                                                         func=ast.Name(id='convert_to_ui', ctx=ast.Load()),
                                                         args=[
                                                            ast.Subscript(
                                                               value=ast.Name(id='structure', ctx=ast.Load()),
                                                               slice=ast.Name(id='v', ctx=ast.Load()),
                                                               ctx=ast.Load())],
                                                         keywords=[]),
                                                      generators=[
                                                         ast.comprehension(
                                                            target=ast.Name(id='v', ctx=ast.Store()),
                                                            iter=ast.Name(id='integer_variables', ctx=ast.Load()),
                                                            ifs=[],
                                                            is_async=0)]),
                                                   ast.List(
                                                      elts=[
                                                         ast.Call(
                                                            func=ast.Name(id='unsat_message', ctx=ast.Load()),
                                                            args=[
                                                               ast.Name(id='unsat_fields', ctx=ast.Load())],
                                                            keywords=[])],
                                                      ctx=ast.Load())],
                                                ctx=ast.Load()))])],
                                 orelse=[])],
                           orelse=[]),
                        ast.If(
                           test=ast.Compare(
                              left=ast.Subscript(
                                 value=ast.Name(id='changed_id', ctx=ast.Load()),
                                 slice=ast.Constant(value='type'),
                                 ctx=ast.Load()),
                              ops=[
                                 ast.Eq()],
                              comparators=[
                                 ast.Constant(value='dropdown')]),
                           body=[
                              ast.If(
                                 test=ast.Compare(
                                    left=ast.Name(id='changed_value', ctx=ast.Load()),
                                    ops=[
                                       ast.NotEq()],
                                    comparators=[
                                       ast.Constant(value=None)]),
                                 body=[
                                    ast.Assign(
                                       targets=[
                                          ast.Name(id='changes', ctx=ast.Store())],
                                       value=ast.Dict(
                                          keys=[
                                             ast.Subscript(
                                                value=ast.Name(id='changed_id', ctx=ast.Load()),
                                                slice=ast.Constant(value='index'),
                                                ctx=ast.Load())],
                                          values=[
                                             ast.Set(
                                                elts=[
                                                   ast.Name(id='changed_value', ctx=ast.Load())])])),
                                    ast.Assign(
                                       targets=[
                                          ast.Name(id='unsat_fields', ctx=ast.Store())],
                                       value=ast.Call(
                                          func=ast.Name(id='propagation_loop', ctx=ast.Load()),
                                          args=[
                                             ast.Name(id='changes', ctx=ast.Load())],
                                          keywords=[])),
                                    ast.If(
                                       test=ast.Compare(
                                          left=ast.Call(
                                             func=ast.Name(id='len', ctx=ast.Load()),
                                             args=[
                                                ast.Name(id='unsat_fields', ctx=ast.Load())],
                                             keywords=[]),
                                          ops=[
                                             ast.Eq()],
                                          comparators=[
                                             ast.Constant(value=0)]),
                                       body=[
                                          ast.Return(
                                             value=ast.Tuple(
                                                elts=[
                                                   ast.ListComp(
                                                      elt=ast.Call(
                                                         func=ast.Name(id='convert_to_ui', ctx=ast.Load()),
                                                         args=[
                                                            ast.Subscript(
                                                               value=ast.Name(id='structure', ctx=ast.Load()),
                                                               slice=ast.Name(id='v', ctx=ast.Load()),
                                                               ctx=ast.Load())],
                                                         keywords=[]),
                                                      generators=[
                                                         ast.comprehension(
                                                            target=ast.Name(id='v', ctx=ast.Store()),
                                                            iter=ast.Name(id='boolean_variables', ctx=ast.Load()),
                                                            ifs=[],
                                                            is_async=0)]),
                                                   ast.ListComp(
                                                      elt=ast.Call(
                                                         func=ast.Name(id='convert_to_ui', ctx=ast.Load()),
                                                         args=[
                                                            ast.Subscript(
                                                               value=ast.Name(id='structure', ctx=ast.Load()),
                                                               slice=ast.Name(id='v', ctx=ast.Load()),
                                                               ctx=ast.Load())],
                                                         keywords=[]),
                                                      generators=[
                                                         ast.comprehension(
                                                            target=ast.Name(id='v', ctx=ast.Store()),
                                                            iter=ast.Name(id='integer_variables', ctx=ast.Load()),
                                                            ifs=[],
                                                            is_async=0)]),
                                                   ast.List(
                                                      elts=[
                                                         ast.Constant(value='No inconsistencies detected yet')],
                                                      ctx=ast.Load())],
                                                ctx=ast.Load()))],
                                       orelse=[
                                          ast.Return(
                                             value=ast.Tuple(
                                                elts=[
                                                   ast.Name(id='checkbox_values', ctx=ast.Load()),
                                                   ast.ListComp(
                                                      elt=ast.Call(
                                                         func=ast.Name(id='convert_to_ui', ctx=ast.Load()),
                                                         args=[
                                                            ast.Subscript(
                                                               value=ast.Name(id='structure', ctx=ast.Load()),
                                                               slice=ast.Name(id='v', ctx=ast.Load()),
                                                               ctx=ast.Load())],
                                                         keywords=[]),
                                                      generators=[
                                                         ast.comprehension(
                                                            target=ast.Name(id='v', ctx=ast.Store()),
                                                            iter=ast.Name(id='integer_variables', ctx=ast.Load()),
                                                            ifs=[],
                                                            is_async=0)]),
                                                   ast.List(
                                                      elts=[
                                                         ast.Call(
                                                            func=ast.Name(id='unsat_message', ctx=ast.Load()),
                                                            args=[
                                                               ast.Name(id='unsat_fields', ctx=ast.Load())],
                                                            keywords=[])],
                                                      ctx=ast.Load())],
                                                ctx=ast.Load()))])],
                                 orelse=[])],
                           orelse=[])],
                     orelse=[]),
                  ast.Return(
                     value=ast.Tuple(
                        elts=[
                           ast.Name(id='checkbox_values', ctx=ast.Load()),
                           ast.ListComp(
                              elt=ast.Call(
                                 func=ast.Name(id='convert_to_ui', ctx=ast.Load()),
                                 args=[
                                    ast.Subscript(
                                       value=ast.Name(id='structure', ctx=ast.Load()),
                                       slice=ast.Name(id='v', ctx=ast.Load()),
                                       ctx=ast.Load())],
                                 keywords=[]),
                              generators=[
                                 ast.comprehension(
                                    target=ast.Name(id='v', ctx=ast.Store()),
                                    iter=ast.Name(id='integer_variables', ctx=ast.Load()),
                                    ifs=[],
                                    is_async=0)]),
                           ast.List(
                              elts=[
                                 ast.Constant(value='No inconsistencies detected yet')],
                              ctx=ast.Load())],
                        ctx=ast.Load()))],
               decorator_list=[
                  ast.Call(
                     func=ast.Attribute(
                        value=ast.Name(id='app', ctx=ast.Load()),
                        attr='callback',
                        ctx=ast.Load()),
                     args=[
                        ast.List(
                           elts=[
                              ast.Call(
                                 func=ast.Name(id='Output', ctx=ast.Load()),
                                 args=[
                                    ast.Dict(
                                       keys=[
                                          ast.Constant(value='type'),
                                          ast.Constant(value='index')],
                                       values=[
                                          ast.Constant(value='checkboxes'),
                                          ast.Name(id='ALL', ctx=ast.Load())]),
                                    ast.Constant(value='value')],
                                 keywords=[]),
                              ast.Call(
                                 func=ast.Name(id='Output', ctx=ast.Load()),
                                 args=[
                                    ast.Dict(
                                       keys=[
                                          ast.Constant(value='type'),
                                          ast.Constant(value='index')],
                                       values=[
                                          ast.Constant(value='dropdown'),
                                          ast.Name(id='ALL', ctx=ast.Load())]),
                                    ast.Constant(value='options')],
                                 keywords=[]),
                              ast.Call(
                                 func=ast.Name(id='Output', ctx=ast.Load()),
                                 args=[
                                    ast.Dict(
                                       keys=[
                                          ast.Constant(value='type')],
                                       values=[
                                          ast.Constant(value='text-output')]),
                                    ast.Constant(value='children')],
                                 keywords=[])],
                           ctx=ast.Load()),
                        ast.List(
                           elts=[
                              ast.Call(
                                 func=ast.Name(id='Input', ctx=ast.Load()),
                                 args=[
                                    ast.Dict(
                                       keys=[
                                          ast.Constant(value='type'),
                                          ast.Constant(value='index')],
                                       values=[
                                          ast.Constant(value='checkboxes'),
                                          ast.Name(id='ALL', ctx=ast.Load())]),
                                    ast.Constant(value='value')],
                                 keywords=[]),
                              ast.Call(
                                 func=ast.Name(id='Input', ctx=ast.Load()),
                                 args=[
                                    ast.Dict(
                                       keys=[
                                          ast.Constant(value='type'),
                                          ast.Constant(value='index')],
                                       values=[
                                          ast.Constant(value='dropdown'),
                                          ast.Name(id='ALL', ctx=ast.Load())]),
                                    ast.Constant(value='value')],
                                 keywords=[]),
                              ast.Call(
                                 func=ast.Name(id='Input', ctx=ast.Load()),
                                 args=[
                                    ast.Constant(value='reset-button'),
                                    ast.Constant(value='n_clicks')],
                                 keywords=[])],
                           ctx=ast.Load()),
                        ast.List(
                           elts=[
                              ast.Call(
                                 func=ast.Name(id='State', ctx=ast.Load()),
                                 args=[
                                    ast.Dict(
                                       keys=[
                                          ast.Constant(value='type'),
                                          ast.Constant(value='index')],
                                       values=[
                                          ast.Constant(value='checkboxes'),
                                          ast.Name(id='ALL', ctx=ast.Load())]),
                                    ast.Constant(value='id')],
                                 keywords=[]),
                              ast.Call(
                                 func=ast.Name(id='State', ctx=ast.Load()),
                                 args=[
                                    ast.Dict(
                                       keys=[
                                          ast.Constant(value='type'),
                                          ast.Constant(value='index')],
                                       values=[
                                          ast.Constant(value='dropdown'),
                                          ast.Name(id='ALL', ctx=ast.Load())]),
                                    ast.Constant(value='id')],
                                 keywords=[])],
                           ctx=ast.Load())],
                     keywords=[])]),
            ast.Expr(
               value=ast.Call(
                  func=ast.Attribute(
                     value=ast.Name(id='app', ctx=ast.Load()),
                     attr='run_server',
                     ctx=ast.Load()),
                  args=[],
                  keywords=[
                     ast.keyword(
                        arg='debug',
                        value=ast.Constant(value=True))]))],
         decorator_list=[]),
      ast.If(
         test=ast.Compare(
            left=ast.Name(id='__name__', ctx=ast.Load()),
            ops=[
               ast.Eq()],
            comparators=[
               ast.Constant(value='__main__')]),
         body=[
            ast.Expr(
               value=ast.Call(
                  func=ast.Name(id='launch_dash_app', ctx=ast.Load()),
                  args=[],
                  keywords=[]))],
         orelse=[])],
   type_ignores=[])


# Generates AST for a helper function
def generate_dash_application():
    return ast.Module(
   body=[
      ast.ImportFrom(
         module='dash',
         names=[
            ast.alias(name='Dash'),
            ast.alias(name='html'),
            ast.alias(name='dcc'),
            ast.alias(name='State'),
            ast.alias(name='Input'),
            ast.alias(name='Output'),
            ast.alias(name='ALL')],
         level=0),
      ast.Assign(
         targets=[
            ast.Name(id='app', ctx=ast.Store())],
         value=ast.Call(
            func=ast.Name(id='Dash', ctx=ast.Load()),
            args=[
               ast.Name(id='__name__', ctx=ast.Load())],
            keywords=[])),

      ast.Assign(
           targets=[
               ast.Name(id='variables', ctx=ast.Store())],
           value=ast.SetComp(
               elt=ast.Name(id='v', ctx=ast.Load()),
               generators=[
                   ast.comprehension(
                       target=ast.Name(id='v', ctx=ast.Store()),
                       iter=ast.Call(
                           func=ast.Attribute(
                               value=ast.Name(id='structure', ctx=ast.Load()),
                               attr='keys',
                               ctx=ast.Load()),
                           args=[],
                           keywords=[]),
                       ifs=[
                           ast.UnaryOp(
                               op=ast.Not(),
                               operand=ast.Call(
                                   func=ast.Attribute(
                                       value=ast.Name(id='v', ctx=ast.Load()),
                                       attr='startswith',
                                       ctx=ast.Load()),
                                   args=[
                                       ast.Constant(value='_')],
                                   keywords=[]))],
                       is_async=0)])),

       ast.Assign(
         targets=[
            ast.Attribute(
               value=ast.Name(id='app', ctx=ast.Load()),
               attr='layout',
               ctx=ast.Store())],
         value=ast.Call(
            func=ast.Attribute(
               value=ast.Name(id='html', ctx=ast.Load()),
               attr='Div',
               ctx=ast.Load()),
            args=[
               ast.List(
                  elts=[
                     ast.Call(
                        func=ast.Attribute(
                           value=ast.Name(id='html', ctx=ast.Load()),
                           attr='H1',
                           ctx=ast.Load()),
                        args=[
                           ast.Constant(value='Interactive configuration')],
                        keywords=[]),
                     ast.Call(
                        func=ast.Attribute(
                           value=ast.Name(id='html', ctx=ast.Load()),
                           attr='Div',
                           ctx=ast.Load()),
                        args=[
                           ast.SetComp(
                              elt=ast.Call(
                                 func=ast.Attribute(
                                    value=ast.Name(id='html', ctx=ast.Load()),
                                    attr='Div',
                                    ctx=ast.Load()),
                                 args=[
                                    ast.List(
                                       elts=[
                                          ast.Call(
                                             func=ast.Attribute(
                                                value=ast.Name(id='html', ctx=ast.Load()),
                                                attr='Label',
                                                ctx=ast.Load()),
                                             args=[
                                                ast.JoinedStr(
                                                   values=[
                                                      ast.FormattedValue(
                                                         value=ast.Name(id='var', ctx=ast.Load()),
                                                         conversion=-1),
                                                      ast.Constant(value=':')])],
                                             keywords=[]),
                                          ast.Call(
                                             func=ast.Attribute(
                                                value=ast.Name(id='dcc', ctx=ast.Load()),
                                                attr='Checklist',
                                                ctx=ast.Load()),
                                             args=[],
                                             keywords=[
                                                ast.keyword(
                                                   arg='id',
                                                   value=ast.Dict(
                                                      keys=[
                                                         ast.Constant(value='type'),
                                                         ast.Constant(value='index')],
                                                      values=[
                                                         ast.Constant(value='checkboxes'),
                                                         ast.Name(id='var', ctx=ast.Load())])),
                                                ast.keyword(
                                                   arg='options',
                                                   value=ast.List(
                                                      elts=[
                                                         ast.Dict(
                                                            keys=[
                                                               ast.Constant(value='label'),
                                                               ast.Constant(value='value')],
                                                            values=[
                                                               ast.Constant(value='True'),
                                                               ast.Constant(value=True)]),
                                                         ast.Dict(
                                                            keys=[
                                                               ast.Constant(value='label'),
                                                               ast.Constant(value='value')],
                                                            values=[
                                                               ast.Constant(value='False'),
                                                               ast.Constant(value=False)])],
                                                      ctx=ast.Load())),
                                                ast.keyword(
                                                   arg='value',
                                                   value=ast.List(elts=[], ctx=ast.Load())),
                                                ast.keyword(
                                                   arg='inline',
                                                   value=ast.Constant(value=True))]),
                                          ast.Call(
                                             func=ast.Attribute(
                                                value=ast.Name(id='html', ctx=ast.Load()),
                                                attr='Div',
                                                ctx=ast.Load()),
                                             args=[],
                                             keywords=[
                                                ast.keyword(
                                                   arg='id',
                                                   value=ast.Dict(
                                                      keys=[
                                                         ast.Constant(value='type'),
                                                         ast.Constant(value='index')],
                                                      values=[
                                                         ast.Constant(value='output'),
                                                         ast.Name(id='var', ctx=ast.Load())]))])],
                                       ctx=ast.Load())],
                                 keywords=[]),
                              generators=[
                                 ast.comprehension(
                                    target=ast.Name(id='var', ctx=ast.Store()),
                                    iter=ast.Name(id='variables', ctx=ast.Load()),
                                    ifs=[],
                                    is_async=0)])],
                        keywords=[])],
                  ctx=ast.Load())],
            keywords=[])),
      ast.FunctionDef(
         name='update_output',
         args=ast.arguments(
            posonlyargs=[],
            args=[
               ast.arg(arg='selected_values_list'),
               ast.arg(arg='component_id_list')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            ast.Assign(
               targets=[
                  ast.Name(id='updated_values', ctx=ast.Store())],
               value=ast.Dict(keys=[], values=[])),
            ast.For(
               target=ast.Tuple(
                  elts=[
                     ast.Name(id='selected_values', ctx=ast.Store()),
                     ast.Name(id='component_id', ctx=ast.Store())],
                  ctx=ast.Store()),
               iter=ast.Call(
                  func=ast.Name(id='zip', ctx=ast.Load()),
                  args=[
                     ast.Name(id='selected_values_list', ctx=ast.Load()),
                     ast.Name(id='component_id_list', ctx=ast.Load())],
                  keywords=[]),
               body=[
                  ast.Assign(
                     targets=[
                        ast.Name(id='variable_name', ctx=ast.Store())],
                     value=ast.Subscript(
                        value=ast.Name(id='component_id', ctx=ast.Load()),
                        slice=ast.Constant(value='index'),
                        ctx=ast.Load())),
                  ast.If(
                     test=ast.Compare(
                        left=ast.Call(
                           func=ast.Name(id='len', ctx=ast.Load()),
                           args=[
                              ast.Name(id='selected_values', ctx=ast.Load())],
                           keywords=[]),
                        ops=[
                           ast.Gt()],
                        comparators=[
                           ast.Constant(value=0)]),
                     body=[
                        ast.Expr(
                           value=ast.Call(
                              func=ast.Name(id='propagate_loop', ctx=ast.Load()),
                              args=[
                                 ast.Name(id='variable_name', ctx=ast.Load()),
                                 ast.Subscript(
                                    value=ast.Name(id='selected_values', ctx=ast.Load()),
                                    slice=ast.UnaryOp(
                                       op=ast.USub(),
                                       operand=ast.Constant(value=1)),
                                    ctx=ast.Load())],
                              keywords=[])),
                        ast.For(
                           target=ast.Name(id='var', ctx=ast.Store()),
                           iter=ast.Call(
                              func=ast.Attribute(
                                 value=ast.Name(id='structure', ctx=ast.Load()),
                                 attr='keys',
                                 ctx=ast.Load()),
                              args=[],
                              keywords=[]),
                           body=[
                              ast.If(
                                 test=ast.Compare(
                                    left=ast.Subscript(
                                       value=ast.Name(id='structure', ctx=ast.Load()),
                                       slice=ast.Name(id='var', ctx=ast.Load()),
                                       ctx=ast.Load()),
                                    ops=[
                                       ast.NotEq()],
                                    comparators=[
                                       ast.Constant(value=None)]),
                                 body=[
                                    ast.Assign(
                                       targets=[
                                          ast.Subscript(
                                             value=ast.Name(id='updated_values', ctx=ast.Load()),
                                             slice=ast.Name(id='var', ctx=ast.Load()),
                                             ctx=ast.Store())],
                                       value=ast.List(
                                          elts=[
                                             ast.Subscript(
                                                value=ast.Name(id='structure', ctx=ast.Load()),
                                                slice=ast.Name(id='var', ctx=ast.Load()),
                                                ctx=ast.Load())],
                                          ctx=ast.Load()))],
                                 orelse=[])],
                           orelse=[])],
                     orelse=[])],
               orelse=[]),
            ast.Return(
               value=ast.SetComp(
                  elt=ast.Call(
                     func=ast.Attribute(
                        value=ast.Name(id='updated_values', ctx=ast.Load()),
                        attr='get',
                        ctx=ast.Load()),
                     args=[
                        ast.Name(id='var', ctx=ast.Load()),
                        ast.List(elts=[], ctx=ast.Load())],
                     keywords=[]),
                  generators=[
                     ast.comprehension(
                        target=ast.Name(id='var', ctx=ast.Store()),
                        iter=ast.Name(id='variables', ctx=ast.Load()),
                        ifs=[],
                        is_async=0)]))],
         decorator_list=[
            ast.Call(
               func=ast.Attribute(
                  value=ast.Name(id='app', ctx=ast.Load()),
                  attr='callback',
                  ctx=ast.Load()),
               args=[
                  ast.Call(
                     func=ast.Name(id='Output', ctx=ast.Load()),
                     args=[
                        ast.Dict(
                           keys=[
                              ast.Constant(value='type'),
                              ast.Constant(value='index')],
                           values=[
                              ast.Constant(value='checkboxes'),
                              ast.Name(id='ALL', ctx=ast.Load())]),
                        ast.Constant(value='value')],
                     keywords=[]),
                  ast.Call(
                     func=ast.Name(id='Input', ctx=ast.Load()),
                     args=[
                        ast.Dict(
                           keys=[
                              ast.Constant(value='type'),
                              ast.Constant(value='index')],
                           values=[
                              ast.Constant(value='checkboxes'),
                              ast.Name(id='ALL', ctx=ast.Load())]),
                        ast.Constant(value='value')],
                     keywords=[]),
                  ast.Call(
                     func=ast.Name(id='State', ctx=ast.Load()),
                     args=[
                        ast.Dict(
                           keys=[
                              ast.Constant(value='type'),
                              ast.Constant(value='index')],
                           values=[
                              ast.Constant(value='checkboxes'),
                              ast.Name(id='ALL', ctx=ast.Load())]),
                        ast.Constant(value='id')],
                     keywords=[])],
               keywords=[])]),
      ast.If(
         test=ast.Compare(
            left=ast.Name(id='__name__', ctx=ast.Load()),
            ops=[
               ast.Eq()],
            comparators=[
               ast.Constant(value='__main__')]),
         body=[
            ast.Expr(
               value=ast.Call(
                  func=ast.Attribute(
                     value=ast.Name(id='app', ctx=ast.Load()),
                     attr='run_server',
                     ctx=ast.Load()),
                  args=[],
                  keywords=[
                     ast.keyword(
                        arg='debug',
                        value=ast.Constant(value=True))]))],
         orelse=[])],
   type_ignores=[])


















# Generates the initial possible values of all atoms.
# They can initially all be both true and false.
# This can, however, change when the propagate()-function is called for the first time.
def generate_domains(enfs):
    domains = {}
    for enf in enfs:
        if type(enf) == AssertLiteral:
            domains[enf.literal.atom] = {True, False}
        else:
            domains[enf.left.atom] = {True, False}
            for lit in enf.right:
                domains[lit.atom] = {True, False}
    return domains

# Main function that:
#    - first generates the domains of all atoms using the ENF-rules.
#    - next builds the AST for the initial 'structure' containing all atoms and their truth values.
#    - next generates ASTs for all functions in the propagation algorithm, including the main propagate()-function, for which the DerivedPropagator-objects are used
#    - next groups all ASTs together into one and uses the unparse library to convert it to a Python-file
# The third argument of this function determines whether the generated code will work with the terminal, or with an interactive browser application.

def generate(enfs, props, interactive_application=False):
    domains = generate_domains(enfs)
    second_time = time.time()
    initial_structure = generate_initial_structure(enfs, domains)
    print("initial_structure: ", time.time() - second_time)
    update_structure = generate_update_structure()
    print("update_structure: ", time.time() - second_time)
    print_structure = generate_print_structure()
    print("print_structure: ", time.time() - second_time)
    check_unsat_fields = generate_check_unsat_fields()
    print("check_unsat_fields: ", time.time() - second_time)
    intersect_changes = generate_intersect_changes()
    print("intersect_changes: ", time.time() - second_time)
    propagate_function = generate_propagate(props)
    print("propagate_function: ", time.time() - second_time)
    # feedback_loop = generate_feedback_loop() # for interaction with console
    propagation_loop = generate_propagation_loop_with_contradiction_check()
    print("propagation_loop ", time.time() - second_time)
    feedback_loop = generate_feedback_loop_with_contradiction_check()  # for interaction with console, with contradiction checking
    print("feedback_loop ", time.time() - second_time)
    propagate_loop_function = generate_propagate_loop()  # for dash
    dash_application = generate_dash_application()
    print("ast generation: ", time.time() - second_time)
    if not interactive_application:
       module = ast.Module(
           body=[initial_structure, update_structure, print_structure, check_unsat_fields, intersect_changes,
                 propagate_function, propagation_loop, feedback_loop.body], type_ignores=[])
       print("ast before unparse: ", time.time() - second_time)
       code = astunparse.unparse(module)
       print("ast unparse: ", time.time() - second_time)
       with open("first_method_generated_code.py", "w") as file:
          file.write(code)
    else:
       dash_imports = generate_dash_imports()
       first_initial_structure = generate_initial_structure(enfs, domains, "initial_structure")
       current_structure = generate_initial_structure(enfs, domains, "structure")
       handle_reset = generate_handle_reset()
       get_dropdown_options = generate_get_dropdown_options()
       convert_to_ui = generate_convert_to_ui()
       convert_from_ui = generate_convert_from_ui()
       unsat_message = generate_unsat_message()
       launch_dash_app = generate_launch_dash_app()
       dash_module = ast.Module(body=[dash_imports, first_initial_structure, current_structure, update_structure, handle_reset, check_unsat_fields, intersect_changes, propagate_function, propagation_loop, get_dropdown_options, convert_to_ui, convert_from_ui, unsat_message, launch_dash_app.body])
       print("ast before unparse: ", time.time() - second_time)
       code = astunparse.unparse(dash_module)
       print("ast unparse: ", time.time() - second_time)
       with open("first_method_generated_code.py", "w") as file:
          file.write(code)