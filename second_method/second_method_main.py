# This is the main method calling all the necessary steps of the compiler implementing the second method as described in section 4.4 of the thesis text.
# The following steps are executed in order and can be found in the following files respectively:
# 1) Parsing (second_method_parsing.py)
# 2) Function transformation (second_method_function_transformation.py)
# 3) Transformation to Negation Normal Form (second_method_nnf.py)
# 4) Transformation to Equivalence Normal Form (second_method_enf.py)
# 5) Transformation to (high-level) propagators (second_method_propagators.py)
# 6) Construction of AST and Python-file (second_method_generate.py)

# The resulting program is written to second_method_generated_code.py
# To see an example of a generated Python program with commentary, go to second_method_generated_code_example.py

# Choice:
# 1 for interactive application,
# 2 for terminal interaction,
# 3 for writing consequences to .pkl file (no interaction with user, only initial propagation)
# 4 for random assignments (no interaction with user, only initial propagation, continues until all assignments are made or until inconsistency)

choice = 2

import time
from datetime import datetime
import pandas as pd
import second_method_parsing, second_method_function_transformation, second_method_nnf, second_method_enf, second_method_propagators, second_method_generate



def main(choice):
    start_compilation = time.time()
    with open("idp_program2.idp", "r") as file:
        idp_program = file.read()

    parsed_idp = second_method_parsing.parse(idp_program)
    new_rules = second_method_function_transformation.transform_functions(parsed_idp.rules, parsed_idp.functions, parsed_idp.predicates)
    nnf_rules = second_method_nnf.transform_to_nnf(new_rules)
    enf_rules, new_predicates = second_method_enf.transform_to_enf(nnf_rules, parsed_idp.predicates)
    parsed_idp.predicates = new_predicates
    propagators = second_method_propagators.group_propagators(enf_rules, parsed_idp.functions)
    second_method_generate.generate(enf_rules, propagators, parsed_idp.types, parsed_idp.predicates,
                                    parsed_idp.functions, parsed_idp.interpreted_predicates, choice)
    end_compilation = time.time()
    compilation_time = end_compilation - start_compilation
    print("Compilation time: ", compilation_time)
    #file_path = "../experimental_data.csv"
    #new_row = {"timestamp" : datetime.now(), "value" : compilation_time}
    #data_frame_row = pd.DataFrame([new_row])
    #data_frame_row.to_csv(file_path, mode='a', header=not pd.io.common.file_exists(file_path), index=False)


main(choice)