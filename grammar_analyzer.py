import enum


class Rule(object):
    def __init__(self, left: str, right: str):
        self.left = left
        self.right = right


class Types(enum.Enum):
    zero = 'Тип 0'
    context_sensitive = 'Контекстно-зависимая'
    context_free = 'Контекстно-свободная'
    left_regular = 'Лево-регулярная грамматика'
    right_regular = 'Право-регулярная грамматика'


class Grammar:
    def __init__(self, terms: set, non_terms: set, rules: set):
        self.terms = terms
        self.non_terms = non_terms
        self.rules = rules

    def __is_term(self, symbol):
        return symbol in self.terms

    def __is_non_term(self, symbol):
        return symbol in self.non_terms

    def __is_regular(self, rule):
        if len(rule.left) != 1:
            return False
        if not len(rule.right) in range(1, 3):
            return False
        if len(rule.right) == 1 and self.__is_non_term(rule.right[0]):
            return False
        if len(rule.right) == 2 and self.__is_non_term(rule.right[0]) and self.__is_non_term(rule.right[1]):
            return False
        if len(rule.right) == 2 and self.__is_term(rule.right[0]) and self.__is_term(rule.right[1]):
            return False

    def is_left_regular(self):
        for rule in self.rules:
            self.__is_regular(rule)
            if len(rule.right) == 2 and self.__is_term(rule.right[0]) and self.__is_non_term(rule.right[1]):
                return False
        return True

    def is_right_regular(self):
        for rule in self.rules:
            self.__is_regular(rule)
            if len(rule.right) == 2 and self.__is_non_term(rule.right[0]) and self.__is_term(rule.right[1]):
                return False
        return True

    def is_context_free(self):
        for rule in self.rules:
            if len(rule.left) != 1:
                return False
        return True

    def is_context_sensitive(self):
        for rule in self.rules:
            if len(rule.right) == 0:
                return False
        return True

    def get_type(self):
        if self.is_left_regular():
            return Types.left_regular
        if self.is_right_regular():
            return Types.right_regular
        if self.is_context_free():
            return Types.context_free
        if self.is_context_sensitive():
            return Types.context_sensitive
        return Types.zero




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
    print(grammar.get_type().value)
