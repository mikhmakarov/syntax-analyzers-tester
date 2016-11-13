# -*- coding: utf-8 -*-
import argparse
import antlr4
from antlr4 import *

from antlr_files.InputGrammarLexer import InputGrammarLexer
from antlr_files.InputGrammarParser import InputGrammarParser


class Symbol(object):
    """Представляет символ входного языка"""

    TOKEN_TERMINAL = 'terminal'
    TOKEN_EPSILON = 'eps'

    TYPE_TERMINAL = 0
    TYPE_NON_TERMINAL = 1
    TYPE_SPECIAL_SYMBOL = 2
    TYPE_EPSILON = 3
    TYPES = [TYPE_TERMINAL, TYPE_NON_TERMINAL, TYPE_SPECIAL_SYMBOL, TYPE_EPSILON]

    SPECIAL_SYMBOLS = ['*', '+', '?', '|', '(', ')']

    # Отображение символа на его версию
    versions_mapping = {}

    def __init__(self, symbol_type, image):
        if symbol_type not in Symbol.TYPES:
            raise ParserError('Incorrect symbol type \'%s\'' % symbol_type)

        self._type = symbol_type
        self._image = image

        if self._type == Symbol.TYPE_NON_TERMINAL:
            if self._image not in Symbol.versions_mapping:
                Symbol.versions_mapping[self._image] = 0
            else:
                Symbol.versions_mapping[self._image] += 1

            self._version = Symbol.versions_mapping[self._image]

    def get_type(self):
        return self._type

    def get_image(self):
        return self._image

    def is_terminal(self):
        return self._type == Symbol.TYPE_TERMINAL

    def is_non_terminal(self):
        return self._type == Symbol.TYPE_NON_TERMINAL

    def is_epsilon(self):
        return self._type == Symbol.TYPE_EPSILON

    def __str__(self):
        if self._type == Symbol.TYPE_TERMINAL:
            return '<{0}>'.format(self._image)
        elif self._type == Symbol.TYPE_NON_TERMINAL:
            return '[{0}_{1}]'.format(self._image, self._version)
        elif self._type == Symbol.TYPE_EPSILON:
            return self._image

    def __eq__(self, other):
        return str(self) == str(other)

    def __cmp__(self, other):
        if str(self) > str(other):
            return 1
        elif str(self) < str(other):
            return -1
        else:
            return 0

    # Получает на вход строку и возвращает True, если символ является "специальным"
    @staticmethod
    def is_special_symbol(symbol):
        return symbol in Symbol.SPECIAL_SYMBOLS


class EBNFStructure(object):
    """
    Представляет структуру РБНФ (*, +, ?, |, ())
    Имеет ссылки на дочерние структуры или символы
    """

    # item OP_MUL
    TYPE_MUL = 0
    # item OP_PLUS
    TYPE_PLUS = 1
    # item OP_QUEST
    TYPE_QUEST = 2
    # item (OP_OR item)+
    TYPE_OR = 3
    # OP_LP item+ OP_RP
    TYPE_PARENS = 4
    # IDENTS+
    TYPE_IDENTS = 5
    TYPES = [TYPE_MUL, TYPE_PLUS, TYPE_QUEST, TYPE_OR, TYPE_PARENS, TYPE_IDENTS]

    def __init__(self, structure_type, children):
        if structure_type not in EBNFStructure.TYPES:
            raise ParserError('Incorrect ESBNF structure type \'%s\'' % structure_type)

        self._type = structure_type
        self._children = children

    def get_children(self):
        return self._children

    def get_type(self):
        return self._type

    def __str__(self):
        result = ''
        for child in self._children:
            if self._type == EBNFStructure.TYPE_OR:
                result += child.__str__() + '|'
            else:
                result += child.__str__()

        if self._type == EBNFStructure.TYPE_MUL:
            return result + '*'

        if self._type == EBNFStructure.TYPE_PLUS:
            return result + '+'

        if self._type == EBNFStructure.TYPE_QUEST:
            return result + '?'

        if self._type == EBNFStructure.TYPE_OR and len(self._children) > 0:
                result = result[:-1]

        if self._type == EBNFStructure.TYPE_PARENS:
            return '(' + result + ')'

        return result


class Rule(object):
    """Представляет правило входного языка"""
    def __init__(self, lhs, rhs):
        # lhs - символ в левой части правила
        self._lhs = lhs
        # rhs - массив деревьев, каждое из которых является деревом РБНФ
        self._rhs = rhs

    def get_rhs(self):
        return self._rhs

    def get_lhs(self):
        return self._lhs

    # Возвращает True, если все символы из правой части являются терминалами или epsilon
    def all_rhs_symbols_terminals_or_eps(self):
        result = True

        for item in self._rhs:
            if not isinstance(item, Symbol):
                result = False
                break
            else:
                if not (item.is_terminal() or item.is_epsilon()):
                    result = False
                    break

        return result

    # Возвращает set из всех нетерминалов, входящих в правую часть (на первом уровне вложенности)
    def get_all_rhs_non_terminals(self):
        s = set()

        for item in self._rhs:
            if isinstance(item, Symbol) and item.is_non_terminal():
                s.add(item)

        return s

    # Возвращает True, если правило содержит nt в левой или правой части, иначе False
    def contains_non_terminal(self, nt):
        result = False

        if nt == self._lhs:
            result = True
        else:
            for item in self._rhs:
                if isinstance(item, Symbol) and item.is_non_terminal() and nt == item:
                    result = True

        return result

    def __str__(self):
        string = str(self._lhs) + ' ::= '

        for symbol in self._rhs:
            string += str(symbol)

        return string


class ASTParser(object):
    """Выделяет терминалы, нетерминалы, правила из входной грамматики"""
    def __init__(self, tree):
        self._terminals = []
        self._non_terminals = []
        # правила РБНФ
        self._rules = []
        self._bnf_rules = []
        self._tree = tree
        self._header, self._main = list(self._tree.getChildren())
        # Выделяем терминалы и нетерминалы
        self.handle_header()
        # Выделяем правила
        self.handle_main()
        # Переводим РБНФ в БНФ
        self.transform_ebnf_to_bnf()
        # Удаляем бесполезные символы
        # self.delete_useless_symbols()

    def get_terminals(self):
        return self._terminals

    def get_non_terminals(self):
        return self._non_terminals

    def get_rules(self):
        return self._rules

    def get_bnf_rules(self):
        return self._bnf_rules

    def handle_header(self):
        # Описание терминалов и нетерминалов грамматики
        items = list(self._header.getChildren())
        terminal_index = 0
        # Идем по header'у, пропуская токен "non-terminal" и запятые и сохраняя нетерминалы,
        # пока не найдем токен "terminal"
        for i in range(1, len(items), 2):
            if items[i].getText() == Symbol.TOKEN_TERMINAL:
                terminal_index = i
                break
            else:
                self._non_terminals.append(Symbol(Symbol.TYPE_NON_TERMINAL, items[i].getText()))

        # Идем по header'у, пропуская токен "terminal" и запятые и сохраняя терминалы
        for i in range(terminal_index + 1, len(items), 2):
            self._terminals.append(Symbol(Symbol.TYPE_TERMINAL, items[i].getText()))

    def handle_main(self):
        rules = list(self._main.getChildren())
        for r in rules:
            items = list(r.getChildren())
            lhs = items[0]
            if not self.is_terminal_or_non_terminal(lhs.getText()):
                raise ParserError('Symbol \'%s\' was not defined' % lhs.getText())
            else:
                if self.is_non_terminal(lhs.getText()):
                    lhs = self.get_non_terminal(lhs.getText())
                else:
                    raise ParserError('Symbol in the left side of a rule should be non terminal, got terminal \'%s\''
                                      % lhs.getText())

            rhs = []
            # Отбрасываем символы ::= и ;
            for symbol in items[2:-1]:
                rhs.append(self.create_ebnf_structure(symbol))

            self._rules.append(Rule(lhs, rhs))

    # Принимает на вход узел antlr и возвращает экземпляр класса EBNFStructure
    def create_ebnf_structure(self, node):
        children = list(node.getChildren())
        node_type = self.get_item_type(node)
        descendants = []
        # IDENT+
        if node_type == EBNFStructure.TYPE_IDENTS:
            for child in children:
                if self.is_terminal(child.getText()):
                    descendants.append(self.get_terminal(child.getText()))
                elif self.is_non_terminal(child.getText()):
                    descendants.append(self.get_non_terminal(child.getText()))

        # item (OP_OR item)+
        if node_type == EBNFStructure.TYPE_OR:
            # пропускаем |
            for i in range(0, len(children), 2):
                if ASTParser.is_antlr_terminal_node(children[i]):
                    if self.is_terminal(children[i].getText()):
                        descendants.append(self.get_terminal(children[i].getText()))
                    elif self.is_non_terminal(children[i].getText()):
                        descendants.append(self.get_non_terminal(children[i].getText()))
                else:
                    descendants.append(self.create_ebnf_structure(children[i]))

        # item (OP_MUL | OP_PLUS | OP_QUEST)
        if node_type == EBNFStructure.TYPE_MUL or node_type == EBNFStructure.TYPE_PLUS \
                or node_type == EBNFStructure.TYPE_QUEST:
            # пропускаем * (или +, или ?)
            for i in range(0, len(children) - 1):
                descendants.append(self.create_ebnf_structure(children[i]))

        # OP_LP item+ OP_RP
        if node_type == EBNFStructure.TYPE_PARENS:
            # пропускаем ( и )
            for i in range(1, len(children) - 1):
                descendants.append(self.create_ebnf_structure(children[i]))

        return EBNFStructure(node_type, descendants)

    # получает на вход строку и проверяет, содержится ли символ с таким образом в массиве терминалов
    def is_terminal(self, symbol):
        for term in self._terminals:
            if term.get_image() == symbol:
                return True

        return False

    # получает на вход строку и проверяет, содержится ли символ с таким образом в массиве нетерминалов
    def is_non_terminal(self, symbol):
        for non_term in self._non_terminals:
            if non_term.get_image() == symbol:
                return True

        return False

    # получает на вход строку и проверяет, содержится ли символ с таким образом в массиве нетерминалов или нетерминалов
    def is_terminal_or_non_terminal(self, symbol):
        return self.is_terminal(symbol) or self.is_non_terminal(symbol)

    # На вход "образ" терминала, выдает терминал с данным образом или None
    def get_terminal(self, image):
        for terminal in self._terminals:
            if terminal.get_image() == image:
                return terminal

        return None

    # На вход "образ" нетерминала, выдает нетерминал с данным образом или None
    def get_non_terminal(self, image):
        for non_terminal in self._non_terminals:
            if non_terminal.get_image() == image:
                return non_terminal

        return None

    # На вход узел AST antlr, представляющий нетерминал item, на выходе - тип нетерминала
    def get_item_type(self, item):
        children = list(item.getChildren())
        # IDENT+
        all_terminals = True
        # item (OP_OR item)+
        alternative = False
        # OP_LP item+ OP_RP
        parens = False
        # item OP_MUL
        mul = False
        # item OP_PLUS
        plus = False
        # item OP_QUEST
        quest = False

        for child in children:

            if (ASTParser.is_antlr_terminal_node(child)
                and not self.is_terminal_or_non_terminal(child.getText())
                    and not Symbol.is_special_symbol(child.getText())):
                raise ParserError('Symbol \'%s\' was not defined' % child.getText())

            if not (ASTParser.is_antlr_terminal_node(child) and
                    self.is_terminal_or_non_terminal(child.getText())):
                all_terminals = False

            if ASTParser.is_antlr_terminal_node(child) and child.getText() == '|':
                alternative = True
                break

            if ASTParser.is_antlr_terminal_node(child) and child.getText() == '(':
                parens = True
                break

            if ASTParser.is_antlr_terminal_node(child) and child.getText() == '*':
                mul = True
                break

            if ASTParser.is_antlr_terminal_node(child) and child.getText() == '+':
                plus = True
                break

            if ASTParser.is_antlr_terminal_node(child) and child.getText() == '?':
                quest = True
                break

        if all_terminals:
            return EBNFStructure.TYPE_IDENTS
        elif alternative:
            return EBNFStructure.TYPE_OR
        elif parens:
            return EBNFStructure.TYPE_PARENS
        elif mul:
            return EBNFStructure.TYPE_MUL
        elif plus:
            return EBNFStructure.TYPE_PLUS
        elif quest:
            return EBNFStructure.TYPE_QUEST
        else:
            raise ParserError('WRONG EBNF TYPE FOR %s' % (item.getText()))

    # Этот метод изменяет список нетерминалов и правил
    def transform_ebnf_to_bnf(self):
        self._bnf_rules = list(self._rules)
        while True:
            # Список индексов правил, которые должныть быть удалены (т.к. они изменились)
            to_delete = []
            to_append = []
            for i, rule in enumerate(self._bnf_rules):
                changed = False
                new_rule_rhs = []
                lhs = rule.get_lhs()
                for element in rule.get_rhs():
                    if isinstance(element, EBNFStructure):
                        if element.get_type() == EBNFStructure.TYPE_IDENTS:
                            for ident in element.get_children():
                                new_rule_rhs.append(ident)
                        # x -> ... y* ... => x_0 -> ... x_1 ...
                        # x_1 -> eps
                        # x_1 -> y x_1
                        elif element.get_type() == EBNFStructure.TYPE_MUL:
                            new_lhs = Symbol(Symbol.TYPE_NON_TERMINAL, lhs.get_image())
                            self._non_terminals.append(new_lhs)
                            new_rule_rhs.append(new_lhs)
                            to_append.append(Rule(new_lhs, [Symbol(Symbol.TYPE_EPSILON, Symbol.TOKEN_EPSILON)]))
                            to_append.append(Rule(new_lhs, element.get_children() + [new_lhs]))
                        # x -> ... y+ ... => x_0 -> ... y x_1 ...
                        # x_1 -> eps
                        # x_1 -> y x_1
                        elif element.get_type() == EBNFStructure.TYPE_PLUS:
                            new_lhs = Symbol(Symbol.TYPE_NON_TERMINAL, lhs.get_image())
                            self._non_terminals.append(new_lhs)
                            new_rule_rhs.extend(element.get_children() + [new_lhs])
                            to_append.append(Rule(new_lhs, [Symbol(Symbol.TYPE_EPSILON, Symbol.TOKEN_EPSILON)]))
                            to_append.append(Rule(new_lhs, element.get_children() + [new_lhs]))
                        # x -> a y? b => x_0 -> a x_1 b
                        # x_1 -> eps
                        # x_1 -> y
                        elif element.get_type() == EBNFStructure.TYPE_QUEST:
                            new_lhs = Symbol(Symbol.TYPE_NON_TERMINAL, lhs.get_image())
                            self._non_terminals.append(new_lhs)
                            new_rule_rhs.extend([new_lhs])
                            to_append.append(Rule(new_lhs, [Symbol(Symbol.TYPE_EPSILON, Symbol.TOKEN_EPSILON)]))
                            to_append.append(Rule(new_lhs, element.get_children()))
                        # x -> ... (a|b) ... => x_0 -> ... x_1 ...
                        # x_1 -> a
                        # x_1 -> b
                        elif element.get_type() == EBNFStructure.TYPE_OR:
                            new_lhs = Symbol(Symbol.TYPE_NON_TERMINAL, lhs.get_image())
                            self._non_terminals.append(new_lhs)
                            new_rule_rhs.append(new_lhs)
                            to_append.append(Rule(new_lhs, [element.get_children()[0]]))
                            to_append.append(Rule(new_lhs, [element.get_children()[1]]))
                        # Удаляем скобки
                        elif element.get_type() == EBNFStructure.TYPE_PARENS:
                            new_rule_rhs.extend(element.get_children())

                        changed = True
                    # element - Symbol
                    else:
                        new_rule_rhs.append(element)

                if changed:
                    to_delete.append(i)
                    to_append.append(Rule(lhs, new_rule_rhs))

            if len(to_delete) == 0:
                break

            for i in sorted(to_delete, reverse=True):
                del self._bnf_rules[i]

            for r in to_append:
                self._bnf_rules.append(r)

            self._bnf_rules.sort(key=lambda x: x.get_lhs())

    # Удаление бесполезных символов из грамматики
    # 1. Удалить из грамматики правила, содержащие непорождающие нетерминалы.
    # 2. Удалить из грамматики правила, содержащие недостижимые нетерминалы.
    def delete_useless_symbols(self):
        all_non_terminals = set(self._non_terminals)
        # Нетерминалы, которые  являются левыми частями правил, у которых в правых частях стоят только терминалы
        # или epsilon'ы
        generating_non_terminals = set(
            map(lambda x: x.get_lhs(), filter(lambda r: r.all_rhs_symbols_terminals_or_eps(), self._bnf_rules))
        )
        current_length = len(generating_non_terminals)

        while True:
            for r in self._bnf_rules:
                # Если найдено такое правило, что все нетерминалы, стоящие в его правой части, уже входят в множество,
                # то добавить в множество нетерминалы, стоящие в его левой части.
                if generating_non_terminals.issuperset(r.get_all_rhs_non_terminals()):
                    generating_non_terminals.add(r.get_lhs())

            if current_length < len(generating_non_terminals):
                current_length = len(generating_non_terminals)
            else:
                break

        # Непорождающие нетерминалы
        non_generating = all_non_terminals - generating_non_terminals
        # Индексы нетерминалов, которые нужно удалить
        non_terminals_to_delete = []
        # Индексы правил, которые нужно удалить
        rules_to_delete = []

        for i, nt in enumerate(self._non_terminals):
            if nt in non_generating:
                non_terminals_to_delete.append(i)

        for nt in non_generating:
            print 'WARNING: symbol %s is useless' % nt
            for i, r in enumerate(self._bnf_rules):
                if r.contains_non_terminal(nt):
                    if i not in rules_to_delete:
                        rules_to_delete.append(i)

        rules_to_delete.sort()

        for i in reversed(non_terminals_to_delete):
            del self._non_terminals[i]

        for i in reversed(rules_to_delete):
            del self._bnf_rules[i]

        all_non_terminals = set(self._non_terminals)
        reachable = {self._non_terminals[0]}
        current_length = len(reachable)

        while True:
            # Если найдено правило, в левой части которого стоит нетерминал, содержащийся в множестве,
            # добавить в множество все нетерминалы из правой части.
            for r in self._bnf_rules:
                if r.get_lhs() in reachable:
                    reachable = reachable | r.get_all_rhs_non_terminals()

            if current_length < len(reachable):
                current_length = len(reachable)
            else:
                break

        # Непорождающие нетерминалы
        non_reachable = all_non_terminals - reachable
        # Индексы нетерминалов, которые нужно удалить
        non_terminals_to_delete = []
        # Индексы правил, которые нужно удалить
        rules_to_delete = []

        for i, nt in enumerate(self._non_terminals):
            if nt in non_reachable:
                non_terminals_to_delete.append(i)

        for nt in non_reachable:
            print 'WARNING: symbol %s is useless' % nt
            for i, r in enumerate(self._bnf_rules):
                if r.contains_non_terminal(nt):
                    if i not in rules_to_delete:
                        rules_to_delete.append(i)

        rules_to_delete.sort()

        for i in reversed(non_terminals_to_delete):
            del self._non_terminals[i]

        for i in reversed(rules_to_delete):
            del self._bnf_rules[i]

    # Распечатать терминалы, нетерминалы и правила
    def print_abstract_ast(self):
        if len(self._terminals) > 0:
            terminals = reduce(lambda x, y: x + ' ' + y, [str(t) for t in self._terminals])
        else:
            terminals = ''

        if len(self._non_terminals) > 0:
            non_terminals = reduce(lambda x, y: x + ' ' + y, [str(nt) for nt in self._non_terminals])
        else:
            non_terminals = ''

        if len(self._rules):
            rules = reduce(lambda x, y: x + '\n' + y, [str(r) for r in self._rules])
        else:
            rules = ''

        if len(self._bnf_rules):
            bnf_rules = reduce(lambda x, y: x + '\n' + y, [str(r) for r in self._bnf_rules])
        else:
            bnf_rules = ''

        print 'terminals: ' + terminals
        print 'non-terminals: ' + non_terminals
        print 'rules:\n' + rules
        print 'bnf rules:\n' + bnf_rules

    # Получает на вход узел AST antlr, возвращает True, если узел - терминал
    @staticmethod
    def is_antlr_terminal_node(node):
        return isinstance(node, antlr4.tree.Tree.TerminalNode)


class Tester(object):
    """
    Получает на вход абстрактное AST (в виде объекта класса ASTParser), строит множества FIRST и FOLLOW,
    таблицу разбора, порождает набор позитивных и негативных тестов
    """
    def __init__(self, parser):
        self._parser = parser
        self._terminals = parser.get_terminals()
        self._non_terminals = parser.get_non_terminals()
        self._rules = parser.get_bnf_rules()


class ParserError(Exception):
    """Ошибки, возникающие при работе парсера"""
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return repr(self._value)


def print_tokens(stream):
    stream.fill()
    for token in stream.tokens:
        print token


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '-i',
        '--input',
        default='input.txt',
        help='path to file with a grammar',
        type=str,
        metavar=''
    )

    args = parser.parse_args()

    lexer = InputGrammarLexer(FileStream(args.input, encoding='utf-8'))
    stream = CommonTokenStream(lexer)
    parser = InputGrammarParser(stream)
    tree = parser.sample()
    ast_parser = ASTParser(tree)
    tester = Tester(ast_parser)
    ast_parser.print_abstract_ast()

if __name__ == '__main__':
    main()
