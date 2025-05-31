# This is the main method calling all the necessary steps of the compiler implementing the first method as described in section 4.3.
# The following steps are executed in order and can be found in the following files respectively:
# 1) Parsing (first_method_parsing.py)
# 2) Function transformation (first_method_function_transformation.py)
# 3) Transformation to Negation Normal Form (first_method_nnf.py)
# 4) Transformation to Equivalence Normal Form (first_method_enf.py)
# 5) Grounding ENF rules (first_method_grounding.py)
# 5) Transformation to UNSAT-sets (first_method_unsat_sets.py)
# 6) Transformation to propagators (first_method_propagators.py)
# 7) Construction of AST and Python-file (first_method_generate.py)
# The resulting program is written to first_method_generated_code.py
# To see an example of a generated Python program with commentary, go to first_method_generated_code_example.py

import time
from datetime import datetime
import pandas as pd
from first_method import (first_method_parsing, first_method_function_transformation, first_method_nnf,
                          first_method_enf, first_method_grounding, first_method_unsat_sets, first_method_propagators,
                          first_method_generate)

def main():
    start_compilation = time.time()
    with open("idp_program.idp", "r") as file:
        idp_program = file.read()

    parsed_idp = first_method_parsing.parse(idp_program)
    new_rules = first_method_function_transformation.transform_functions(parsed_idp.rules, parsed_idp.functions, parsed_idp.predicates)
    nnf_rules = first_method_nnf.transform_to_nnf(new_rules)
    enf_rules = first_method_enf.transform_to_enf(nnf_rules)
    grounded_enf_rules = first_method_grounding.ground(enf_rules, parsed_idp.types)
    unsat_sets = first_method_unsat_sets.derive_unsat_sets(grounded_enf_rules)
    propagators = first_method_propagators.derive_propagators(unsat_sets)
    first_method_generate.generate(grounded_enf_rules, propagators, False) # True for interactive application, False for terminal interaction

    end_compilation = time.time()
    compilation_time = end_compilation - start_compilation
    print("Compilation time: ", compilation_time)
    file_path = "../experimental_data.csv"
    new_row = {"timestamp": datetime.now(), "value": compilation_time}
    data_frame_row = pd.DataFrame([new_row])
    data_frame_row.to_csv(file_path, mode='a', header=not pd.io.common.file_exists(file_path), index=False)

main()