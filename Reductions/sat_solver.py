# TODO: Your name, Cornell NetID
# TODO: Your Partner's name, Cornell NetID

from helpers import *
from cnf_sat_solver import dpll

# DO NOT CHANGE SAT_solver 
# Convert to Conjunctive Normal Form (CNF)
"""
>>> to_cnf_gadget('~(B | C)')
(~B & ~C)
"""
def to_cnf_gadget(s):
    s = expr(s)
    if isinstance(s, str):
        s = expr(s)
    step1 = parse_iff_implies(s)
    #print(step1)# Steps 1
    step2 = deMorgansLaw(step1)  # Step 2
    return distibutiveLaw(step2)  # Step 3

# ______________________________________________________________________________
# STEP1: if s has IFF or IMPLIES, parse them

# TODO: depending on whether the operator contains IMPLIES('==>') or IFF('<=>'),
# Change them into equivalent form with only &, |, and ~ as logical operators
# The return value should be an Expression (e.g. ~a | b )

# Hint: you may use the expr() helper function to help you parse a string into an Expr
# you may also use the is_symbol() helper function to determine if you have encountered a propositional symbol
def parse_iff_implies(s):
    # TODO: write your code here, change the return values accordingly
    s = rec_parse_iff_implies(s) 
    return s

def rec_parse_iff_implies(exp):
    #exp = Expr(s.op, s.args[0], s.args[1])
    #s = exp
    if len(exp.args) < 2:
        return exp
    
    argA, argB = exp.args[0], exp.args[1]
    expA = rec_parse_iff_implies(argA)
    
    expB = rec_parse_iff_implies(argB)
    
    if exp.op == "==>":
        expA = expA.__invert__()
        expA = expA.__or__(expB)
        
    elif exp.op == "<==>":
        expAA = Expr("==>", expA, expB)
        expAA = rec_parse_iff_implies(expAA)
        expBB = Expr("==>", expB, expA)
        expBB = rec_parse_iff_implies(expBB)
        expAA = expAA.__and__(expBB)
        expA = expAA
    
    return expA
    

# ______________________________________________________________________________
# STEP2: if there is NOT(~), move it inside, change the operations accordingly.


""" Example:
>>> deMorgansLaw(~(A | B))
(~A & ~B)
"""

# TODO: recursively apply deMorgansLaw if you encounter a negation('~')
# The return value should be an Expression (e.g. ~a | b )

# Hint: you may use the associate() helper function to help you flatten the expression
# you may also use the is_symbol() helper function to determine if you have encountered a propositional symbol
def deMorgansLaw(s):
    # TODO: write your code here, change the return values accordingly
    #print(expr(s.args[0][0]).args)
    #print(s.op)
    s = rec_deMorgansLaw(s)
    print(s)
    return s

def rec_deMorgansLaw(exp): 
    print("\nBegin!")
    print(exp)
    print(exp.op)
    print(exp.args)
    if len(exp.args) == 0:
        print("\nReturn: ")
        print(exp)
        return exp
    
    if exp.op == '~':
        current = rec_deMorgansLaw(exp.args[0])
        if current.op == '~':
            exp = current.args[0]
        elif not is_symbol(current.op):
            #print("\nHERE")
            #exp = expA.__invert__()
            #print(exp)
            #exp = expA
        #else:
            op = current.op
            argA = current.args[0]
            argB = current.args[1]
            argA = argA.__invert__()
            expA = rec_deMorgansLaw(argA)
            argB = argB.__invert__()
            expB = rec_deMorgansLaw(argB)
            if op == '&':
                op = '|'
            elif op == '|':
                op = '&'
            exp = Expr(op, expA, expB)
        else:
            exp = Expr(exp.op, current)
    
    else:
        argA, argB = exp.args[0], exp.args[1]
        expA = rec_deMorgansLaw(argA)
        expB = rec_deMorgansLaw(argB)
        exp = Expr(exp.op, expA, expB)
    
    print("\nReturn: ")    
    print(exp)
    return exp             
        

# ______________________________________________________________________________
# STEP3: use Distibutive Law to distribute and('&') over or('|')


""" Example:
>>> distibutiveLaw((A & B) | C)
((A | C) & (B | C))
"""

# TODO: apply distibutiveLaw so as to return an equivalent expression in CNF form
# Hint: you may use the associate() helper function to help you flatten the expression
def distibutiveLaw(s):
    # TODO: write your code here, change the return values accordingly
    return Expr(s.op, *args)


# ______________________________________________________________________________

# DO NOT CHANGE SAT_solver 
# Check satisfiability of an arbitrary looking Boolean Expression.
# It returns a satisfying assignment(Non-deterministic, non exhaustive) when it succeeds.
# returns False if the formula is unsatisfiable
# Don't need to care about the heuristic part


""" Example: 
>>> SAT_solver(A |'<=>'| B) == {A: True, B: True}
True
"""

""" unsatisfiable example: 
>>> SAT_solver(A & ~A )
False
"""
def SAT_solver(s, heuristic=no_heuristic):
    return dpll(conjuncts(to_cnf_gadget(s)), prop_symbols(s), {}, heuristic)


if __name__ == "__main__":

# Initialization
    A, B, C, D, E, F = expr('A, B, C, D, E, F')
    P, Q, R = expr('P, Q, R')

# Shows alternative ways to write your expression
    assert SAT_solver(~(~ (~( ~B)))) == {A: True, B: True}
    assert SAT_solver(~ (A | ~(B & C))) == {A: True, B: True}
    assert SAT_solver((A | '<==>' | B) | '==>' | C) == {A: True, B: True}
    assert SAT_solver(expr('A <=> B')) == {A: True, B: True}

# Some unsatisfiable examples
    assert SAT_solver(P & ~P) is False
    # The whole expression below is essentially just (A&~A)
    assert SAT_solver((A | B | C) & (A | B | ~C) & (A | ~B | C) & (A | ~B | ~C) & (
        ~A | B | C) & (~A | B | ~C) & (~A | ~B | C) & (~A | ~B | ~C)) is False

# This is the same example in the instructions.
    # Notice that SAT_solver's return value  is *Non-deterministic*, and *Non-exhaustive* when the expression is satisfiable,
    # meaning that it will only return *a* satisfying assignment when it succeeds.
    # If you run the same instruction multiple times, you may see different returns, but they should all be satisfying ones.
    result = SAT_solver((~(P | '==>' | Q)) | (R | '==>' | P))
    assert pl_true((~(P | '==>' | Q)) | (R | '==>' | P), result)

    assert pl_true((~(P | '==>' | Q)) | (R | '==>' | P), {P: True})
    assert pl_true((~(P | '==>' | Q)) | (R | '==>' | P), {Q: False, R: False})
    assert pl_true((~(P | '==>' | Q)) | (R | '==>' | P), {R: False})

# Some Boolean expressions has unique satisfying solutions
    assert SAT_solver(A & ~B & C & (A | ~D) & (~E | ~D) & (C | ~D) & (~A | ~F) & (E | ~F) & (~D | ~F) &
                      (B | ~C | D) & (A | ~E | F) & (~A | E | D)) == \
        {B: False, C: True, A: True, F: False, D: True, E: False}
    assert SAT_solver(A & B & ~C & D) == {C: False, A: True, D: True, B: True}
    assert SAT_solver((A | (B & C)) | '<=>' | ((A | B) & (A | C))) == {
        C: True, A: True} or {C: True, B: True}
    assert SAT_solver(A & ~B) == {A: True, B: False}

# The order in which the satisfying variable assignments get returned doen't matter.
    assert {A: True, B: False} == {B: False, A: True}
    print("No assertion errors found so far")
