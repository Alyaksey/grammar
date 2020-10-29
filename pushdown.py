from grammar_analyzer import Rule, Grammar, Types
from automata.pda.npda import NPDA
from automata.pda.dpda import DPDA

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
        right = right.split('|')
        for r in right:
            rule_set.add(Rule(left, r))
    grammar = Grammar(terms, non_terms, rule_set)
    if grammar.type.value[1] < Types.context_free.value[1]:
        print('Грамматика не является контекстно-свободной!')
        exit(0)
    print('Введите строку для проверки МП-автоматом:')
    s = input()
    transitions = dict()
    transitions['q'] = dict()
    transitions['q'][''] = {x: set() for x in grammar.non_terms}
    for rule in grammar.rules:
        transitions['q'][''][rule.left].add(('q', tuple(rule.right)))
    for term in grammar.terms:
        transitions['q'][term] = {term: {('q', '')}}
    npda = NPDA(
        states={'q'},
        input_symbols=grammar.terms,
        stack_symbols=list(grammar.terms | grammar.non_terms),
        transitions=transitions,
        initial_state='q',
        initial_stack_symbol='S',
        final_states={'q'},
        acceptance_mode='empty_stack'
    )
    print(npda.accepts_input(s))
    print('Введите строку для проверки расширенным МП-автоматом:')

