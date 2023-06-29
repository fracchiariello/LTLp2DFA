from pythomata import SimpleDFA
from flloat.parser.ltlf import LTLfParser
import sys 

def symbolic_to_singleton(symbolic_dfa,letters):
    states = symbolic_dfa.states
    initial_state = symbolic_dfa.initial_state
    accepting_states = symbolic_dfa.accepting_states
    
    transition_function = {}
    for s in states:
        transitions_of_s = {}
        for _, formula, s_1  in symbolic_dfa.get_transitions_from(s):
            for letter in letters:
                interpretation = {l:0 for l in letters}
                interpretation[letter] = 1
                if formula.subs(interpretation):
                    transitions_of_s[letter] = s_1
        transition_function[s] = transitions_of_s
    
    singleton_dfa = SimpleDFA(states, letters, initial_state, accepting_states, transition_function)
    singleton_dfa = singleton_dfa#.minimize().trim()
    singleton_dfa = singleton_dfa.complete()
    #graph = singleton_dfa.to_graphviz()
    #graph.render('/DFA')
    return singleton_dfa

def alphabet(parsed_formula):
    letters = parsed_formula.find_labels()
    return letters

def parse(formula):
    parser = LTLfParser()
    parsed_formula = parser(formula)
    return parsed_formula

def to_dfa(parsed_formula):
    symbolic_dfa = parsed_formula.to_automaton() 
    return symbolic_dfa


def main():
    formula = sys.argv[1]
    parsed_formula = parse(formula)
    symbolic_dfa = to_dfa(parsed_formula)
    letters = alphabet(parsed_formula)
    letters.add('*') #symbol representing activities non appearing in the formula
    singleton_dfa = symbolic_to_singleton(symbolic_dfa,letters)
    graph = singleton_dfa.to_graphviz()
    graph.render("output/DFA")
    print(singleton_dfa.transition_function)
    
main()


