# This part of the compiler is responsible for converting grounded ENF-rules to UNSAT-sets.
# This happens in the following way:
# L ⇔ L1 ∧ … ∧ Ln (ENFConjunctive) becomes {L, ~L1}, ..., {L, ~Ln}, {~L, L1, ..., Ln}
# L ⇔ L1 ∨ … ∨ Ln (ENFDisjunctive) becomes {~L, L1}, ..., {~L, Ln}, {L, ~L1, ..., ~Ln}
# true ⇔ L (AssertLiteral) becomes {~L}
# UNSAT-sets express that at least one literal in the set has to evaluate to false.
# In this way, propagators can be derived in the next step.

# More details about this part of the compiler can be found in the thesis text, in section 4.3.6.



from first_method_enf import ENFDisjunctive, ENFConjunctive, AssertLiteral

# Function that handles the transformation from an ENF-rule to multiple UNSAT-sets.
def derive_unsat_sets_for_rule(enf_rule):
    unsat_sets = []
    if type(enf_rule) == ENFDisjunctive:
        for literal in enf_rule.right:
            unsat_sets.append({literal,enf_rule.left.negate()})
        prop_set = {enf_rule.left}
        for literal in enf_rule.right[:-1]:
            prop_set.add(literal.negate())
        prop_set.add(enf_rule.right[-1].negate())
        unsat_sets.append(prop_set)
    elif type(enf_rule) == ENFConjunctive:
        for literal in enf_rule.right:
            unsat_sets.append({enf_rule.left, literal.negate()})
        prop_set = set()
        for literal in enf_rule.right:
            prop_set.add(literal)
        prop_set.add(enf_rule.left.negate())
        unsat_sets.append(prop_set)

    elif type(enf_rule) == AssertLiteral:
        unsat_sets.append({enf_rule.literal.negate()})

    return unsat_sets

# Main function, calling the function that does the transformation.
def derive_unsat_sets(rules):
    unsat_sets = [derive_unsat_sets_for_rule(rule) for rule in rules]
    unsat_sets_flat = [item for sublist in unsat_sets for item in sublist]
    return unsat_sets_flat
