import os
from pythomata.impl.simple import SimpleNFA
from pythomata import SimpleDFA
from grammar_analyzer import Rule, Grammar
from collections import OrderedDict
from collections import Counter
import string


class Automata(object):
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.accepting_states = set()
        self.transitions = dict.fromkeys(self.grammar.non_terms)
        self.used_letters = self.grammar.non_terms

    def add_rules(self):
        for rule in self.grammar.rules:
            if len(rule.right) == 1:
                is_found = False
                for _rule in self.grammar.rules:
                    if len(_rule.right) == 2 and rule.right == _rule.right[0] and rule.left == _rule.left:
                        is_found = True
                        self.accepting_states.add(_rule.right[1])
                        break
                if not is_found:
                    rule.right += 'N'
                    self.grammar.non_terms.add('N')
                    self.accepting_states.add('N')

    def create_transitions(self):
        for key in self.transitions.keys():
            self.transitions[key] = {}
            for rule in self.grammar.rules:
                if key == rule.left and len(rule.right) == 2:
                    try:
                        self.transitions[key][rule.right[0]].add(rule.right[1])
                    except KeyError:
                        self.transitions[key][rule.right[0]] = {rule.right[1]}

    def determinize(self):
        new_states = {}
        for non_term in list(self.transitions):
            for term in self.transitions[non_term]:
                if len(self.transitions[non_term][term]) > 1 and non_term not in new_states:
                    new_state = "".join(self.transitions[non_term][term])
                    self.transitions[new_state] = {}
                    new_states[new_state] = ''
                    for symbol in new_state:
                        for key in self.transitions[symbol].keys():
                            try:
                                self.transitions[new_state][key] |= self.transitions[symbol][key]
                            except KeyError:
                                self.transitions[new_state][key] = set()
                                self.transitions[new_state][key] |= self.transitions[symbol][key]
        for new_state in new_states.keys():
            for symbol in string.ascii_letters:
                if symbol.upper() not in self.grammar.non_terms:
                    new_states[new_state] = symbol.upper()
                    self.grammar.non_terms.add(symbol.upper())
                    break
        for state in list(self.transitions):
            if len(state) > 1:
                self.transitions[new_states[state]] = self.transitions.pop(state)
                for symbol in state:
                    if symbol in self.accepting_states:
                        self.accepting_states.add(new_states[state])
        for state in list(self.transitions):
            for term in self.transitions[state]:
                if len(self.transitions[state][term]) > 1 and ''.join(self.transitions[state][term]) in new_states.keys():
                    self.transitions[state][term] = new_states[''.join(self.transitions[state][term])]
        for state in list(self.transitions):
            for term in self.transitions[state]:
                self.transitions[state][term] = ''.join(self.transitions[state][term])



os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'

if __name__ == '__main__':
    print('Введите терминальные символы без запятой:')
    terms = set(input())
    print('Введите нетерминальные символы без запятой:')
    non_terms = set(input())
    print('Введите правила в формате \'A->B\' через запятую')
    rules = input()
    rules = rules.split(',')
    rule_set = set()
    for rule in rules:
        parts = rule.split('->')
        left = parts[0]
        right = parts[1]
        rule_set.add(Rule(left, right))
    grammar = Grammar(terms, non_terms, rule_set)
    automata = Automata(grammar)
    automata.add_rules()
    automata.create_transitions()
    alphabet = grammar.terms
    states = grammar.non_terms
    initial_state = 'S'
    accepting_states = automata.accepting_states
    nfa = SimpleNFA(states, alphabet, initial_state, accepting_states, automata.transitions).to_graphviz().render('NFA')
    automata.determinize()
    dfa = SimpleDFA(states, alphabet, initial_state, accepting_states, automata.transitions).to_graphviz().render('DFA')
