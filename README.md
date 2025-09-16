# compiler-for-kbs

This repository contains a compiler that converts an IDP program into a Python program performing the propagation inference task. The motivation for developing the compiler, the implementation steps of the compiler, and experimental results regarding the compiler are discussed in my thesis text. (An efficient compiler for a knowledge base system, Wout Piessens, 2025) 

I have implemented two methods, the differences are discussed in the thesis text. It is important to note that the first method is not practically feasible on larger IDP-programs, it is added to the repository for illustrative purposes.

For both methods, to be able to use tree-sitter-fodot to parse IDP programs, install the tree-sitter parsing library in Python. Make sure this is version 0.21.3! Next, clone the following repository [1] inside the working folder (first_method or second_method). Enter the tree-sitter-fodot repository, and execute:

git checkout 674dabc2  

This returns the repository to the version of July 17, 2024, ensuring compatibility with my code.

The following installations need to be performed:

<pre> 
pip install tree_sitter=0.21.3 
  
pip install astunparse 
  
pip install xarray 
  
pip install dash </pre>

For the first method: run first_method/first_method_main.py to execute the compiler with input idp_program.idp. The generated Python code will appear in first_method/first_method_generated_code.py. 

For the second method: run second_method/second_method_main.py to execute the compiler with input idp_program2.idp. The generated Python code will appear in second_method/second_method_generated_code.py.

To understand the workings of the compiler, read the thesis text, or consult the comments added to the code under first_method or second_method. An illustrative example of how all helper functions work in the generated Python program performing propagation inference is given in first_method_generated_code_example.py and second_method_generated_code_example.py.
In order to reproduce the experiments in chapter 5 of the thesis text, here is some extra information:
-	To test the second method without caching, you can adapt the generated Python program by setting the global variables true_list and unknown_list as equal to the empty list.
-	To test the second method without function propagators, and instead with adding extra rules to the theory, you have to change the compiler code in two locations:
  1) Add the function add_new_function_rules() in second_method/second_method_function_transformation.py (this function is now commented), and call the function in transform_functions().
  2) In second_method/second_method_propagators.py, in the function group_propagators(), remove the for loop that adds a FunctionPropagator for every function in the theory.
-	To test the second method without incremental propagation, you have to change the parameter choice to 4 in the function generate() in second_method/second_method_generate.py. Warning: this change regularly results in bugs in the generated code.


The three changes in the second method mentioned here lead to worse performance than the second method with caching, with function propagators and with incremental propagation. This is shown in the experiments of my thesis text. Therefore, they are only for illustrative purposes. 

Note that the implementation of propagation inference on mathematical operators (<, <=, >, >=, =, ~=) is not great regarding time efficiency.

Also note that the compiler doesn’t do all necessary checks on correct IDP syntax, so an IDP program with wrong syntax can lead to unpredictable behavior: either an exception in the compiler, an exception in the generated code, or wrong propagation results. Especially, do not forget to end rules in the theory and interpretations in the structure with a dot.

[1] https://gitlab.com/sli-lib/tree-sitter-fodot
