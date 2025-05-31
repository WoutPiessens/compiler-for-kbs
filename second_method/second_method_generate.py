# This part of the compiler uses all gathered information (propagators, predicates, functions, types) to generate a Python program.
# This Python program can perform propagation inference on the original IDP program.
# First, an abstract syntax tree is built containing all necessary parts of the program.
# Then, using the astunparse library, it is converted to a Python file.

# For more clarity about what the auxiliary functions do, see second_method_generated_code_example.py

from ast import *
import random
import time
from second_method.second_method_parsing import IntegerRange
from second_method.second_method_enf import ENFConjunctive, ENFDisjunctive, ENFExistential, ENFUniversal, ENFReductive, AssertLiteral
from second_method.second_method_propagators import NormalPropagator, SpecifyingPropagator, GeneralizingPropagator, FunctionPropagator

import astunparse

# This class represents objects that will be converted to AST's representing DataArrays of the xarray library.
class TempDataArray:
    def __init__(self, name, dims, coords):
        self.name = name
        self.dims = dims
        self.coords = coords



# This function constructs multidimensional arrays (xarray.DataArray), based on the types, predicates and functions of the original IDP program.
# Every dimension needs to receive a unique name, otherwise xarray.DataArray considers these dimensions as identical.
def construct_data_arrays(types, predicates):
    temp_data_arrays = {}
    type_dict = {t.name : t.domain for t in types}
    for pred in predicates:
        coords = {f"x{i}" : type_dict[t] for i,t in enumerate(pred.argtypes)}
        temp_data_arrays[pred.name] = TempDataArray(pred.name, tuple(coords.keys()), coords)
    #for func in functions:
    #    coords = {f"x{i}" : type_dict[t] for i,t in enumerate(func.argtypes + [func.scopetype])}
    #    temp_data_arrays[';p;' + func.name] = TempDataArray(';p;' + func.name, tuple(coords.keys()), coords)
    return temp_data_arrays


# Determines the list of auxiliary variables that necessarily evaluate to true, hereby speeding up the propagation process.
def determine_true_list(enf_rules):
    true_list = []
    temp_true_list = [enf.literal.atom.name for enf in enf_rules if type(enf) == AssertLiteral and enf.literal.pos and len(enf.literal.atom.args) == 0]

    while len(temp_true_list) > 0:
        new_temp_true_list = []
        for enf_rule in enf_rules:
            if type(enf_rule) != AssertLiteral:
                if enf_rule.left.atom.name in temp_true_list:
                    if type(enf_rule) == ENFConjunctive:
                        for lit in enf_rule.right:
                            if lit.pos:
                                true_list.append(lit.atom.name)
                                new_temp_true_list.append(lit.atom.name)
                    if type(enf_rule) == ENFUniversal:
                        true_list.append(enf_rule.right.atom.name)
                        new_temp_true_list.append(enf_rule.right.atom.name)
        temp_true_list = new_temp_true_list
    return [elem for elem in true_list if elem.startswith('_X')]



# AST of an auxiliary function
def generate_imports():
    return Module(
   body=[
      Import(
         names=[
            alias(name='math')]),
      Import(
         names=[
            alias(name='time')]),
      Import(
         names=[
            alias(name='pickle')]),
      ImportFrom(
         module='enum',
         names=[
            alias(name='Enum')],
         level=0),
      ImportFrom(
         module='itertools',
         names=[
            alias(name='product')],
         level=0),
      Import(
         names=[
            alias(name='xarray', asname='xr')]),
      Import(
         names=[
            alias(name='numpy', asname='np')]),
      ImportFrom(
         module='dash',
         names=[
            alias(name='Dash'),
            alias(name='html'),
            alias(name='dcc'),
            alias(name='State'),
            alias(name='Input'),
            alias(name='Output'),
            alias(name='ALL'),
            alias(name='callback_context')],
         level=0)],
   type_ignores=[])

# AST of an auxiliary function
def generate_auxiliary_classes():
    return Module(
   body=[
       ClassDef(
           name='EB',
           bases=[
               Name(id='Enum', ctx=Load())],
           keywords=[],
           body=[
               Assign(
                   targets=[
                       Name(id='TRUE', ctx=Store())],
                   value=Constant(value=1)),
               Assign(
                   targets=[
                       Name(id='FALSE', ctx=Store())],
                   value=Constant(value=2)),
               Assign(
                   targets=[
                       Name(id='UNKNOWN', ctx=Store())],
                   value=Constant(value=0)),
               Assign(
                   targets=[
                       Name(id='INCONSISTENT', ctx=Store())],
                   value=UnaryOp(
                       op=USub(),
                       operand=Constant(value=1))),
               Assign(
                   targets=[
                       Name(id='NONE', ctx=Store())],
                   value=UnaryOp(
                       op=USub(),
                       operand=Constant(value=2)))],
           decorator_list=[]),
      ClassDef(
         name='Change',
         bases=[],
         keywords=[],
         body=[
            FunctionDef(
               name='__init__',
               args=arguments(
                  posonlyargs=[],
                  args=[
                     arg(arg='self'),
                     arg(arg='name'),
                     arg(arg='true_slicing'),
                     arg(arg='false_slicing')],
                  kwonlyargs=[],
                  kw_defaults=[],
                  defaults=[]),
               body=[
                  Assign(
                     targets=[
                        Attribute(
                           value=Name(id='self', ctx=Load()),
                           attr='name',
                           ctx=Store())],
                     value=Name(id='name', ctx=Load())),
                  Assign(
                     targets=[
                        Attribute(
                           value=Name(id='self', ctx=Load()),
                           attr='true_slicing',
                           ctx=Store())],
                     value=Name(id='true_slicing', ctx=Load())),
                  Assign(
                     targets=[
                        Attribute(
                           value=Name(id='self', ctx=Load()),
                           attr='false_slicing',
                           ctx=Store())],
                     value=Name(id='false_slicing', ctx=Load()))],
               decorator_list=[])],
         decorator_list=[]),
      ClassDef(
         name='LiteralCollection',
         bases=[],
         keywords=[],
         body=[
            FunctionDef(
               name='__init__',
               args=arguments(
                  posonlyargs=[],
                  args=[
                     arg(arg='self'),
                     arg(arg='name'),
                     arg(arg='slicing'),
                     arg(arg='b')],
                  kwonlyargs=[],
                  kw_defaults=[],
                  defaults=[]),
               body=[
                  Assign(
                     targets=[
                        Attribute(
                           value=Name(id='self', ctx=Load()),
                           attr='name',
                           ctx=Store())],
                     value=Name(id='name', ctx=Load())),
                  Assign(
                     targets=[
                        Attribute(
                           value=Name(id='self', ctx=Load()),
                           attr='slicing',
                           ctx=Store())],
                     value=Name(id='slicing', ctx=Load())),
                  Assign(
                     targets=[
                        Attribute(
                           value=Name(id='self', ctx=Load()),
                           attr='b',
                           ctx=Store())],
                     value=Name(id='b', ctx=Load()))],
               decorator_list=[])],
         decorator_list=[]),
      ClassDef(
         name='PropagateResult',
         bases=[],
         keywords=[],
         body=[
            FunctionDef(
               name='__init__',
               args=arguments(
                  posonlyargs=[],
                  args=[
                     arg(arg='self'),
                     arg(arg='truth'),
                     arg(arg='position')],
                  kwonlyargs=[],
                  kw_defaults=[],
                  defaults=[
                     Constant(value=0)]),
               body=[
                  Assign(
                     targets=[
                        Attribute(
                           value=Name(id='self', ctx=Load()),
                           attr='truth',
                           ctx=Store())],
                     value=Name(id='truth', ctx=Load())),
                  Assign(
                     targets=[
                        Attribute(
                           value=Name(id='self', ctx=Load()),
                           attr='position',
                           ctx=Store())],
                     value=Name(id='position', ctx=Load()))],
               decorator_list=[])],
         decorator_list=[])],
   type_ignores=[])

# Determines the size of the domain of a type.
def domain_size(dom):
    if type(dom) == IntegerRange:
        return dom.ub - dom.lb + 1
    else:
        return len(dom)

# Generates the full domain of a type.
def create_full_domain(dom):
    if type(dom) == IntegerRange:
        return list(range(dom.lb, dom.ub+1))
    else:
        return dom


# Generates the AST for DataArrays, based on the TempDataArray objects.
def generate_data_arrays(temp_data_arrays):
    list_elems = []
    for temp_da in temp_data_arrays.values():
        if len(temp_da.dims) == 0:
            data_array = Call(
                  func=Attribute(
                     value=Name(id='xr', ctx=Load()),
                     attr='DataArray',
                     ctx=Load()),
                  args=[
                     Call(
                        func=Attribute(
                           value=Name(id='np', ctx=Load()),
                           attr='array',
                           ctx=Load()),
                        args=[
                           Attribute(
                              value=Name(id='EB', ctx=Load()),
                              attr='UNKNOWN',
                              ctx=Load())],
                        keywords=[])],
                  keywords=[
                     keyword(
                        arg='name',
                        value=Constant(value=temp_da.name))])
            list_elems.append(data_array)
        else:
            dimension_sizes = [Constant(value=domain_size(temp_da.coords[d])) for d in temp_da.dims]
            dimensions = [Constant(value=dim) for dim in temp_da.dims]
            domains = [List(elts=[Constant(value=el) for el in create_full_domain(temp_da.coords[dim])], ctx=Load()) for dim in temp_da.dims]
            data_array = Call(
                  func=Attribute(
                     value=Name(id='xr', ctx=Load()),
                     attr='DataArray',
                     ctx=Load()),
                  args=[
                     Call(
                        func=Attribute(
                           value=Name(id='np', ctx=Load()),
                           attr='full',
                           ctx=Load()),
                        args=[
                           Tuple(
                              elts=dimension_sizes,
                              ctx=Load()),
                           Attribute(
                              value=Name(id='EB', ctx=Load()),
                              attr='UNKNOWN',
                              ctx=Load())],
                        keywords=[])],
                  keywords=[
                     keyword(
                        arg='name',
                        value=Constant(value=temp_da.name)),
                     keyword(
                        arg='dims',
                        value=Tuple(
                           elts=dimensions,
                           ctx=Load())),
                     keyword(
                        arg='coords',
                        value=Dict(
                           keys=dimensions,
                           values=domains))])
            list_elems.append(data_array)
    return Module(
   body=[
      Assign(
         targets=[
            Name(id='predicates', ctx=Store())],
         value=List(
            elts=list_elems,
            ctx=Load()))],
   type_ignores=[])

# AST of an auxiliary function
def generate_data_arrays_extra():
    return Module(body=[Assign(
         targets=[
            Name(id='predicate_dict', ctx=Store())],
         value=DictComp(
            key=Attribute(
               value=Name(id='pred', ctx=Load()),
               attr='name',
               ctx=Load()),
            value=Name(id='pred', ctx=Load()),
            generators=[
               comprehension(
                  target=Name(id='pred', ctx=Store()),
                  iter=Name(id='predicates', ctx=Load()),
                  ifs=[],
                  is_async=0)]))],
   type_ignores=[])

# AST of an auxiliary function
def generate_data_arrays_extra_dash():
    return Module(
   body=[
      Assign(
         targets=[
            Name(id='predicate_dict_original', ctx=Store())],
         value=DictComp(
            key=Attribute(
               value=Name(id='pred', ctx=Load()),
               attr='name',
               ctx=Load()),
            value=Name(id='pred', ctx=Load()),
            generators=[
               comprehension(
                  target=Name(id='pred', ctx=Store()),
                  iter=Name(id='predicates', ctx=Load()),
                  ifs=[],
                  is_async=0)])),
      Assign(
         targets=[
            Name(id='predicate_dict', ctx=Store())],
         value=DictComp(
            key=Attribute(
               value=Name(id='pred', ctx=Load()),
               attr='name',
               ctx=Load()),
            value=Call(
               func=Attribute(
                  value=Name(id='pred', ctx=Load()),
                  attr='copy',
                  ctx=Load()),
               args=[],
               keywords=[
                  keyword(
                     arg='deep',
                     value=Constant(value=True))]),
            generators=[
               comprehension(
                  target=Name(id='pred', ctx=Store()),
                  iter=Name(id='predicates', ctx=Load()),
                  ifs=[],
                  is_async=0)])),
      FunctionDef(
         name='handle_reset',
         args=arguments(
            posonlyargs=[],
            args=[],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            For(
               target=Name(id='pred_name', ctx=Store()),
               iter=Call(
                  func=Attribute(
                     value=Name(id='predicate_dict', ctx=Load()),
                     attr='keys',
                     ctx=Load()),
                  args=[],
                  keywords=[]),
               body=[
                  Assign(
                     targets=[
                        Subscript(
                           value=Name(id='predicate_dict', ctx=Load()),
                           slice=Name(id='pred_name', ctx=Load()),
                           ctx=Store())],
                     value=Call(
                        func=Attribute(
                           value=Subscript(
                              value=Name(id='predicate_dict_original', ctx=Load()),
                              slice=Name(id='pred_name', ctx=Load()),
                              ctx=Load()),
                           attr='copy',
                           ctx=Load()),
                        args=[],
                        keywords=[
                           keyword(
                              arg='deep',
                              value=Constant(value=True))]))],
               orelse=[])],
         decorator_list=[])],
   type_ignores=[])


# AST for two auxiliary lists
def generate_true_and_unknown_lists(true_list):
    true_list_ast = []
    for elem in true_list:
        true_list_ast.append(Constant(value=elem))
    return Module(
   body=[
      Assign(
         targets=[
            Name(id='true_list', ctx=Store())],
         value=List(
            elts=true_list_ast,
            ctx=Load())),
      Assign(
         targets=[
            Name(id='unknown_list', ctx=Store())],
         value=ListComp(
            elt=Attribute(
               value=Name(id='pred', ctx=Load()),
               attr='name',
               ctx=Load()),
            generators=[
               comprehension(
                  target=Name(id='pred', ctx=Store()),
                  iter=Name(id='predicates', ctx=Load()),
                  ifs=[],
                  is_async=0)]))],
   type_ignores=[])



# AST of an auxiliary function
def generate_conditional_propagate():
    return Module(
   body=[
      FunctionDef(
         name='conditional_propagate',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='args')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='mask', ctx=Store())],
               value=Compare(
                  left=Name(id='args', ctx=Load()),
                  ops=[
                     NotEq()],
                  comparators=[
                     Attribute(
                        value=Name(id='EB', ctx=Load()),
                        attr='TRUE',
                        ctx=Load())])),
            Assign(
               targets=[
                  Name(id='s', ctx=Store())],
               value=Call(
                  func=Attribute(
                     value=Name(id='mask', ctx=Load()),
                     attr='sum',
                     ctx=Load()),
                  args=[],
                  keywords=[])),
            If(
               test=Compare(
                  left=Name(id='s', ctx=Load()),
                  ops=[
                     Eq()],
                  comparators=[
                     Constant(value=1)]),
               body=[
                  Assign(
                     targets=[
                        Name(id='index', ctx=Store())],
                     value=Subscript(
                        value=Subscript(
                           value=Call(
                              func=Attribute(
                                 value=Name(id='np', ctx=Load()),
                                 attr='where',
                                 ctx=Load()),
                              args=[
                                 Name(id='mask', ctx=Load())],
                              keywords=[]),
                           slice=Constant(value=0),
                           ctx=Load()),
                        slice=Constant(value=0),
                        ctx=Load())),
                  If(
                     test=Compare(
                        left=Subscript(
                           value=Name(id='args', ctx=Load()),
                           slice=Name(id='index', ctx=Load()),
                           ctx=Load()),
                        ops=[
                           Eq()],
                        comparators=[
                           Attribute(
                              value=Name(id='EB', ctx=Load()),
                              attr='UNKNOWN',
                              ctx=Load())]),
                     body=[
                        Return(
                           value=Call(
                              func=Name(id='PropagateResult', ctx=Load()),
                              args=[
                                 Attribute(
                                    value=Name(id='EB', ctx=Load()),
                                    attr='TRUE',
                                    ctx=Load()),
                                 Call(
                                    func=Attribute(
                                       value=Name(id='index', ctx=Load()),
                                       attr='item',
                                       ctx=Load()),
                                    args=[],
                                    keywords=[])],
                              keywords=[]))],
                     orelse=[]),
                  Return(
                     value=Call(
                        func=Name(id='PropagateResult', ctx=Load()),
                        args=[
                           Attribute(
                              value=Name(id='EB', ctx=Load()),
                              attr='NONE',
                              ctx=Load())],
                        keywords=[]))],
               orelse=[]),
            If(
               test=Compare(
                  left=Name(id='s', ctx=Load()),
                  ops=[
                     Eq()],
                  comparators=[
                     Constant(value=0)]),
               body=[
                  Return(
                     value=Call(
                        func=Name(id='PropagateResult', ctx=Load()),
                        args=[
                           Attribute(
                              value=Name(id='EB', ctx=Load()),
                              attr='INCONSISTENT',
                              ctx=Load())],
                        keywords=[]))],
               orelse=[]),
            Return(
               value=Call(
                  func=Name(id='PropagateResult', ctx=Load()),
                  args=[
                     Attribute(
                        value=Name(id='EB', ctx=Load()),
                        attr='NONE',
                        ctx=Load())],
                  keywords=[]))],
         decorator_list=[])],
   type_ignores=[])

# AST of an auxiliary function
def generate_unconditional_propagate():
    return Module(
   body=[
      FunctionDef(
         name='unconditional_propagate',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='args')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='mapping', ctx=Store())],
               value=Dict(
                  keys=[
                     Attribute(
                        value=Name(id='EB', ctx=Load()),
                        attr='UNKNOWN',
                        ctx=Load()),
                     Attribute(
                        value=Name(id='EB', ctx=Load()),
                        attr='TRUE',
                        ctx=Load()),
                     Attribute(
                        value=Name(id='EB', ctx=Load()),
                        attr='FALSE',
                        ctx=Load())],
                  values=[
                     Attribute(
                        value=Name(id='EB', ctx=Load()),
                        attr='TRUE',
                        ctx=Load()),
                     Attribute(
                        value=Name(id='EB', ctx=Load()),
                        attr='NONE',
                        ctx=Load()),
                     Attribute(
                        value=Name(id='EB', ctx=Load()),
                        attr='INCONSISTENT',
                        ctx=Load())])),
            Return(
               value=ListComp(
                  elt=Call(
                     func=Attribute(
                        value=Name(id='mapping', ctx=Load()),
                        attr='get',
                        ctx=Load()),
                     args=[
                        Name(id='arg', ctx=Load()),
                        Name(id='arg', ctx=Load())],
                     keywords=[]),
                  generators=[
                     comprehension(
                        target=Name(id='arg', ctx=Store()),
                        iter=Name(id='args', ctx=Load()),
                        ifs=[],
                        is_async=0)]))],
         decorator_list=[])],
   type_ignores=[])

# AST of an auxiliary function
def generate_get_from_data_array():
    return Module(
   body=[
      FunctionDef(
         name='get_from_data_array',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='data_array'),
               arg(arg='slices'),
               arg(arg='threshold')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[
               Constant(value=100)]),
         body=[
            If(
               test=Compare(
                  left=Call(
                     func=Name(id='len', ctx=Load()),
                     args=[
                        Name(id='slices', ctx=Load())],
                     keywords=[]),
                  ops=[
                     Gt()],
                  comparators=[
                     Name(id='threshold', ctx=Load())]),
               body=[
                  Assign(
                     targets=[
                        Name(id='vals', ctx=Store())],
                     value=Attribute(
                        value=Subscript(
                           value=Attribute(
                              value=Call(
                                 func=Attribute(
                                    value=Name(id='data_array', ctx=Load()),
                                    attr='stack',
                                    ctx=Load()),
                                 args=[],
                                 keywords=[
                                    keyword(
                                       arg='points',
                                       value=Attribute(
                                          value=Name(id='data_array', ctx=Load()),
                                          attr='dims',
                                          ctx=Load()))]),
                              attr='loc',
                              ctx=Load()),
                           slice=Name(id='slices', ctx=Load()),
                           ctx=Load()),
                        attr='values',
                        ctx=Load()))],
               orelse=[
                  Assign(
                     targets=[
                        Name(id='index_list', ctx=Store())],
                     value=ListComp(
                        elt=Call(
                           func=Name(id='dict', ctx=Load()),
                           args=[
                              Call(
                                 func=Name(id='zip', ctx=Load()),
                                 args=[
                                    Attribute(
                                       value=Name(id='data_array', ctx=Load()),
                                       attr='dims',
                                       ctx=Load()),
                                    Name(id='t', ctx=Load())],
                                 keywords=[])],
                           keywords=[]),
                        generators=[
                           comprehension(
                              target=Name(id='t', ctx=Store()),
                              iter=Name(id='slices', ctx=Load()),
                              ifs=[],
                              is_async=0)])),
                  Assign(
                     targets=[
                        Name(id='vals', ctx=Store())],
                     value=ListComp(
                        elt=Call(
                           func=Attribute(
                              value=Attribute(
                                 value=Subscript(
                                    value=Attribute(
                                       value=Name(id='data_array', ctx=Load()),
                                       attr='loc',
                                       ctx=Load()),
                                    slice=Name(id='i', ctx=Load()),
                                    ctx=Load()),
                                 attr='values',
                                 ctx=Load()),
                              attr='item',
                              ctx=Load()),
                           args=[],
                           keywords=[]),
                        generators=[
                           comprehension(
                              target=Name(id='i', ctx=Store()),
                              iter=Name(id='index_list', ctx=Load()),
                              ifs=[],
                              is_async=0)]))]),
            Return(
               value=Name(id='vals', ctx=Load()))],
         decorator_list=[])],
   type_ignores=[])

# AST of an auxiliary function
def generate_inverse():
    return Module(
   body=[
      FunctionDef(
         name='inverse',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='x')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            If(
               test=Compare(
                  left=Name(id='x', ctx=Load()),
                  ops=[
                     Eq()],
                  comparators=[
                     Attribute(
                        value=Name(id='EB', ctx=Load()),
                        attr='TRUE',
                        ctx=Load())]),
               body=[
                  Return(
                     value=Attribute(
                        value=Name(id='EB', ctx=Load()),
                        attr='FALSE',
                        ctx=Load()))],
               orelse=[]),
            If(
               test=Compare(
                  left=Name(id='x', ctx=Load()),
                  ops=[
                     Eq()],
                  comparators=[
                     Attribute(
                        value=Name(id='EB', ctx=Load()),
                        attr='FALSE',
                        ctx=Load())]),
               body=[
                  Return(
                     value=Attribute(
                        value=Name(id='EB', ctx=Load()),
                        attr='TRUE',
                        ctx=Load()))],
               orelse=[]),
            Return(
               value=Name(id='x', ctx=Load()))],
         decorator_list=[])],
   type_ignores=[])

# AST of an auxiliary function
def generate_append_changes():
    return Module(
        body=[
            FunctionDef(
                name='append_changes',
                args=arguments(
                    posonlyargs=[],
                    args=[
                        arg(arg='old'),
                        arg(arg='new')],
                    kwonlyargs=[],
                    kw_defaults=[],
                    defaults=[]),
                body=[
                    Global(
                        names=[
                            'unknown_list']),
                    For(
                        target=Name(id='key', ctx=Store()),
                        iter=Call(
                            func=Attribute(
                                value=Name(id='new', ctx=Load()),
                                attr='keys',
                                ctx=Load()),
                            args=[],
                            keywords=[]),
                        body=[
                            If(
                                test=Compare(
                                    left=Name(id='key', ctx=Load()),
                                    ops=[
                                        In()],
                                    comparators=[
                                        Call(
                                            func=Attribute(
                                                value=Name(id='old', ctx=Load()),
                                                attr='keys',
                                                ctx=Load()),
                                            args=[],
                                            keywords=[])]),
                                body=[
                                    Expr(
                                        value=Call(
                                            func=Attribute(
                                                value=Attribute(
                                                    value=Subscript(
                                                        value=Name(id='old', ctx=Load()),
                                                        slice=Name(id='key', ctx=Load()),
                                                        ctx=Load()),
                                                    attr='true_slicing',
                                                    ctx=Load()),
                                                attr='extend',
                                                ctx=Load()),
                                            args=[
                                                Attribute(
                                                    value=Subscript(
                                                        value=Name(id='new', ctx=Load()),
                                                        slice=Name(id='key', ctx=Load()),
                                                        ctx=Load()),
                                                    attr='true_slicing',
                                                    ctx=Load())],
                                            keywords=[])),
                                    Expr(
                                        value=Call(
                                            func=Attribute(
                                                value=Attribute(
                                                    value=Subscript(
                                                        value=Name(id='old', ctx=Load()),
                                                        slice=Name(id='key', ctx=Load()),
                                                        ctx=Load()),
                                                    attr='false_slicing',
                                                    ctx=Load()),
                                                attr='extend',
                                                ctx=Load()),
                                            args=[
                                                Attribute(
                                                    value=Subscript(
                                                        value=Name(id='new', ctx=Load()),
                                                        slice=Name(id='key', ctx=Load()),
                                                        ctx=Load()),
                                                    attr='false_slicing',
                                                    ctx=Load())],
                                            keywords=[]))],
                                orelse=[
                                    Assign(
                                        targets=[
                                            Subscript(
                                                value=Name(id='old', ctx=Load()),
                                                slice=Name(id='key', ctx=Load()),
                                                ctx=Store())],
                                        value=Call(
                                            func=Name(id='Change', ctx=Load()),
                                            args=[
                                                Name(id='key', ctx=Load()),
                                                Attribute(
                                                    value=Subscript(
                                                        value=Name(id='new', ctx=Load()),
                                                        slice=Name(id='key', ctx=Load()),
                                                        ctx=Load()),
                                                    attr='true_slicing',
                                                    ctx=Load()),
                                                Attribute(
                                                    value=Subscript(
                                                        value=Name(id='new', ctx=Load()),
                                                        slice=Name(id='key', ctx=Load()),
                                                        ctx=Load()),
                                                    attr='false_slicing',
                                                    ctx=Load())],
                                            keywords=[]))])],
                        orelse=[]),
                    Assign(
                        targets=[
                            Name(id='unknown_list', ctx=Store())],
                        value=ListComp(
                            elt=Name(id='elem', ctx=Load()),
                            generators=[
                                comprehension(
                                    target=Name(id='elem', ctx=Store()),
                                    iter=Name(id='unknown_list', ctx=Load()),
                                    ifs=[
                                        Compare(
                                            left=Name(id='elem', ctx=Load()),
                                            ops=[
                                                NotIn()],
                                            comparators=[
                                                Call(
                                                    func=Attribute(
                                                        value=Name(id='new', ctx=Load()),
                                                        attr='keys',
                                                        ctx=Load()),
                                                    args=[],
                                                    keywords=[])])],
                                    is_async=0)]))],
                decorator_list=[])],
        type_ignores=[])


# AST of an auxiliary function
def generate_get_from_data_array_wrap():
    return Module(
   body=[
      FunctionDef(
         name='get_from_data_array_wrap',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='name'),
               arg(arg='slice'),
               arg(arg='bool')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            If(
               test=Compare(
                  left=Name(id='name', ctx=Load()),
                  ops=[
                     Eq()],
                  comparators=[
                     Constant(value=';EQ')]),
               body=[
                  Assign(
                     targets=[
                        Name(id='temp_result', ctx=Store())],
                     value=ListComp(
                        elt=IfExp(
                           test=Compare(
                              left=Subscript(
                                 value=Name(id='s', ctx=Load()),
                                 slice=Constant(value=0),
                                 ctx=Load()),
                              ops=[
                                 Eq()],
                              comparators=[
                                 Subscript(
                                    value=Name(id='s', ctx=Load()),
                                    slice=Constant(value=1),
                                    ctx=Load())]),
                           body=Attribute(
                              value=Name(id='EB', ctx=Load()),
                              attr='TRUE',
                              ctx=Load()),
                           orelse=Attribute(
                              value=Name(id='EB', ctx=Load()),
                              attr='FALSE',
                              ctx=Load())),
                        generators=[
                           comprehension(
                              target=Name(id='s', ctx=Store()),
                              iter=Name(id='slice', ctx=Load()),
                              ifs=[],
                              is_async=0)]))],
               orelse=[
                  If(
                     test=Compare(
                        left=Name(id='name', ctx=Load()),
                        ops=[
                           Eq()],
                        comparators=[
                           Constant(value='_NEQ')]),
                     body=[
                        Assign(
                           targets=[
                              Name(id='temp_result', ctx=Store())],
                           value=ListComp(
                              elt=IfExp(
                                 test=Compare(
                                    left=Subscript(
                                       value=Name(id='s', ctx=Load()),
                                       slice=Constant(value=0),
                                       ctx=Load()),
                                    ops=[
                                       NotEq()],
                                    comparators=[
                                       Subscript(
                                          value=Name(id='s', ctx=Load()),
                                          slice=Constant(value=1),
                                          ctx=Load())]),
                                 body=Attribute(
                                    value=Name(id='EB', ctx=Load()),
                                    attr='TRUE',
                                    ctx=Load()),
                                 orelse=Attribute(
                                    value=Name(id='EB', ctx=Load()),
                                    attr='FALSE',
                                    ctx=Load())),
                              generators=[
                                 comprehension(
                                    target=Name(id='s', ctx=Store()),
                                    iter=Name(id='slice', ctx=Load()),
                                    ifs=[],
                                    is_async=0)]))],
                     orelse=[
                        If(
                           test=Compare(
                              left=Name(id='name', ctx=Load()),
                              ops=[
                                 Eq()],
                              comparators=[
                                 Constant(value='_LEQ')]),
                           body=[
                              Assign(
                                 targets=[
                                    Name(id='temp_result', ctx=Store())],
                                 value=ListComp(
                                    elt=IfExp(
                                       test=Compare(
                                          left=Subscript(
                                             value=Name(id='s', ctx=Load()),
                                             slice=Constant(value=0),
                                             ctx=Load()),
                                          ops=[
                                             LtE()],
                                          comparators=[
                                             Subscript(
                                                value=Name(id='s', ctx=Load()),
                                                slice=Constant(value=1),
                                                ctx=Load())]),
                                       body=Attribute(
                                          value=Name(id='EB', ctx=Load()),
                                          attr='TRUE',
                                          ctx=Load()),
                                       orelse=Attribute(
                                          value=Name(id='EB', ctx=Load()),
                                          attr='FALSE',
                                          ctx=Load())),
                                    generators=[
                                       comprehension(
                                          target=Name(id='s', ctx=Store()),
                                          iter=Name(id='slice', ctx=Load()),
                                          ifs=[],
                                          is_async=0)]))],
                           orelse=[
                              If(
                                 test=Compare(
                                    left=Name(id='name', ctx=Load()),
                                    ops=[
                                       Eq()],
                                    comparators=[
                                       Constant(value='_LE')]),
                                 body=[
                                    Assign(
                                       targets=[
                                          Name(id='temp_result', ctx=Store())],
                                       value=ListComp(
                                          elt=IfExp(
                                             test=Compare(
                                                left=Subscript(
                                                   value=Name(id='s', ctx=Load()),
                                                   slice=Constant(value=0),
                                                   ctx=Load()),
                                                ops=[
                                                   Lt()],
                                                comparators=[
                                                   Subscript(
                                                      value=Name(id='s', ctx=Load()),
                                                      slice=Constant(value=1),
                                                      ctx=Load())]),
                                             body=Attribute(
                                                value=Name(id='EB', ctx=Load()),
                                                attr='TRUE',
                                                ctx=Load()),
                                             orelse=Attribute(
                                                value=Name(id='EB', ctx=Load()),
                                                attr='FALSE',
                                                ctx=Load())),
                                          generators=[
                                             comprehension(
                                                target=Name(id='s', ctx=Store()),
                                                iter=Name(id='slice', ctx=Load()),
                                                ifs=[],
                                                is_async=0)]))],
                                 orelse=[
                                    If(
                                       test=Compare(
                                          left=Name(id='name', ctx=Load()),
                                          ops=[
                                             Eq()],
                                          comparators=[
                                             Constant(value='_GE')]),
                                       body=[
                                          Assign(
                                             targets=[
                                                Name(id='temp_result', ctx=Store())],
                                             value=ListComp(
                                                elt=IfExp(
                                                   test=Compare(
                                                      left=Subscript(
                                                         value=Name(id='s', ctx=Load()),
                                                         slice=Constant(value=0),
                                                         ctx=Load()),
                                                      ops=[
                                                         Gt()],
                                                      comparators=[
                                                         Subscript(
                                                            value=Name(id='s', ctx=Load()),
                                                            slice=Constant(value=1),
                                                            ctx=Load())]),
                                                   body=Attribute(
                                                      value=Name(id='EB', ctx=Load()),
                                                      attr='TRUE',
                                                      ctx=Load()),
                                                   orelse=Attribute(
                                                      value=Name(id='EB', ctx=Load()),
                                                      attr='FALSE',
                                                      ctx=Load())),
                                                generators=[
                                                   comprehension(
                                                      target=Name(id='s', ctx=Store()),
                                                      iter=Name(id='slice', ctx=Load()),
                                                      ifs=[],
                                                      is_async=0)]))],
                                       orelse=[
                                          If(
                                             test=Compare(
                                                left=Name(id='name', ctx=Load()),
                                                ops=[
                                                   Eq()],
                                                comparators=[
                                                   Constant(value='_GEQ')]),
                                             body=[
                                                Assign(
                                                   targets=[
                                                      Name(id='temp_result', ctx=Store())],
                                                   value=ListComp(
                                                      elt=IfExp(
                                                         test=Compare(
                                                            left=Subscript(
                                                               value=Name(id='s', ctx=Load()),
                                                               slice=Constant(value=0),
                                                               ctx=Load()),
                                                            ops=[
                                                               GtE()],
                                                            comparators=[
                                                               Subscript(
                                                                  value=Name(id='s', ctx=Load()),
                                                                  slice=Constant(value=1),
                                                                  ctx=Load())]),
                                                         body=Attribute(
                                                            value=Name(id='EB', ctx=Load()),
                                                            attr='TRUE',
                                                            ctx=Load()),
                                                         orelse=Attribute(
                                                            value=Name(id='EB', ctx=Load()),
                                                            attr='FALSE',
                                                            ctx=Load())),
                                                      generators=[
                                                         comprehension(
                                                            target=Name(id='s', ctx=Store()),
                                                            iter=Name(id='slice', ctx=Load()),
                                                            ifs=[],
                                                            is_async=0)]))],
                                             orelse=[
                                                If(
                                                   test=Compare(
                                                      left=Name(id='name', ctx=Load()),
                                                      ops=[
                                                         In()],
                                                      comparators=[
                                                         Name(id='true_list', ctx=Load())]),
                                                   body=[
                                                      Assign(
                                                         targets=[
                                                            Name(id='temp_result', ctx=Store())],
                                                         value=ListComp(
                                                            elt=Attribute(
                                                               value=Name(id='EB', ctx=Load()),
                                                               attr='TRUE',
                                                               ctx=Load()),
                                                            generators=[
                                                               comprehension(
                                                                  target=Name(id='_', ctx=Store()),
                                                                  iter=Name(id='slice', ctx=Load()),
                                                                  ifs=[],
                                                                  is_async=0)]))],
                                                   orelse=[
                                                      If(
                                                         test=Compare(
                                                            left=Name(id='name', ctx=Load()),
                                                            ops=[
                                                               In()],
                                                            comparators=[
                                                               Name(id='unknown_list', ctx=Load())]),
                                                         body=[
                                                            Return(
                                                               value=ListComp(
                                                                  elt=Attribute(
                                                                     value=Name(id='EB', ctx=Load()),
                                                                     attr='UNKNOWN',
                                                                     ctx=Load()),
                                                                  generators=[
                                                                     comprehension(
                                                                        target=Name(id='_', ctx=Store()),
                                                                        iter=Name(id='slice', ctx=Load()),
                                                                        ifs=[],
                                                                        is_async=0)]))],
                                                         orelse=[
                                                            Assign(
                                                               targets=[
                                                                  Name(id='temp_result', ctx=Store())],
                                                               value=Call(
                                                                  func=Name(id='get_from_data_array', ctx=Load()),
                                                                  args=[
                                                                     Subscript(
                                                                        value=Name(id='predicate_dict', ctx=Load()),
                                                                        slice=Name(id='name', ctx=Load()),
                                                                        ctx=Load()),
                                                                     Name(id='slice', ctx=Load())],
                                                                  keywords=[]))])])])])])])])]),
            If(
               test=Name(id='bool', ctx=Load()),
               body=[
                  Return(
                     value=Name(id='temp_result', ctx=Load()))],
               orelse=[
                  Return(
                     value=Call(
                        func=Call(
                           func=Attribute(
                              value=Name(id='np', ctx=Load()),
                              attr='vectorize',
                              ctx=Load()),
                           args=[
                              Name(id='inverse', ctx=Load())],
                           keywords=[]),
                        args=[
                           Name(id='temp_result', ctx=Load())],
                        keywords=[]))])],
         decorator_list=[])],
   type_ignores=[])

# AST of an auxiliary function
def generate_write_to_data_array():
    return Module(
   body=[
      FunctionDef(
         name='write_to_data_array',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='slice_dict')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='new_changes', ctx=Store())],
               value=Dict(keys=[], values=[])),
            For(
               target=Name(id='p', ctx=Store()),
               iter=Call(
                  func=Attribute(
                     value=Name(id='slice_dict', ctx=Load()),
                     attr='keys',
                     ctx=Load()),
                  args=[],
                  keywords=[]),
               body=[
                  If(
                     test=Compare(
                        left=Call(
                           func=Name(id='len', ctx=Load()),
                           args=[
                              Subscript(
                                 value=Name(id='slice_dict', ctx=Load()),
                                 slice=Name(id='p', ctx=Load()),
                                 ctx=Load())],
                           keywords=[]),
                        ops=[
                           Gt()],
                        comparators=[
                           Constant(value=100)]),
                     body=[
                        Assign(
                           targets=[
                              Name(id='da', ctx=Store())],
                           value=Subscript(
                              value=Name(id='predicate_dict', ctx=Load()),
                              slice=Attribute(
                                 value=Name(id='p', ctx=Load()),
                                 attr='name',
                                 ctx=Load()),
                              ctx=Load())),
                        Assign(
                           targets=[
                              Name(id='stacked', ctx=Store())],
                           value=Call(
                              func=Attribute(
                                 value=Subscript(
                                    value=Name(id='predicate_dict', ctx=Load()),
                                    slice=Attribute(
                                       value=Name(id='p', ctx=Load()),
                                       attr='name',
                                       ctx=Load()),
                                    ctx=Load()),
                                 attr='stack',
                                 ctx=Load()),
                              args=[],
                              keywords=[
                                 keyword(
                                    arg='points',
                                    value=Attribute(
                                       value=Name(id='da', ctx=Load()),
                                       attr='dims',
                                       ctx=Load()))])),
                        If(
                           test=Attribute(
                              value=Name(id='p', ctx=Load()),
                              attr='b',
                              ctx=Load()),
                           body=[
                              Assign(
                                 targets=[
                                    Subscript(
                                       value=Attribute(
                                          value=Name(id='stacked', ctx=Load()),
                                          attr='loc',
                                          ctx=Load()),
                                       slice=Subscript(
                                          value=Name(id='slice_dict', ctx=Load()),
                                          slice=Name(id='p', ctx=Load()),
                                          ctx=Load()),
                                       ctx=Store())],
                                 value=Attribute(
                                    value=Name(id='EB', ctx=Load()),
                                    attr='FALSE',
                                    ctx=Load())),
                              Expr(
                                 value=Call(
                                    func=Name(id='append_changes', ctx=Load()),
                                    args=[
                                       Name(id='new_changes', ctx=Load()),
                                       Dict(
                                          keys=[
                                             Attribute(
                                                value=Name(id='p', ctx=Load()),
                                                attr='name',
                                                ctx=Load())],
                                          values=[
                                             Call(
                                                func=Name(id='Change', ctx=Load()),
                                                args=[
                                                   Attribute(
                                                      value=Name(id='p', ctx=Load()),
                                                      attr='name',
                                                      ctx=Load()),
                                                   List(elts=[], ctx=Load()),
                                                   Subscript(
                                                      value=Name(id='slice_dict', ctx=Load()),
                                                      slice=Name(id='p', ctx=Load()),
                                                      ctx=Load())],
                                                keywords=[])])],
                                    keywords=[]))],
                           orelse=[
                              Assign(
                                 targets=[
                                    Subscript(
                                       value=Attribute(
                                          value=Name(id='stacked', ctx=Load()),
                                          attr='loc',
                                          ctx=Load()),
                                       slice=Subscript(
                                          value=Name(id='slice_dict', ctx=Load()),
                                          slice=Name(id='p', ctx=Load()),
                                          ctx=Load()),
                                       ctx=Store())],
                                 value=Attribute(
                                    value=Name(id='EB', ctx=Load()),
                                    attr='TRUE',
                                    ctx=Load())),
                              Expr(
                                 value=Call(
                                    func=Name(id='append_changes', ctx=Load()),
                                    args=[
                                       Name(id='new_changes', ctx=Load()),
                                       Dict(
                                          keys=[
                                             Attribute(
                                                value=Name(id='p', ctx=Load()),
                                                attr='name',
                                                ctx=Load())],
                                          values=[
                                             Call(
                                                func=Name(id='Change', ctx=Load()),
                                                args=[
                                                   Attribute(
                                                      value=Name(id='p', ctx=Load()),
                                                      attr='name',
                                                      ctx=Load()),
                                                   Subscript(
                                                      value=Name(id='slice_dict', ctx=Load()),
                                                      slice=Name(id='p', ctx=Load()),
                                                      ctx=Load()),
                                                   List(elts=[], ctx=Load())],
                                                keywords=[])])],
                                    keywords=[]))]),
                        Assign(
                           targets=[
                              Subscript(
                                 value=Name(id='predicate_dict', ctx=Load()),
                                 slice=Attribute(
                                    value=Name(id='p', ctx=Load()),
                                    attr='name',
                                    ctx=Load()),
                                 ctx=Store())],
                           value=Call(
                              func=Attribute(
                                 value=Name(id='stacked', ctx=Load()),
                                 attr='unstack',
                                 ctx=Load()),
                              args=[],
                              keywords=[]))],
                     orelse=[
                        If(
                           test=Attribute(
                              value=Name(id='p', ctx=Load()),
                              attr='b',
                              ctx=Load()),
                           body=[
                              For(
                                 target=Name(id='s', ctx=Store()),
                                 iter=Subscript(
                                    value=Name(id='slice_dict', ctx=Load()),
                                    slice=Name(id='p', ctx=Load()),
                                    ctx=Load()),
                                 body=[
                                    Assign(
                                       targets=[
                                          Subscript(
                                             value=Attribute(
                                                value=Subscript(
                                                   value=Name(id='predicate_dict', ctx=Load()),
                                                   slice=Attribute(
                                                      value=Name(id='p', ctx=Load()),
                                                      attr='name',
                                                      ctx=Load()),
                                                   ctx=Load()),
                                                attr='loc',
                                                ctx=Load()),
                                             slice=Name(id='s', ctx=Load()),
                                             ctx=Store())],
                                       value=Attribute(
                                          value=Name(id='EB', ctx=Load()),
                                          attr='FALSE',
                                          ctx=Load()))],
                                 orelse=[]),
                              Expr(
                                 value=Call(
                                    func=Name(id='append_changes', ctx=Load()),
                                    args=[
                                       Name(id='new_changes', ctx=Load()),
                                       Dict(
                                          keys=[
                                             Attribute(
                                                value=Name(id='p', ctx=Load()),
                                                attr='name',
                                                ctx=Load())],
                                          values=[
                                             Call(
                                                func=Name(id='Change', ctx=Load()),
                                                args=[
                                                   Attribute(
                                                      value=Name(id='p', ctx=Load()),
                                                      attr='name',
                                                      ctx=Load()),
                                                   List(elts=[], ctx=Load()),
                                                   Subscript(
                                                      value=Name(id='slice_dict', ctx=Load()),
                                                      slice=Name(id='p', ctx=Load()),
                                                      ctx=Load())],
                                                keywords=[])])],
                                    keywords=[]))],
                           orelse=[
                              For(
                                 target=Name(id='s', ctx=Store()),
                                 iter=Subscript(
                                    value=Name(id='slice_dict', ctx=Load()),
                                    slice=Name(id='p', ctx=Load()),
                                    ctx=Load()),
                                 body=[
                                    Assign(
                                       targets=[
                                          Subscript(
                                             value=Attribute(
                                                value=Subscript(
                                                   value=Name(id='predicate_dict', ctx=Load()),
                                                   slice=Attribute(
                                                      value=Name(id='p', ctx=Load()),
                                                      attr='name',
                                                      ctx=Load()),
                                                   ctx=Load()),
                                                attr='loc',
                                                ctx=Load()),
                                             slice=Name(id='s', ctx=Load()),
                                             ctx=Store())],
                                       value=Attribute(
                                          value=Name(id='EB', ctx=Load()),
                                          attr='TRUE',
                                          ctx=Load()))],
                                 orelse=[]),
                              Expr(
                                 value=Call(
                                    func=Name(id='append_changes', ctx=Load()),
                                    args=[
                                       Name(id='new_changes', ctx=Load()),
                                       Dict(
                                          keys=[
                                             Attribute(
                                                value=Name(id='p', ctx=Load()),
                                                attr='name',
                                                ctx=Load())],
                                          values=[
                                             Call(
                                                func=Name(id='Change', ctx=Load()),
                                                args=[
                                                   Attribute(
                                                      value=Name(id='p', ctx=Load()),
                                                      attr='name',
                                                      ctx=Load()),
                                                   Subscript(
                                                      value=Name(id='slice_dict', ctx=Load()),
                                                      slice=Name(id='p', ctx=Load()),
                                                      ctx=Load()),
                                                   List(elts=[], ctx=Load())],
                                                keywords=[])])],
                                    keywords=[]))])])],
               orelse=[]),
            Return(
               value=Name(id='new_changes', ctx=Load()))],
         decorator_list=[])],
   type_ignores=[])



# AST of an auxiliary function
def generate_handle_conditional_propagate_results():
    return Module(
   body=[
      FunctionDef(
         name='handle_conditional_propagate_results',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='rule'),
               arg(arg='result_list')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='incons_indices', ctx=Store())],
               value=Subscript(
                  value=Call(
                     func=Attribute(
                        value=Name(id='np', ctx=Load()),
                        attr='where',
                        ctx=Load()),
                     args=[
                        ListComp(
                           elt=Compare(
                              left=Attribute(
                                 value=Name(id='res', ctx=Load()),
                                 attr='truth',
                                 ctx=Load()),
                              ops=[
                                 Eq()],
                              comparators=[
                                 Attribute(
                                    value=Name(id='EB', ctx=Load()),
                                    attr='INCONSISTENT',
                                    ctx=Load())]),
                           generators=[
                              comprehension(
                                 target=Name(id='res', ctx=Store()),
                                 iter=Name(id='result_list', ctx=Load()),
                                 ifs=[],
                                 is_async=0)])],
                     keywords=[]),
                  slice=Constant(value=0),
                  ctx=Load())),
            If(
               test=Compare(
                  left=Call(
                     func=Name(id='len', ctx=Load()),
                     args=[
                        Name(id='incons_indices', ctx=Load())],
                     keywords=[]),
                  ops=[
                     Gt()],
                  comparators=[
                     Constant(value=0)]),
               body=[
                  Raise(
                     exc=Call(
                        func=Name(id='Exception', ctx=Load()),
                        args=[
                           BinOp(
                              left=Constant(value='Inconsistency error in: '),
                              op=Add(),
                              right=Attribute(
                                 value=Subscript(
                                    value=Name(id='rule', ctx=Load()),
                                    slice=Constant(value=0),
                                    ctx=Load()),
                                 attr='name',
                                 ctx=Load()))],
                        keywords=[]))],
               orelse=[]),
            Assign(
               targets=[
                  Name(id='true_indices', ctx=Store())],
               value=Subscript(
                  value=Call(
                     func=Attribute(
                        value=Name(id='np', ctx=Load()),
                        attr='where',
                        ctx=Load()),
                     args=[
                        ListComp(
                           elt=Compare(
                              left=Attribute(
                                 value=Name(id='res', ctx=Load()),
                                 attr='truth',
                                 ctx=Load()),
                              ops=[
                                 Eq()],
                              comparators=[
                                 Attribute(
                                    value=Name(id='EB', ctx=Load()),
                                    attr='TRUE',
                                    ctx=Load())]),
                           generators=[
                              comprehension(
                                 target=Name(id='res', ctx=Store()),
                                 iter=Name(id='result_list', ctx=Load()),
                                 ifs=[],
                                 is_async=0)])],
                     keywords=[]),
                  slice=Constant(value=0),
                  ctx=Load())),
            If(
               test=Compare(
                  left=Call(
                     func=Name(id='len', ctx=Load()),
                     args=[
                        Name(id='true_indices', ctx=Load())],
                     keywords=[]),
                  ops=[
                     Gt()],
                  comparators=[
                     Constant(value=0)]),
               body=[
                  Assign(
                     targets=[
                        Name(id='changed_slices', ctx=Store())],
                     value=ListComp(
                        elt=Subscript(
                           value=Attribute(
                              value=Subscript(
                                 value=Name(id='rule', ctx=Load()),
                                 slice=Attribute(
                                    value=Subscript(
                                       value=Name(id='result_list', ctx=Load()),
                                       slice=Name(id='i', ctx=Load()),
                                       ctx=Load()),
                                    attr='position',
                                    ctx=Load()),
                                 ctx=Load()),
                              attr='slicing',
                              ctx=Load()),
                           slice=Name(id='i', ctx=Load()),
                           ctx=Load()),
                        generators=[
                           comprehension(
                              target=Name(id='i', ctx=Store()),
                              iter=Name(id='true_indices', ctx=Load()),
                              ifs=[],
                              is_async=0)])),
                  Assign(
                     targets=[
                        Name(id='changed_lcs', ctx=Store())],
                     value=ListComp(
                        elt=Subscript(
                           value=Name(id='rule', ctx=Load()),
                           slice=Attribute(
                              value=Subscript(
                                 value=Name(id='result_list', ctx=Load()),
                                 slice=Name(id='i', ctx=Load()),
                                 ctx=Load()),
                              attr='position',
                              ctx=Load()),
                           ctx=Load()),
                        generators=[
                           comprehension(
                              target=Name(id='i', ctx=Store()),
                              iter=Name(id='true_indices', ctx=Load()),
                              ifs=[],
                              is_async=0)])),
                  Assign(
                     targets=[
                        Name(id='slices_per_lc', ctx=Store())],
                     value=Dict(keys=[], values=[])),
                  For(
                     target=Tuple(
                        elts=[
                           Name(id='s', ctx=Store()),
                           Name(id='p', ctx=Store())],
                        ctx=Store()),
                     iter=Call(
                        func=Name(id='zip', ctx=Load()),
                        args=[
                           Name(id='changed_slices', ctx=Load()),
                           Name(id='changed_lcs', ctx=Load())],
                        keywords=[]),
                     body=[
                        If(
                           test=Compare(
                              left=Name(id='p', ctx=Load()),
                              ops=[
                                 NotIn()],
                              comparators=[
                                 Call(
                                    func=Attribute(
                                       value=Name(id='slices_per_lc', ctx=Load()),
                                       attr='keys',
                                       ctx=Load()),
                                    args=[],
                                    keywords=[])]),
                           body=[
                              Assign(
                                 targets=[
                                    Subscript(
                                       value=Name(id='slices_per_lc', ctx=Load()),
                                       slice=Name(id='p', ctx=Load()),
                                       ctx=Store())],
                                 value=List(
                                    elts=[
                                       Name(id='s', ctx=Load())],
                                    ctx=Load()))],
                           orelse=[
                              Expr(
                                 value=Call(
                                    func=Attribute(
                                       value=Subscript(
                                          value=Name(id='slices_per_lc', ctx=Load()),
                                          slice=Name(id='p', ctx=Load()),
                                          ctx=Load()),
                                       attr='append',
                                       ctx=Load()),
                                    args=[
                                       Name(id='s', ctx=Load())],
                                    keywords=[]))])],
                     orelse=[]),
                  Return(
                     value=Call(
                        func=Name(id='write_to_data_array', ctx=Load()),
                        args=[
                           Name(id='slices_per_lc', ctx=Load())],
                        keywords=[]))],
               orelse=[]),
            Return(
               value=Dict(keys=[], values=[]))],
         decorator_list=[])],
   type_ignores=[])




# AST of an auxiliary function
def generate_normal_propagation():
    return Module(
   body=[
      FunctionDef(
         name='normal_propagation',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='rule')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='truth_list', ctx=Store())],
               value=ListComp(
                  elt=Call(
                     func=Name(id='get_from_data_array_wrap', ctx=Load()),
                     args=[
                        Attribute(
                           value=Name(id='r', ctx=Load()),
                           attr='name',
                           ctx=Load()),
                        Attribute(
                           value=Name(id='r', ctx=Load()),
                           attr='slicing',
                           ctx=Load()),
                        Attribute(
                           value=Name(id='r', ctx=Load()),
                           attr='b',
                           ctx=Load())],
                     keywords=[]),
                  generators=[
                     comprehension(
                        target=Name(id='r', ctx=Store()),
                        iter=Name(id='rule', ctx=Load()),
                        ifs=[],
                        is_async=0)])),
            Assign(
               targets=[
                  Name(id='result_list', ctx=Store())],
               value=Call(
                  func=Attribute(
                     value=Name(id='np', ctx=Load()),
                     attr='apply_along_axis',
                     ctx=Load()),
                  args=[
                     Name(id='conditional_propagate', ctx=Load())],
                  keywords=[
                     keyword(
                        arg='axis',
                        value=Constant(value=0)),
                     keyword(
                        arg='arr',
                        value=Call(
                           func=Attribute(
                              value=Name(id='np', ctx=Load()),
                              attr='array',
                              ctx=Load()),
                           args=[
                              Name(id='truth_list', ctx=Load())],
                           keywords=[]))])),
            Try(
               body=[
                  Assign(
                     targets=[
                        Name(id='new_changes', ctx=Store())],
                     value=Call(
                        func=Name(id='handle_conditional_propagate_results', ctx=Load()),
                        args=[
                           Name(id='rule', ctx=Load()),
                           Name(id='result_list', ctx=Load())],
                        keywords=[])),
                  Return(
                     value=Name(id='new_changes', ctx=Load()))],
               handlers=[
                  ExceptHandler(
                     type=Name(id='Exception', ctx=Load()),
                     name='e',
                     body=[
                        Raise(
                           exc=Call(
                              func=Name(id='Exception', ctx=Load()),
                              args=[
                                 Name(id='e', ctx=Load())],
                              keywords=[]))])],
               orelse=[],
               finalbody=[])],
         decorator_list=[])],
   type_ignores=[])

# AST of an auxiliary function
def generate_handle_unconditional_propagate_results():
   return Module(
   body=[
      FunctionDef(
         name='handle_unconditional_propagate_results',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='name'),
               arg(arg='slices'),
               arg(arg='result_list'),
               arg(arg='bool_value')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='incons_indices', ctx=Store())],
               value=Subscript(
                  value=Call(
                     func=Attribute(
                        value=Name(id='np', ctx=Load()),
                        attr='where',
                        ctx=Load()),
                     args=[
                        Compare(
                           left=Name(id='result_list', ctx=Load()),
                           ops=[
                              Eq()],
                           comparators=[
                              Attribute(
                                 value=Name(id='EB', ctx=Load()),
                                 attr='INCONSISTENT',
                                 ctx=Load())])],
                     keywords=[]),
                  slice=Constant(value=0),
                  ctx=Load())),
            If(
               test=Compare(
                  left=Call(
                     func=Name(id='len', ctx=Load()),
                     args=[
                        Name(id='incons_indices', ctx=Load())],
                     keywords=[]),
                  ops=[
                     Gt()],
                  comparators=[
                     Constant(value=0)]),
               body=[
                  Raise(
                     exc=Call(
                        func=Name(id='Exception', ctx=Load()),
                        args=[
                           BinOp(
                              left=Constant(value='Inconsistency error in: '),
                              op=Add(),
                              right=Name(id='name', ctx=Load()))],
                        keywords=[]))],
               orelse=[]),
            Assign(
               targets=[
                  Name(id='true_indices', ctx=Store())],
               value=Subscript(
                  value=Call(
                     func=Attribute(
                        value=Name(id='np', ctx=Load()),
                        attr='where',
                        ctx=Load()),
                     args=[
                        Compare(
                           left=Name(id='result_list', ctx=Load()),
                           ops=[
                              Eq()],
                           comparators=[
                              Attribute(
                                 value=Name(id='EB', ctx=Load()),
                                 attr='TRUE',
                                 ctx=Load())])],
                     keywords=[]),
                  slice=Constant(value=0),
                  ctx=Load())),
            If(
               test=Compare(
                  left=Call(
                     func=Name(id='len', ctx=Load()),
                     args=[
                        Name(id='true_indices', ctx=Load())],
                     keywords=[]),
                  ops=[
                     Gt()],
                  comparators=[
                     Constant(value=0)]),
               body=[
                  Assign(
                     targets=[
                        Name(id='changed_slices', ctx=Store())],
                     value=ListComp(
                        elt=Subscript(
                           value=Name(id='slices', ctx=Load()),
                           slice=Name(id='i', ctx=Load()),
                           ctx=Load()),
                        generators=[
                           comprehension(
                              target=Name(id='i', ctx=Store()),
                              iter=Name(id='true_indices', ctx=Load()),
                              ifs=[],
                              is_async=0)])),
                  Assign(
                     targets=[
                        Name(id='slices_per_lc', ctx=Store())],
                     value=Dict(
                        keys=[
                           Call(
                              func=Name(id='LiteralCollection', ctx=Load()),
                              args=[
                                 Name(id='name', ctx=Load()),
                                 Name(id='slices', ctx=Load()),
                                 UnaryOp(
                                    op=Not(),
                                    operand=Name(id='bool_value', ctx=Load()))],
                              keywords=[])],
                        values=[
                           Name(id='changed_slices', ctx=Load())])),
                  Return(
                     value=Call(
                        func=Name(id='write_to_data_array', ctx=Load()),
                        args=[
                           Name(id='slices_per_lc', ctx=Load())],
                        keywords=[]))],
               orelse=[]),
            Return(
               value=Dict(keys=[], values=[]))],
         decorator_list=[])],
   type_ignores=[])


# AST of an auxiliary function
def generate_unconditional_propagate_wrap():
    return Module(
   body=[
      FunctionDef(
         name='unconditional_propagate_wrap',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='big_array'),
               arg(arg='big_slices'),
               arg(arg='bool_value')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='args', ctx=Store())],
               value=Call(
                  func=Name(id='get_from_data_array_wrap', ctx=Load()),
                  args=[
                     Attribute(
                        value=Name(id='big_array', ctx=Load()),
                        attr='name',
                        ctx=Load()),
                     Name(id='big_slices', ctx=Load()),
                     Name(id='bool_value', ctx=Load())],
                  keywords=[])),
            Assign(
               targets=[
                  Name(id='result_list', ctx=Store())],
               value=Call(
                  func=Attribute(
                     value=Name(id='np', ctx=Load()),
                     attr='array',
                     ctx=Load()),
                  args=[
                     Call(
                        func=Name(id='unconditional_propagate', ctx=Load()),
                        args=[
                           Call(
                              func=Attribute(
                                 value=Name(id='np', ctx=Load()),
                                 attr='array',
                                 ctx=Load()),
                              args=[
                                 Name(id='args', ctx=Load())],
                              keywords=[])],
                        keywords=[])],
                  keywords=[])),
            Try(
               body=[
                  Assign(
                     targets=[
                        Name(id='new_changes', ctx=Store())],
                     value=Call(
                        func=Name(id='handle_unconditional_propagate_results', ctx=Load()),
                        args=[
                           Attribute(
                              value=Name(id='big_array', ctx=Load()),
                              attr='name',
                              ctx=Load()),
                           Name(id='big_slices', ctx=Load()),
                           Name(id='result_list', ctx=Load()),
                           Name(id='bool_value', ctx=Load())],
                        keywords=[])),
                  Return(
                     value=Name(id='new_changes', ctx=Load()))],
               handlers=[
                  ExceptHandler(
                     type=Name(id='Exception', ctx=Load()),
                     name='e',
                     body=[
                        Raise(
                           exc=Call(
                              func=Name(id='Exception', ctx=Load()),
                              args=[
                                 Name(id='e', ctx=Load())],
                              keywords=[]))])],
               orelse=[],
               finalbody=[])],
         decorator_list=[])],
   type_ignores=[])




# AST of an auxiliary function
def generate_calculate_first_coordinate():
    return Module(
   body=[
      FunctionDef(
         name='calculate_first_coordinate',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='small_coordinate'),
               arg(arg='data_array'),
               arg(arg='changing_dims')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='new_coordinate', ctx=Store())],
               value=Call(
                  func=Name(id='tuple', ctx=Load()),
                  args=[
                     Name(id='small_coordinate', ctx=Load())],
                  keywords=[])),
            Assign(
               targets=[
                  Name(id='index', ctx=Store())],
               value=Constant(value=0)),
            For(
               target=Name(id='dim', ctx=Store()),
               iter=Attribute(
                  value=Name(id='data_array', ctx=Load()),
                  attr='dims',
                  ctx=Load()),
               body=[
                  If(
                     test=Compare(
                        left=Name(id='dim', ctx=Load()),
                        ops=[
                           In()],
                        comparators=[
                           Name(id='changing_dims', ctx=Load())]),
                     body=[
                        Assign(
                           targets=[
                              Name(id='new_coordinate', ctx=Store())],
                           value=BinOp(
                              left=BinOp(
                                 left=Subscript(
                                    value=Name(id='new_coordinate', ctx=Load()),
                                    slice=Slice(
                                       upper=Name(id='index', ctx=Load())),
                                    ctx=Load()),
                                 op=Add(),
                                 right=Tuple(
                                    elts=[
                                       Call(
                                          func=Attribute(
                                             value=Subscript(
                                                value=Subscript(
                                                   value=Attribute(
                                                      value=Name(id='data_array', ctx=Load()),
                                                      attr='coords',
                                                      ctx=Load()),
                                                   slice=Name(id='dim', ctx=Load()),
                                                   ctx=Load()),
                                                slice=Constant(value=0),
                                                ctx=Load()),
                                             attr='item',
                                             ctx=Load()),
                                          args=[],
                                          keywords=[])],
                                    ctx=Load())),
                              op=Add(),
                              right=Subscript(
                                 value=Name(id='new_coordinate', ctx=Load()),
                                 slice=Slice(
                                    lower=Name(id='index', ctx=Load())),
                                 ctx=Load())))],
                     orelse=[]),
                  AugAssign(
                     target=Name(id='index', ctx=Store()),
                     op=Add(),
                     value=Constant(value=1))],
               orelse=[]),
            Return(
               value=Name(id='new_coordinate', ctx=Load()))],
         decorator_list=[])],
   type_ignores=[])

# AST of an auxiliary function
def generate_calculate_next_coordinate():
    return Module(
   body=[
      FunctionDef(
         name='calculate_next_coordinate',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='coordinate'),
               arg(arg='data_array'),
               arg(arg='changing_dims')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='next_coordinate', ctx=Store())],
               value=Call(
                  func=Name(id='tuple', ctx=Load()),
                  args=[
                     Name(id='coordinate', ctx=Load())],
                  keywords=[])),
            Assign(
               targets=[
                  Name(id='index', ctx=Store())],
               value=Constant(value=0)),
            For(
               target=Name(id='dim', ctx=Store()),
               iter=Attribute(
                  value=Name(id='data_array', ctx=Load()),
                  attr='dims',
                  ctx=Load()),
               body=[
                  If(
                     test=Compare(
                        left=Name(id='dim', ctx=Load()),
                        ops=[
                           In()],
                        comparators=[
                           Name(id='changing_dims', ctx=Load())]),
                     body=[
                        Assign(
                           targets=[
                              Name(id='current_value', ctx=Store())],
                           value=Subscript(
                              value=Name(id='coordinate', ctx=Load()),
                              slice=Name(id='index', ctx=Load()),
                              ctx=Load())),
                        Assign(
                           targets=[
                              Name(id='current_coords', ctx=Store())],
                           value=Attribute(
                              value=Subscript(
                                 value=Attribute(
                                    value=Name(id='data_array', ctx=Load()),
                                    attr='coords',
                                    ctx=Load()),
                                 slice=Name(id='dim', ctx=Load()),
                                 ctx=Load()),
                              attr='values',
                              ctx=Load())),
                        Assign(
                           targets=[
                              Name(id='current_index', ctx=Store())],
                           value=Subscript(
                              value=Subscript(
                                 value=Call(
                                    func=Attribute(
                                       value=Name(id='np', ctx=Load()),
                                       attr='where',
                                       ctx=Load()),
                                    args=[
                                       Compare(
                                          left=Name(id='current_coords', ctx=Load()),
                                          ops=[
                                             Eq()],
                                          comparators=[
                                             Name(id='current_value', ctx=Load())])],
                                    keywords=[]),
                                 slice=Constant(value=0),
                                 ctx=Load()),
                              slice=Constant(value=0),
                              ctx=Load())),
                        If(
                           test=Compare(
                              left=Name(id='current_index', ctx=Load()),
                              ops=[
                                 Lt()],
                              comparators=[
                                 BinOp(
                                    left=Call(
                                       func=Name(id='len', ctx=Load()),
                                       args=[
                                          Name(id='current_coords', ctx=Load())],
                                       keywords=[]),
                                    op=Sub(),
                                    right=Constant(value=1))]),
                           body=[
                              If(
                                 test=Compare(
                                    left=Name(id='index', ctx=Load()),
                                    ops=[
                                       Lt()],
                                    comparators=[
                                       BinOp(
                                          left=Call(
                                             func=Name(id='len', ctx=Load()),
                                             args=[
                                                Attribute(
                                                   value=Name(id='data_array', ctx=Load()),
                                                   attr='dims',
                                                   ctx=Load())],
                                             keywords=[]),
                                          op=Sub(),
                                          right=Constant(value=1))]),
                                 body=[
                                    Assign(
                                       targets=[
                                          Name(id='next_coordinate', ctx=Store())],
                                       value=BinOp(
                                          left=BinOp(
                                             left=Subscript(
                                                value=Name(id='next_coordinate', ctx=Load()),
                                                slice=Slice(
                                                   upper=Name(id='index', ctx=Load())),
                                                ctx=Load()),
                                             op=Add(),
                                             right=Tuple(
                                                elts=[
                                                   Call(
                                                      func=Attribute(
                                                         value=Subscript(
                                                            value=Subscript(
                                                               value=Attribute(
                                                                  value=Name(id='data_array', ctx=Load()),
                                                                  attr='coords',
                                                                  ctx=Load()),
                                                               slice=Name(id='dim', ctx=Load()),
                                                               ctx=Load()),
                                                            slice=BinOp(
                                                               left=Name(id='current_index', ctx=Load()),
                                                               op=Add(),
                                                               right=Constant(value=1)),
                                                            ctx=Load()),
                                                         attr='item',
                                                         ctx=Load()),
                                                      args=[],
                                                      keywords=[])],
                                                ctx=Load())),
                                          op=Add(),
                                          right=Subscript(
                                             value=Name(id='next_coordinate', ctx=Load()),
                                             slice=Slice(
                                                lower=BinOp(
                                                   left=Name(id='index', ctx=Load()),
                                                   op=Add(),
                                                   right=Constant(value=1))),
                                             ctx=Load())))],
                                 orelse=[
                                    Assign(
                                       targets=[
                                          Name(id='next_coordinate', ctx=Store())],
                                       value=BinOp(
                                          left=Subscript(
                                             value=Name(id='next_coordinate', ctx=Load()),
                                             slice=Slice(
                                                upper=Name(id='index', ctx=Load())),
                                             ctx=Load()),
                                          op=Add(),
                                          right=Tuple(
                                             elts=[
                                                Call(
                                                   func=Attribute(
                                                      value=Subscript(
                                                         value=Subscript(
                                                            value=Attribute(
                                                               value=Name(id='data_array', ctx=Load()),
                                                               attr='coords',
                                                               ctx=Load()),
                                                            slice=Name(id='dim', ctx=Load()),
                                                            ctx=Load()),
                                                         slice=BinOp(
                                                            left=Name(id='current_index', ctx=Load()),
                                                            op=Add(),
                                                            right=Constant(value=1)),
                                                         ctx=Load()),
                                                      attr='item',
                                                      ctx=Load()),
                                                   args=[],
                                                   keywords=[])],
                                             ctx=Load())))]),
                              Return(
                                 value=Name(id='next_coordinate', ctx=Load()))],
                           orelse=[
                              If(
                                 test=Compare(
                                    left=Name(id='index', ctx=Load()),
                                    ops=[
                                       Lt()],
                                    comparators=[
                                       BinOp(
                                          left=Call(
                                             func=Name(id='len', ctx=Load()),
                                             args=[
                                                Attribute(
                                                   value=Name(id='data_array', ctx=Load()),
                                                   attr='dims',
                                                   ctx=Load())],
                                             keywords=[]),
                                          op=Sub(),
                                          right=Constant(value=1))]),
                                 body=[
                                    Assign(
                                       targets=[
                                          Name(id='next_coordinate', ctx=Store())],
                                       value=BinOp(
                                          left=BinOp(
                                             left=Subscript(
                                                value=Name(id='next_coordinate', ctx=Load()),
                                                slice=Slice(
                                                   upper=Name(id='index', ctx=Load())),
                                                ctx=Load()),
                                             op=Add(),
                                             right=Tuple(
                                                elts=[
                                                   Call(
                                                      func=Attribute(
                                                         value=Subscript(
                                                            value=Subscript(
                                                               value=Attribute(
                                                                  value=Name(id='data_array', ctx=Load()),
                                                                  attr='coords',
                                                                  ctx=Load()),
                                                               slice=Name(id='dim', ctx=Load()),
                                                               ctx=Load()),
                                                            slice=Constant(value=0),
                                                            ctx=Load()),
                                                         attr='item',
                                                         ctx=Load()),
                                                      args=[],
                                                      keywords=[])],
                                                ctx=Load())),
                                          op=Add(),
                                          right=Subscript(
                                             value=Name(id='next_coordinate', ctx=Load()),
                                             slice=Slice(
                                                lower=BinOp(
                                                   left=Name(id='index', ctx=Load()),
                                                   op=Add(),
                                                   right=Constant(value=1))),
                                             ctx=Load())))],
                                 orelse=[
                                    Return(
                                       value=Constant(value=None))])])],
                     orelse=[]),
                  AugAssign(
                     target=Name(id='index', ctx=Store()),
                     op=Add(),
                     value=Constant(value=1))],
               orelse=[])],
         decorator_list=[])],
   type_ignores=[])

# AST of an auxiliary function
def generate_incremental_propagate():
    return Module(
   body=[
      FunctionDef(
         name='incremental_propagate',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='data_array'),
               arg(arg='small_coordinates'),
               arg(arg='changing_dims'),
               arg(arg='b'),
               arg(arg='unknown_coordinates_list'),
               arg(arg='boolean_list'),
               arg(arg='small_array')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[
               Constant(value=None),
               Constant(value=None),
               Constant(value=None)]),
         body=[
            Assign(
               targets=[
                  Name(id='continue_list', ctx=Store())],
               value=ListComp(
                  elt=Constant(value=True),
                  generators=[
                     comprehension(
                        target=Name(id='_', ctx=Store()),
                        iter=Call(
                           func=Name(id='range', ctx=Load()),
                           args=[
                              Call(
                                 func=Name(id='len', ctx=Load()),
                                 args=[
                                    Name(id='small_coordinates', ctx=Load())],
                                 keywords=[])],
                           keywords=[]),
                        ifs=[],
                        is_async=0)])),
            If(
               test=Compare(
                  left=Name(id='unknown_coordinates_list', ctx=Load()),
                  ops=[
                     Is()],
                  comparators=[
                     Constant(value=None)]),
               body=[
                  Assign(
                     targets=[
                        Name(id='unknown_coordinates_list', ctx=Store())],
                     value=ListComp(
                        elt=List(elts=[], ctx=Load()),
                        generators=[
                           comprehension(
                              target=Name(id='_', ctx=Store()),
                              iter=Call(
                                 func=Name(id='range', ctx=Load()),
                                 args=[
                                    Call(
                                       func=Name(id='len', ctx=Load()),
                                       args=[
                                          Name(id='small_coordinates', ctx=Load())],
                                       keywords=[])],
                                 keywords=[]),
                              ifs=[],
                              is_async=0)]))],
               orelse=[]),
            Assign(
               targets=[
                  Name(id='coordinates', ctx=Store())],
               value=ListComp(
                  elt=Call(
                     func=Name(id='calculate_first_coordinate', ctx=Load()),
                     args=[
                        Name(id='small_coordinate', ctx=Load()),
                        Name(id='data_array', ctx=Load()),
                        Name(id='changing_dims', ctx=Load())],
                     keywords=[]),
                  generators=[
                     comprehension(
                        target=Name(id='small_coordinate', ctx=Store()),
                        iter=Name(id='small_coordinates', ctx=Load()),
                        ifs=[],
                        is_async=0)])),
            While(
               test=BoolOp(
                  op=And(),
                  values=[
                     Call(
                        func=Name(id='any', ctx=Load()),
                        args=[
                           Name(id='continue_list', ctx=Load())],
                        keywords=[]),
                     Compare(
                        left=Constant(value=None),
                        ops=[
                           NotIn()],
                        comparators=[
                           Name(id='coordinates', ctx=Load())])]),
               body=[
                  Assign(
                     targets=[
                        Name(id='results', ctx=Store())],
                     value=Call(
                        func=Name(id='get_from_data_array_wrap', ctx=Load()),
                        args=[
                           Attribute(
                              value=Name(id='data_array', ctx=Load()),
                              attr='name',
                              ctx=Load()),
                           Name(id='coordinates', ctx=Load()),
                           Name(id='b', ctx=Load())],
                        keywords=[])),
                  Assign(
                     targets=[
                        Name(id='unknown_coordinates_list', ctx=Store())],
                     value=ListComp(
                        elt=IfExp(
                           test=BoolOp(
                              op=And(),
                              values=[
                                 Compare(
                                    left=Subscript(
                                       value=Name(id='results', ctx=Load()),
                                       slice=Name(id='i', ctx=Load()),
                                       ctx=Load()),
                                    ops=[
                                       Eq()],
                                    comparators=[
                                       Attribute(
                                          value=Name(id='EB', ctx=Load()),
                                          attr='UNKNOWN',
                                          ctx=Load())]),
                                 Compare(
                                    left=Call(
                                       func=Name(id='len', ctx=Load()),
                                       args=[
                                          Subscript(
                                             value=Name(id='unknown_coordinates_list', ctx=Load()),
                                             slice=Name(id='i', ctx=Load()),
                                             ctx=Load())],
                                       keywords=[]),
                                    ops=[
                                       LtE()],
                                    comparators=[
                                       Constant(value=1)])]),
                           body=BinOp(
                              left=Subscript(
                                 value=Name(id='unknown_coordinates_list', ctx=Load()),
                                 slice=Name(id='i', ctx=Load()),
                                 ctx=Load()),
                              op=Add(),
                              right=List(
                                 elts=[
                                    Subscript(
                                       value=Name(id='coordinates', ctx=Load()),
                                       slice=Name(id='i', ctx=Load()),
                                       ctx=Load())],
                                 ctx=Load())),
                           orelse=Subscript(
                              value=Name(id='unknown_coordinates_list', ctx=Load()),
                              slice=Name(id='i', ctx=Load()),
                              ctx=Load())),
                        generators=[
                           comprehension(
                              target=Name(id='i', ctx=Store()),
                              iter=Call(
                                 func=Name(id='range', ctx=Load()),
                                 args=[
                                    Call(
                                       func=Name(id='len', ctx=Load()),
                                       args=[
                                          Name(id='small_coordinates', ctx=Load())],
                                       keywords=[])],
                                 keywords=[]),
                              ifs=[],
                              is_async=0)])),
                  Assign(
                     targets=[
                        Name(id='continue_list', ctx=Store())],
                     value=ListComp(
                        elt=BoolOp(
                           op=And(),
                           values=[
                              BoolOp(
                                 op=Or(),
                                 values=[
                                    Compare(
                                       left=Subscript(
                                          value=Name(id='results', ctx=Load()),
                                          slice=Name(id='i', ctx=Load()),
                                          ctx=Load()),
                                       ops=[
                                          Eq()],
                                       comparators=[
                                          Attribute(
                                             value=Name(id='EB', ctx=Load()),
                                             attr='TRUE',
                                             ctx=Load())]),
                                    Compare(
                                       left=Subscript(
                                          value=Name(id='results', ctx=Load()),
                                          slice=Name(id='i', ctx=Load()),
                                          ctx=Load()),
                                       ops=[
                                          Eq()],
                                       comparators=[
                                          Attribute(
                                             value=Name(id='EB', ctx=Load()),
                                             attr='UNKNOWN',
                                             ctx=Load())])]),
                              Compare(
                                 left=Call(
                                    func=Name(id='len', ctx=Load()),
                                    args=[
                                       Subscript(
                                          value=Name(id='unknown_coordinates_list', ctx=Load()),
                                          slice=Name(id='i', ctx=Load()),
                                          ctx=Load())],
                                    keywords=[]),
                                 ops=[
                                    LtE()],
                                 comparators=[
                                    Constant(value=1)]),
                              Subscript(
                                 value=Name(id='continue_list', ctx=Load()),
                                 slice=Name(id='i', ctx=Load()),
                                 ctx=Load())]),
                        generators=[
                           comprehension(
                              target=Name(id='i', ctx=Store()),
                              iter=Call(
                                 func=Name(id='range', ctx=Load()),
                                 args=[
                                    Call(
                                       func=Name(id='len', ctx=Load()),
                                       args=[
                                          Name(id='results', ctx=Load())],
                                       keywords=[])],
                                 keywords=[]),
                              ifs=[],
                              is_async=0)])),
                  Assign(
                     targets=[
                        Name(id='coordinates', ctx=Store())],
                     value=ListComp(
                        elt=IfExp(
                           test=Subscript(
                              value=Name(id='continue_list', ctx=Load()),
                              slice=Name(id='i', ctx=Load()),
                              ctx=Load()),
                           body=Call(
                              func=Name(id='calculate_next_coordinate', ctx=Load()),
                              args=[
                                 Subscript(
                                    value=Name(id='coordinates', ctx=Load()),
                                    slice=Name(id='i', ctx=Load()),
                                    ctx=Load()),
                                 Name(id='data_array', ctx=Load()),
                                 Name(id='changing_dims', ctx=Load())],
                              keywords=[]),
                           orelse=Subscript(
                              value=Name(id='coordinates', ctx=Load()),
                              slice=Name(id='i', ctx=Load()),
                              ctx=Load())),
                        generators=[
                           comprehension(
                              target=Name(id='i', ctx=Store()),
                              iter=Call(
                                 func=Name(id='range', ctx=Load()),
                                 args=[
                                    Call(
                                       func=Name(id='len', ctx=Load()),
                                       args=[
                                          Name(id='coordinates', ctx=Load())],
                                       keywords=[])],
                                 keywords=[]),
                              ifs=[],
                              is_async=0)]))],
               orelse=[]),
            Assign(
               targets=[
                  Name(id='new_changes', ctx=Store())],
               value=Dict(keys=[], values=[])),
            For(
               target=Tuple(
                  elts=[
                     Name(id='i', ctx=Store()),
                     Name(id='coord_list', ctx=Store())],
                  ctx=Store()),
               iter=Call(
                  func=Name(id='enumerate', ctx=Load()),
                  args=[
                     Name(id='unknown_coordinates_list', ctx=Load())],
                  keywords=[]),
               body=[
                  If(
                     test=BoolOp(
                        op=And(),
                        values=[
                           Compare(
                              left=Call(
                                 func=Name(id='len', ctx=Load()),
                                 args=[
                                    Name(id='coord_list', ctx=Load())],
                                 keywords=[]),
                              ops=[
                                 Eq()],
                              comparators=[
                                 Constant(value=1)]),
                           Subscript(
                              value=Name(id='continue_list', ctx=Load()),
                              slice=Name(id='i', ctx=Load()),
                              ctx=Load())]),
                     body=[
                        Assign(
                           targets=[
                              Name(id='coord', ctx=Store())],
                           value=Subscript(
                              value=Name(id='coord_list', ctx=Load()),
                              slice=Constant(value=0),
                              ctx=Load())),
                        If(
                           test=BoolOp(
                              op=And(),
                              values=[
                                 Compare(
                                    left=Name(id='boolean_list', ctx=Load()),
                                    ops=[
                                       IsNot()],
                                    comparators=[
                                       Constant(value=None)]),
                                 Subscript(
                                    value=Name(id='boolean_list', ctx=Load()),
                                    slice=Name(id='i', ctx=Load()),
                                    ctx=Load())]),
                           body=[
                              If(
                                 test=Name(id='b', ctx=Load()),
                                 body=[
                                    Assign(
                                       targets=[
                                          Subscript(
                                             value=Attribute(
                                                value=Name(id='small_array', ctx=Load()),
                                                attr='loc',
                                                ctx=Load()),
                                             slice=Name(id='coord', ctx=Load()),
                                             ctx=Store())],
                                       value=Attribute(
                                          value=Name(id='EB', ctx=Load()),
                                          attr='TRUE',
                                          ctx=Load())),
                                    Expr(
                                       value=Call(
                                          func=Name(id='append_changes', ctx=Load()),
                                          args=[
                                             Name(id='new_changes', ctx=Load()),
                                             Dict(
                                                keys=[
                                                   Attribute(
                                                      value=Name(id='small_array', ctx=Load()),
                                                      attr='name',
                                                      ctx=Load())],
                                                values=[
                                                   Call(
                                                      func=Name(id='Change', ctx=Load()),
                                                      args=[
                                                         Attribute(
                                                            value=Name(id='small_array', ctx=Load()),
                                                            attr='name',
                                                            ctx=Load()),
                                                         List(
                                                            elts=[
                                                               Name(id='coord', ctx=Load())],
                                                            ctx=Load()),
                                                         List(elts=[], ctx=Load())],
                                                      keywords=[])])],
                                          keywords=[]))],
                                 orelse=[
                                    Assign(
                                       targets=[
                                          Subscript(
                                             value=Attribute(
                                                value=Name(id='small_array', ctx=Load()),
                                                attr='loc',
                                                ctx=Load()),
                                             slice=Name(id='coord', ctx=Load()),
                                             ctx=Store())],
                                       value=Attribute(
                                          value=Name(id='EB', ctx=Load()),
                                          attr='FALSE',
                                          ctx=Load())),
                                    Expr(
                                       value=Call(
                                          func=Name(id='append_changes', ctx=Load()),
                                          args=[
                                             Name(id='new_changes', ctx=Load()),
                                             Dict(
                                                keys=[
                                                   Attribute(
                                                      value=Name(id='small_array', ctx=Load()),
                                                      attr='name',
                                                      ctx=Load())],
                                                values=[
                                                   Call(
                                                      func=Name(id='Change', ctx=Load()),
                                                      args=[
                                                         Attribute(
                                                            value=Name(id='small_array', ctx=Load()),
                                                            attr='name',
                                                            ctx=Load()),
                                                         List(elts=[], ctx=Load()),
                                                         List(
                                                            elts=[
                                                               Name(id='coord', ctx=Load())],
                                                            ctx=Load())],
                                                      keywords=[])])],
                                          keywords=[]))])],
                           orelse=[
                              If(
                                 test=Name(id='b', ctx=Load()),
                                 body=[
                                    Assign(
                                       targets=[
                                          Subscript(
                                             value=Attribute(
                                                value=Name(id='data_array', ctx=Load()),
                                                attr='loc',
                                                ctx=Load()),
                                             slice=Name(id='coord', ctx=Load()),
                                             ctx=Store())],
                                       value=Attribute(
                                          value=Name(id='EB', ctx=Load()),
                                          attr='FALSE',
                                          ctx=Load())),
                                    Expr(
                                       value=Call(
                                          func=Name(id='append_changes', ctx=Load()),
                                          args=[
                                             Name(id='new_changes', ctx=Load()),
                                             Dict(
                                                keys=[
                                                   Attribute(
                                                      value=Name(id='data_array', ctx=Load()),
                                                      attr='name',
                                                      ctx=Load())],
                                                values=[
                                                   Call(
                                                      func=Name(id='Change', ctx=Load()),
                                                      args=[
                                                         Attribute(
                                                            value=Name(id='data_array', ctx=Load()),
                                                            attr='name',
                                                            ctx=Load()),
                                                         List(elts=[], ctx=Load()),
                                                         List(
                                                            elts=[
                                                               Name(id='coord', ctx=Load())],
                                                            ctx=Load())],
                                                      keywords=[])])],
                                          keywords=[]))],
                                 orelse=[
                                    Assign(
                                       targets=[
                                          Subscript(
                                             value=Attribute(
                                                value=Name(id='data_array', ctx=Load()),
                                                attr='loc',
                                                ctx=Load()),
                                             slice=Name(id='coord', ctx=Load()),
                                             ctx=Store())],
                                       value=Attribute(
                                          value=Name(id='EB', ctx=Load()),
                                          attr='TRUE',
                                          ctx=Load())),
                                    Expr(
                                       value=Call(
                                          func=Name(id='append_changes', ctx=Load()),
                                          args=[
                                             Name(id='new_changes', ctx=Load()),
                                             Dict(
                                                keys=[
                                                   Attribute(
                                                      value=Name(id='data_array', ctx=Load()),
                                                      attr='name',
                                                      ctx=Load())],
                                                values=[
                                                   Call(
                                                      func=Name(id='Change', ctx=Load()),
                                                      args=[
                                                         Attribute(
                                                            value=Name(id='data_array', ctx=Load()),
                                                            attr='name',
                                                            ctx=Load()),
                                                         List(
                                                            elts=[
                                                               Name(id='coord', ctx=Load())],
                                                            ctx=Load()),
                                                         List(elts=[], ctx=Load())],
                                                      keywords=[])])],
                                          keywords=[]))])])],
                     orelse=[]),
                  If(
                     test=BoolOp(
                        op=And(),
                        values=[
                           Compare(
                              left=Call(
                                 func=Name(id='len', ctx=Load()),
                                 args=[
                                    Name(id='coord_list', ctx=Load())],
                                 keywords=[]),
                              ops=[
                                 Eq()],
                              comparators=[
                                 Constant(value=0)]),
                           Subscript(
                              value=Name(id='continue_list', ctx=Load()),
                              slice=Name(id='i', ctx=Load()),
                              ctx=Load())]),
                     body=[
                        Raise(
                           exc=Call(
                              func=Name(id='Exception', ctx=Load()),
                              args=[
                                 BinOp(
                                    left=Constant(value='Inconsistency error in: '),
                                    op=Add(),
                                    right=Attribute(
                                       value=Name(id='data_array', ctx=Load()),
                                       attr='name',
                                       ctx=Load()))],
                              keywords=[]))],
                     orelse=[])],
               orelse=[]),
            Return(
               value=Name(id='new_changes', ctx=Load()))],
         decorator_list=[])],
   type_ignores=[])

# AST of an auxiliary function
def generate_incremental_propagate_wrap():
    return Module(
   body=[
      FunctionDef(
         name='incremental_propagate_wrap',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='big_array'),
               arg(arg='small_array'),
               arg(arg='small_coordinates'),
               arg(arg='changing_dims'),
               arg(arg='b')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='results', ctx=Store())],
               value=Call(
                  func=Name(id='get_from_data_array_wrap', ctx=Load()),
                  args=[
                     Attribute(
                        value=Name(id='small_array', ctx=Load()),
                        attr='name',
                        ctx=Load()),
                     Name(id='small_coordinates', ctx=Load()),
                     UnaryOp(
                        op=Not(),
                        operand=Name(id='b', ctx=Load()))],
                  keywords=[])),
            Assign(
               targets=[
                  Name(id='used_small_coordinates', ctx=Store())],
               value=List(elts=[], ctx=Load())),
            Assign(
               targets=[
                  Name(id='unknown_coordinates_list', ctx=Store())],
               value=List(elts=[], ctx=Load())),
            Assign(
               targets=[
                  Name(id='boolean_list', ctx=Store())],
               value=List(elts=[], ctx=Load())),
            For(
               target=Tuple(
                  elts=[
                     Name(id='i', ctx=Store()),
                     Name(id='res', ctx=Store())],
                  ctx=Store()),
               iter=Call(
                  func=Name(id='enumerate', ctx=Load()),
                  args=[
                     Name(id='results', ctx=Load())],
                  keywords=[]),
               body=[
                  If(
                     test=Compare(
                        left=Name(id='res', ctx=Load()),
                        ops=[
                           Eq()],
                        comparators=[
                           Attribute(
                              value=Name(id='EB', ctx=Load()),
                              attr='TRUE',
                              ctx=Load())]),
                     body=[
                        Expr(
                           value=Call(
                              func=Attribute(
                                 value=Name(id='used_small_coordinates', ctx=Load()),
                                 attr='append',
                                 ctx=Load()),
                              args=[
                                 Subscript(
                                    value=Name(id='small_coordinates', ctx=Load()),
                                    slice=Name(id='i', ctx=Load()),
                                    ctx=Load())],
                              keywords=[])),
                        Expr(
                           value=Call(
                              func=Attribute(
                                 value=Name(id='unknown_coordinates_list', ctx=Load()),
                                 attr='append',
                                 ctx=Load()),
                              args=[
                                 List(elts=[], ctx=Load())],
                              keywords=[])),
                        Expr(
                           value=Call(
                              func=Attribute(
                                 value=Name(id='boolean_list', ctx=Load()),
                                 attr='append',
                                 ctx=Load()),
                              args=[
                                 Constant(value=False)],
                              keywords=[]))],
                     orelse=[]),
                  If(
                     test=Compare(
                        left=Name(id='res', ctx=Load()),
                        ops=[
                           Eq()],
                        comparators=[
                           Attribute(
                              value=Name(id='EB', ctx=Load()),
                              attr='UNKNOWN',
                              ctx=Load())]),
                     body=[
                        Expr(
                           value=Call(
                              func=Attribute(
                                 value=Name(id='used_small_coordinates', ctx=Load()),
                                 attr='append',
                                 ctx=Load()),
                              args=[
                                 Subscript(
                                    value=Name(id='small_coordinates', ctx=Load()),
                                    slice=Name(id='i', ctx=Load()),
                                    ctx=Load())],
                              keywords=[])),
                        Expr(
                           value=Call(
                              func=Attribute(
                                 value=Name(id='unknown_coordinates_list', ctx=Load()),
                                 attr='append',
                                 ctx=Load()),
                              args=[
                                 List(
                                    elts=[
                                       Subscript(
                                          value=Name(id='small_coordinates', ctx=Load()),
                                          slice=Name(id='i', ctx=Load()),
                                          ctx=Load())],
                                    ctx=Load())],
                              keywords=[])),
                        Expr(
                           value=Call(
                              func=Attribute(
                                 value=Name(id='boolean_list', ctx=Load()),
                                 attr='append',
                                 ctx=Load()),
                              args=[
                                 Constant(value=True)],
                              keywords=[]))],
                     orelse=[])],
               orelse=[]),
            If(
               test=Compare(
                  left=Call(
                     func=Name(id='len', ctx=Load()),
                     args=[
                        Name(id='used_small_coordinates', ctx=Load())],
                     keywords=[]),
                  ops=[
                     Gt()],
                  comparators=[
                     Constant(value=0)]),
               body=[
                  Return(
                     value=Call(
                        func=Name(id='incremental_propagate', ctx=Load()),
                        args=[
                           Name(id='big_array', ctx=Load()),
                           Name(id='used_small_coordinates', ctx=Load()),
                           Name(id='changing_dims', ctx=Load()),
                           Name(id='b', ctx=Load()),
                           Name(id='unknown_coordinates_list', ctx=Load()),
                           Name(id='boolean_list', ctx=Load()),
                           Name(id='small_array', ctx=Load())],
                        keywords=[]))],
               orelse=[]),
            Return(
               value=Dict(keys=[], values=[]))],
         decorator_list=[])],
   type_ignores=[])






# AST of an auxiliary function
def generate_map_indices():
    return Module(
   body=[
      FunctionDef(
         name='map_indices',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='index'),
               arg(arg='binding1'),
               arg(arg='binding2')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='match_with_index', ctx=Store())],
               value=Dict(keys=[], values=[])),
            For(
               target=Tuple(
                  elts=[
                     Name(id='i', ctx=Store()),
                     Name(id='bind1', ctx=Store())],
                  ctx=Store()),
               iter=Call(
                  func=Name(id='enumerate', ctx=Load()),
                  args=[
                     Name(id='binding1', ctx=Load())],
                  keywords=[]),
               body=[
                  Assign(
                     targets=[
                        Subscript(
                           value=Name(id='match_with_index', ctx=Load()),
                           slice=Name(id='bind1', ctx=Load()),
                           ctx=Store())],
                     value=Subscript(
                        value=Name(id='index', ctx=Load()),
                        slice=Name(id='i', ctx=Load()),
                        ctx=Load()))],
               orelse=[]),
            Assign(
               targets=[
                  Name(id='new_index', ctx=Store())],
               value=Call(
                  func=Name(id='tuple', ctx=Load()),
                  args=[],
                  keywords=[])),
            For(
               target=Name(id='bind2', ctx=Store()),
               iter=Name(id='binding2', ctx=Load()),
               body=[
                  If(
                     test=Compare(
                        left=Name(id='bind2', ctx=Load()),
                        ops=[
                           In()],
                        comparators=[
                           Call(
                              func=Attribute(
                                 value=Name(id='match_with_index', ctx=Load()),
                                 attr='keys',
                                 ctx=Load()),
                              args=[],
                              keywords=[])]),
                     body=[
                        AugAssign(
                           target=Name(id='new_index', ctx=Store()),
                           op=Add(),
                           value=Tuple(
                              elts=[
                                 Subscript(
                                    value=Name(id='match_with_index', ctx=Load()),
                                    slice=Name(id='bind2', ctx=Load()),
                                    ctx=Load())],
                              ctx=Load()))],
                     orelse=[
                        AugAssign(
                           target=Name(id='new_index', ctx=Store()),
                           op=Add(),
                           value=Tuple(
                              elts=[
                                 Name(id='bind2', ctx=Load())],
                              ctx=Load()))])],
               orelse=[]),
            Return(
               value=Name(id='new_index', ctx=Load()))],
         decorator_list=[])],
   type_ignores=[])

# AST of an auxiliary function
def generate_is_valid_index():
    return Module(
   body=[
      FunctionDef(
         name='is_valid_index',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='s'),
               arg(arg='argument'),
               arg(arg='quantified_var')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='var_mapping', ctx=Store())],
               value=Dict(keys=[], values=[])),
            For(
               target=Tuple(
                  elts=[
                     Name(id='i', ctx=Store()),
                     Name(id='elem', ctx=Store())],
                  ctx=Store()),
               iter=Call(
                  func=Name(id='enumerate', ctx=Load()),
                  args=[
                     Name(id='s', ctx=Load())],
                  keywords=[]),
               body=[
                  If(
                     test=Compare(
                        left=Subscript(
                           value=Name(id='argument', ctx=Load()),
                           slice=Name(id='i', ctx=Load()),
                           ctx=Load()),
                        ops=[
                           NotIn()],
                        comparators=[
                           Name(id='quantified_var', ctx=Load())]),
                     body=[
                        If(
                           test=Compare(
                              left=Name(id='elem', ctx=Load()),
                              ops=[
                                 NotEq()],
                              comparators=[
                                 Subscript(
                                    value=Name(id='argument', ctx=Load()),
                                    slice=Name(id='i', ctx=Load()),
                                    ctx=Load())]),
                           body=[
                              Return(
                                 value=Constant(value=False))],
                           orelse=[])],
                     orelse=[
                        Assign(
                           targets=[
                              Name(id='arg', ctx=Store())],
                           value=Subscript(
                              value=Name(id='argument', ctx=Load()),
                              slice=Name(id='i', ctx=Load()),
                              ctx=Load())),
                        If(
                           test=Compare(
                              left=Name(id='arg', ctx=Load()),
                              ops=[
                                 In()],
                              comparators=[
                                 Call(
                                    func=Attribute(
                                       value=Name(id='var_mapping', ctx=Load()),
                                       attr='keys',
                                       ctx=Load()),
                                    args=[],
                                    keywords=[])]),
                           body=[
                              If(
                                 test=Compare(
                                    left=Name(id='elem', ctx=Load()),
                                    ops=[
                                       NotEq()],
                                    comparators=[
                                       Subscript(
                                          value=Name(id='var_mapping', ctx=Load()),
                                          slice=Name(id='arg', ctx=Load()),
                                          ctx=Load())]),
                                 body=[
                                    Return(
                                       value=Constant(value=False))],
                                 orelse=[])],
                           orelse=[
                              Assign(
                                 targets=[
                                    Subscript(
                                       value=Name(id='var_mapping', ctx=Load()),
                                       slice=Name(id='arg', ctx=Load()),
                                       ctx=Store())],
                                 value=Name(id='elem', ctx=Load()))])])],
               orelse=[]),
            Return(
               value=Constant(value=True))],
         decorator_list=[])],
   type_ignores=[])

# AST of an auxiliary function
def generate_map_indices_wrap():
    return Module(
   body=[
      FunctionDef(
         name='map_indices_wrap',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='argument_dict'),
               arg(arg='changed_var'),
               arg(arg='slicing'),
               arg(arg='quantified_var')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            If(
               test=Compare(
                  left=Call(
                     func=Name(id='len', ctx=Load()),
                     args=[
                        Name(id='slicing', ctx=Load())],
                     keywords=[]),
                  ops=[
                     Eq()],
                  comparators=[
                     Constant(value=0)]),
               body=[
                  Return(
                     value=Constant(value=None))],
               orelse=[]),
            Assign(
               targets=[
                  Name(id='slicing_dict', ctx=Store())],
               value=Dict(keys=[], values=[])),
            Assign(
               targets=[
                  Name(id='valid_slicing', ctx=Store())],
               value=ListComp(
                  elt=Name(id='s', ctx=Load()),
                  generators=[
                     comprehension(
                        target=Name(id='s', ctx=Store()),
                        iter=Name(id='slicing', ctx=Load()),
                        ifs=[
                           Call(
                              func=Name(id='is_valid_index', ctx=Load()),
                              args=[
                                 Name(id='s', ctx=Load()),
                                 Subscript(
                                    value=Name(id='argument_dict', ctx=Load()),
                                    slice=Name(id='changed_var', ctx=Load()),
                                    ctx=Load()),
                                 Name(id='quantified_var', ctx=Load())],
                              keywords=[])],
                        is_async=0)])),
            Assign(
               targets=[
                  Subscript(
                     value=Name(id='slicing_dict', ctx=Load()),
                     slice=Name(id='changed_var', ctx=Load()),
                     ctx=Store())],
               value=Name(id='valid_slicing', ctx=Load())),
            For(
               target=Tuple(
                  elts=[
                     Name(id='key', ctx=Store()),
                     Name(id='val', ctx=Store())],
                  ctx=Store()),
               iter=Call(
                  func=Attribute(
                     value=Name(id='argument_dict', ctx=Load()),
                     attr='items',
                     ctx=Load()),
                  args=[],
                  keywords=[]),
               body=[
                  If(
                     test=Compare(
                        left=Name(id='val', ctx=Load()),
                        ops=[
                           NotEq()],
                        comparators=[
                           Subscript(
                              value=Name(id='argument_dict', ctx=Load()),
                              slice=Name(id='changed_var', ctx=Load()),
                              ctx=Load())]),
                     body=[
                        Assign(
                           targets=[
                              Name(id='new_slicing', ctx=Store())],
                           value=ListComp(
                              elt=Call(
                                 func=Name(id='map_indices', ctx=Load()),
                                 args=[
                                    Name(id='index', ctx=Load()),
                                    Subscript(
                                       value=Name(id='argument_dict', ctx=Load()),
                                       slice=Name(id='changed_var', ctx=Load()),
                                       ctx=Load()),
                                    Subscript(
                                       value=Name(id='argument_dict', ctx=Load()),
                                       slice=Name(id='key', ctx=Load()),
                                       ctx=Load())],
                                 keywords=[]),
                              generators=[
                                 comprehension(
                                    target=Name(id='index', ctx=Store()),
                                    iter=Subscript(
                                       value=Name(id='slicing_dict', ctx=Load()),
                                       slice=Name(id='changed_var', ctx=Load()),
                                       ctx=Load()),
                                    ifs=[],
                                    is_async=0)])),
                        Assign(
                           targets=[
                              Subscript(
                                 value=Name(id='slicing_dict', ctx=Load()),
                                 slice=Name(id='key', ctx=Load()),
                                 ctx=Store())],
                           value=Name(id='new_slicing', ctx=Load()))],
                     orelse=[
                        Assign(
                           targets=[
                              Subscript(
                                 value=Name(id='slicing_dict', ctx=Load()),
                                 slice=Name(id='key', ctx=Load()),
                                 ctx=Store())],
                           value=Name(id='valid_slicing', ctx=Load()))])],
               orelse=[]),
            Return(
               value=Name(id='slicing_dict', ctx=Load()))],
         decorator_list=[])],
   type_ignores=[])

# AST of an auxiliary function
def generate_add_dims():
    return Module(
   body=[
      FunctionDef(
         name='add_dims',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='slicing'),
               arg(arg='new'),
               arg(arg='extra_dims')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='new_slicing', ctx=Store())],
               value=List(elts=[], ctx=Load())),
            Expr(
               value=Call(
                  func=Attribute(
                     value=Name(id='new_slicing', ctx=Load()),
                     attr='append',
                     ctx=Load()),
                  args=[
                     Call(
                        func=Attribute(
                           value=Name(id='slicing', ctx=Load()),
                           attr='copy',
                           ctx=Load()),
                        args=[],
                        keywords=[])],
                  keywords=[])),
            Assign(
               targets=[
                  Name(id='new_domains', ctx=Store())],
               value=ListComp(
                  elt=Attribute(
                     value=Subscript(
                        value=Attribute(
                           value=Name(id='new', ctx=Load()),
                           attr='coords',
                           ctx=Load()),
                        slice=Name(id='dim', ctx=Load()),
                        ctx=Load()),
                     attr='values',
                     ctx=Load()),
                  generators=[
                     comprehension(
                        target=Name(id='dim', ctx=Store()),
                        iter=Name(id='extra_dims', ctx=Load()),
                        ifs=[],
                        is_async=0)])),
            For(
               target=Name(id='comb', ctx=Store()),
               iter=Call(
                  func=Name(id='product', ctx=Load()),
                  args=[
                     Starred(
                        value=Name(id='new_domains', ctx=Load()),
                        ctx=Load())],
                  keywords=[]),
               body=[
                  Assign(
                     targets=[
                        Name(id='new_slice', ctx=Store())],
                     value=Call(
                        func=Attribute(
                           value=Name(id='slicing', ctx=Load()),
                           attr='copy',
                           ctx=Load()),
                        args=[],
                        keywords=[])),
                  Assign(
                     targets=[
                        Name(id='index', ctx=Store())],
                     value=Constant(value=0)),
                  Assign(
                     targets=[
                        Name(id='c_index', ctx=Store())],
                     value=Constant(value=0)),
                  For(
                     target=Name(id='dim', ctx=Store()),
                     iter=Attribute(
                        value=Name(id='new', ctx=Load()),
                        attr='dims',
                        ctx=Load()),
                     body=[
                        If(
                           test=Compare(
                              left=Name(id='dim', ctx=Load()),
                              ops=[
                                 In()],
                              comparators=[
                                 Name(id='extra_dims', ctx=Load())]),
                           body=[
                              Assign(
                                 targets=[
                                    Name(id='new_slice', ctx=Store())],
                                 value=ListComp(
                                    elt=BinOp(
                                       left=BinOp(
                                          left=Subscript(
                                             value=Name(id='elem', ctx=Load()),
                                             slice=Slice(
                                                upper=Name(id='index', ctx=Load())),
                                             ctx=Load()),
                                          op=Add(),
                                          right=Tuple(
                                             elts=[
                                                Call(
                                                   func=Attribute(
                                                      value=Subscript(
                                                         value=Name(id='comb', ctx=Load()),
                                                         slice=Name(id='c_index', ctx=Load()),
                                                         ctx=Load()),
                                                      attr='item',
                                                      ctx=Load()),
                                                   args=[],
                                                   keywords=[])],
                                             ctx=Load())),
                                       op=Add(),
                                       right=Subscript(
                                          value=Name(id='elem', ctx=Load()),
                                          slice=Slice(
                                             lower=Name(id='index', ctx=Load())),
                                          ctx=Load())),
                                    generators=[
                                       comprehension(
                                          target=Name(id='elem', ctx=Store()),
                                          iter=Name(id='new_slice', ctx=Load()),
                                          ifs=[],
                                          is_async=0)])),
                              AugAssign(
                                 target=Name(id='c_index', ctx=Store()),
                                 op=Add(),
                                 value=Constant(value=1))],
                           orelse=[]),
                        AugAssign(
                           target=Name(id='index', ctx=Store()),
                           op=Add(),
                           value=Constant(value=1))],
                     orelse=[]),
                  Expr(
                     value=Call(
                        func=Attribute(
                           value=Name(id='new_slicing', ctx=Load()),
                           attr='append',
                           ctx=Load()),
                        args=[
                           Name(id='new_slice', ctx=Load())],
                        keywords=[]))],
               orelse=[]),
            Assign(
               targets=[
                  Name(id='big_slices', ctx=Store())],
               value=ListComp(
                  elt=Call(
                     func=Name(id='list', ctx=Load()),
                     args=[
                        Name(id='val', ctx=Load())],
                     keywords=[]),
                  generators=[
                     comprehension(
                        target=Tuple(
                           elts=[
                              Name(id='key', ctx=Store()),
                              Name(id='val', ctx=Store())],
                           ctx=Store()),
                        iter=Call(
                           func=Name(id='zip', ctx=Load()),
                           args=[
                              Subscript(
                                 value=Name(id='new_slicing', ctx=Load()),
                                 slice=Constant(value=0),
                                 ctx=Load()),
                              Call(
                                 func=Name(id='zip', ctx=Load()),
                                 args=[
                                    Starred(
                                       value=Subscript(
                                          value=Name(id='new_slicing', ctx=Load()),
                                          slice=Slice(
                                             lower=Constant(value=1)),
                                          ctx=Load()),
                                       ctx=Load())],
                                 keywords=[])],
                           keywords=[]),
                        ifs=[],
                        is_async=0)])),
            Return(
               value=ListComp(
                  elt=Name(id='item', ctx=Load()),
                  generators=[
                     comprehension(
                        target=Name(id='sublist', ctx=Store()),
                        iter=Name(id='big_slices', ctx=Load()),
                        ifs=[],
                        is_async=0),
                     comprehension(
                        target=Name(id='item', ctx=Store()),
                        iter=Name(id='sublist', ctx=Load()),
                        ifs=[],
                        is_async=0)]))],
         decorator_list=[])],
   type_ignores=[])


# AST of an auxiliary function
def generate_reduce_dims():
    return Module(
   body=[
      FunctionDef(
         name='reduce_dims',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='slicing'),
               arg(arg='old'),
               arg(arg='extra_dims')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='indices', ctx=Store())],
               value=Call(
                  func=Attribute(
                     value=Name(id='np', ctx=Load()),
                     attr='array',
                     ctx=Load()),
                  args=[
                     ListComp(
                        elt=Name(id='i', ctx=Load()),
                        generators=[
                           comprehension(
                              target=Tuple(
                                 elts=[
                                    Name(id='i', ctx=Store()),
                                    Name(id='value', ctx=Store())],
                                 ctx=Store()),
                              iter=Call(
                                 func=Name(id='enumerate', ctx=Load()),
                                 args=[
                                    Attribute(
                                       value=Name(id='old', ctx=Load()),
                                       attr='dims',
                                       ctx=Load())],
                                 keywords=[]),
                              ifs=[
                                 Compare(
                                    left=Name(id='value', ctx=Load()),
                                    ops=[
                                       NotIn()],
                                    comparators=[
                                       Name(id='extra_dims', ctx=Load())])],
                              is_async=0)])],
                  keywords=[])),
            Assign(
               targets=[
                  Name(id='new_slicing', ctx=Store())],
               value=SetComp(
                  elt=Call(
                     func=Name(id='tuple', ctx=Load()),
                     args=[
                        GeneratorExp(
                           elt=Subscript(
                              value=Name(id='tup', ctx=Load()),
                              slice=Name(id='i', ctx=Load()),
                              ctx=Load()),
                           generators=[
                              comprehension(
                                 target=Name(id='i', ctx=Store()),
                                 iter=Name(id='indices', ctx=Load()),
                                 ifs=[],
                                 is_async=0)])],
                     keywords=[]),
                  generators=[
                     comprehension(
                        target=Name(id='tup', ctx=Store()),
                        iter=Name(id='slicing', ctx=Load()),
                        ifs=[],
                        is_async=0)])),
            Return(
               value=Name(id='new_slicing', ctx=Load()))],
         decorator_list=[])],
   type_ignores=[])

# AST of an auxiliary function
def generate_specifying_propagation():
    return Module(
   body=[
      FunctionDef(
         name='specifying_propagation',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='big'),
               arg(arg='true_slices'),
               arg(arg='false_slices'),
               arg(arg='new_dims'),
               arg(arg='universal')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='big_array', ctx=Store())],
               value=Subscript(
                  value=Name(id='predicate_dict', ctx=Load()),
                  slice=Name(id='big', ctx=Load()),
                  ctx=Load())),
            Assign(
               targets=[
                  Name(id='new_changes', ctx=Store())],
               value=Dict(keys=[], values=[])),
            If(
               test=Compare(
                  left=Call(
                     func=Name(id='len', ctx=Load()),
                     args=[
                        Name(id='true_slices', ctx=Load())],
                     keywords=[]),
                  ops=[
                     Gt()],
                  comparators=[
                     Constant(value=0)]),
               body=[
                  If(
                     test=Name(id='universal', ctx=Load()),
                     body=[
                        Assign(
                           targets=[
                              Name(id='big_slices', ctx=Store())],
                           value=Call(
                              func=Name(id='add_dims', ctx=Load()),
                              args=[
                                 Name(id='true_slices', ctx=Load()),
                                 Name(id='big_array', ctx=Load()),
                                 Name(id='new_dims', ctx=Load())],
                              keywords=[])),
                        If(
                           test=Compare(
                              left=Name(id='big', ctx=Load()),
                              ops=[
                                 In()],
                              comparators=[
                                 Name(id='true_list', ctx=Load())]),
                           body=[
                              Assign(
                                 targets=[
                                    Name(id='detected_changes', ctx=Store())],
                                 value=Dict(
                                    keys=[
                                       Name(id='big', ctx=Load())],
                                    values=[
                                       Call(
                                          func=Name(id='Change', ctx=Load()),
                                          args=[
                                             Name(id='big', ctx=Load()),
                                             Name(id='big_slices', ctx=Load()),
                                             List(elts=[], ctx=Load())],
                                          keywords=[])]))],
                           orelse=[
                              Try(
                                 body=[
                                    Assign(
                                       targets=[
                                          Name(id='detected_changes', ctx=Store())],
                                       value=Call(
                                          func=Name(id='unconditional_propagate_wrap', ctx=Load()),
                                          args=[
                                             Name(id='big_array', ctx=Load()),
                                             Name(id='big_slices', ctx=Load()),
                                             Constant(value=True)],
                                          keywords=[]))],
                                 handlers=[
                                    ExceptHandler(
                                       type=Name(id='Exception', ctx=Load()),
                                       name='e',
                                       body=[
                                          Raise(
                                             exc=Call(
                                                func=Name(id='Exception', ctx=Load()),
                                                args=[
                                                   Name(id='e', ctx=Load())],
                                                keywords=[]))])],
                                 orelse=[],
                                 finalbody=[])]),
                        Expr(
                           value=Call(
                              func=Name(id='append_changes', ctx=Load()),
                              args=[
                                 Name(id='new_changes', ctx=Load()),
                                 Name(id='detected_changes', ctx=Load())],
                              keywords=[]))],
                     orelse=[
                        Try(
                           body=[
                              Assign(
                                 targets=[
                                    Name(id='detected_changes', ctx=Store())],
                                 value=Call(
                                    func=Name(id='incremental_propagate', ctx=Load()),
                                    args=[
                                       Name(id='big_array', ctx=Load()),
                                       Name(id='true_slices', ctx=Load()),
                                       Name(id='new_dims', ctx=Load()),
                                       Constant(value=False)],
                                    keywords=[]))],
                           handlers=[
                              ExceptHandler(
                                 type=Name(id='Exception', ctx=Load()),
                                 name='e',
                                 body=[
                                    Raise(
                                       exc=Call(
                                          func=Name(id='Exception', ctx=Load()),
                                          args=[
                                             Name(id='e', ctx=Load())],
                                          keywords=[]))])],
                           orelse=[],
                           finalbody=[]),
                        Expr(
                           value=Call(
                              func=Name(id='append_changes', ctx=Load()),
                              args=[
                                 Name(id='new_changes', ctx=Load()),
                                 Name(id='detected_changes', ctx=Load())],
                              keywords=[]))])],
               orelse=[]),
            If(
               test=Compare(
                  left=Call(
                     func=Name(id='len', ctx=Load()),
                     args=[
                        Name(id='false_slices', ctx=Load())],
                     keywords=[]),
                  ops=[
                     Gt()],
                  comparators=[
                     Constant(value=0)]),
               body=[
                  If(
                     test=Name(id='universal', ctx=Load()),
                     body=[
                        Try(
                           body=[
                              Assign(
                                 targets=[
                                    Name(id='detected_changes', ctx=Store())],
                                 value=Call(
                                    func=Name(id='incremental_propagate', ctx=Load()),
                                    args=[
                                       Name(id='big_array', ctx=Load()),
                                       Name(id='false_slices', ctx=Load()),
                                       Name(id='new_dims', ctx=Load()),
                                       Constant(value=True)],
                                    keywords=[]))],
                           handlers=[
                              ExceptHandler(
                                 type=Name(id='Exception', ctx=Load()),
                                 name='e',
                                 body=[
                                    Raise(
                                       exc=Call(
                                          func=Name(id='Exception', ctx=Load()),
                                          args=[
                                             Name(id='e', ctx=Load())],
                                          keywords=[]))])],
                           orelse=[],
                           finalbody=[]),
                        Expr(
                           value=Call(
                              func=Name(id='append_changes', ctx=Load()),
                              args=[
                                 Name(id='new_changes', ctx=Load()),
                                 Name(id='detected_changes', ctx=Load())],
                              keywords=[]))],
                     orelse=[
                        Assign(
                           targets=[
                              Name(id='big_slices', ctx=Store())],
                           value=Call(
                              func=Name(id='add_dims', ctx=Load()),
                              args=[
                                 Name(id='false_slices', ctx=Load()),
                                 Name(id='big_array', ctx=Load()),
                                 Name(id='new_dims', ctx=Load())],
                              keywords=[])),
                        Try(
                           body=[
                              Assign(
                                 targets=[
                                    Name(id='detected_changes', ctx=Store())],
                                 value=Call(
                                    func=Name(id='unconditional_propagate_wrap', ctx=Load()),
                                    args=[
                                       Name(id='big_array', ctx=Load()),
                                       Name(id='big_slices', ctx=Load()),
                                       Constant(value=False)],
                                    keywords=[]))],
                           handlers=[
                              ExceptHandler(
                                 type=Name(id='Exception', ctx=Load()),
                                 name='e',
                                 body=[
                                    Raise(
                                       exc=Call(
                                          func=Name(id='Exception', ctx=Load()),
                                          args=[
                                             Name(id='e', ctx=Load())],
                                          keywords=[]))])],
                           orelse=[],
                           finalbody=[]),
                        Expr(
                           value=Call(
                              func=Name(id='append_changes', ctx=Load()),
                              args=[
                                 Name(id='new_changes', ctx=Load()),
                                 Name(id='detected_changes', ctx=Load())],
                              keywords=[]))])],
               orelse=[]),
            Return(
               value=Name(id='new_changes', ctx=Load()))],
         decorator_list=[])],
   type_ignores=[])


# AST of an auxiliary function (without incremental propagation)

def generate_specifying_propagation_2():
   return Module(
   body=[
      FunctionDef(
         name='specifying_propagation',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='big'),
               arg(arg='true_slices'),
               arg(arg='false_slices'),
               arg(arg='new_dims'),
               arg(arg='universal')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='big_array', ctx=Store())],
               value=Subscript(
                  value=Name(id='predicate_dict', ctx=Load()),
                  slice=Name(id='big', ctx=Load()),
                  ctx=Load())),
            Assign(
               targets=[
                  Name(id='new_changes', ctx=Store())],
               value=Dict(keys=[], values=[])),
            If(
               test=Compare(
                  left=Call(
                     func=Name(id='len', ctx=Load()),
                     args=[
                        Name(id='true_slices', ctx=Load())],
                     keywords=[]),
                  ops=[
                     Gt()],
                  comparators=[
                     Constant(value=0)]),
               body=[
                  Assign(
                     targets=[
                        Name(id='big_slices', ctx=Store())],
                     value=Call(
                        func=Name(id='add_dims', ctx=Load()),
                        args=[
                           Name(id='true_slices', ctx=Load()),
                           Name(id='big_array', ctx=Load()),
                           Name(id='new_dims', ctx=Load())],
                        keywords=[])),
                  If(
                     test=Name(id='universal', ctx=Load()),
                     body=[
                        If(
                           test=Compare(
                              left=Name(id='big', ctx=Load()),
                              ops=[
                                 In()],
                              comparators=[
                                 Name(id='true_list', ctx=Load())]),
                           body=[
                              Assign(
                                 targets=[
                                    Name(id='detected_changes', ctx=Store())],
                                 value=Dict(
                                    keys=[
                                       Name(id='big', ctx=Load())],
                                    values=[
                                       Call(
                                          func=Name(id='Change', ctx=Load()),
                                          args=[
                                             Name(id='big', ctx=Load()),
                                             Name(id='big_slices', ctx=Load()),
                                             List(elts=[], ctx=Load())],
                                          keywords=[])]))],
                           orelse=[
                              Try(
                                 body=[
                                    Assign(
                                       targets=[
                                          Name(id='detected_changes', ctx=Store())],
                                       value=Call(
                                          func=Name(id='unconditional_propagate_wrap', ctx=Load()),
                                          args=[
                                             Name(id='big_array', ctx=Load()),
                                             Name(id='big_slices', ctx=Load()),
                                             Constant(value=True)],
                                          keywords=[]))],
                                 handlers=[
                                    ExceptHandler(
                                       type=Name(id='Exception', ctx=Load()),
                                       name='e',
                                       body=[
                                          Raise(
                                             exc=Call(
                                                func=Name(id='Exception', ctx=Load()),
                                                args=[
                                                   Name(id='e', ctx=Load())],
                                                keywords=[]))])],
                                 orelse=[],
                                 finalbody=[])]),
                        Expr(
                           value=Call(
                              func=Name(id='append_changes', ctx=Load()),
                              args=[
                                 Name(id='new_changes', ctx=Load()),
                                 Name(id='detected_changes', ctx=Load())],
                              keywords=[]))],
                     orelse=[
                        Assign(
                           targets=[
                              Name(id='rule', ctx=Store())],
                           value=ListComp(
                              elt=Call(
                                 func=Name(id='LiteralCollection', ctx=Load()),
                                 args=[
                                    Name(id='big', ctx=Load()),
                                    Name(id='big_slice', ctx=Load()),
                                    Constant(value=False)],
                                 keywords=[]),
                              generators=[
                                 comprehension(
                                    target=Name(id='big_slice', ctx=Store()),
                                    iter=Call(
                                       func=Name(id='list', ctx=Load()),
                                       args=[
                                          Call(
                                             func=Name(id='map', ctx=Load()),
                                             args=[
                                                Name(id='list', ctx=Load()),
                                                Call(
                                                   func=Name(id='zip', ctx=Load()),
                                                   args=[
                                                      Starred(
                                                         value=Name(id='big_slices', ctx=Load()),
                                                         ctx=Load())],
                                                   keywords=[])],
                                             keywords=[])],
                                       keywords=[]),
                                    ifs=[],
                                    is_async=0)])),
                        Try(
                           body=[
                              Assign(
                                 targets=[
                                    Name(id='detected_changes', ctx=Store())],
                                 value=Call(
                                    func=Name(id='normal_propagation', ctx=Load()),
                                    args=[
                                       Name(id='rule', ctx=Load())],
                                    keywords=[]))],
                           handlers=[
                              ExceptHandler(
                                 type=Name(id='Exception', ctx=Load()),
                                 name='e',
                                 body=[
                                    Raise(
                                       exc=Call(
                                          func=Name(id='Exception', ctx=Load()),
                                          args=[
                                             Name(id='e', ctx=Load())],
                                          keywords=[]))])],
                           orelse=[],
                           finalbody=[]),
                        Expr(
                           value=Call(
                              func=Name(id='append_changes', ctx=Load()),
                              args=[
                                 Name(id='new_changes', ctx=Load()),
                                 Name(id='detected_changes', ctx=Load())],
                              keywords=[]))])],
               orelse=[]),
            If(
               test=Compare(
                  left=Call(
                     func=Name(id='len', ctx=Load()),
                     args=[
                        Name(id='false_slices', ctx=Load())],
                     keywords=[]),
                  ops=[
                     Gt()],
                  comparators=[
                     Constant(value=0)]),
               body=[
                  Assign(
                     targets=[
                        Name(id='big_slices', ctx=Store())],
                     value=Call(
                        func=Name(id='add_dims', ctx=Load()),
                        args=[
                           Name(id='false_slices', ctx=Load()),
                           Name(id='big_array', ctx=Load()),
                           Name(id='new_dims', ctx=Load())],
                        keywords=[])),
                  If(
                     test=Name(id='universal', ctx=Load()),
                     body=[
                        Assign(
                           targets=[
                              Name(id='rule', ctx=Store())],
                           value=ListComp(
                              elt=Call(
                                 func=Name(id='LiteralCollection', ctx=Load()),
                                 args=[
                                    Name(id='big', ctx=Load()),
                                    Name(id='big_slice', ctx=Load()),
                                    Constant(value=True)],
                                 keywords=[]),
                              generators=[
                                 comprehension(
                                    target=Name(id='big_slice', ctx=Store()),
                                    iter=Call(
                                       func=Name(id='list', ctx=Load()),
                                       args=[
                                          Call(
                                             func=Name(id='map', ctx=Load()),
                                             args=[
                                                Name(id='list', ctx=Load()),
                                                Call(
                                                   func=Name(id='zip', ctx=Load()),
                                                   args=[
                                                      Starred(
                                                         value=Name(id='big_slices', ctx=Load()),
                                                         ctx=Load())],
                                                   keywords=[])],
                                             keywords=[])],
                                       keywords=[]),
                                    ifs=[],
                                    is_async=0)])),
                        Try(
                           body=[
                              Assign(
                                 targets=[
                                    Name(id='detected_changes', ctx=Store())],
                                 value=Call(
                                    func=Name(id='normal_propagation', ctx=Load()),
                                    args=[
                                       Name(id='rule', ctx=Load())],
                                    keywords=[]))],
                           handlers=[
                              ExceptHandler(
                                 type=Name(id='Exception', ctx=Load()),
                                 name='e',
                                 body=[
                                    Raise(
                                       exc=Call(
                                          func=Name(id='Exception', ctx=Load()),
                                          args=[
                                             Name(id='e', ctx=Load())],
                                          keywords=[]))])],
                           orelse=[],
                           finalbody=[]),
                        Expr(
                           value=Call(
                              func=Name(id='append_changes', ctx=Load()),
                              args=[
                                 Name(id='new_changes', ctx=Load()),
                                 Name(id='detected_changes', ctx=Load())],
                              keywords=[]))],
                     orelse=[
                        Try(
                           body=[
                              Assign(
                                 targets=[
                                    Name(id='detected_changes', ctx=Store())],
                                 value=Call(
                                    func=Name(id='unconditional_propagate_wrap', ctx=Load()),
                                    args=[
                                       Name(id='big_array', ctx=Load()),
                                       Name(id='big_slices', ctx=Load()),
                                       Constant(value=False)],
                                    keywords=[]))],
                           handlers=[
                              ExceptHandler(
                                 type=Name(id='Exception', ctx=Load()),
                                 name='e',
                                 body=[
                                    Raise(
                                       exc=Call(
                                          func=Name(id='Exception', ctx=Load()),
                                          args=[
                                             Name(id='e', ctx=Load())],
                                          keywords=[]))])],
                           orelse=[],
                           finalbody=[]),
                        Expr(
                           value=Call(
                              func=Name(id='append_changes', ctx=Load()),
                              args=[
                                 Name(id='new_changes', ctx=Load()),
                                 Name(id='detected_changes', ctx=Load())],
                              keywords=[]))])],
               orelse=[]),
            Return(
               value=Name(id='new_changes', ctx=Load()))],
         decorator_list=[])],
   type_ignores=[])




# AST of an auxiliary function, without incremental propagation
def generate_generate_rule():
   return Module(
   body=[
      FunctionDef(
         name='generate_rule',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='big_array'),
               arg(arg='small_array'),
               arg(arg='small_slices'),
               arg(arg='extra_dims'),
               arg(arg='universal')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='domain_sizes', ctx=Store())],
               value=ListComp(
                  elt=Call(
                     func=Name(id='len', ctx=Load()),
                     args=[
                        Subscript(
                           value=Attribute(
                              value=Name(id='big_array', ctx=Load()),
                              attr='coords',
                              ctx=Load()),
                           slice=Name(id='dim', ctx=Load()),
                           ctx=Load())],
                     keywords=[]),
                  generators=[
                     comprehension(
                        target=Name(id='dim', ctx=Store()),
                        iter=Name(id='extra_dims', ctx=Load()),
                        ifs=[],
                        is_async=0)])),
            Assign(
               targets=[
                  Name(id='slice_array', ctx=Store())],
               value=ListComp(
                  elt=List(elts=[], ctx=Load()),
                  generators=[
                     comprehension(
                        target=Name(id='_', ctx=Store()),
                        iter=Call(
                           func=Name(id='range', ctx=Load()),
                           args=[
                              BinOp(
                                 left=Call(
                                    func=Attribute(
                                       value=Name(id='math', ctx=Load()),
                                       attr='prod',
                                       ctx=Load()),
                                    args=[
                                       Name(id='domain_sizes', ctx=Load())],
                                    keywords=[]),
                                 op=Add(),
                                 right=Constant(value=1))],
                           keywords=[]),
                        ifs=[],
                        is_async=0)])),
            For(
               target=Name(id='small_slice', ctx=Store()),
               iter=Name(id='small_slices', ctx=Load()),
               body=[
                  Expr(
                     value=Call(
                        func=Attribute(
                           value=Subscript(
                              value=Name(id='slice_array', ctx=Load()),
                              slice=Constant(value=0),
                              ctx=Load()),
                           attr='append',
                           ctx=Load()),
                        args=[
                           Name(id='small_slice', ctx=Load())],
                        keywords=[])),
                  Assign(
                     targets=[
                        Name(id='big_slices', ctx=Store())],
                     value=Call(
                        func=Name(id='add_dims', ctx=Load()),
                        args=[
                           List(
                              elts=[
                                 Name(id='small_slice', ctx=Load())],
                              ctx=Load()),
                           Name(id='big_array', ctx=Load()),
                           Name(id='extra_dims', ctx=Load())],
                        keywords=[])),
                  For(
                     target=Tuple(
                        elts=[
                           Name(id='i', ctx=Store()),
                           Name(id='big_slice', ctx=Store())],
                        ctx=Store()),
                     iter=Call(
                        func=Name(id='enumerate', ctx=Load()),
                        args=[
                           Name(id='big_slices', ctx=Load())],
                        keywords=[]),
                     body=[
                        Expr(
                           value=Call(
                              func=Attribute(
                                 value=Subscript(
                                    value=Name(id='slice_array', ctx=Load()),
                                    slice=BinOp(
                                       left=Name(id='i', ctx=Load()),
                                       op=Add(),
                                       right=Constant(value=1)),
                                    ctx=Load()),
                                 attr='append',
                                 ctx=Load()),
                              args=[
                                 Name(id='big_slice', ctx=Load())],
                              keywords=[]))],
                     orelse=[])],
               orelse=[]),
            Assign(
               targets=[
                  Name(id='rule', ctx=Store())],
               value=List(
                  elts=[
                     Call(
                        func=Name(id='LiteralCollection', ctx=Load()),
                        args=[
                           Attribute(
                              value=Name(id='small_array', ctx=Load()),
                              attr='name',
                              ctx=Load()),
                           Subscript(
                              value=Name(id='slice_array', ctx=Load()),
                              slice=Constant(value=0),
                              ctx=Load()),
                           UnaryOp(
                              op=Not(),
                              operand=Name(id='universal', ctx=Load()))],
                        keywords=[])],
                  ctx=Load())),
            For(
               target=Name(id='i', ctx=Store()),
               iter=Call(
                  func=Name(id='range', ctx=Load()),
                  args=[
                     Constant(value=1),
                     Call(
                        func=Name(id='len', ctx=Load()),
                        args=[
                           Name(id='slice_array', ctx=Load())],
                        keywords=[])],
                  keywords=[]),
               body=[
                  Expr(
                     value=Call(
                        func=Attribute(
                           value=Name(id='rule', ctx=Load()),
                           attr='append',
                           ctx=Load()),
                        args=[
                           Call(
                              func=Name(id='LiteralCollection', ctx=Load()),
                              args=[
                                 Attribute(
                                    value=Name(id='big_array', ctx=Load()),
                                    attr='name',
                                    ctx=Load()),
                                 Subscript(
                                    value=Name(id='slice_array', ctx=Load()),
                                    slice=Name(id='i', ctx=Load()),
                                    ctx=Load()),
                                 Name(id='universal', ctx=Load())],
                              keywords=[])],
                        keywords=[]))],
               orelse=[]),
            Return(
               value=Name(id='rule', ctx=Load()))],
         decorator_list=[])],
   type_ignores=[])






# AST of an auxiliary function
def generate_generalizing_propagation():
    return Module(
   body=[
      FunctionDef(
         name='generalizing_propagation',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='big'),
               arg(arg='small'),
               arg(arg='true_slices'),
               arg(arg='false_slices'),
               arg(arg='old_dims'),
               arg(arg='universal')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='small_array', ctx=Store())],
               value=Subscript(
                  value=Name(id='predicate_dict', ctx=Load()),
                  slice=Name(id='small', ctx=Load()),
                  ctx=Load())),
            Assign(
               targets=[
                  Name(id='big_array', ctx=Store())],
               value=Subscript(
                  value=Name(id='predicate_dict', ctx=Load()),
                  slice=Name(id='big', ctx=Load()),
                  ctx=Load())),
            Assign(
               targets=[
                  Name(id='new_changes', ctx=Store())],
               value=Dict(keys=[], values=[])),
            If(
               test=Compare(
                  left=Call(
                     func=Name(id='len', ctx=Load()),
                     args=[
                        Name(id='true_slices', ctx=Load())],
                     keywords=[]),
                  ops=[
                     Gt()],
                  comparators=[
                     Constant(value=0)]),
               body=[
                  Assign(
                     targets=[
                        Name(id='small_slices', ctx=Store())],
                     value=Call(
                        func=Name(id='reduce_dims', ctx=Load()),
                        args=[
                           Name(id='true_slices', ctx=Load()),
                           Name(id='big_array', ctx=Load()),
                           Name(id='old_dims', ctx=Load())],
                        keywords=[])),
                  If(
                     test=Name(id='universal', ctx=Load()),
                     body=[
                        Try(
                           body=[
                              Assign(
                                 targets=[
                                    Name(id='detected_changes', ctx=Store())],
                                 value=Call(
                                    func=Name(id='incremental_propagate_wrap', ctx=Load()),
                                    args=[
                                       Name(id='big_array', ctx=Load()),
                                       Name(id='small_array', ctx=Load()),
                                       Call(
                                          func=Name(id='list', ctx=Load()),
                                          args=[
                                             Name(id='small_slices', ctx=Load())],
                                          keywords=[]),
                                       Name(id='old_dims', ctx=Load()),
                                       Constant(value=True)],
                                    keywords=[])),
                              Expr(
                                 value=Call(
                                    func=Name(id='append_changes', ctx=Load()),
                                    args=[
                                       Name(id='new_changes', ctx=Load()),
                                       Name(id='detected_changes', ctx=Load())],
                                    keywords=[]))],
                           handlers=[
                              ExceptHandler(
                                 type=Name(id='Exception', ctx=Load()),
                                 name='e',
                                 body=[
                                    Raise(
                                       exc=Call(
                                          func=Name(id='Exception', ctx=Load()),
                                          args=[
                                             Name(id='e', ctx=Load())],
                                          keywords=[]))])],
                           orelse=[],
                           finalbody=[])],
                     orelse=[
                        Try(
                           body=[
                              Assign(
                                 targets=[
                                    Name(id='detected_changes', ctx=Store())],
                                 value=Call(
                                    func=Name(id='unconditional_propagate_wrap', ctx=Load()),
                                    args=[
                                       Name(id='small_array', ctx=Load()),
                                       Call(
                                          func=Name(id='list', ctx=Load()),
                                          args=[
                                             Name(id='small_slices', ctx=Load())],
                                          keywords=[]),
                                       Constant(value=True)],
                                    keywords=[])),
                              Expr(
                                 value=Call(
                                    func=Name(id='append_changes', ctx=Load()),
                                    args=[
                                       Name(id='new_changes', ctx=Load()),
                                       Name(id='detected_changes', ctx=Load())],
                                    keywords=[]))],
                           handlers=[
                              ExceptHandler(
                                 type=Name(id='Exception', ctx=Load()),
                                 name='e',
                                 body=[
                                    Raise(
                                       exc=Call(
                                          func=Name(id='Exception', ctx=Load()),
                                          args=[
                                             Name(id='e', ctx=Load())],
                                          keywords=[]))])],
                           orelse=[],
                           finalbody=[])])],
               orelse=[]),
            If(
               test=Compare(
                  left=Call(
                     func=Name(id='len', ctx=Load()),
                     args=[
                        Name(id='false_slices', ctx=Load())],
                     keywords=[]),
                  ops=[
                     Gt()],
                  comparators=[
                     Constant(value=0)]),
               body=[
                  Assign(
                     targets=[
                        Name(id='small_slices', ctx=Store())],
                     value=Call(
                        func=Name(id='reduce_dims', ctx=Load()),
                        args=[
                           Name(id='false_slices', ctx=Load()),
                           Name(id='big_array', ctx=Load()),
                           Name(id='old_dims', ctx=Load())],
                        keywords=[])),
                  If(
                     test=Name(id='universal', ctx=Load()),
                     body=[
                        Try(
                           body=[
                              Assign(
                                 targets=[
                                    Name(id='detected_changes', ctx=Store())],
                                 value=Call(
                                    func=Name(id='unconditional_propagate_wrap', ctx=Load()),
                                    args=[
                                       Name(id='small_array', ctx=Load()),
                                       Call(
                                          func=Name(id='list', ctx=Load()),
                                          args=[
                                             Name(id='small_slices', ctx=Load())],
                                          keywords=[]),
                                       Constant(value=False)],
                                    keywords=[])),
                              Expr(
                                 value=Call(
                                    func=Name(id='append_changes', ctx=Load()),
                                    args=[
                                       Name(id='new_changes', ctx=Load()),
                                       Name(id='detected_changes', ctx=Load())],
                                    keywords=[]))],
                           handlers=[
                              ExceptHandler(
                                 type=Name(id='Exception', ctx=Load()),
                                 name='e',
                                 body=[
                                    Raise(
                                       exc=Call(
                                          func=Name(id='Exception', ctx=Load()),
                                          args=[
                                             Name(id='e', ctx=Load())],
                                          keywords=[]))])],
                           orelse=[],
                           finalbody=[])],
                     orelse=[
                        Try(
                           body=[
                              Assign(
                                 targets=[
                                    Name(id='detected_changes', ctx=Store())],
                                 value=Call(
                                    func=Name(id='incremental_propagate_wrap', ctx=Load()),
                                    args=[
                                       Name(id='big_array', ctx=Load()),
                                       Name(id='small_array', ctx=Load()),
                                       Call(
                                          func=Name(id='list', ctx=Load()),
                                          args=[
                                             Name(id='small_slices', ctx=Load())],
                                          keywords=[]),
                                       Name(id='old_dims', ctx=Load()),
                                       Constant(value=False)],
                                    keywords=[])),
                              Expr(
                                 value=Call(
                                    func=Name(id='append_changes', ctx=Load()),
                                    args=[
                                       Name(id='new_changes', ctx=Load()),
                                       Name(id='detected_changes', ctx=Load())],
                                    keywords=[]))],
                           handlers=[
                              ExceptHandler(
                                 type=Name(id='Exception', ctx=Load()),
                                 name='e',
                                 body=[
                                    Raise(
                                       exc=Call(
                                          func=Name(id='Exception', ctx=Load()),
                                          args=[
                                             Name(id='e', ctx=Load())],
                                          keywords=[]))])],
                           orelse=[],
                           finalbody=[])])],
               orelse=[]),
            Return(
               value=Name(id='new_changes', ctx=Load()))],
         decorator_list=[])],
   type_ignores=[])



# AST of an auxiliary function, without incremental propagation

def generate_generalizing_propagation_2():
   return Module(
   body=[
      FunctionDef(
         name='generalizing_propagation',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='big'),
               arg(arg='small'),
               arg(arg='true_slices'),
               arg(arg='false_slices'),
               arg(arg='old_dims'),
               arg(arg='universal')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='small_array', ctx=Store())],
               value=Subscript(
                  value=Name(id='predicate_dict', ctx=Load()),
                  slice=Name(id='small', ctx=Load()),
                  ctx=Load())),
            Assign(
               targets=[
                  Name(id='big_array', ctx=Store())],
               value=Subscript(
                  value=Name(id='predicate_dict', ctx=Load()),
                  slice=Name(id='big', ctx=Load()),
                  ctx=Load())),
            Assign(
               targets=[
                  Name(id='new_changes', ctx=Store())],
               value=Dict(keys=[], values=[])),
            If(
               test=Compare(
                  left=Call(
                     func=Name(id='len', ctx=Load()),
                     args=[
                        Name(id='true_slices', ctx=Load())],
                     keywords=[]),
                  ops=[
                     Gt()],
                  comparators=[
                     Constant(value=0)]),
               body=[
                  Assign(
                     targets=[
                        Name(id='small_slices', ctx=Store())],
                     value=Call(
                        func=Name(id='reduce_dims', ctx=Load()),
                        args=[
                           Name(id='true_slices', ctx=Load()),
                           Name(id='big_array', ctx=Load()),
                           Name(id='old_dims', ctx=Load())],
                        keywords=[])),
                  If(
                     test=Name(id='universal', ctx=Load()),
                     body=[
                        Assign(
                           targets=[
                              Name(id='rule', ctx=Store())],
                           value=Call(
                              func=Name(id='generate_rule', ctx=Load()),
                              args=[
                                 Name(id='big_array', ctx=Load()),
                                 Name(id='small_array', ctx=Load()),
                                 Name(id='small_slices', ctx=Load()),
                                 Name(id='old_dims', ctx=Load()),
                                 Constant(value=True)],
                              keywords=[])),
                        Try(
                           body=[
                              Assign(
                                 targets=[
                                    Name(id='detected_changes', ctx=Store())],
                                 value=Call(
                                    func=Name(id='normal_propagation', ctx=Load()),
                                    args=[
                                       Name(id='rule', ctx=Load())],
                                    keywords=[])),
                              Expr(
                                 value=Call(
                                    func=Name(id='append_changes', ctx=Load()),
                                    args=[
                                       Name(id='new_changes', ctx=Load()),
                                       Name(id='detected_changes', ctx=Load())],
                                    keywords=[]))],
                           handlers=[
                              ExceptHandler(
                                 type=Name(id='Exception', ctx=Load()),
                                 name='e',
                                 body=[
                                    Raise(
                                       exc=Call(
                                          func=Name(id='Exception', ctx=Load()),
                                          args=[
                                             Name(id='e', ctx=Load())],
                                          keywords=[]))])],
                           orelse=[],
                           finalbody=[])],
                     orelse=[
                        Try(
                           body=[
                              Assign(
                                 targets=[
                                    Name(id='detected_changes', ctx=Store())],
                                 value=Call(
                                    func=Name(id='unconditional_propagate_wrap', ctx=Load()),
                                    args=[
                                       Name(id='small_array', ctx=Load()),
                                       Call(
                                          func=Name(id='list', ctx=Load()),
                                          args=[
                                             Name(id='small_slices', ctx=Load())],
                                          keywords=[]),
                                       Constant(value=True)],
                                    keywords=[])),
                              Expr(
                                 value=Call(
                                    func=Name(id='append_changes', ctx=Load()),
                                    args=[
                                       Name(id='new_changes', ctx=Load()),
                                       Name(id='detected_changes', ctx=Load())],
                                    keywords=[]))],
                           handlers=[
                              ExceptHandler(
                                 type=Name(id='Exception', ctx=Load()),
                                 name='e',
                                 body=[
                                    Raise(
                                       exc=Call(
                                          func=Name(id='Exception', ctx=Load()),
                                          args=[
                                             Name(id='e', ctx=Load())],
                                          keywords=[]))])],
                           orelse=[],
                           finalbody=[])])],
               orelse=[]),
            If(
               test=Compare(
                  left=Call(
                     func=Name(id='len', ctx=Load()),
                     args=[
                        Name(id='false_slices', ctx=Load())],
                     keywords=[]),
                  ops=[
                     Gt()],
                  comparators=[
                     Constant(value=0)]),
               body=[
                  Assign(
                     targets=[
                        Name(id='small_slices', ctx=Store())],
                     value=Call(
                        func=Name(id='reduce_dims', ctx=Load()),
                        args=[
                           Name(id='false_slices', ctx=Load()),
                           Name(id='big_array', ctx=Load()),
                           Name(id='old_dims', ctx=Load())],
                        keywords=[])),
                  If(
                     test=Name(id='universal', ctx=Load()),
                     body=[
                        Try(
                           body=[
                              Assign(
                                 targets=[
                                    Name(id='detected_changes', ctx=Store())],
                                 value=Call(
                                    func=Name(id='unconditional_propagate_wrap', ctx=Load()),
                                    args=[
                                       Name(id='small_array', ctx=Load()),
                                       Call(
                                          func=Name(id='list', ctx=Load()),
                                          args=[
                                             Name(id='small_slices', ctx=Load())],
                                          keywords=[]),
                                       Constant(value=False)],
                                    keywords=[])),
                              Expr(
                                 value=Call(
                                    func=Name(id='append_changes', ctx=Load()),
                                    args=[
                                       Name(id='new_changes', ctx=Load()),
                                       Name(id='detected_changes', ctx=Load())],
                                    keywords=[]))],
                           handlers=[
                              ExceptHandler(
                                 type=Name(id='Exception', ctx=Load()),
                                 name='e',
                                 body=[
                                    Raise(
                                       exc=Call(
                                          func=Name(id='Exception', ctx=Load()),
                                          args=[
                                             Name(id='e', ctx=Load())],
                                          keywords=[]))])],
                           orelse=[],
                           finalbody=[])],
                     orelse=[
                        Assign(
                           targets=[
                              Name(id='rule', ctx=Store())],
                           value=Call(
                              func=Name(id='generate_rule', ctx=Load()),
                              args=[
                                 Name(id='big_array', ctx=Load()),
                                 Name(id='small_array', ctx=Load()),
                                 Name(id='small_slices', ctx=Load()),
                                 Name(id='old_dims', ctx=Load()),
                                 Constant(value=False)],
                              keywords=[])),
                        Try(
                           body=[
                              Assign(
                                 targets=[
                                    Name(id='detected_changes', ctx=Store())],
                                 value=Call(
                                    func=Name(id='normal_propagation', ctx=Load()),
                                    args=[
                                       Name(id='rule', ctx=Load())],
                                    keywords=[])),
                              Expr(
                                 value=Call(
                                    func=Name(id='append_changes', ctx=Load()),
                                    args=[
                                       Name(id='new_changes', ctx=Load()),
                                       Name(id='detected_changes', ctx=Load())],
                                    keywords=[]))],
                           handlers=[
                              ExceptHandler(
                                 type=Name(id='Exception', ctx=Load()),
                                 name='e',
                                 body=[
                                    Raise(
                                       exc=Call(
                                          func=Name(id='Exception', ctx=Load()),
                                          args=[
                                             Name(id='e', ctx=Load())],
                                          keywords=[]))])],
                           orelse=[],
                           finalbody=[])])],
               orelse=[]),
            Return(
               value=Name(id='new_changes', ctx=Load()))],
         decorator_list=[])],
   type_ignores=[])




# AST of an auxiliary function

def generate_add_all_function_outputs():
    return Module(
   body=[
      FunctionDef(
         name='add_all_function_outputs',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='data_array'),
               arg(arg='slice')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='all_outputs', ctx=Store())],
               value=List(elts=[], ctx=Load())),
            Assign(
               targets=[
                  Name(id='scope', ctx=Store())],
               value=Attribute(
                  value=Subscript(
                     value=Attribute(
                        value=Name(id='data_array', ctx=Load()),
                        attr='coords',
                        ctx=Load()),
                     slice=Subscript(
                        value=Attribute(
                           value=Name(id='data_array', ctx=Load()),
                           attr='dims',
                           ctx=Load()),
                        slice=UnaryOp(
                           op=USub(),
                           operand=Constant(value=1)),
                        ctx=Load()),
                     ctx=Load()),
                  attr='values',
                  ctx=Load())),
            For(
               target=Name(id='elem', ctx=Store()),
               iter=Name(id='scope', ctx=Load()),
               body=[
                  If(
                     test=Compare(
                        left=Name(id='elem', ctx=Load()),
                        ops=[
                           NotEq()],
                        comparators=[
                           Subscript(
                              value=Name(id='slice', ctx=Load()),
                              slice=UnaryOp(
                                 op=USub(),
                                 operand=Constant(value=1)),
                              ctx=Load())]),
                     body=[
                        Expr(
                           value=Call(
                              func=Attribute(
                                 value=Name(id='all_outputs', ctx=Load()),
                                 attr='append',
                                 ctx=Load()),
                              args=[
                                 BinOp(
                                    left=Subscript(
                                       value=Name(id='slice', ctx=Load()),
                                       slice=Slice(
                                          upper=UnaryOp(
                                             op=USub(),
                                             operand=Constant(value=1))),
                                       ctx=Load()),
                                    op=Add(),
                                    right=Tuple(
                                       elts=[
                                          Call(
                                             func=Attribute(
                                                value=Name(id='elem', ctx=Load()),
                                                attr='item',
                                                ctx=Load()),
                                             args=[],
                                             keywords=[])],
                                       ctx=Load()))],
                              keywords=[]))],
                     orelse=[])],
               orelse=[]),
            Return(
               value=Name(id='all_outputs', ctx=Load()))],
         decorator_list=[])],
   type_ignores=[])


# AST of an auxiliary function

def generate_function_propagation():
    return Module(
   body=[
      FunctionDef(
         name='function_propagation',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='name'),
               arg(arg='true_slices'),
               arg(arg='false_slices')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='new_changes', ctx=Store())],
               value=Dict(keys=[], values=[])),
            Assign(
               targets=[
                  Name(id='data_array', ctx=Store())],
               value=Subscript(
                  value=Name(id='predicate_dict', ctx=Load()),
                  slice=Name(id='name', ctx=Load()),
                  ctx=Load())),
            If(
               test=Compare(
                  left=Call(
                     func=Name(id='len', ctx=Load()),
                     args=[
                        Name(id='true_slices', ctx=Load())],
                     keywords=[]),
                  ops=[
                     Gt()],
                  comparators=[
                     Constant(value=0)]),
               body=[
                  Assign(
                     targets=[
                        Name(id='corresponding_function_slices', ctx=Store())],
                     value=ListComp(
                        elt=Call(
                           func=Name(id='add_all_function_outputs', ctx=Load()),
                           args=[
                              Name(id='data_array', ctx=Load()),
                              Name(id='slice', ctx=Load())],
                           keywords=[]),
                        generators=[
                           comprehension(
                              target=Name(id='slice', ctx=Store()),
                              iter=Name(id='true_slices', ctx=Load()),
                              ifs=[],
                              is_async=0)])),
                  Assign(
                     targets=[
                        Name(id='corresponding_function_slices_flat', ctx=Store())],
                     value=ListComp(
                        elt=Name(id='item', ctx=Load()),
                        generators=[
                           comprehension(
                              target=Name(id='sublist', ctx=Store()),
                              iter=Name(id='corresponding_function_slices', ctx=Load()),
                              ifs=[],
                              is_async=0),
                           comprehension(
                              target=Name(id='item', ctx=Store()),
                              iter=Name(id='sublist', ctx=Load()),
                              ifs=[],
                              is_async=0)])),
                  Try(
                     body=[
                        Assign(
                           targets=[
                              Name(id='detected_changes', ctx=Store())],
                           value=Call(
                              func=Name(id='unconditional_propagate_wrap', ctx=Load()),
                              args=[
                                 Name(id='data_array', ctx=Load()),
                                 Name(id='corresponding_function_slices_flat', ctx=Load()),
                                 Constant(value=False)],
                              keywords=[]))],
                     handlers=[
                        ExceptHandler(
                           type=Name(id='Exception', ctx=Load()),
                           name='e',
                           body=[
                              Raise(
                                 exc=Call(
                                    func=Name(id='Exception', ctx=Load()),
                                    args=[
                                       Name(id='e', ctx=Load())],
                                    keywords=[]))])],
                     orelse=[],
                     finalbody=[]),
                  Expr(
                     value=Call(
                        func=Name(id='append_changes', ctx=Load()),
                        args=[
                           Name(id='new_changes', ctx=Load()),
                           Name(id='detected_changes', ctx=Load())],
                        keywords=[]))],
               orelse=[]),
            If(
               test=Compare(
                  left=Call(
                     func=Name(id='len', ctx=Load()),
                     args=[
                        Name(id='false_slices', ctx=Load())],
                     keywords=[]),
                  ops=[
                     Gt()],
                  comparators=[
                     Constant(value=0)]),
               body=[
                  Assign(
                     targets=[
                        Name(id='last_dim', ctx=Store())],
                     value=Subscript(
                        value=Attribute(
                           value=Subscript(
                              value=Name(id='predicate_dict', ctx=Load()),
                              slice=Name(id='name', ctx=Load()),
                              ctx=Load()),
                           attr='dims',
                           ctx=Load()),
                        slice=UnaryOp(
                           op=USub(),
                           operand=Constant(value=1)),
                        ctx=Load())),
                  Assign(
                     targets=[
                        Name(id='reduced_slices', ctx=Store())],
                     value=Call(
                        func=Name(id='reduce_dims', ctx=Load()),
                        args=[
                           Name(id='false_slices', ctx=Load()),
                           Name(id='data_array', ctx=Load()),
                           List(
                              elts=[
                                 Name(id='last_dim', ctx=Load())],
                              ctx=Load())],
                        keywords=[])),
                  Try(
                     body=[
                        Assign(
                           targets=[
                              Name(id='detected_changes', ctx=Store())],
                           value=Call(
                              func=Name(id='incremental_propagate', ctx=Load()),
                              args=[
                                 Subscript(
                                    value=Name(id='predicate_dict', ctx=Load()),
                                    slice=Name(id='name', ctx=Load()),
                                    ctx=Load()),
                                 Call(
                                    func=Name(id='list', ctx=Load()),
                                    args=[
                                       Name(id='reduced_slices', ctx=Load())],
                                    keywords=[]),
                                 List(
                                    elts=[
                                       Name(id='last_dim', ctx=Load())],
                                    ctx=Load()),
                                 Constant(value=False)],
                              keywords=[]))],
                     handlers=[
                        ExceptHandler(
                           type=Name(id='Exception', ctx=Load()),
                           name='e',
                           body=[
                              Raise(
                                 exc=Call(
                                    func=Name(id='Exception', ctx=Load()),
                                    args=[
                                       Name(id='e', ctx=Load())],
                                    keywords=[]))])],
                     orelse=[],
                     finalbody=[]),
                  Expr(
                     value=Call(
                        func=Name(id='append_changes', ctx=Load()),
                        args=[
                           Name(id='new_changes', ctx=Load()),
                           Name(id='detected_changes', ctx=Load())],
                        keywords=[]))],
               orelse=[]),
            Return(
               value=Name(id='new_changes', ctx=Load()))],
         decorator_list=[])],
   type_ignores=[])


# AST for an auxiliary function, without incremental propagation
def generate_function_propagation_2():
   return Module(
   body=[
      FunctionDef(
         name='function_propagation',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='name'),
               arg(arg='true_slices'),
               arg(arg='false_slices')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='new_changes', ctx=Store())],
               value=Dict(keys=[], values=[])),
            Assign(
               targets=[
                  Name(id='data_array', ctx=Store())],
               value=Subscript(
                  value=Name(id='predicate_dict', ctx=Load()),
                  slice=Name(id='name', ctx=Load()),
                  ctx=Load())),
            If(
               test=Compare(
                  left=Call(
                     func=Name(id='len', ctx=Load()),
                     args=[
                        Name(id='true_slices', ctx=Load())],
                     keywords=[]),
                  ops=[
                     Gt()],
                  comparators=[
                     Constant(value=0)]),
               body=[
                  Assign(
                     targets=[
                        Name(id='corresponding_function_slices', ctx=Store())],
                     value=ListComp(
                        elt=Call(
                           func=Name(id='add_all_function_outputs', ctx=Load()),
                           args=[
                              Name(id='data_array', ctx=Load()),
                              Name(id='slice', ctx=Load())],
                           keywords=[]),
                        generators=[
                           comprehension(
                              target=Name(id='slice', ctx=Store()),
                              iter=Name(id='true_slices', ctx=Load()),
                              ifs=[],
                              is_async=0)])),
                  Assign(
                     targets=[
                        Name(id='corresponding_function_slices_flat', ctx=Store())],
                     value=ListComp(
                        elt=Name(id='item', ctx=Load()),
                        generators=[
                           comprehension(
                              target=Name(id='sublist', ctx=Store()),
                              iter=Name(id='corresponding_function_slices', ctx=Load()),
                              ifs=[],
                              is_async=0),
                           comprehension(
                              target=Name(id='item', ctx=Store()),
                              iter=Name(id='sublist', ctx=Load()),
                              ifs=[],
                              is_async=0)])),
                  Try(
                     body=[
                        Assign(
                           targets=[
                              Name(id='detected_changes', ctx=Store())],
                           value=Call(
                              func=Name(id='unconditional_propagate_wrap', ctx=Load()),
                              args=[
                                 Name(id='data_array', ctx=Load()),
                                 Name(id='corresponding_function_slices_flat', ctx=Load()),
                                 Constant(value=False)],
                              keywords=[]))],
                     handlers=[
                        ExceptHandler(
                           type=Name(id='Exception', ctx=Load()),
                           name='e',
                           body=[
                              Raise(
                                 exc=Call(
                                    func=Name(id='Exception', ctx=Load()),
                                    args=[
                                       Name(id='e', ctx=Load())],
                                    keywords=[]))])],
                     orelse=[],
                     finalbody=[]),
                  Expr(
                     value=Call(
                        func=Name(id='append_changes', ctx=Load()),
                        args=[
                           Name(id='new_changes', ctx=Load()),
                           Name(id='detected_changes', ctx=Load())],
                        keywords=[]))],
               orelse=[]),
            If(
               test=Compare(
                  left=Call(
                     func=Name(id='len', ctx=Load()),
                     args=[
                        Name(id='false_slices', ctx=Load())],
                     keywords=[]),
                  ops=[
                     Gt()],
                  comparators=[
                     Constant(value=0)]),
               body=[
                  Assign(
                     targets=[
                        Name(id='corresponding_function_slices', ctx=Store())],
                     value=ListComp(
                        elt=Call(
                           func=Name(id='add_all_function_outputs', ctx=Load()),
                           args=[
                              Name(id='data_array', ctx=Load()),
                              Name(id='slice', ctx=Load())],
                           keywords=[]),
                        generators=[
                           comprehension(
                              target=Name(id='slice', ctx=Store()),
                              iter=Name(id='false_slices', ctx=Load()),
                              ifs=[],
                              is_async=0)])),
                  Try(
                     body=[
                        Assign(
                           targets=[
                              Name(id='detected_changes', ctx=Store())],
                           value=Call(
                              func=Name(id='normal_propagation', ctx=Load()),
                              args=[
                                 ListComp(
                                    elt=Call(
                                       func=Name(id='LiteralCollection', ctx=Load()),
                                       args=[
                                          Name(id='name', ctx=Load()),
                                          Name(id='sl', ctx=Load()),
                                          Constant(value=False)],
                                       keywords=[]),
                                    generators=[
                                       comprehension(
                                          target=Name(id='sl', ctx=Store()),
                                          iter=Call(
                                             func=Name(id='list', ctx=Load()),
                                             args=[
                                                Call(
                                                   func=Name(id='map', ctx=Load()),
                                                   args=[
                                                      Name(id='list', ctx=Load()),
                                                      Call(
                                                         func=Name(id='zip', ctx=Load()),
                                                         args=[
                                                            Starred(
                                                               value=Name(id='corresponding_function_slices', ctx=Load()),
                                                               ctx=Load())],
                                                         keywords=[])],
                                                   keywords=[])],
                                             keywords=[]),
                                          ifs=[],
                                          is_async=0)])],
                              keywords=[]))],
                     handlers=[
                        ExceptHandler(
                           type=Name(id='Exception', ctx=Load()),
                           name='e',
                           body=[
                              Raise(
                                 exc=Call(
                                    func=Name(id='Exception', ctx=Load()),
                                    args=[
                                       Name(id='e', ctx=Load())],
                                    keywords=[]))])],
                     orelse=[],
                     finalbody=[]),
                  Expr(
                     value=Call(
                        func=Name(id='append_changes', ctx=Load()),
                        args=[
                           Name(id='new_changes', ctx=Load()),
                           Name(id='detected_changes', ctx=Load())],
                        keywords=[]))],
               orelse=[]),
            Return(
               value=Name(id='new_changes', ctx=Load()))],
         decorator_list=[])],
   type_ignores=[])




# This function gets a normal propagator as input, and returns an AST consisting of LiteralCollections.
def get_literal_collections_for_normal_propagator(normal_propagator):
    rule = []
    for lit in normal_propagator.unsat:
        rule.append(Call(
            func=Name(id='LiteralCollection', ctx=Load()),
            args=[
                Constant(value=lit.atom.name),
                Subscript(
                    value=Name(id='slicing_dict', ctx=Load()),
                    slice=Constant(value=lit.atom.name),
                    ctx=Load()),
                Constant(value=lit.pos)],
            keywords=[]))
    return rule

# This function adds the code for a normal propagator to the propagate() function.
def generate_propagate_rule_from_normal_propagation(normal_prop, var, truth):
    if truth:
        change_array = 'true_slicing'
    else:
        change_array = 'false_slicing'
    quantified_var = [Constant(value=var.name) for var in normal_prop.bindings]
    argument_keys = [Constant(value=lit.atom.name) for lit in normal_prop.unsat]
    argument_values = [List(elts=[Constant(value=arg.name) for arg in lit.atom.args], ctx=Load()) for lit in normal_prop.unsat]
    literal_collections = get_literal_collections_for_normal_propagator(normal_prop)
    #argument_dict
    return Module(
   body=[
       If(
         test=Compare(
            left=Call(
               func=Name(id='len', ctx=Load()),
               args=[
                  Attribute(
                     value=Name(id='change', ctx=Load()),
                     attr=change_array,
                     ctx=Load())],
               keywords=[]),
            ops=[
               Gt()],
            comparators=[
               Constant(value=0)]),
         body=[
            Assign(
               targets=[
                  Name(id='quantified_var', ctx=Store())],
               value=List(
                  elts=quantified_var,
                  ctx=Load())),
            Assign(
               targets=[
                  Name(id='argument_dict', ctx=Store())],
               value=Dict(
                  keys=argument_keys,
                  values=argument_values)),
            Assign(
               targets=[
                  Name(id='slicing_dict', ctx=Store())],
               value=Call(
                  func=Name(id='map_indices_wrap', ctx=Load()),
                  args=[
                     Name(id='argument_dict', ctx=Load()),
                     Attribute(
                        value=Name(id='change', ctx=Load()),
                        attr='name',
                        ctx=Load()),
                     Attribute(
                        value=Name(id='change', ctx=Load()),
                        attr=change_array,
                        ctx=Load()),
                     Name(id='quantified_var', ctx=Load())],
                  keywords=[])),
            If(
               test=BoolOp(
                  op=And(),
                  values=[
                     Compare(
                        left=Name(id='slicing_dict', ctx=Load()),
                        ops=[
                           IsNot()],
                        comparators=[
                           Constant(value=None)]),
                     Compare(
                        left=Call(
                           func=Name(id='len', ctx=Load()),
                           args=[
                              Subscript(
                                 value=Name(id='slicing_dict', ctx=Load()),
                                 slice=Constant(value=var),
                                 ctx=Load())],
                           keywords=[]),
                        ops=[
                           Gt()],
                        comparators=[
                           Constant(value=0)])]),
               body=[
                  Try(
                     body=[
                        Assign(
                           targets=[
                              Name(id='detected_changes', ctx=Store())],
                           value=Call(
                              func=Name(id='normal_propagation', ctx=Load()),
                              args=[
                                 List(
                                    elts=literal_collections,
                                    ctx=Load())],
                              keywords=[])),
                        Expr(
                           value=Call(
                              func=Name(id='append_changes', ctx=Load()),
                              args=[
                                 Name(id='new_changes', ctx=Load()),
                                 Name(id='detected_changes', ctx=Load())],
                              keywords=[]))],
                     handlers=[
                        ExceptHandler(
                           type=Name(id='Exception', ctx=Load()),
                           name='e',
                           body=[
                              Raise(
                                 exc=Call(
                                    func=Name(id='Exception', ctx=Load()),
                                    args=[
                                       Name(id='e', ctx=Load())],
                                    keywords=[]))])],
                     orelse=[],
                     finalbody=[])],
               orelse=[])],
         orelse=[])],
   type_ignores=[])


# This function determines the new dimensions of an atom compared to another atom.
def determine_new_dimensions(old, new):
    new_dims = []
    old_arguments = [arg.name for arg in old.atom.args]
    for i, arg in enumerate(new.atom.args):
        if arg.name not in old_arguments:
            new_dims.append(Constant(value=f'x{i}'))
    return new_dims

# This function adds the code for a 'specifying propagator' to the propagate() function.
def generate_propagate_rule_from_specifying_propagation(sp):
    new_dims = determine_new_dimensions(sp.general, sp.specific)
    return Module(
   body=[
      Try(
         body=[
            Assign(
               targets=[
                  Name(id='new_dims', ctx=Store())],
               value=List(
                  elts=new_dims,
                  ctx=Load())),
            Assign(
               targets=[
                  Name(id='detected_changes', ctx=Store())],
               value=Call(
                  func=Name(id='specifying_propagation', ctx=Load()),
                  args=[
                     Constant(value=sp.specific.atom.name),
                     Attribute(
                        value=Name(id='change', ctx=Load()),
                        attr='true_slicing',
                        ctx=Load()),
                     Attribute(
                        value=Name(id='change', ctx=Load()),
                        attr='false_slicing',
                        ctx=Load()),
                     Name(id='new_dims', ctx=Load()),
                     Constant(value=sp.universal)],
                  keywords=[])),
            Expr(
               value=Call(
                  func=Name(id='append_changes', ctx=Load()),
                  args=[
                     Name(id='new_changes', ctx=Load()),
                     Name(id='detected_changes', ctx=Load())],
                  keywords=[]))],
         handlers=[
            ExceptHandler(
               type=Name(id='Exception', ctx=Load()),
               name='e',
               body=[
                  Raise(
                     exc=Call(
                        func=Name(id='Exception', ctx=Load()),
                        args=[
                           Name(id='e', ctx=Load())],
                        keywords=[]))])],
         orelse=[],
         finalbody=[])],
   type_ignores=[])

# This function adds the code for a 'generalizing propagator' to the propagate() function.
def generate_propagate_rule_from_generalizing_propagation(ge):
    old_dims = determine_new_dimensions(ge.general, ge.specific)
    return Module(
        body=[
      Try(
         body=[
            Assign(
               targets=[
                  Name(id='old_dims', ctx=Store())],
               value=List(
                  elts=old_dims,
                  ctx=Load())),
            Assign(
               targets=[
                  Name(id='detected_changes', ctx=Store())],
               value=Call(
                  func=Name(id='generalizing_propagation', ctx=Load()),
                  args=[
                     Constant(value=ge.specific.atom.name),
                     Constant(value=ge.general.atom.name),
                     Attribute(
                        value=Name(id='change', ctx=Load()),
                        attr='true_slicing',
                        ctx=Load()),
                     Attribute(
                        value=Name(id='change', ctx=Load()),
                        attr='false_slicing',
                        ctx=Load()),
                     Name(id='old_dims', ctx=Load()),
                     Constant(value=ge.universal)],
                  keywords=[])),
            Expr(
               value=Call(
                  func=Name(id='append_changes', ctx=Load()),
                  args=[
                     Name(id='new_changes', ctx=Load()),
                     Name(id='detected_changes', ctx=Load())],
                  keywords=[]))],
         handlers=[
            ExceptHandler(
               type=Name(id='Exception', ctx=Load()),
               name='e',
               body=[
                  Raise(
                     exc=Call(
                        func=Name(id='Exception', ctx=Load()),
                        args=[
                           Name(id='e', ctx=Load())],
                        keywords=[]))])],
         orelse=[],
         finalbody=[])],
   type_ignores=[])

# This function adds the code for a 'function propagator' to the propagate() function.
def generate_propagate_rule_from_function_propagation(prop):
    return Module(
   body=[
      Try(
         body=[
            Assign(
               targets=[
                  Name(id='detected_changes', ctx=Store())],
               value=Call(
                  func=Name(id='function_propagation', ctx=Load()),
                  args=[
                     Constant(value=prop.name),
                     Attribute(
                        value=Name(id='change', ctx=Load()),
                        attr='true_slicing',
                        ctx=Load()),
                     Attribute(
                        value=Name(id='change', ctx=Load()),
                        attr='false_slicing',
                        ctx=Load())],
                  keywords=[])),
            Expr(
               value=Call(
                  func=Name(id='append_changes', ctx=Load()),
                  args=[
                     Name(id='new_changes', ctx=Load()),
                     Name(id='detected_changes', ctx=Load())],
                  keywords=[]))],
         handlers=[
            ExceptHandler(
               type=Name(id='Exception', ctx=Load()),
               name='e',
               body=[
                  Raise(
                     exc=Call(
                        func=Name(id='Exception', ctx=Load()),
                        args=[
                           Name(id='e', ctx=Load())],
                        keywords=[]))])],
         orelse=[],
         finalbody=[])],
   type_ignores=[])

# This function generates the code for all propagators belonging to a certain atom name.
def generate_propagator_code(atom_name, propagators):
    if_body = []
    for prop in propagators:
        if type(prop) == NormalPropagator:
            truth_value = prop.unsat[0].pos
            if_body.append(generate_propagate_rule_from_normal_propagation(prop, atom_name, truth_value).body)
        if type(prop) == SpecifyingPropagator:
            if_body.append(generate_propagate_rule_from_specifying_propagation(prop))
        if type(prop) == GeneralizingPropagator:
            if_body.append(generate_propagate_rule_from_generalizing_propagation(prop))
        if type(prop) == FunctionPropagator:
            if_body.append(generate_propagate_rule_from_function_propagation(prop))
    return If(
         test=Compare(
            left=Attribute(
               value=Name(id='change', ctx=Load()),
               attr='name',
               ctx=Load()),
            ops=[
               Eq()],
            comparators=[
               Constant(value=atom_name)]),
         body=if_body,
         orelse=[])


# This function generates the propagate() function based on the dictionary that contains propagators for every predicate/function name in the IDP-program.
def generate_propagate(grouped_propagators):
    cases = []
    for key, val in grouped_propagators.items():
        propagators = generate_propagator_code(key, val)
        cases.append(propagators)
    return Module(
   body=[
      FunctionDef(
         name='propagate',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='changes')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='new_changes', ctx=Store())],
               value=Dict(keys=[], values=[])),
            For(
               target=Name(id='change', ctx=Store()),
               iter=Call(
                  func=Attribute(
                     value=Name(id='changes', ctx=Load()),
                     attr='values',
                     ctx=Load()),
                  args=[],
                  keywords=[]),
               body=cases,
               orelse=[]),
            Return(
               value=Name(id='new_changes', ctx=Load()))],
         decorator_list=[])],
   type_ignores=[])

# AST of an auxiliary function
def generate_propagate_full():
    return Module(
   body=[
      FunctionDef(
         name='propagate_full',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='changes')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            While(
               test=Compare(
                  left=Call(
                     func=Name(id='len', ctx=Load()),
                     args=[
                        Name(id='changes', ctx=Load())],
                     keywords=[]),
                  ops=[
                     NotEq()],
                  comparators=[
                     Constant(value=0)]),
               body=[
                  Assign(
                     targets=[
                        Name(id='changes', ctx=Store())],
                     value=Call(
                        func=Name(id='propagate', ctx=Load()),
                        args=[
                           Name(id='changes', ctx=Load())],
                        keywords=[]))],
               orelse=[])],
         decorator_list=[])],
   type_ignores=[])


# This function generates code to support mathematical operators (=, !=, <, <=, >, >=)
def get_domain_elements_tested_on_equality(enfs, types):
    domain_elem = set()
    operators = set()
    for enf in enfs:
        if type(enf) == ENFConjunctive:
            if len(enf.right) == 1 and enf.right[0].atom.name in [';EQ', '_NEQ', '_GE', '_GEQ', '_LE', '_LEQ']:
                operators.add(enf.right[0].atom.name)
                tested_types = [var.type for var in enf.bindings]
                tested_domains = [create_full_domain(t.domain) for t in types if t.name in tested_types]
                tested_domains_flat = [item for sublist in tested_domains for item in sublist]
                domain_elem.update(set(tested_domains_flat))
    return domain_elem, operators

# AST of an auxiliary function
def generate_fill_in_interpreted_domain():
    return Module(
   body=[
      FunctionDef(
         name='fill_in_interpreted_domain',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='predicate_list')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='changes', ctx=Store())],
               value=Dict(keys=[], values=[])),
            For(
               target=Name(id='pred', ctx=Store()),
               iter=Name(id='predicate_list', ctx=Load()),
               body=[
                  Assign(
                     targets=[
                        Name(id='data_array', ctx=Store())],
                     value=Subscript(
                        value=Name(id='predicate_dict', ctx=Load()),
                        slice=Name(id='pred', ctx=Load()),
                        ctx=Load())),
                  Assign(
                     targets=[
                        Name(id='mask', ctx=Store())],
                     value=Compare(
                        left=Name(id='data_array', ctx=Load()),
                        ops=[
                           NotEq()],
                        comparators=[
                           Attribute(
                              value=Name(id='EB', ctx=Load()),
                              attr='TRUE',
                              ctx=Load())])),
                  Assign(
                     targets=[
                        Subscript(
                           value=Attribute(
                              value=Name(id='data_array', ctx=Load()),
                              attr='values',
                              ctx=Load()),
                           slice=Name(id='mask', ctx=Load()),
                           ctx=Store())],
                     value=Attribute(
                        value=Name(id='EB', ctx=Load()),
                        attr='FALSE',
                        ctx=Load())),
                  Assign(
                     targets=[
                        Name(id='index_tuples', ctx=Store())],
                     value=Call(
                        func=Attribute(
                           value=Name(id='np', ctx=Load()),
                           attr='argwhere',
                           ctx=Load()),
                        args=[
                           Attribute(
                              value=Name(id='mask', ctx=Load()),
                              attr='values',
                              ctx=Load())],
                        keywords=[])),
                  Assign(
                     targets=[
                        Name(id='false_indices', ctx=Store())],
                     value=ListComp(
                        elt=Call(
                           func=Name(id='tuple', ctx=Load()),
                           args=[
                              GeneratorExp(
                                 elt=Subscript(
                                    value=Attribute(
                                       value=Subscript(
                                          value=Name(id='data_array', ctx=Load()),
                                          slice=Name(id='d', ctx=Load()),
                                          ctx=Load()),
                                       attr='values',
                                       ctx=Load()),
                                    slice=Name(id='i', ctx=Load()),
                                    ctx=Load()),
                                 generators=[
                                    comprehension(
                                       target=Tuple(
                                          elts=[
                                             Name(id='d', ctx=Store()),
                                             Name(id='i', ctx=Store())],
                                          ctx=Store()),
                                       iter=Call(
                                          func=Name(id='zip', ctx=Load()),
                                          args=[
                                             Attribute(
                                                value=Name(id='data_array', ctx=Load()),
                                                attr='dims',
                                                ctx=Load()),
                                             Name(id='idx', ctx=Load())],
                                          keywords=[]),
                                       ifs=[],
                                       is_async=0)])],
                           keywords=[]),
                        generators=[
                           comprehension(
                              target=Name(id='idx', ctx=Store()),
                              iter=Name(id='index_tuples', ctx=Load()),
                              ifs=[],
                              is_async=0)])),
                  Expr(
                     value=Call(
                        func=Name(id='append_changes', ctx=Load()),
                        args=[
                           Name(id='changes', ctx=Load()),
                           Dict(
                              keys=[
                                 Name(id='pred', ctx=Load())],
                              values=[
                                 Call(
                                    func=Name(id='Change', ctx=Load()),
                                    args=[
                                       Name(id='pred', ctx=Load()),
                                       List(elts=[], ctx=Load()),
                                       Name(id='false_indices', ctx=Load())],
                                    keywords=[])])],
                        keywords=[]))],
               orelse=[]),
            Return(
               value=Name(id='changes', ctx=Load()))],
         decorator_list=[])],
   type_ignores=[])

# AST of an auxiliary function
def generate_get_changes_for_comparison_operators():
    return Module(
   body=[
      FunctionDef(
         name='get_changes_for_comparison_operators',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='operator_list'),
               arg(arg='domain')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='changes', ctx=Store())],
               value=Dict(keys=[], values=[])),
            If(
               test=BoolOp(
                  op=Or(),
                  values=[
                     Compare(
                        left=Constant(value=';EQ'),
                        ops=[
                           In()],
                        comparators=[
                           Name(id='operator_list', ctx=Load())]),
                     Compare(
                        left=Constant(value='_NEQ'),
                        ops=[
                           In()],
                        comparators=[
                           Name(id='operator_list', ctx=Load())])]),
               body=[
                  Assign(
                     targets=[
                        Name(id='equal_pairs', ctx=Store())],
                     value=ListComp(
                        elt=Tuple(
                           elts=[
                              Name(id='elem', ctx=Load()),
                              Name(id='elem', ctx=Load())],
                           ctx=Load()),
                        generators=[
                           comprehension(
                              target=Name(id='elem', ctx=Store()),
                              iter=Name(id='domain', ctx=Load()),
                              ifs=[],
                              is_async=0)])),
                  Assign(
                     targets=[
                        Name(id='unequal_pairs', ctx=Store())],
                     value=ListComp(
                        elt=Tuple(
                           elts=[
                              Name(id='elem1', ctx=Load()),
                              Name(id='elem2', ctx=Load())],
                           ctx=Load()),
                        generators=[
                           comprehension(
                              target=Name(id='elem1', ctx=Store()),
                              iter=Name(id='domain', ctx=Load()),
                              ifs=[],
                              is_async=0),
                           comprehension(
                              target=Name(id='elem2', ctx=Store()),
                              iter=Name(id='domain', ctx=Load()),
                              ifs=[
                                 Compare(
                                    left=Name(id='elem1', ctx=Load()),
                                    ops=[
                                       NotEq()],
                                    comparators=[
                                       Name(id='elem2', ctx=Load())])],
                              is_async=0)])),
                  If(
                     test=Compare(
                        left=Constant(value=';EQ'),
                        ops=[
                           In()],
                        comparators=[
                           Name(id='operator_list', ctx=Load())]),
                     body=[
                        Expr(
                           value=Call(
                              func=Name(id='append_changes', ctx=Load()),
                              args=[
                                 Name(id='changes', ctx=Load()),
                                 Dict(
                                    keys=[
                                       Constant(value=';EQ')],
                                    values=[
                                       Call(
                                          func=Name(id='Change', ctx=Load()),
                                          args=[
                                             Constant(value=';EQ'),
                                             Name(id='equal_pairs', ctx=Load()),
                                             Name(id='unequal_pairs', ctx=Load())],
                                          keywords=[])])],
                              keywords=[]))],
                     orelse=[]),
                  If(
                     test=Compare(
                        left=Constant(value='_NEQ'),
                        ops=[
                           In()],
                        comparators=[
                           Name(id='operator_list', ctx=Load())]),
                     body=[
                        Expr(
                           value=Call(
                              func=Name(id='append_changes', ctx=Load()),
                              args=[
                                 Name(id='changes', ctx=Load()),
                                 Dict(
                                    keys=[
                                       Constant(value='_NEQ')],
                                    values=[
                                       Call(
                                          func=Name(id='Change', ctx=Load()),
                                          args=[
                                             Constant(value='_NEQ'),
                                             Name(id='unequal_pairs', ctx=Load()),
                                             Name(id='equal_pairs', ctx=Load())],
                                          keywords=[])])],
                              keywords=[]))],
                     orelse=[])],
               orelse=[]),
            If(
               test=BoolOp(
                  op=Or(),
                  values=[
                     Compare(
                        left=Constant(value='_LEQ'),
                        ops=[
                           In()],
                        comparators=[
                           Name(id='operator_list', ctx=Load())]),
                     Compare(
                        left=Constant(value='_LE'),
                        ops=[
                           In()],
                        comparators=[
                           Name(id='operator_list', ctx=Load())]),
                     Compare(
                        left=Constant(value='_GEQ'),
                        ops=[
                           In()],
                        comparators=[
                           Name(id='operator_list', ctx=Load())]),
                     Compare(
                        left=Constant(value='_GE'),
                        ops=[
                           In()],
                        comparators=[
                           Name(id='operator_list', ctx=Load())])]),
               body=[
                  Assign(
                     targets=[
                        Name(id='integer_domain', ctx=Store())],
                     value=SetComp(
                        elt=Name(id='elem', ctx=Load()),
                        generators=[
                           comprehension(
                              target=Name(id='elem', ctx=Store()),
                              iter=Name(id='domain', ctx=Load()),
                              ifs=[
                                 Compare(
                                    left=Call(
                                       func=Name(id='type', ctx=Load()),
                                       args=[
                                          Name(id='elem', ctx=Load())],
                                       keywords=[]),
                                    ops=[
                                       Eq()],
                                    comparators=[
                                       Name(id='int', ctx=Load())])],
                              is_async=0)])),
                  Assign(
                     targets=[
                        Name(id='integer_pairs', ctx=Store())],
                     value=ListComp(
                        elt=Tuple(
                           elts=[
                              Name(id='elem1', ctx=Load()),
                              Name(id='elem2', ctx=Load())],
                           ctx=Load()),
                        generators=[
                           comprehension(
                              target=Name(id='elem1', ctx=Store()),
                              iter=Name(id='integer_domain', ctx=Load()),
                              ifs=[],
                              is_async=0),
                           comprehension(
                              target=Name(id='elem2', ctx=Store()),
                              iter=Name(id='integer_domain', ctx=Load()),
                              ifs=[],
                              is_async=0)])),
                  Assign(
                     targets=[
                        Name(id='integer_equal_pairs', ctx=Store())],
                     value=ListComp(
                        elt=Tuple(
                           elts=[
                              Name(id='elem', ctx=Load()),
                              Name(id='elem', ctx=Load())],
                           ctx=Load()),
                        generators=[
                           comprehension(
                              target=Name(id='elem', ctx=Store()),
                              iter=Name(id='integer_domain', ctx=Load()),
                              ifs=[],
                              is_async=0)])),
                  Assign(
                     targets=[
                        Name(id='integer_gt_pairs', ctx=Store())],
                     value=ListComp(
                        elt=Tuple(
                           elts=[
                              Name(id='elem1', ctx=Load()),
                              Name(id='elem2', ctx=Load())],
                           ctx=Load()),
                        generators=[
                           comprehension(
                              target=Name(id='elem1', ctx=Store()),
                              iter=Name(id='integer_domain', ctx=Load()),
                              ifs=[],
                              is_async=0),
                           comprehension(
                              target=Name(id='elem2', ctx=Store()),
                              iter=Name(id='integer_domain', ctx=Load()),
                              ifs=[
                                 Compare(
                                    left=Name(id='elem1', ctx=Load()),
                                    ops=[
                                       Gt()],
                                    comparators=[
                                       Name(id='elem2', ctx=Load())])],
                              is_async=0)])),
                  If(
                     test=Compare(
                        left=Constant(value='_LEQ'),
                        ops=[
                           In()],
                        comparators=[
                           Name(id='operator_list', ctx=Load())]),
                     body=[
                        Expr(
                           value=Call(
                              func=Name(id='append_changes', ctx=Load()),
                              args=[
                                 Name(id='changes', ctx=Load()),
                                 Dict(
                                    keys=[
                                       Constant(value='_LEQ')],
                                    values=[
                                       Call(
                                          func=Name(id='Change', ctx=Load()),
                                          args=[
                                             Constant(value='_LEQ'),
                                             ListComp(
                                                elt=Name(id='pair', ctx=Load()),
                                                generators=[
                                                   comprehension(
                                                      target=Name(id='pair', ctx=Store()),
                                                      iter=Name(id='integer_pairs', ctx=Load()),
                                                      ifs=[
                                                         Compare(
                                                            left=Name(id='pair', ctx=Load()),
                                                            ops=[
                                                               NotIn()],
                                                            comparators=[
                                                               Name(id='integer_gt_pairs', ctx=Load())])],
                                                      is_async=0)]),
                                             Name(id='integer_gt_pairs', ctx=Load())],
                                          keywords=[])])],
                              keywords=[]))],
                     orelse=[]),
                  If(
                     test=Compare(
                        left=Constant(value='_LE'),
                        ops=[
                           In()],
                        comparators=[
                           Name(id='operator_list', ctx=Load())]),
                     body=[
                        Expr(
                           value=Call(
                              func=Name(id='append_changes', ctx=Load()),
                              args=[
                                 Name(id='changes', ctx=Load()),
                                 Dict(
                                    keys=[
                                       Constant(value='_LE')],
                                    values=[
                                       Call(
                                          func=Name(id='Change', ctx=Load()),
                                          args=[
                                             Constant(value='_LE'),
                                             ListComp(
                                                elt=Name(id='pair', ctx=Load()),
                                                generators=[
                                                   comprehension(
                                                      target=Name(id='pair', ctx=Store()),
                                                      iter=Name(id='integer_pairs', ctx=Load()),
                                                      ifs=[
                                                         BoolOp(
                                                            op=And(),
                                                            values=[
                                                               Compare(
                                                                  left=Name(id='pair', ctx=Load()),
                                                                  ops=[
                                                                     NotIn()],
                                                                  comparators=[
                                                                     Name(id='integer_gt_pairs', ctx=Load())]),
                                                               Compare(
                                                                  left=Name(id='pair', ctx=Load()),
                                                                  ops=[
                                                                     NotIn()],
                                                                  comparators=[
                                                                     Name(id='integer_equal_pairs', ctx=Load())])])],
                                                      is_async=0)]),
                                             BinOp(
                                                left=Name(id='integer_gt_pairs', ctx=Load()),
                                                op=Add(),
                                                right=Name(id='integer_equal_pairs', ctx=Load()))],
                                          keywords=[])])],
                              keywords=[]))],
                     orelse=[]),
                  If(
                     test=Compare(
                        left=Constant(value='_GE'),
                        ops=[
                           In()],
                        comparators=[
                           Name(id='operator_list', ctx=Load())]),
                     body=[
                        Expr(
                           value=Call(
                              func=Name(id='append_changes', ctx=Load()),
                              args=[
                                 Name(id='changes', ctx=Load()),
                                 Dict(
                                    keys=[
                                       Constant(value='_GE')],
                                    values=[
                                       Call(
                                          func=Name(id='Change', ctx=Load()),
                                          args=[
                                             Constant(value='_GE'),
                                             Name(id='integer_gt_pairs', ctx=Load()),
                                             ListComp(
                                                elt=Name(id='pair', ctx=Load()),
                                                generators=[
                                                   comprehension(
                                                      target=Name(id='pair', ctx=Store()),
                                                      iter=Name(id='integer_pairs', ctx=Load()),
                                                      ifs=[
                                                         Compare(
                                                            left=Name(id='pair', ctx=Load()),
                                                            ops=[
                                                               NotIn()],
                                                            comparators=[
                                                               Name(id='integer_gt_pairs', ctx=Load())])],
                                                      is_async=0)])],
                                          keywords=[])])],
                              keywords=[]))],
                     orelse=[]),
                  If(
                     test=Compare(
                        left=Constant(value='_GEQ'),
                        ops=[
                           In()],
                        comparators=[
                           Name(id='operator_list', ctx=Load())]),
                     body=[
                        Expr(
                           value=Call(
                              func=Name(id='append_changes', ctx=Load()),
                              args=[
                                 Name(id='changes', ctx=Load()),
                                 Dict(
                                    keys=[
                                       Constant(value='_GEQ')],
                                    values=[
                                       Call(
                                          func=Name(id='Change', ctx=Load()),
                                          args=[
                                             Constant(value='_GEQ'),
                                             BinOp(
                                                left=Name(id='integer_gt_pairs', ctx=Load()),
                                                op=Add(),
                                                right=Name(id='integer_equal_pairs', ctx=Load())),
                                             ListComp(
                                                elt=Name(id='pair', ctx=Load()),
                                                generators=[
                                                   comprehension(
                                                      target=Name(id='pair', ctx=Store()),
                                                      iter=Name(id='integer_pairs', ctx=Load()),
                                                      ifs=[
                                                         BoolOp(
                                                            op=And(),
                                                            values=[
                                                               Compare(
                                                                  left=Name(id='pair', ctx=Load()),
                                                                  ops=[
                                                                     NotIn()],
                                                                  comparators=[
                                                                     Name(id='integer_gt_pairs', ctx=Load())]),
                                                               Compare(
                                                                  left=Name(id='pair', ctx=Load()),
                                                                  ops=[
                                                                     NotIn()],
                                                                  comparators=[
                                                                     Name(id='integer_equal_pairs', ctx=Load())])])],
                                                      is_async=0)])],
                                          keywords=[])])],
                              keywords=[]))],
                     orelse=[])],
               orelse=[]),
            Return(
               value=Name(id='changes', ctx=Load()))],
         decorator_list=[])],
   type_ignores=[])



# This function implements the initial_propagation() function. To do this, it looks at AssertLiteral rules.
# After the ENF algorithm, AssertLiteral rules are rules over a propositional symbol that represent a rule, and as a consequence, the propositional symbol has to evaluate to True.
# This function also contains code to propagate knowledge over mathematical operators.
def generate_initial_propagation(grouped_propagators, equality_domain, interpreted_predicates, operator_set):
    tuple_list = []
    for key, val in grouped_propagators.items():
        for prop in val:
            if type(prop) == AssertLiteral:
                if prop.literal.pos:
                    truth_string = 'TRUE'
                else:
                    truth_string = 'FALSE'

                arg_list = []
                for arg in prop.literal.atom.args:
                    arg_list.append(Constant(value=arg.name))

                tuple_list.append(Tuple(
                                    elts=[
                                        Constant(value=prop.literal.atom.name),
                                        Tuple(elts=arg_list, ctx=Load()),
                                        Attribute(
                                            value=Name(id='EB', ctx=Load()),
                                            attr=truth_string,
                                            ctx=Load())],
                                    ctx=Load()))

    interpreted_predicates_list = []
    for elem in interpreted_predicates:
        interpreted_predicates_list.append(Constant(value=elem))
    equality_domain_list = []

    for elem in equality_domain:
        equality_domain_list.append(Constant(value=elem))

    operator_list = []
    for elem in operator_set:
        operator_list.append(Constant(value=elem))



    return Module(
   body=[
      FunctionDef(
         name='initial_propagation',
         args=arguments(
            posonlyargs=[],
            args=[],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='asserted_literals', ctx=Store())],
               value=List(
                  elts=tuple_list,
                  ctx=Load())),
            Assign(
               targets=[
                  Name(id='changes', ctx=Store())],
               value=Dict(keys=[], values=[])),
            For(
               target=Name(id='asserted_lit', ctx=Store()),
               iter=Name(id='asserted_literals', ctx=Load()),
               body=[
                  Assign(
                     targets=[
                        Subscript(
                           value=Attribute(
                              value=Subscript(
                                 value=Name(id='predicate_dict', ctx=Load()),
                                 slice=Subscript(
                                    value=Name(id='asserted_lit', ctx=Load()),
                                    slice=Constant(value=0),
                                    ctx=Load()),
                                 ctx=Load()),
                              attr='loc',
                              ctx=Load()),
                           slice=Subscript(
                              value=Name(id='asserted_lit', ctx=Load()),
                              slice=Constant(value=1),
                              ctx=Load()),
                           ctx=Store())],
                     value=Subscript(
                        value=Name(id='asserted_lit', ctx=Load()),
                        slice=Constant(value=2),
                        ctx=Load())),
                  If(
                     test=Compare(
                        left=Subscript(
                           value=Name(id='asserted_lit', ctx=Load()),
                           slice=Constant(value=2),
                           ctx=Load()),
                        ops=[
                           Eq()],
                        comparators=[
                           Attribute(
                              value=Name(id='EB', ctx=Load()),
                              attr='TRUE',
                              ctx=Load())]),
                     body=[
                        Expr(
                           value=Call(
                              func=Name(id='append_changes', ctx=Load()),
                              args=[
                                 Name(id='changes', ctx=Load()),
                                 Dict(
                                    keys=[
                                       Subscript(
                                          value=Name(id='asserted_lit', ctx=Load()),
                                          slice=Constant(value=0),
                                          ctx=Load())],
                                    values=[
                                       Call(
                                          func=Name(id='Change', ctx=Load()),
                                          args=[
                                             Subscript(
                                                value=Name(id='asserted_lit', ctx=Load()),
                                                slice=Constant(value=0),
                                                ctx=Load()),
                                             List(
                                                elts=[
                                                   Subscript(
                                                      value=Name(id='asserted_lit', ctx=Load()),
                                                      slice=Constant(value=1),
                                                      ctx=Load())],
                                                ctx=Load()),
                                             List(elts=[], ctx=Load())],
                                          keywords=[])])],
                              keywords=[]))],
                     orelse=[
                        If(
                           test=Compare(
                              left=Subscript(
                                 value=Name(id='asserted_lit', ctx=Load()),
                                 slice=Constant(value=2),
                                 ctx=Load()),
                              ops=[
                                 Eq()],
                              comparators=[
                                 Attribute(
                                    value=Name(id='EB', ctx=Load()),
                                    attr='FALSE',
                                    ctx=Load())]),
                           body=[
                              Expr(
                                 value=Call(
                                    func=Name(id='append_changes', ctx=Load()),
                                    args=[
                                       Name(id='changes', ctx=Load()),
                                       Dict(
                                          keys=[
                                             Subscript(
                                                value=Name(id='asserted_lit', ctx=Load()),
                                                slice=Constant(value=0),
                                                ctx=Load())],
                                          values=[
                                             Call(
                                                func=Name(id='Change', ctx=Load()),
                                                args=[
                                                   Subscript(
                                                      value=Name(id='asserted_lit', ctx=Load()),
                                                      slice=Constant(value=0),
                                                      ctx=Load()),
                                                   List(elts=[], ctx=Load()),
                                                   List(
                                                      elts=[
                                                         Subscript(
                                                            value=Name(id='asserted_lit', ctx=Load()),
                                                            slice=Constant(value=1),
                                                            ctx=Load())],
                                                      ctx=Load())],
                                                keywords=[])])],
                                    keywords=[]))],
                           orelse=[])])],
               orelse=[]),
            Expr(
               value=Call(
                  func=Name(id='append_changes', ctx=Load()),
                  args=[
                     Name(id='changes', ctx=Load()),
                     Call(
                        func=Name(id='fill_in_interpreted_domain', ctx=Load()),
                        args=[
                           List(elts=interpreted_predicates_list, ctx=Load())],
                        keywords=[])],
                  keywords=[])),
            Assign(
               targets=[
                  Name(id='operator_list', ctx=Store())],
               value=List(
                  elts=operator_list,
                  ctx=Load())),
            Assign(
               targets=[
                  Name(id='domain', ctx=Store())],
               value=List(
                  elts=equality_domain_list,
                  ctx=Load())),
            Assign(
               targets=[
                  Name(id='comparison_changes', ctx=Store())],
               value=Call(
                  func=Name(id='get_changes_for_comparison_operators', ctx=Load()),
                  args=[
                     Name(id='operator_list', ctx=Load()),
                     Name(id='domain', ctx=Load())],
                  keywords=[])),
            Expr(
               value=Call(
                  func=Name(id='append_changes', ctx=Load()),
                  args=[
                     Name(id='changes', ctx=Load()),
                     Name(id='comparison_changes', ctx=Load())],
                  keywords=[])),
            Expr(
               value=Call(
                  func=Name(id='propagate_full', ctx=Load()),
                  args=[
                     Name(id='changes', ctx=Load())],
                  keywords=[]))],
         decorator_list=[])],
   type_ignores=[])

# AST of an auxiliary function
def generate_get_grounded_atom_name():
    return Module(
   body=[
      FunctionDef(
         name='get_grounded_atom_name',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='name'),
               arg(arg='comb')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='atom_name', ctx=Store())],
               value=Name(id='name', ctx=Load())),
            For(
               target=Name(id='elem', ctx=Store()),
               iter=Name(id='comb', ctx=Load()),
               body=[
                  AugAssign(
                     target=Name(id='atom_name', ctx=Store()),
                     op=Add(),
                     value=BinOp(
                        left=Constant(value='_'),
                        op=Add(),
                        right=Call(
                           func=Name(id='str', ctx=Load()),
                           args=[
                              Call(
                                 func=Attribute(
                                    value=Name(id='elem', ctx=Load()),
                                    attr='item',
                                    ctx=Load()),
                                 args=[],
                                 keywords=[])],
                           keywords=[])))],
               orelse=[]),
            Return(
               value=Name(id='atom_name', ctx=Load()))],
         decorator_list=[])],
   type_ignores=[])

# AST of an auxiliary function
def generate_get_grounded_atoms_for_display():
    return Module(
   body=[
      FunctionDef(
         name='get_grounded_atoms_for_display',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='atom_name')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='ground_atoms', ctx=Store())],
               value=Dict(keys=[], values=[])),
            Assign(
               targets=[
                  Name(id='data_array', ctx=Store())],
               value=Subscript(
                  value=Name(id='predicate_dict', ctx=Load()),
                  slice=Name(id='atom_name', ctx=Load()),
                  ctx=Load())),
            Assign(
               targets=[
                  Name(id='name', ctx=Store())],
               value=Attribute(
                  value=Name(id='data_array', ctx=Load()),
                  attr='name',
                  ctx=Load())),
            Assign(
               targets=[
                  Name(id='new_domains', ctx=Store())],
               value=ListComp(
                  elt=Attribute(
                     value=Subscript(
                        value=Attribute(
                           value=Name(id='data_array', ctx=Load()),
                           attr='coords',
                           ctx=Load()),
                        slice=Name(id='dim', ctx=Load()),
                        ctx=Load()),
                     attr='values',
                     ctx=Load()),
                  generators=[
                     comprehension(
                        target=Name(id='dim', ctx=Store()),
                        iter=Attribute(
                           value=Name(id='data_array', ctx=Load()),
                           attr='dims',
                           ctx=Load()),
                        ifs=[],
                        is_async=0)])),
            For(
               target=Name(id='comb', ctx=Store()),
               iter=Call(
                  func=Name(id='product', ctx=Load()),
                  args=[
                     Starred(
                        value=Name(id='new_domains', ctx=Load()),
                        ctx=Load())],
                  keywords=[]),
               body=[
                  Assign(
                     targets=[
                        Name(id='ground_atom_name', ctx=Store())],
                     value=Call(
                        func=Name(id='get_grounded_atom_name', ctx=Load()),
                        args=[
                           Name(id='name', ctx=Load()),
                           Name(id='comb', ctx=Load())],
                        keywords=[])),
                  Assign(
                     targets=[
                        Subscript(
                           value=Name(id='ground_atoms', ctx=Load()),
                           slice=Name(id='ground_atom_name', ctx=Load()),
                           ctx=Store())],
                     value=Call(
                        func=Attribute(
                           value=Attribute(
                              value=Subscript(
                                 value=Attribute(
                                    value=Name(id='data_array', ctx=Load()),
                                    attr='loc',
                                    ctx=Load()),
                                 slice=Name(id='comb', ctx=Load()),
                                 ctx=Load()),
                              attr='values',
                              ctx=Load()),
                           attr='item',
                           ctx=Load()),
                        args=[],
                        keywords=[]))],
               orelse=[]),
            Return(
               value=Name(id='ground_atoms', ctx=Load()))],
         decorator_list=[])],
   type_ignores=[])

# AST of an auxiliary function
def generate_terminal_test():
    return Module(
   body=[
      FunctionDef(
         name='test_on_user_input',
         args=arguments(
            posonlyargs=[],
            args=[],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='current_var', ctx=Store())],
               value=Constant(value='')),
            Assign(
               targets=[
                  Name(id='start', ctx=Store())],
               value=Call(
                  func=Attribute(
                     value=Name(id='time', ctx=Load()),
                     attr='time',
                     ctx=Load()),
                  args=[],
                  keywords=[])),
            Expr(
               value=Call(
                  func=Name(id='initial_propagation', ctx=Load()),
                  args=[],
                  keywords=[])),
            Assign(
               targets=[
                  Name(id='end', ctx=Store())],
               value=Call(
                  func=Attribute(
                     value=Name(id='time', ctx=Load()),
                     attr='time',
                     ctx=Load()),
                  args=[],
                  keywords=[])),
            Expr(
               value=Call(
                  func=Name(id='print', ctx=Load()),
                  args=[
                     Constant(value='Initial propagation: '),
                     BinOp(
                        left=Name(id='end', ctx=Load()),
                        op=Sub(),
                        right=Name(id='start', ctx=Load()))],
                  keywords=[])),
            For(
               target=Name(id='var_name', ctx=Store()),
               iter=Call(
                  func=Attribute(
                     value=Name(id='predicate_dict', ctx=Load()),
                     attr='keys',
                     ctx=Load()),
                  args=[],
                  keywords=[]),
               body=[
                  If(
                     test=UnaryOp(
                        op=Not(),
                        operand=Call(
                           func=Attribute(
                              value=Name(id='var_name', ctx=Load()),
                              attr='startswith',
                              ctx=Load()),
                           args=[
                              Constant(value='_')],
                           keywords=[])),
                     body=[
                        Expr(
                           value=Call(
                              func=Name(id='print', ctx=Load()),
                              args=[
                                 Constant(value='__________________________')],
                              keywords=[])),
                        Assign(
                           targets=[
                              Name(id='grounded_var', ctx=Store())],
                           value=Call(
                              func=Name(id='get_grounded_atoms_for_display', ctx=Load()),
                              args=[
                                 Name(id='var_name', ctx=Load())],
                              keywords=[])),
                        For(
                           target=Tuple(
                              elts=[
                                 Name(id='key', ctx=Store()),
                                 Name(id='val', ctx=Store())],
                              ctx=Store()),
                           iter=Call(
                              func=Attribute(
                                 value=Name(id='grounded_var', ctx=Load()),
                                 attr='items',
                                 ctx=Load()),
                              args=[],
                              keywords=[]),
                           body=[
                              Expr(
                                 value=Call(
                                    func=Name(id='print', ctx=Load()),
                                    args=[
                                       BinOp(
                                          left=BinOp(
                                             left=Name(id='key', ctx=Load()),
                                             op=Add(),
                                             right=Constant(value=': ')),
                                          op=Add(),
                                          right=Call(
                                             func=Name(id='str', ctx=Load()),
                                             args=[
                                                Name(id='val', ctx=Load())],
                                             keywords=[]))],
                                    keywords=[]))],
                           orelse=[]),
                        Expr(
                           value=Call(
                              func=Name(id='print', ctx=Load()),
                              args=[
                                 Constant(value='__________________________')],
                              keywords=[]))],
                     orelse=[])],
               orelse=[]),
            While(
               test=Compare(
                  left=Call(
                     func=Attribute(
                        value=Name(id='current_var', ctx=Load()),
                        attr='lower',
                        ctx=Load()),
                     args=[],
                     keywords=[]),
                  ops=[
                     NotEq()],
                  comparators=[
                     Constant(value='stop')]),
               body=[
                  Assign(
                     targets=[
                        Name(id='current_var', ctx=Store())],
                     value=Call(
                        func=Name(id='input', ctx=Load()),
                        args=[
                           Constant(value='Give the name of the variable\n')],
                        keywords=[])),
                  If(
                     test=Compare(
                        left=Name(id='current_var', ctx=Load()),
                        ops=[
                           NotIn()],
                        comparators=[
                           Call(
                              func=Attribute(
                                 value=Name(id='predicate_dict', ctx=Load()),
                                 attr='keys',
                                 ctx=Load()),
                              args=[],
                              keywords=[])]),
                     body=[
                        Expr(
                           value=Call(
                              func=Name(id='print', ctx=Load()),
                              args=[
                                 Constant(value="Try again, this variable doesn't exist")],
                              keywords=[])),
                        Continue()],
                     orelse=[]),
                  Assign(
                     targets=[
                        Name(id='args', ctx=Store())],
                     value=List(elts=[], ctx=Load())),
                  For(
                     target=Name(id='i', ctx=Store()),
                     iter=Call(
                        func=Name(id='range', ctx=Load()),
                        args=[
                           Call(
                              func=Name(id='len', ctx=Load()),
                              args=[
                                 Attribute(
                                    value=Subscript(
                                       value=Name(id='predicate_dict', ctx=Load()),
                                       slice=Name(id='current_var', ctx=Load()),
                                       ctx=Load()),
                                    attr='dims',
                                    ctx=Load())],
                              keywords=[])],
                        keywords=[]),
                     body=[
                        Assign(
                           targets=[
                              Name(id='new_arg', ctx=Store())],
                           value=Call(
                              func=Name(id='input', ctx=Load()),
                              args=[
                                 JoinedStr(
                                    values=[
                                       Constant(value='Give argument number '),
                                       FormattedValue(
                                          value=BinOp(
                                             left=Name(id='i', ctx=Load()),
                                             op=Add(),
                                             right=Constant(value=1)),
                                          conversion=-1),
                                       Constant(value=':\n')])],
                              keywords=[])),
                        If(
                           test=Call(
                              func=Attribute(
                                 value=Name(id='new_arg', ctx=Load()),
                                 attr='isdigit',
                                 ctx=Load()),
                              args=[],
                              keywords=[]),
                           body=[
                              Expr(
                                 value=Call(
                                    func=Attribute(
                                       value=Name(id='args', ctx=Load()),
                                       attr='append',
                                       ctx=Load()),
                                    args=[
                                       Call(
                                          func=Name(id='int', ctx=Load()),
                                          args=[
                                             Name(id='new_arg', ctx=Load())],
                                          keywords=[])],
                                    keywords=[]))],
                           orelse=[
                              Expr(
                                 value=Call(
                                    func=Attribute(
                                       value=Name(id='args', ctx=Load()),
                                       attr='append',
                                       ctx=Load()),
                                    args=[
                                       Name(id='new_arg', ctx=Load())],
                                    keywords=[]))])],
                     orelse=[]),
                  Assign(
                     targets=[
                        Name(id='b', ctx=Store())],
                     value=Call(
                        func=Name(id='input', ctx=Load()),
                        args=[
                           Constant(value='True (1) or false (0)?\n')],
                        keywords=[])),
                  If(
                     test=Compare(
                        left=Name(id='b', ctx=Load()),
                        ops=[
                           NotEq()],
                        comparators=[
                           Constant(value='0')]),
                     body=[
                        Assign(
                           targets=[
                              Name(id='b_val', ctx=Store())],
                           value=Attribute(
                              value=Name(id='EB', ctx=Load()),
                              attr='TRUE',
                              ctx=Load()))],
                     orelse=[
                        Assign(
                           targets=[
                              Name(id='b_val', ctx=Store())],
                           value=Attribute(
                              value=Name(id='EB', ctx=Load()),
                              attr='FALSE',
                              ctx=Load()))]),
                  Assign(
                     targets=[
                        Name(id='current_array', ctx=Store())],
                     value=Subscript(
                        value=Name(id='predicate_dict', ctx=Load()),
                        slice=Name(id='current_var', ctx=Load()),
                        ctx=Load())),
                  If(
                     test=Compare(
                        left=Subscript(
                           value=Attribute(
                              value=Name(id='current_array', ctx=Load()),
                              attr='loc',
                              ctx=Load()),
                           slice=Tuple(
                              elts=[
                                 Starred(
                                    value=Name(id='args', ctx=Load()),
                                    ctx=Load())],
                              ctx=Load()),
                           ctx=Load()),
                        ops=[
                           Eq()],
                        comparators=[
                           Attribute(
                              value=Name(id='EB', ctx=Load()),
                              attr='UNKNOWN',
                              ctx=Load())]),
                     body=[
                        Assign(
                           targets=[
                              Subscript(
                                 value=Attribute(
                                    value=Name(id='current_array', ctx=Load()),
                                    attr='loc',
                                    ctx=Load()),
                                 slice=Tuple(
                                    elts=[
                                       Starred(
                                          value=Name(id='args', ctx=Load()),
                                          ctx=Load())],
                                    ctx=Load()),
                                 ctx=Store())],
                           value=Name(id='b_val', ctx=Load()))],
                     orelse=[
                        Expr(
                           value=Call(
                              func=Name(id='print', ctx=Load()),
                              args=[
                                 Constant(value='Sorry, this variable is already assigned a value')],
                              keywords=[])),
                        Continue()]),
                  Assign(
                     targets=[
                        Name(id='change', ctx=Store())],
                     value=Dict(keys=[], values=[])),
                  If(
                     test=Compare(
                        left=Name(id='b_val', ctx=Load()),
                        ops=[
                           Eq()],
                        comparators=[
                           Attribute(
                              value=Name(id='EB', ctx=Load()),
                              attr='TRUE',
                              ctx=Load())]),
                     body=[
                        Expr(
                           value=Call(
                              func=Name(id='append_changes', ctx=Load()),
                              args=[
                                 Name(id='change', ctx=Load()),
                                 Dict(
                                    keys=[
                                       Name(id='current_var', ctx=Load())],
                                    values=[
                                       Call(
                                          func=Name(id='Change', ctx=Load()),
                                          args=[
                                             Name(id='current_var', ctx=Load()),
                                             List(
                                                elts=[
                                                   Call(
                                                      func=Name(id='tuple', ctx=Load()),
                                                      args=[
                                                         Name(id='args', ctx=Load())],
                                                      keywords=[])],
                                                ctx=Load()),
                                             List(elts=[], ctx=Load())],
                                          keywords=[])])],
                              keywords=[]))],
                     orelse=[
                        Expr(
                           value=Call(
                              func=Name(id='append_changes', ctx=Load()),
                              args=[
                                 Name(id='change', ctx=Load()),
                                 Dict(
                                    keys=[
                                       Name(id='current_var', ctx=Load())],
                                    values=[
                                       Call(
                                          func=Name(id='Change', ctx=Load()),
                                          args=[
                                             Name(id='current_var', ctx=Load()),
                                             List(elts=[], ctx=Load()),
                                             List(
                                                elts=[
                                                   Call(
                                                      func=Name(id='tuple', ctx=Load()),
                                                      args=[
                                                         Name(id='args', ctx=Load())],
                                                      keywords=[])],
                                                ctx=Load())],
                                          keywords=[])])],
                              keywords=[]))]),
                  Assign(
                     targets=[
                        Name(id='start', ctx=Store())],
                     value=Call(
                        func=Attribute(
                           value=Name(id='time', ctx=Load()),
                           attr='time',
                           ctx=Load()),
                        args=[],
                        keywords=[])),
                  Expr(
                     value=Call(
                        func=Name(id='propagate_full', ctx=Load()),
                        args=[
                           Name(id='change', ctx=Load())],
                        keywords=[])),
                  Assign(
                     targets=[
                        Name(id='end', ctx=Store())],
                     value=Call(
                        func=Attribute(
                           value=Name(id='time', ctx=Load()),
                           attr='time',
                           ctx=Load()),
                        args=[],
                        keywords=[])),
                  For(
                     target=Name(id='var_name', ctx=Store()),
                     iter=Call(
                        func=Attribute(
                           value=Name(id='predicate_dict', ctx=Load()),
                           attr='keys',
                           ctx=Load()),
                        args=[],
                        keywords=[]),
                     body=[
                        If(
                           test=UnaryOp(
                              op=Not(),
                              operand=Call(
                                 func=Attribute(
                                    value=Name(id='var_name', ctx=Load()),
                                    attr='startswith',
                                    ctx=Load()),
                                 args=[
                                    Constant(value='_')],
                                 keywords=[])),
                           body=[
                              Expr(
                                 value=Call(
                                    func=Name(id='print', ctx=Load()),
                                    args=[
                                       Constant(value='__________________________')],
                                    keywords=[])),
                              Assign(
                                 targets=[
                                    Name(id='grounded_var', ctx=Store())],
                                 value=Call(
                                    func=Name(id='get_grounded_atoms_for_display', ctx=Load()),
                                    args=[
                                       Name(id='var_name', ctx=Load())],
                                    keywords=[])),
                              For(
                                 target=Tuple(
                                    elts=[
                                       Name(id='key', ctx=Store()),
                                       Name(id='val', ctx=Store())],
                                    ctx=Store()),
                                 iter=Call(
                                    func=Attribute(
                                       value=Name(id='grounded_var', ctx=Load()),
                                       attr='items',
                                       ctx=Load()),
                                    args=[],
                                    keywords=[]),
                                 body=[
                                    Expr(
                                       value=Call(
                                          func=Name(id='print', ctx=Load()),
                                          args=[
                                             BinOp(
                                                left=BinOp(
                                                   left=Name(id='key', ctx=Load()),
                                                   op=Add(),
                                                   right=Constant(value=': ')),
                                                op=Add(),
                                                right=Call(
                                                   func=Name(id='str', ctx=Load()),
                                                   args=[
                                                      Name(id='val', ctx=Load())],
                                                   keywords=[]))],
                                          keywords=[]))],
                                 orelse=[]),
                              Expr(
                                 value=Call(
                                    func=Name(id='print', ctx=Load()),
                                    args=[
                                       Constant(value='__________________________')],
                                    keywords=[]))],
                           orelse=[])],
                     orelse=[]),
                  Expr(
                     value=Call(
                        func=Name(id='print', ctx=Load()),
                        args=[
                           Constant(value='Time to propagate: '),
                           BinOp(
                              left=Name(id='end', ctx=Load()),
                              op=Sub(),
                              right=Name(id='start', ctx=Load()))],
                        keywords=[]))],
               orelse=[])],
         decorator_list=[]),
      Expr(
         value=Call(
            func=Name(id='test_on_user_input', ctx=Load()),
            args=[],
            keywords=[]))],
   type_ignores=[])


# AST of an auxiliary function
def generate_dash_functionality():
    return Module(
   body=[
      FunctionDef(
         name='unground',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='ground_name')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='parts', ctx=Store())],
               value=Call(
                  func=Attribute(
                     value=Name(id='ground_name', ctx=Load()),
                     attr='split',
                     ctx=Load()),
                  args=[
                     Constant(value='_')],
                  keywords=[])),
            Assign(
               targets=[
                  Name(id='name', ctx=Store())],
               value=Subscript(
                  value=Name(id='parts', ctx=Load()),
                  slice=Constant(value=0),
                  ctx=Load())),
            Assign(
               targets=[
                  Name(id='args', ctx=Store())],
               value=Call(
                  func=Name(id='tuple', ctx=Load()),
                  args=[
                     GeneratorExp(
                        elt=IfExp(
                           test=Call(
                              func=Attribute(
                                 value=Name(id='x', ctx=Load()),
                                 attr='isdigit',
                                 ctx=Load()),
                              args=[],
                              keywords=[]),
                           body=Call(
                              func=Name(id='int', ctx=Load()),
                              args=[
                                 Name(id='x', ctx=Load())],
                              keywords=[]),
                           orelse=Name(id='x', ctx=Load())),
                        generators=[
                           comprehension(
                              target=Name(id='x', ctx=Store()),
                              iter=Subscript(
                                 value=Name(id='parts', ctx=Load()),
                                 slice=Slice(
                                    lower=Constant(value=1)),
                                 ctx=Load()),
                              ifs=[],
                              is_async=0)])],
                  keywords=[])),
            Return(
               value=Tuple(
                  elts=[
                     Name(id='name', ctx=Load()),
                     Name(id='args', ctx=Load())],
                  ctx=Load()))],
         decorator_list=[]),
      FunctionDef(
         name='get_dropdown_options',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='integer_list')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='options_list', ctx=Store())],
               value=List(elts=[], ctx=Load())),
            For(
               target=Name(id='i', ctx=Store()),
               iter=Name(id='integer_list', ctx=Load()),
               body=[
                  Expr(
                     value=Call(
                        func=Attribute(
                           value=Name(id='options_list', ctx=Load()),
                           attr='append',
                           ctx=Load()),
                        args=[
                           Dict(
                              keys=[
                                 Constant(value='label'),
                                 Constant(value='value')],
                              values=[
                                 Call(
                                    func=Name(id='str', ctx=Load()),
                                    args=[
                                       Name(id='i', ctx=Load())],
                                    keywords=[]),
                                 Name(id='i', ctx=Load())])],
                        keywords=[]))],
               orelse=[]),
            Return(
               value=Name(id='options_list', ctx=Load()))],
         decorator_list=[]),
      FunctionDef(
         name='convert_to_ui',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='values')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            If(
               test=Compare(
                  left=Name(id='values', ctx=Load()),
                  ops=[
                     Eq()],
                  comparators=[
                     Attribute(
                        value=Name(id='EB', ctx=Load()),
                        attr='UNKNOWN',
                        ctx=Load())]),
               body=[
                  Return(
                     value=List(elts=[], ctx=Load()))],
               orelse=[]),
            If(
               test=Compare(
                  left=Name(id='values', ctx=Load()),
                  ops=[
                     Eq()],
                  comparators=[
                     Attribute(
                        value=Name(id='EB', ctx=Load()),
                        attr='TRUE',
                        ctx=Load())]),
               body=[
                  Return(
                     value=List(
                        elts=[
                           Constant(value=True)],
                        ctx=Load()))],
               orelse=[]),
            If(
               test=Compare(
                  left=Name(id='values', ctx=Load()),
                  ops=[
                     Eq()],
                  comparators=[
                     Attribute(
                        value=Name(id='EB', ctx=Load()),
                        attr='FALSE',
                        ctx=Load())]),
               body=[
                  Return(
                     value=List(
                        elts=[
                           Constant(value=False)],
                        ctx=Load()))],
               orelse=[]),
            If(
               test=Compare(
                  left=Name(id='values', ctx=Load()),
                  ops=[
                     Eq()],
                  comparators=[
                     Attribute(
                        value=Name(id='EB', ctx=Load()),
                        attr='INCONSISTENT',
                        ctx=Load())]),
               body=[
                  Return(
                     value=List(elts=[], ctx=Load()))],
               orelse=[
                  Return(
                     value=Call(
                        func=Name(id='get_dropdown_options', ctx=Load()),
                        args=[
                           Name(id='values', ctx=Load())],
                        keywords=[]))])],
         decorator_list=[]),
      FunctionDef(
         name='convert_from_ui',
         args=arguments(
            posonlyargs=[],
            args=[
               arg(arg='values')],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            If(
               test=BoolOp(
                  op=Or(),
                  values=[
                     Compare(
                        left=Name(id='values', ctx=Load()),
                        ops=[
                           Eq()],
                        comparators=[
                           List(
                              elts=[
                                 Constant(value=True),
                                 Constant(value=False)],
                              ctx=Load())]),
                     Compare(
                        left=Name(id='values', ctx=Load()),
                        ops=[
                           Eq()],
                        comparators=[
                           List(
                              elts=[
                                 Constant(value=False),
                                 Constant(value=True)],
                              ctx=Load())])]),
               body=[
                  Return(
                     value=Attribute(
                        value=Name(id='EB', ctx=Load()),
                        attr='INCONSISTENT',
                        ctx=Load()))],
               orelse=[]),
            If(
               test=Compare(
                  left=Name(id='values', ctx=Load()),
                  ops=[
                     Eq()],
                  comparators=[
                     List(
                        elts=[
                           Constant(value=True)],
                        ctx=Load())]),
               body=[
                  Return(
                     value=Attribute(
                        value=Name(id='EB', ctx=Load()),
                        attr='TRUE',
                        ctx=Load()))],
               orelse=[]),
            If(
               test=Compare(
                  left=Name(id='values', ctx=Load()),
                  ops=[
                     Eq()],
                  comparators=[
                     List(
                        elts=[
                           Constant(value=False)],
                        ctx=Load())]),
               body=[
                  Return(
                     value=Attribute(
                        value=Name(id='EB', ctx=Load()),
                        attr='FALSE',
                        ctx=Load()))],
               orelse=[
                  Return(
                     value=Attribute(
                        value=Name(id='EB', ctx=Load()),
                        attr='UNKNOWN',
                        ctx=Load()))])],
         decorator_list=[]),
      FunctionDef(
         name='launch_dash_app',
         args=arguments(
            posonlyargs=[],
            args=[],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='app', ctx=Store())],
               value=Call(
                  func=Name(id='Dash', ctx=Load()),
                  args=[
                     Name(id='__name__', ctx=Load())],
                  keywords=[])),
            Expr(
               value=Call(
                  func=Name(id='initial_propagation', ctx=Load()),
                  args=[],
                  keywords=[])),
            Assign(
               targets=[
                  Name(id='structure', ctx=Store())],
               value=Dict(keys=[], values=[])),
            For(
               target=Name(id='var_name', ctx=Store()),
               iter=Call(
                  func=Attribute(
                     value=Name(id='predicate_dict', ctx=Load()),
                     attr='keys',
                     ctx=Load()),
                  args=[],
                  keywords=[]),
               body=[
                  Expr(
                     value=Call(
                        func=Attribute(
                           value=Name(id='structure', ctx=Load()),
                           attr='update',
                           ctx=Load()),
                        args=[
                           Call(
                              func=Name(id='get_grounded_atoms_for_display', ctx=Load()),
                              args=[
                                 Name(id='var_name', ctx=Load())],
                              keywords=[])],
                        keywords=[]))],
               orelse=[]),
            Assign(
               targets=[
                  Name(id='boolean_variables', ctx=Store())],
               value=ListComp(
                  elt=Name(id='v', ctx=Load()),
                  generators=[
                     comprehension(
                        target=Name(id='v', ctx=Store()),
                        iter=Call(
                           func=Attribute(
                              value=Name(id='structure', ctx=Load()),
                              attr='keys',
                              ctx=Load()),
                           args=[],
                           keywords=[]),
                        ifs=[
                           UnaryOp(
                              op=Not(),
                              operand=Call(
                                 func=Attribute(
                                    value=Name(id='v', ctx=Load()),
                                    attr='startswith',
                                    ctx=Load()),
                                 args=[
                                    Constant(value='_')],
                                 keywords=[]))],
                        is_async=0)])),
            Expr(
               value=Call(
                  func=Attribute(
                     value=Name(id='boolean_variables', ctx=Load()),
                     attr='sort',
                     ctx=Load()),
                  args=[],
                  keywords=[])),
            Assign(
               targets=[
                  Name(id='integer_variables', ctx=Store())],
               value=List(elts=[], ctx=Load())),
            Assign(
               targets=[
                  Attribute(
                     value=Name(id='app', ctx=Load()),
                     attr='layout',
                     ctx=Store())],
               value=Call(
                  func=Attribute(
                     value=Name(id='html', ctx=Load()),
                     attr='Div',
                     ctx=Load()),
                  args=[
                     List(
                        elts=[
                           Call(
                              func=Attribute(
                                 value=Name(id='html', ctx=Load()),
                                 attr='H1',
                                 ctx=Load()),
                              args=[
                                 Constant(value='Interactive configuration')],
                              keywords=[]),
                           Call(
                              func=Attribute(
                                 value=Name(id='html', ctx=Load()),
                                 attr='Button',
                                 ctx=Load()),
                              args=[
                                 Constant(value='Reset')],
                              keywords=[
                                 keyword(
                                    arg='id',
                                    value=Constant(value='reset-button')),
                                 keyword(
                                    arg='n_clicks',
                                    value=Constant(value=0))]),
                           Call(
                              func=Attribute(
                                 value=Name(id='html', ctx=Load()),
                                 attr='Div',
                                 ctx=Load()),
                              args=[
                                 ListComp(
                                    elt=Call(
                                       func=Attribute(
                                          value=Name(id='html', ctx=Load()),
                                          attr='Div',
                                          ctx=Load()),
                                       args=[
                                          List(
                                             elts=[
                                                Call(
                                                   func=Attribute(
                                                      value=Name(id='html', ctx=Load()),
                                                      attr='Label',
                                                      ctx=Load()),
                                                   args=[
                                                      JoinedStr(
                                                         values=[
                                                            FormattedValue(
                                                               value=Name(id='var', ctx=Load()),
                                                               conversion=-1),
                                                            Constant(value=':')])],
                                                   keywords=[]),
                                                Call(
                                                   func=Attribute(
                                                      value=Name(id='dcc', ctx=Load()),
                                                      attr='Checklist',
                                                      ctx=Load()),
                                                   args=[],
                                                   keywords=[
                                                      keyword(
                                                         arg='id',
                                                         value=Dict(
                                                            keys=[
                                                               Constant(value='type'),
                                                               Constant(value='index')],
                                                            values=[
                                                               Constant(value='checkboxes'),
                                                               Name(id='var', ctx=Load())])),
                                                      keyword(
                                                         arg='options',
                                                         value=List(
                                                            elts=[
                                                               Dict(
                                                                  keys=[
                                                                     Constant(value='label'),
                                                                     Constant(value='value')],
                                                                  values=[
                                                                     Constant(value='True'),
                                                                     Constant(value=True)]),
                                                               Dict(
                                                                  keys=[
                                                                     Constant(value='label'),
                                                                     Constant(value='value')],
                                                                  values=[
                                                                     Constant(value='False'),
                                                                     Constant(value=False)])],
                                                            ctx=Load())),
                                                      keyword(
                                                         arg='value',
                                                         value=Call(
                                                            func=Name(id='convert_to_ui', ctx=Load()),
                                                            args=[
                                                               Subscript(
                                                                  value=Name(id='structure', ctx=Load()),
                                                                  slice=Name(id='var', ctx=Load()),
                                                                  ctx=Load())],
                                                            keywords=[])),
                                                      keyword(
                                                         arg='inline',
                                                         value=Constant(value=True))]),
                                                Call(
                                                   func=Attribute(
                                                      value=Name(id='html', ctx=Load()),
                                                      attr='Div',
                                                      ctx=Load()),
                                                   args=[],
                                                   keywords=[
                                                      keyword(
                                                         arg='id',
                                                         value=Dict(
                                                            keys=[
                                                               Constant(value='type'),
                                                               Constant(value='index')],
                                                            values=[
                                                               Constant(value='output'),
                                                               Name(id='var', ctx=Load())]))])],
                                             ctx=Load())],
                                       keywords=[]),
                                    generators=[
                                       comprehension(
                                          target=Name(id='var', ctx=Store()),
                                          iter=Name(id='boolean_variables', ctx=Load()),
                                          ifs=[],
                                          is_async=0)])],
                              keywords=[]),
                           Call(
                              func=Attribute(
                                 value=Name(id='html', ctx=Load()),
                                 attr='Div',
                                 ctx=Load()),
                              args=[
                                 ListComp(
                                    elt=Call(
                                       func=Attribute(
                                          value=Name(id='html', ctx=Load()),
                                          attr='Div',
                                          ctx=Load()),
                                       args=[
                                          List(
                                             elts=[
                                                Call(
                                                   func=Attribute(
                                                      value=Name(id='html', ctx=Load()),
                                                      attr='Label',
                                                      ctx=Load()),
                                                   args=[
                                                      JoinedStr(
                                                         values=[
                                                            FormattedValue(
                                                               value=Name(id='var', ctx=Load()),
                                                               conversion=-1),
                                                            Constant(value=':')])],
                                                   keywords=[]),
                                                Call(
                                                   func=Attribute(
                                                      value=Name(id='dcc', ctx=Load()),
                                                      attr='Dropdown',
                                                      ctx=Load()),
                                                   args=[],
                                                   keywords=[
                                                      keyword(
                                                         arg='id',
                                                         value=Dict(
                                                            keys=[
                                                               Constant(value='type'),
                                                               Constant(value='index')],
                                                            values=[
                                                               Constant(value='dropdown'),
                                                               Name(id='var', ctx=Load())])),
                                                      keyword(
                                                         arg='options',
                                                         value=Call(
                                                            func=Name(id='get_dropdown_options', ctx=Load()),
                                                            args=[
                                                               Subscript(
                                                                  value=Name(id='structure', ctx=Load()),
                                                                  slice=Name(id='var', ctx=Load()),
                                                                  ctx=Load())],
                                                            keywords=[])),
                                                      keyword(
                                                         arg='placeholder',
                                                         value=Constant(value='Select a number'))]),
                                                Call(
                                                   func=Attribute(
                                                      value=Name(id='html', ctx=Load()),
                                                      attr='Div',
                                                      ctx=Load()),
                                                   args=[],
                                                   keywords=[
                                                      keyword(
                                                         arg='id',
                                                         value=Dict(
                                                            keys=[
                                                               Constant(value='type'),
                                                               Constant(value='index')],
                                                            values=[
                                                               Constant(value='output'),
                                                               Name(id='var', ctx=Load())]))])],
                                             ctx=Load())],
                                       keywords=[]),
                                    generators=[
                                       comprehension(
                                          target=Name(id='var', ctx=Store()),
                                          iter=Name(id='integer_variables', ctx=Load()),
                                          ifs=[],
                                          is_async=0)])],
                              keywords=[]),
                           Call(
                              func=Attribute(
                                 value=Name(id='html', ctx=Load()),
                                 attr='Div',
                                 ctx=Load()),
                              args=[
                                 List(
                                    elts=[
                                       Call(
                                          func=Attribute(
                                             value=Name(id='html', ctx=Load()),
                                             attr='Div',
                                             ctx=Load()),
                                          args=[],
                                          keywords=[
                                             keyword(
                                                arg='id',
                                                value=Dict(
                                                   keys=[
                                                      Constant(value='type')],
                                                   values=[
                                                      Constant(value='text-output')])),
                                             keyword(
                                                arg='children',
                                                value=Constant(value='No inconsistencies detected yet'))])],
                                    ctx=Load())],
                              keywords=[])],
                        ctx=Load())],
                  keywords=[])),
            FunctionDef(
               name='handle_changes',
               args=arguments(
                  posonlyargs=[],
                  args=[
                     arg(arg='checkbox_values'),
                     arg(arg='dropdown_values'),
                     arg(arg='checkbox_ids'),
                     arg(arg='dropdown_ids'),
                     arg(arg='reset')],
                  kwonlyargs=[],
                  kw_defaults=[],
                  defaults=[]),
               body=[
                  Assign(
                     targets=[
                        Name(id='triggered', ctx=Store())],
                     value=Attribute(
                        value=Name(id='callback_context', ctx=Load()),
                        attr='triggered',
                        ctx=Load())),
                  If(
                     test=Name(id='triggered', ctx=Load()),
                     body=[
                        Assign(
                           targets=[
                              Name(id='changed_component', ctx=Store())],
                           value=Subscript(
                              value=Call(
                                 func=Attribute(
                                    value=Subscript(
                                       value=Subscript(
                                          value=Name(id='triggered', ctx=Load()),
                                          slice=Constant(value=0),
                                          ctx=Load()),
                                       slice=Constant(value='prop_id'),
                                       ctx=Load()),
                                    attr='split',
                                    ctx=Load()),
                                 args=[
                                    Constant(value='.')],
                                 keywords=[]),
                              slice=Constant(value=0),
                              ctx=Load())),
                        Assign(
                           targets=[
                              Name(id='changed_value', ctx=Store())],
                           value=Subscript(
                              value=Subscript(
                                 value=Name(id='triggered', ctx=Load()),
                                 slice=Constant(value=0),
                                 ctx=Load()),
                              slice=Constant(value='value'),
                              ctx=Load())),
                        If(
                           test=Compare(
                              left=Name(id='changed_component', ctx=Load()),
                              ops=[
                                 Eq()],
                              comparators=[
                                 Constant(value='reset-button')]),
                           body=[
                              Expr(
                                 value=Call(
                                    func=Name(id='print', ctx=Load()),
                                    args=[
                                       Constant(value='reset is being handled')],
                                    keywords=[])),
                              Expr(
                                 value=Call(
                                    func=Name(id='handle_reset', ctx=Load()),
                                    args=[],
                                    keywords=[])),
                              Expr(
                                 value=Call(
                                    func=Name(id='initial_propagation', ctx=Load()),
                                    args=[],
                                    keywords=[])),
                              For(
                                 target=Name(id='var_name', ctx=Store()),
                                 iter=Call(
                                    func=Attribute(
                                       value=Name(id='predicate_dict', ctx=Load()),
                                       attr='keys',
                                       ctx=Load()),
                                    args=[],
                                    keywords=[]),
                                 body=[
                                    Expr(
                                       value=Call(
                                          func=Attribute(
                                             value=Name(id='structure', ctx=Load()),
                                             attr='update',
                                             ctx=Load()),
                                          args=[
                                             Call(
                                                func=Name(id='get_grounded_atoms_for_display', ctx=Load()),
                                                args=[
                                                   Name(id='var_name', ctx=Load())],
                                                keywords=[])],
                                          keywords=[]))],
                                 orelse=[]),
                              Assign(
                                 targets=[
                                    Name(id='checkbox_values', ctx=Store())],
                                 value=ListComp(
                                    elt=Call(
                                       func=Name(id='convert_to_ui', ctx=Load()),
                                       args=[
                                          Subscript(
                                             value=Name(id='structure', ctx=Load()),
                                             slice=Name(id='val', ctx=Load()),
                                             ctx=Load())],
                                       keywords=[]),
                                    generators=[
                                       comprehension(
                                          target=Name(id='val', ctx=Store()),
                                          iter=Name(id='boolean_variables', ctx=Load()),
                                          ifs=[],
                                          is_async=0)])),
                              Assign(
                                 targets=[
                                    Name(id='dropdown_options', ctx=Store())],
                                 value=ListComp(
                                    elt=Call(
                                       func=Name(id='get_dropdown_options', ctx=Load()),
                                       args=[
                                          Subscript(
                                             value=Name(id='structure', ctx=Load()),
                                             slice=Name(id='v', ctx=Load()),
                                             ctx=Load())],
                                       keywords=[]),
                                    generators=[
                                       comprehension(
                                          target=Name(id='v', ctx=Store()),
                                          iter=Name(id='integer_variables', ctx=Load()),
                                          ifs=[],
                                          is_async=0)])),
                              Return(
                                 value=Tuple(
                                    elts=[
                                       Name(id='checkbox_values', ctx=Load()),
                                       Name(id='dropdown_options', ctx=Load()),
                                       List(
                                          elts=[
                                             Constant(value='No inconsistencies detected yet')],
                                          ctx=Load())],
                                    ctx=Load()))],
                           orelse=[]),
                        Assign(
                           targets=[
                              Name(id='changed_id', ctx=Store())],
                           value=Call(
                              func=Name(id='eval', ctx=Load()),
                              args=[
                                 Name(id='changed_component', ctx=Load())],
                              keywords=[])),
                        If(
                           test=Compare(
                              left=Subscript(
                                 value=Name(id='changed_id', ctx=Load()),
                                 slice=Constant(value='type'),
                                 ctx=Load()),
                              ops=[
                                 Eq()],
                              comparators=[
                                 Constant(value='checkboxes')]),
                           body=[
                              If(
                                 test=Compare(
                                    left=Call(
                                       func=Name(id='len', ctx=Load()),
                                       args=[
                                          Name(id='changed_value', ctx=Load())],
                                       keywords=[]),
                                    ops=[
                                       Gt()],
                                    comparators=[
                                       Constant(value=0)]),
                                 body=[
                                    Assign(
                                       targets=[
                                          Name(id='grounded_name', ctx=Store())],
                                       value=Subscript(
                                          value=Name(id='changed_id', ctx=Load()),
                                          slice=Constant(value='index'),
                                          ctx=Load())),
                                    Expr(
                                       value=Call(
                                          func=Name(id='print', ctx=Load()),
                                          args=[
                                             Constant(value='Grounded name: '),
                                             Name(id='grounded_name', ctx=Load())],
                                          keywords=[])),
                                    Assign(
                                       targets=[
                                          Name(id='grounded_value', ctx=Store())],
                                       value=Call(
                                          func=Name(id='convert_from_ui', ctx=Load()),
                                          args=[
                                             Name(id='changed_value', ctx=Load())],
                                          keywords=[])),
                                    Expr(
                                       value=Call(
                                          func=Name(id='print', ctx=Load()),
                                          args=[
                                             Constant(value='Grounded value: '),
                                             Name(id='grounded_value', ctx=Load())],
                                          keywords=[])),
                                    Assign(
                                       targets=[
                                          Tuple(
                                             elts=[
                                                Name(id='name', ctx=Store()),
                                                Name(id='arguments', ctx=Store())],
                                             ctx=Store())],
                                       value=Call(
                                          func=Name(id='unground', ctx=Load()),
                                          args=[
                                             Name(id='grounded_name', ctx=Load())],
                                          keywords=[])),
                                    Assign(
                                       targets=[
                                          Subscript(
                                             value=Attribute(
                                                value=Subscript(
                                                   value=Name(id='predicate_dict', ctx=Load()),
                                                   slice=Name(id='name', ctx=Load()),
                                                   ctx=Load()),
                                                attr='loc',
                                                ctx=Load()),
                                             slice=Tuple(
                                                elts=[
                                                   Starred(
                                                      value=Name(id='arguments', ctx=Load()),
                                                      ctx=Load())],
                                                ctx=Load()),
                                             ctx=Store())],
                                       value=Name(id='grounded_value', ctx=Load())),
                                    Expr(
                                       value=Call(
                                          func=Name(id='print', ctx=Load()),
                                          args=[
                                             Constant(value='Name: '),
                                             Name(id='name', ctx=Load())],
                                          keywords=[])),
                                    Expr(
                                       value=Call(
                                          func=Name(id='print', ctx=Load()),
                                          args=[
                                             Constant(value='Arguments: '),
                                             Name(id='arguments', ctx=Load())],
                                          keywords=[])),
                                    Assign(
                                       targets=[
                                          Name(id='changes', ctx=Store())],
                                       value=Dict(keys=[], values=[])),
                                    If(
                                       test=Compare(
                                          left=Name(id='grounded_value', ctx=Load()),
                                          ops=[
                                             Eq()],
                                          comparators=[
                                             Attribute(
                                                value=Name(id='EB', ctx=Load()),
                                                attr='TRUE',
                                                ctx=Load())]),
                                       body=[
                                          Expr(
                                             value=Call(
                                                func=Name(id='append_changes', ctx=Load()),
                                                args=[
                                                   Name(id='changes', ctx=Load()),
                                                   Dict(
                                                      keys=[
                                                         Name(id='name', ctx=Load())],
                                                      values=[
                                                         Call(
                                                            func=Name(id='Change', ctx=Load()),
                                                            args=[
                                                               Name(id='name', ctx=Load()),
                                                               List(
                                                                  elts=[
                                                                     Call(
                                                                        func=Name(id='tuple', ctx=Load()),
                                                                        args=[
                                                                           Name(id='arguments', ctx=Load())],
                                                                        keywords=[])],
                                                                  ctx=Load()),
                                                               List(elts=[], ctx=Load())],
                                                            keywords=[])])],
                                                keywords=[]))],
                                       orelse=[]),
                                    If(
                                       test=Compare(
                                          left=Name(id='grounded_value', ctx=Load()),
                                          ops=[
                                             Eq()],
                                          comparators=[
                                             Attribute(
                                                value=Name(id='EB', ctx=Load()),
                                                attr='FALSE',
                                                ctx=Load())]),
                                       body=[
                                          Expr(
                                             value=Call(
                                                func=Name(id='append_changes', ctx=Load()),
                                                args=[
                                                   Name(id='changes', ctx=Load()),
                                                   Dict(
                                                      keys=[
                                                         Name(id='name', ctx=Load())],
                                                      values=[
                                                         Call(
                                                            func=Name(id='Change', ctx=Load()),
                                                            args=[
                                                               Name(id='name', ctx=Load()),
                                                               List(elts=[], ctx=Load()),
                                                               List(
                                                                  elts=[
                                                                     Call(
                                                                        func=Name(id='tuple', ctx=Load()),
                                                                        args=[
                                                                           Name(id='arguments', ctx=Load())],
                                                                        keywords=[])],
                                                                  ctx=Load())],
                                                            keywords=[])])],
                                                keywords=[]))],
                                       orelse=[]),
                                    If(
                                       test=Compare(
                                          left=Name(id='grounded_value', ctx=Load()),
                                          ops=[
                                             Eq()],
                                          comparators=[
                                             Attribute(
                                                value=Name(id='EB', ctx=Load()),
                                                attr='INCONSISTENT',
                                                ctx=Load())]),
                                       body=[
                                          Return(
                                             value=Tuple(
                                                elts=[
                                                   Name(id='checkbox_values', ctx=Load()),
                                                   ListComp(
                                                      elt=Call(
                                                         func=Name(id='convert_to_ui', ctx=Load()),
                                                         args=[
                                                            Subscript(
                                                               value=Name(id='structure', ctx=Load()),
                                                               slice=Name(id='v', ctx=Load()),
                                                               ctx=Load())],
                                                         keywords=[]),
                                                      generators=[
                                                         comprehension(
                                                            target=Name(id='v', ctx=Store()),
                                                            iter=Name(id='integer_variables', ctx=Load()),
                                                            ifs=[],
                                                            is_async=0)]),
                                                   List(
                                                      elts=[
                                                         Constant(value='Unauthorized change, please reset')],
                                                      ctx=Load())],
                                                ctx=Load()))],
                                       orelse=[]),
                                    Assign(
                                       targets=[
                                          Name(id='start', ctx=Store())],
                                       value=Call(
                                          func=Attribute(
                                             value=Name(id='time', ctx=Load()),
                                             attr='time',
                                             ctx=Load()),
                                          args=[],
                                          keywords=[])),
                                    Try(
                                       body=[
                                          Expr(
                                             value=Call(
                                                func=Name(id='propagate_full', ctx=Load()),
                                                args=[
                                                   Name(id='changes', ctx=Load())],
                                                keywords=[])),
                                          Assign(
                                             targets=[
                                                Name(id='end', ctx=Store())],
                                             value=Call(
                                                func=Attribute(
                                                   value=Name(id='time', ctx=Load()),
                                                   attr='time',
                                                   ctx=Load()),
                                                args=[],
                                                keywords=[])),
                                          Expr(
                                             value=Call(
                                                func=Name(id='print', ctx=Load()),
                                                args=[
                                                   Constant(value='Time taken: '),
                                                   BinOp(
                                                      left=Name(id='end', ctx=Load()),
                                                      op=Sub(),
                                                      right=Name(id='start', ctx=Load()))],
                                                keywords=[])),
                                          For(
                                             target=Name(id='var_name', ctx=Store()),
                                             iter=Call(
                                                func=Attribute(
                                                   value=Name(id='predicate_dict', ctx=Load()),
                                                   attr='keys',
                                                   ctx=Load()),
                                                args=[],
                                                keywords=[]),
                                             body=[
                                                Expr(
                                                   value=Call(
                                                      func=Attribute(
                                                         value=Name(id='structure', ctx=Load()),
                                                         attr='update',
                                                         ctx=Load()),
                                                      args=[
                                                         Call(
                                                            func=Name(id='get_grounded_atoms_for_display', ctx=Load()),
                                                            args=[
                                                               Name(id='var_name', ctx=Load())],
                                                            keywords=[])],
                                                      keywords=[]))],
                                             orelse=[]),
                                          Return(
                                             value=Tuple(
                                                elts=[
                                                   ListComp(
                                                      elt=Call(
                                                         func=Name(id='convert_to_ui', ctx=Load()),
                                                         args=[
                                                            Subscript(
                                                               value=Name(id='structure', ctx=Load()),
                                                               slice=Name(id='v', ctx=Load()),
                                                               ctx=Load())],
                                                         keywords=[]),
                                                      generators=[
                                                         comprehension(
                                                            target=Name(id='v', ctx=Store()),
                                                            iter=Name(id='boolean_variables', ctx=Load()),
                                                            ifs=[],
                                                            is_async=0)]),
                                                   ListComp(
                                                      elt=Call(
                                                         func=Name(id='convert_to_ui', ctx=Load()),
                                                         args=[
                                                            Subscript(
                                                               value=Name(id='structure', ctx=Load()),
                                                               slice=Name(id='v', ctx=Load()),
                                                               ctx=Load())],
                                                         keywords=[]),
                                                      generators=[
                                                         comprehension(
                                                            target=Name(id='v', ctx=Store()),
                                                            iter=Name(id='integer_variables', ctx=Load()),
                                                            ifs=[],
                                                            is_async=0)]),
                                                   List(
                                                      elts=[
                                                         Constant(value='No inconsistencies detected yet')],
                                                      ctx=Load())],
                                                ctx=Load()))],
                                       handlers=[
                                          ExceptHandler(
                                             type=Name(id='Exception', ctx=Load()),
                                             name='e',
                                             body=[
                                                Expr(
                                                   value=Call(
                                                      func=Name(id='print', ctx=Load()),
                                                      args=[
                                                         Constant(value='Inconsistent!')],
                                                      keywords=[])),
                                                Expr(
                                                   value=Call(
                                                      func=Name(id='print', ctx=Load()),
                                                      args=[
                                                         Name(id='e', ctx=Load())],
                                                      keywords=[])),
                                                Return(
                                                   value=Tuple(
                                                      elts=[
                                                         Name(id='checkbox_values', ctx=Load()),
                                                         ListComp(
                                                            elt=Call(
                                                               func=Name(id='convert_to_ui', ctx=Load()),
                                                               args=[
                                                                  Subscript(
                                                                     value=Name(id='structure', ctx=Load()),
                                                                     slice=Name(id='v', ctx=Load()),
                                                                     ctx=Load())],
                                                               keywords=[]),
                                                            generators=[
                                                               comprehension(
                                                                  target=Name(id='v', ctx=Store()),
                                                                  iter=Name(id='integer_variables', ctx=Load()),
                                                                  ifs=[],
                                                                  is_async=0)]),
                                                         List(
                                                            elts=[
                                                               Name(id='e', ctx=Load())],
                                                            ctx=Load())],
                                                      ctx=Load()))])],
                                       orelse=[],
                                       finalbody=[])],
                                 orelse=[])],
                           orelse=[]),
                        If(
                           test=Compare(
                              left=Subscript(
                                 value=Name(id='changed_id', ctx=Load()),
                                 slice=Constant(value='type'),
                                 ctx=Load()),
                              ops=[
                                 Eq()],
                              comparators=[
                                 Constant(value='dropdown')]),
                           body=[
                              If(
                                 test=Compare(
                                    left=Name(id='changed_value', ctx=Load()),
                                    ops=[
                                       NotEq()],
                                    comparators=[
                                       Constant(value=None)]),
                                 body=[
                                    Assign(
                                       targets=[
                                          Name(id='changes', ctx=Store())],
                                       value=Dict(
                                          keys=[
                                             Subscript(
                                                value=Name(id='changed_id', ctx=Load()),
                                                slice=Constant(value='index'),
                                                ctx=Load())],
                                          values=[
                                             Set(
                                                elts=[
                                                   Name(id='changed_value', ctx=Load())])])),
                                    Assign(
                                       targets=[
                                          Name(id='unsat_fields', ctx=Store())],
                                       value=Call(
                                          func=Name(id='propagate_full', ctx=Load()),
                                          args=[
                                             Name(id='changes', ctx=Load())],
                                          keywords=[])),
                                    If(
                                       test=Compare(
                                          left=Call(
                                             func=Name(id='len', ctx=Load()),
                                             args=[
                                                Name(id='unsat_fields', ctx=Load())],
                                             keywords=[]),
                                          ops=[
                                             Eq()],
                                          comparators=[
                                             Constant(value=0)]),
                                       body=[
                                          Return(
                                             value=Tuple(
                                                elts=[
                                                   ListComp(
                                                      elt=Call(
                                                         func=Name(id='convert_to_ui', ctx=Load()),
                                                         args=[
                                                            Subscript(
                                                               value=Name(id='structure', ctx=Load()),
                                                               slice=Name(id='v', ctx=Load()),
                                                               ctx=Load())],
                                                         keywords=[]),
                                                      generators=[
                                                         comprehension(
                                                            target=Name(id='v', ctx=Store()),
                                                            iter=Name(id='boolean_variables', ctx=Load()),
                                                            ifs=[],
                                                            is_async=0)]),
                                                   ListComp(
                                                      elt=Call(
                                                         func=Name(id='convert_to_ui', ctx=Load()),
                                                         args=[
                                                            Subscript(
                                                               value=Name(id='structure', ctx=Load()),
                                                               slice=Name(id='v', ctx=Load()),
                                                               ctx=Load())],
                                                         keywords=[]),
                                                      generators=[
                                                         comprehension(
                                                            target=Name(id='v', ctx=Store()),
                                                            iter=Name(id='integer_variables', ctx=Load()),
                                                            ifs=[],
                                                            is_async=0)]),
                                                   List(
                                                      elts=[
                                                         Constant(value='No inconsistencies detected yet')],
                                                      ctx=Load())],
                                                ctx=Load()))],
                                       orelse=[
                                          Return(
                                             value=Tuple(
                                                elts=[
                                                   Name(id='checkbox_values', ctx=Load()),
                                                   ListComp(
                                                      elt=Call(
                                                         func=Name(id='convert_to_ui', ctx=Load()),
                                                         args=[
                                                            Subscript(
                                                               value=Name(id='structure', ctx=Load()),
                                                               slice=Name(id='v', ctx=Load()),
                                                               ctx=Load())],
                                                         keywords=[]),
                                                      generators=[
                                                         comprehension(
                                                            target=Name(id='v', ctx=Store()),
                                                            iter=Name(id='integer_variables', ctx=Load()),
                                                            ifs=[],
                                                            is_async=0)]),
                                                   List(elts=[], ctx=Load())],
                                                ctx=Load()))])],
                                 orelse=[])],
                           orelse=[])],
                     orelse=[]),
                  Return(
                     value=Tuple(
                        elts=[
                           Name(id='checkbox_values', ctx=Load()),
                           ListComp(
                              elt=Call(
                                 func=Name(id='convert_to_ui', ctx=Load()),
                                 args=[
                                    Subscript(
                                       value=Name(id='structure', ctx=Load()),
                                       slice=Name(id='v', ctx=Load()),
                                       ctx=Load())],
                                 keywords=[]),
                              generators=[
                                 comprehension(
                                    target=Name(id='v', ctx=Store()),
                                    iter=Name(id='integer_variables', ctx=Load()),
                                    ifs=[],
                                    is_async=0)]),
                           List(
                              elts=[
                                 Constant(value='No inconsistencies detected yet')],
                              ctx=Load())],
                        ctx=Load()))],
               decorator_list=[
                  Call(
                     func=Attribute(
                        value=Name(id='app', ctx=Load()),
                        attr='callback',
                        ctx=Load()),
                     args=[
                        List(
                           elts=[
                              Call(
                                 func=Name(id='Output', ctx=Load()),
                                 args=[
                                    Dict(
                                       keys=[
                                          Constant(value='type'),
                                          Constant(value='index')],
                                       values=[
                                          Constant(value='checkboxes'),
                                          Name(id='ALL', ctx=Load())]),
                                    Constant(value='value')],
                                 keywords=[]),
                              Call(
                                 func=Name(id='Output', ctx=Load()),
                                 args=[
                                    Dict(
                                       keys=[
                                          Constant(value='type'),
                                          Constant(value='index')],
                                       values=[
                                          Constant(value='dropdown'),
                                          Name(id='ALL', ctx=Load())]),
                                    Constant(value='options')],
                                 keywords=[]),
                              Call(
                                 func=Name(id='Output', ctx=Load()),
                                 args=[
                                    Dict(
                                       keys=[
                                          Constant(value='type')],
                                       values=[
                                          Constant(value='text-output')]),
                                    Constant(value='children')],
                                 keywords=[])],
                           ctx=Load()),
                        List(
                           elts=[
                              Call(
                                 func=Name(id='Input', ctx=Load()),
                                 args=[
                                    Dict(
                                       keys=[
                                          Constant(value='type'),
                                          Constant(value='index')],
                                       values=[
                                          Constant(value='checkboxes'),
                                          Name(id='ALL', ctx=Load())]),
                                    Constant(value='value')],
                                 keywords=[]),
                              Call(
                                 func=Name(id='Input', ctx=Load()),
                                 args=[
                                    Dict(
                                       keys=[
                                          Constant(value='type'),
                                          Constant(value='index')],
                                       values=[
                                          Constant(value='dropdown'),
                                          Name(id='ALL', ctx=Load())]),
                                    Constant(value='value')],
                                 keywords=[]),
                              Call(
                                 func=Name(id='Input', ctx=Load()),
                                 args=[
                                    Constant(value='reset-button'),
                                    Constant(value='n_clicks')],
                                 keywords=[])],
                           ctx=Load()),
                        List(
                           elts=[
                              Call(
                                 func=Name(id='State', ctx=Load()),
                                 args=[
                                    Dict(
                                       keys=[
                                          Constant(value='type'),
                                          Constant(value='index')],
                                       values=[
                                          Constant(value='checkboxes'),
                                          Name(id='ALL', ctx=Load())]),
                                    Constant(value='id')],
                                 keywords=[]),
                              Call(
                                 func=Name(id='State', ctx=Load()),
                                 args=[
                                    Dict(
                                       keys=[
                                          Constant(value='type'),
                                          Constant(value='index')],
                                       values=[
                                          Constant(value='dropdown'),
                                          Name(id='ALL', ctx=Load())]),
                                    Constant(value='id')],
                                 keywords=[])],
                           ctx=Load())],
                     keywords=[])]),
            Expr(
               value=Call(
                  func=Attribute(
                     value=Name(id='app', ctx=Load()),
                     attr='run_server',
                     ctx=Load()),
                  args=[],
                  keywords=[
                     keyword(
                        arg='debug',
                        value=Constant(value=True))]))],
         decorator_list=[]),
      If(
         test=Compare(
            left=Name(id='__name__', ctx=Load()),
            ops=[
               Eq()],
            comparators=[
               Constant(value='__main__')]),
         body=[
            Expr(
               value=Call(
                  func=Name(id='launch_dash_app', ctx=Load()),
                  args=[],
                  keywords=[]))],
         orelse=[])],
   type_ignores=[])



def generate_write_functionality(interpreted_predicates):
   intepreted_predicates_ast = [Constant(value=elem) for elem in interpreted_predicates]
   return Module(
   body=[
      FunctionDef(
         name='store_consequences',
         args=arguments(
            posonlyargs=[],
            args=[],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
         body=[
            Assign(
               targets=[
                  Name(id='start', ctx=Store())],
               value=Call(
                  func=Attribute(
                     value=Name(id='time', ctx=Load()),
                     attr='time',
                     ctx=Load()),
                  args=[],
                  keywords=[])),
            Expr(
               value=Call(
                  func=Name(id='initial_propagation', ctx=Load()),
                  args=[],
                  keywords=[])),
            Assign(
               targets=[
                  Name(id='end', ctx=Store())],
               value=Call(
                  func=Attribute(
                     value=Name(id='time', ctx=Load()),
                     attr='time',
                     ctx=Load()),
                  args=[],
                  keywords=[])),
            Expr(
               value=Call(
                  func=Name(id='print', ctx=Load()),
                  args=[
                     Constant(value='Initial propagation: '),
                     BinOp(
                        left=Name(id='end', ctx=Load()),
                        op=Sub(),
                        right=Name(id='start', ctx=Load()))],
                  keywords=[])),
            Assign(
               targets=[
                  Name(id='consequences_dict', ctx=Store())],
               value=Dict(keys=[], values=[])),
            For(
               target=Name(id='name', ctx=Store()),
               iter=Call(
                  func=Attribute(
                     value=Name(id='predicate_dict', ctx=Load()),
                     attr='keys',
                     ctx=Load()),
                  args=[],
                  keywords=[]),
               body=[
                  If(
                     test=BoolOp(
                        op=And(),
                        values=[
                           Compare(
                              left=Name(id='name', ctx=Load()),
                              ops=[
                                 NotIn()],
                              comparators=[
                                 List(
                                    elts=intepreted_predicates_ast,
                                    ctx=Load())]),
                           UnaryOp(
                              op=Not(),
                              operand=Call(
                                 func=Attribute(
                                    value=Name(id='name', ctx=Load()),
                                    attr='startswith',
                                    ctx=Load()),
                                 args=[
                                    Constant(value='_')],
                                 keywords=[]))]),
                     body=[
                        Assign(
                           targets=[
                              Name(id='data_array', ctx=Store())],
                           value=Subscript(
                              value=Name(id='predicate_dict', ctx=Load()),
                              slice=Name(id='name', ctx=Load()),
                              ctx=Load())),
                        Assign(
                           targets=[
                              Name(id='new_domains', ctx=Store())],
                           value=ListComp(
                              elt=Attribute(
                                 value=Subscript(
                                    value=Attribute(
                                       value=Name(id='data_array', ctx=Load()),
                                       attr='coords',
                                       ctx=Load()),
                                    slice=Name(id='dim', ctx=Load()),
                                    ctx=Load()),
                                 attr='values',
                                 ctx=Load()),
                              generators=[
                                 comprehension(
                                    target=Name(id='dim', ctx=Store()),
                                    iter=Attribute(
                                       value=Name(id='data_array', ctx=Load()),
                                       attr='dims',
                                       ctx=Load()),
                                    ifs=[],
                                    is_async=0)])),
                        Assign(
                           targets=[
                              Subscript(
                                 value=Name(id='consequences_dict', ctx=Load()),
                                 slice=Name(id='name', ctx=Load()),
                                 ctx=Store())],
                           value=SetComp(
                              elt=Call(
                                 func=Name(id='tuple', ctx=Load()),
                                 args=[
                                    GeneratorExp(
                                       elt=Call(
                                          func=Attribute(
                                             value=Name(id='c', ctx=Load()),
                                             attr='item',
                                             ctx=Load()),
                                          args=[],
                                          keywords=[]),
                                       generators=[
                                          comprehension(
                                             target=Name(id='c', ctx=Store()),
                                             iter=Name(id='comb', ctx=Load()),
                                             ifs=[],
                                             is_async=0)])],
                                 keywords=[]),
                              generators=[
                                 comprehension(
                                    target=Name(id='comb', ctx=Store()),
                                    iter=Call(
                                       func=Name(id='product', ctx=Load()),
                                       args=[
                                          Starred(
                                             value=Name(id='new_domains', ctx=Load()),
                                             ctx=Load())],
                                       keywords=[]),
                                    ifs=[
                                       Compare(
                                          left=Call(
                                             func=Attribute(
                                                value=Attribute(
                                                   value=Subscript(
                                                      value=Attribute(
                                                         value=Name(id='data_array', ctx=Load()),
                                                         attr='loc',
                                                         ctx=Load()),
                                                      slice=Name(id='comb', ctx=Load()),
                                                      ctx=Load()),
                                                   attr='values',
                                                   ctx=Load()),
                                                attr='item',
                                                ctx=Load()),
                                             args=[],
                                             keywords=[]),
                                          ops=[
                                             Eq()],
                                          comparators=[
                                             Attribute(
                                                value=Name(id='EB', ctx=Load()),
                                                attr='TRUE',
                                                ctx=Load())])],
                                    is_async=0)]))],
                     orelse=[])],
               orelse=[]),
            With(
               items=[
                  withitem(
                     context_expr=Call(
                        func=Name(id='open', ctx=Load()),
                        args=[
                           Constant(value='consequences.pkl'),
                           Constant(value='wb')],
                        keywords=[]),
                     optional_vars=Name(id='f', ctx=Store()))],
               body=[
                  Expr(
                     value=Call(
                        func=Attribute(
                           value=Name(id='pickle', ctx=Load()),
                           attr='dump',
                           ctx=Load()),
                        args=[
                           Name(id='consequences_dict', ctx=Load()),
                           Name(id='f', ctx=Load())],
                        keywords=[]))])],
         decorator_list=[]),
      Expr(
         value=Call(
            func=Name(id='store_consequences', ctx=Load()),
            args=[],
            keywords=[]))],
   type_ignores=[])


# Main function: receives all ENF rules, grouped propagators, types, predicates, functions, and predicates that are interpreted in the structure of the IDP-program.
# With this input, all parts of the Python program are constructed and joined together as an AST.
# This AST is converted to an executable Python file using the astunparse library.
def generate(enf_rules, grouped_propagators, types, predicates, functions, interpreted_predicates, choice=2):
    # make data arrays: types, predicates, functions necessary + auxiliary var!

    #grouped_propagators = group_propagators(enf_rules, functions)
    temp_data_arrays = construct_data_arrays(types, predicates)
    true_list = determine_true_list(enf_rules)
    equality_domain, operator_set = get_domain_elements_tested_on_equality(enf_rules, types)
    imports = generate_imports()
    auxiliary_classes = generate_auxiliary_classes()
    data_arrays = generate_data_arrays(temp_data_arrays)
    data_arrays_extra = generate_data_arrays_extra()
    true_and_unknown_lists = generate_true_and_unknown_lists(true_list)
    data_arrays_extra_dash = generate_data_arrays_extra_dash()
    conditional_propagate = generate_conditional_propagate()
    unconditional_propagate = generate_unconditional_propagate()
    get_from_data_array = generate_get_from_data_array()
    inverse = generate_inverse()
    append_changes = generate_append_changes()
    get_from_data_array_wrap = generate_get_from_data_array_wrap()
    write_to_data_array = generate_write_to_data_array()
    handle_conditional_propagate_results = generate_handle_conditional_propagate_results()
    normal_propagation = generate_normal_propagation()
    handle_unconditional_propagate_results = generate_handle_unconditional_propagate_results()
    unconditional_propagate_wrap = generate_unconditional_propagate_wrap()
    calculate_first_coordinate = generate_calculate_first_coordinate()
    calculate_next_coordinate = generate_calculate_next_coordinate()
    incremental_propagate = generate_incremental_propagate()
    incremental_propagate_wrap = generate_incremental_propagate_wrap()
    map_indices = generate_map_indices()
    is_valid_index = generate_is_valid_index()
    map_indices_wrap = generate_map_indices_wrap()
    add_dims = generate_add_dims()
    reduce_dims = generate_reduce_dims()
    specifying_propagation = generate_specifying_propagation()
    specifying_propagation_2 = generate_specifying_propagation_2()
    generate_rule = generate_generate_rule()
    generalizing_propagation = generate_generalizing_propagation()
    generalizing_propagation_2 = generate_generalizing_propagation_2()
    add_all_function_outputs = generate_add_all_function_outputs()
    function_propagation = generate_function_propagation()
    function_propagation_2 = generate_function_propagation_2()
    propagate = generate_propagate(grouped_propagators)
    propagate_full = generate_propagate_full()
    fill_in_interpreted_domain = generate_fill_in_interpreted_domain()
    get_changes_for_comparison_operators = generate_get_changes_for_comparison_operators()
    initial_propagation = generate_initial_propagation(grouped_propagators, equality_domain, interpreted_predicates, operator_set)
    get_grounded_atom_name = generate_get_grounded_atom_name()
    get_grounded_atoms_for_display = generate_get_grounded_atoms_for_display()
    terminal_test = generate_terminal_test()
    dash_functionality = generate_dash_functionality()
    write_functionality = generate_write_functionality(interpreted_predicates)
    #prop_list = generate_propagate_rule_from_unsat_set(grouped_propagators['_X2'][0], '_X2', True)
    #spec_prop = generate_propagate_rule_from_specific_propagation(grouped_propagators['_X3'][0])
    #gen_prop = generate_propagate_rule_from_general_propagation(grouped_propagators[';p_C'][0])
    #module = Module(body=gen_prop.body)

    # Uncomment to work without incremental propagation (only for testing purposes, this method is not bug free!)
    #choice = 4
    if choice == 1:
        module = Module(body=imports.body + auxiliary_classes.body + data_arrays.body + data_arrays_extra_dash.body + true_and_unknown_lists.body + conditional_propagate.body + unconditional_propagate.body + get_from_data_array.body + inverse.body + append_changes.body + get_from_data_array_wrap.body + write_to_data_array.body + handle_conditional_propagate_results.body +
                         normal_propagation.body + handle_unconditional_propagate_results.body + unconditional_propagate_wrap.body + calculate_first_coordinate.body + calculate_next_coordinate.body + incremental_propagate.body + incremental_propagate_wrap.body + map_indices.body + is_valid_index.body + map_indices_wrap.body + add_dims.body + reduce_dims.body + specifying_propagation.body +
                         generalizing_propagation.body + add_all_function_outputs.body + function_propagation.body + propagate.body + propagate_full.body + fill_in_interpreted_domain.body + get_changes_for_comparison_operators.body + initial_propagation.body + get_grounded_atom_name.body + get_grounded_atoms_for_display.body + dash_functionality.body)
    elif choice == 2:
        module = Module(body=imports.body + auxiliary_classes.body + data_arrays.body + data_arrays_extra.body + true_and_unknown_lists.body + conditional_propagate.body + unconditional_propagate.body + get_from_data_array.body + inverse.body + append_changes.body + get_from_data_array_wrap.body + write_to_data_array.body + handle_conditional_propagate_results.body +
                         normal_propagation.body + handle_unconditional_propagate_results.body + unconditional_propagate_wrap.body + calculate_first_coordinate.body + calculate_next_coordinate.body + incremental_propagate.body + incremental_propagate_wrap.body + map_indices.body + is_valid_index.body + map_indices_wrap.body + add_dims.body + reduce_dims.body + specifying_propagation.body +
                         generalizing_propagation.body + add_all_function_outputs.body + function_propagation.body + propagate.body + propagate_full.body + fill_in_interpreted_domain.body + get_changes_for_comparison_operators.body + initial_propagation.body + get_grounded_atom_name.body + get_grounded_atoms_for_display.body + terminal_test.body)
    elif choice == 3:
        module = Module(body=imports.body + auxiliary_classes.body + data_arrays.body + data_arrays_extra.body + true_and_unknown_lists.body + conditional_propagate.body + unconditional_propagate.body + get_from_data_array.body + inverse.body + append_changes.body + get_from_data_array_wrap.body + write_to_data_array.body + handle_conditional_propagate_results.body +
                         normal_propagation.body + handle_unconditional_propagate_results.body + unconditional_propagate_wrap.body + calculate_first_coordinate.body + calculate_next_coordinate.body + incremental_propagate.body + incremental_propagate_wrap.body + map_indices.body + is_valid_index.body + map_indices_wrap.body + add_dims.body + reduce_dims.body + specifying_propagation.body +
                         generalizing_propagation.body + add_all_function_outputs.body + function_propagation.body + propagate.body + propagate_full.body + fill_in_interpreted_domain.body + get_changes_for_comparison_operators.body + initial_propagation.body + get_grounded_atom_name.body + get_grounded_atoms_for_display.body + write_functionality.body)

    # No incremental propagation
    elif choice == 4:
        module = Module(body=imports.body + auxiliary_classes.body + data_arrays.body + data_arrays_extra.body + true_and_unknown_lists.body + conditional_propagate.body + unconditional_propagate.body + get_from_data_array.body + inverse.body + append_changes.body + get_from_data_array_wrap.body + write_to_data_array.body + handle_conditional_propagate_results.body +
                         normal_propagation.body + handle_unconditional_propagate_results.body + unconditional_propagate_wrap.body + calculate_first_coordinate.body + calculate_next_coordinate.body + incremental_propagate.body + incremental_propagate_wrap.body + map_indices.body + is_valid_index.body + map_indices_wrap.body + add_dims.body + reduce_dims.body + specifying_propagation_2.body +
                         generate_rule.body + generalizing_propagation_2.body + add_all_function_outputs.body + function_propagation_2.body + propagate.body + propagate_full.body + fill_in_interpreted_domain.body + get_changes_for_comparison_operators.body + initial_propagation.body + get_grounded_atom_name.body + get_grounded_atoms_for_display.body + terminal_test.body)


    code = astunparse.unparse(module)

    with open("second_method_generated_code.py", "w") as file:
        file.write(code)
