#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import argparse
import antlr4
import json
import os
import re
import sys

from antlr4 import *
from antlr_files.InputGrammarLexer import InputGrammarLexer
from antlr_files.InputGrammarParser import InputGrammarParser
from antlr4.error.ErrorListener import ErrorListener


class CustomErrorListener(ErrorListener):
    def __init__(self, grammar_check):
        self._grammar_check = grammar_check
        super(CustomErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise ParserError('(%s, %s) %s' % (line, column, msg))


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

    def get_formatted_image_without_space(self):
        return self.get_formatted_image()[:-1]

    # image без кавычек с пробелом в конце
    def get_formatted_image(self):
        res = self._image
        if res[0] == '\'':
            res = res[1:]

        if res[-1] == '\'':
            res = res[:-1]

        return res + ' '

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

    def toJSON(self):
        if self._type == Symbol.TYPE_TERMINAL:
            return self.get_formatted_image_without_space()
        elif self._type == Symbol.TYPE_NON_TERMINAL:
            return '{0}_{1}'.format(self._image, self._version)
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

    # Возвращает True, если все элементы массива - терминалы или eps
    @staticmethod
    def all_terminals_or_epsilon(array):
        result = True
        for sym in array:
            if not (sym.is_terminal() or sym.is_epsilon()):
                result = False
                break

        return result

    # Возвращает True, если все элементы массива - терминалы
    @staticmethod
    def all_terminals(array):
        result = True
        for sym in array:
            if not (sym.is_terminal()):
                result = False
                break

        return result


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

    # complex_item
    TYPE_COMPLEX_ITEM_ITEMS = 6
    TYPE_COMPLEX_ITEM_OR = 7

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
    def __init__(self, tree, path_to_replacement):
        self._terminals = []
        self._non_terminals = []
        # создаем объект для eps, чтобы потом использовать его для всех эпсилон в грамматике
        self._eps = Symbol(Symbol.TYPE_EPSILON, Symbol.TOKEN_EPSILON)
        # для того, чтобы отсеять неиспользуемые терминалы
        self._used_terminals = {}
        # правила РБНФ
        self._rules = []
        self._bnf_rules = []
        self._tree = tree
        self._header, self._main = list(self._tree.getChildren())

        with open(path_to_replacement) as idents:
            # Словарь используемый для замены идентификаторов на заданные значения
            self._idents = json.load(idents)

        # Выделяем терминалы и нетерминалы
        self.handle_header()
        # Выделяем правила
        self.handle_main()
        # Переводим РБНФ в БНФ
        self.transform_ebnf_to_bnf()
        # Удаляем бесполезные символы
        self.delete_useless_symbols()

        to_delete = []
        for i, t in enumerate(self._terminals):
            if not self._used_terminals[str(t)]:
                to_delete.append(i)

        for i in reversed(to_delete):
            del self._terminals[i]

    def get_terminals(self):
        return self._terminals

    def get_non_terminals(self):
        return self._non_terminals

    def get_rules(self):
        return self._rules

    def get_bnf_rules(self):
        return self._bnf_rules

    # получить объект eps
    def get_epsilon(self):
        return self._eps

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
                # Заменяем нетерминалы, указанные в файле на терминалы
                if items[i].getText() in self._idents:
                    self._terminals.append(Symbol(Symbol.TYPE_TERMINAL, self._idents[items[i].getText()]))
                else:
                    self._non_terminals.append(Symbol(Symbol.TYPE_NON_TERMINAL, items[i].getText()))

        # Идем по header'у, пропуская токен "terminal" и запятые и сохраняя терминалы
        for i in range(terminal_index + 1, len(items), 2):
            # Если символ, который надо заменить и так терминал, то удаляем его из словаря
            if items[i].getText() in self._idents:
                del self._idents[items[i].getText()]
            self._terminals.append(Symbol(Symbol.TYPE_TERMINAL, items[i].getText()))

        for t in self._terminals:
            self._used_terminals[str(t)] = False

    def handle_main(self):
        rules = list(self._main.getChildren())
        for r in rules:
            items = list(r.getChildren())
            lhs = items[0]

            # Отбрасываем те нетерминалы, которые указаны в файле
            if lhs.getText() not in self._idents:
                if not self.is_terminal_non_terminal_eps(lhs.getText()):
                    raise ParserError('Symbol \'%s\' was not defined' % lhs.getText())
                else:
                    if self.is_non_terminal(lhs.getText()):
                        lhs = self.get_non_terminal(lhs.getText())
                    else:
                        raise ParserError('Symbol in the left side of a rule should be non terminal,'
                                          ' got terminal \'%s\'' % lhs.getText())

                # Отбрасываем символы ::= и ; (complex_item имеет индекс 2)
                rhs = self.handle_complex_item(items[2])

                self._rules.append(Rule(lhs, rhs))

    # Обработка нетерминала complex_item из грамматики
    def handle_complex_item(self, node):
        children = list(node.getChildren())
        node_type = self.get_complex_item_type(children)

        result = []
        if node_type == EBNFStructure.TYPE_COMPLEX_ITEM_ITEMS:
            for child in children:
                result.append(self.create_ebnf_structure(child))
        else:
            result.append(self.handle_complex_item_or_rec(children))

        return result

    # Рекурсивная обработка случая item+ (OP_OR item+)+
    def handle_complex_item_or_rec(self, children):
        indx = -1
        descendants = []

        for i in range(len(children)):
            image = children[i].getText()
            if ASTParser.is_antlr_terminal_node(children[i]) and image == '|':
                indx = i
                break

        if indx == -1:
            for child in children:
                descendants.append(self.create_ebnf_structure(child))

            # Представляем набор items+ как (items+)
            return EBNFStructure(EBNFStructure.TYPE_PARENS, descendants)
        else:
            # Слева от |
            lhs = []
            for i in range(0, indx):
                lhs.append(self.create_ebnf_structure(children[i]))

            # Представляем набор items+ как (items+)
            lhs_node = [EBNFStructure(EBNFStructure.TYPE_PARENS, lhs)]
            return EBNFStructure(EBNFStructure.TYPE_OR, lhs_node
                                 + [self.handle_complex_item_or_rec(children[indx + 1:])])

    # Получает тип complex_item: item+ или item+ (OP_OR item+)+
    def get_complex_item_type(self, children):
        alternative = False

        for child in children:
            image = child.getText()
            if ASTParser.is_antlr_terminal_node(child) and image == '|':
                alternative = True
                break

        if alternative:
            return EBNFStructure.TYPE_COMPLEX_ITEM_OR
        else:
            return EBNFStructure.TYPE_COMPLEX_ITEM_ITEMS

    # Принимает на вход узел antlr и возвращает экземпляр класса EBNFStructure
    def create_ebnf_structure(self, node):
        children = list(node.getChildren())
        node_type = self.get_item_type(node)
        descendants = []
        # IDENT+
        if node_type == EBNFStructure.TYPE_IDENTS:
            for child in children:
                image = child.getText()
                # Если нашли идентификатор из файла, то заменяем его на соответствующее значение
                if image in self._idents:
                    image = self._idents[image]

                if self.is_terminal(image):
                    term = self.get_terminal(image)
                    descendants.append(term)
                    self._used_terminals[str(term)] = True
                elif self.is_non_terminal(image):
                    non_term = self.get_non_terminal(image)
                    descendants.append(non_term)
                elif self.is_epsilon(image):
                    descendants.append(self._eps)

        # item (OP_OR item)+
        if node_type == EBNFStructure.TYPE_OR:
            # пропускаем (, |, )
            for i in range(1, len(children) - 1, 2):
                image = children[i].getText()
                # Если нашли идентификатор из файла, то заменяем его на соответствующее значение
                if image in self._idents:
                    image = self._idents[image]

                if ASTParser.is_antlr_terminal_node(children[i]):
                    if self.is_terminal(image):
                        descendants.append(self.get_terminal(image))
                    elif self.is_non_terminal(image):
                        descendants.append(self.get_non_terminal(image))
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

    # получает на вход строку и проверяет, является ли эта строка eps
    def is_epsilon(self, symbol):
        return symbol == Symbol.TOKEN_EPSILON

    # получает на вход строку и проверяет, содержится ли символ с таким образом в массиве нетерминалов или нетерминалов
    # или является
    def is_terminal_non_terminal_eps(self, symbol):
        return self.is_terminal(symbol) or self.is_non_terminal(symbol) or self.is_epsilon(symbol)

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
            image = child.getText()
            if image in self._idents:
                image = self._idents[image]

            if (ASTParser.is_antlr_terminal_node(child)
                and not self.is_terminal_non_terminal_eps(image)
                    and not Symbol.is_special_symbol(image)):
                raise ParserError('Symbol \'%s\' was not defined' % image)

            if not (ASTParser.is_antlr_terminal_node(child) and
                    self.is_terminal_non_terminal_eps(image)):
                all_terminals = False

            if ASTParser.is_antlr_terminal_node(child) and image == '|':
                alternative = True
                break

            # Не делаем break, потому что альтернатива тоже со скобками
            if ASTParser.is_antlr_terminal_node(child) and image == '(':
                parens = True

            if ASTParser.is_antlr_terminal_node(child) and image == '*':
                mul = True
                break

            if ASTParser.is_antlr_terminal_node(child) and image == '+':
                plus = True
                break

            if ASTParser.is_antlr_terminal_node(child) and image == '?':
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
                            to_append.append(Rule(new_lhs, [self._eps]))
                            to_append.append(Rule(new_lhs, element.get_children() + [new_lhs]))
                        # x -> ... y+ ... => x_0 -> ... y x_1 ...
                        # x_1 -> eps
                        # x_1 -> y x_1
                        elif element.get_type() == EBNFStructure.TYPE_PLUS:
                            new_lhs = Symbol(Symbol.TYPE_NON_TERMINAL, lhs.get_image())
                            self._non_terminals.append(new_lhs)
                            new_rule_rhs.extend(element.get_children() + [new_lhs])
                            to_append.append(Rule(new_lhs, [self._eps]))
                            to_append.append(Rule(new_lhs, element.get_children() + [new_lhs]))
                        # x -> a y? b => x_0 -> a x_1 b
                        # x_1 -> eps
                        # x_1 -> y
                        elif element.get_type() == EBNFStructure.TYPE_QUEST:
                            new_lhs = Symbol(Symbol.TYPE_NON_TERMINAL, lhs.get_image())
                            self._non_terminals.append(new_lhs)
                            new_rule_rhs.extend([new_lhs])
                            to_append.append(Rule(new_lhs, [self._eps]))
                            to_append.append(Rule(new_lhs, element.get_children()))
                        # x -> ... (a|b) ... => x_0 -> ... x_1 ...
                        # x_1 -> a
                        # x_1 -> b
                        elif element.get_type() == EBNFStructure.TYPE_OR:
                            new_lhs = Symbol(Symbol.TYPE_NON_TERMINAL, lhs.get_image())
                            self._non_terminals.append(new_lhs)
                            new_rule_rhs.append(new_lhs)
                            for chd in element.get_children():
                                to_append.append(Rule(new_lhs, [chd]))
                            # to_append.append(Rule(new_lhs, [element.get_children()[0]]))
                            # to_append.append(Rule(new_lhs, [element.get_children()[1]]))
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

    @staticmethod
    # Определяет, содержит ли множество эпсилон
    def contains_epsilon(chain):
        for item in chain:
            if item.get_type() == Symbol.TYPE_EPSILON:
                return True

        return False


class State(object):
    """
    Состояние вычислительной среды
    """

    POSITIVE_STATE = 'positive'
    NEGATIVE_INSERT_STATE = 'negative_insert'
    NEGATIVE_REPLACE_STATE = 'negative_replace'

    def __init__(self, prefix, stack, next_symbol=None, state_type=POSITIVE_STATE):
        # префикс сгенерированной цепочки
        self.prefix = prefix
        # магазин
        self.stack = stack
        # следующий входной символ (нужен, если to_open == False)
        self.next_symbol = next_symbol
        # тип состояния
        self.type = state_type
        # Является ли тест негативным
        self.negative = False
        # Для раскрытия последнего нетерминала использовалась кратчайшая цепочка
        self._inappropriate_symbols = False

        if state_type == State.NEGATIVE_INSERT_STATE or state_type == State.NEGATIVE_REPLACE_STATE:
            self.negative = True

        # Один из нетерминалов был раскрыт как eps => не можем гарантировать негативный тест
        self.epsilon_opening = False

    def get_last_symbol_from_stack(self):
        return self.stack[len(self.stack) - 1]

    def remove_last_symbol_from_stack(self):
        self.stack.pop()

    # раскрыть правило на вершине стека по таблице и терминалу
    def open_last_rule(self, table):
        last_symbol = self.get_last_symbol_from_stack()
        symbols = table[str(last_symbol)][str(self.next_symbol)]
        self.stack.pop()

        # Если в ячейке eps, то просто снимаем нетерминал со стека (и запоминаем, что раскрыли как eps)
        if len(symbols) == 1 and symbols[0].is_epsilon():
            self.last_eps = True
            self.last_non_terminal = last_symbol
        else:
            self.last_eps = False
            self.last_non_terminal = None
            self.stack.extend(reversed(list(symbols)))

    def append_symbol(self, symbol):
        self.prefix += symbol.get_formatted_image()
        last_line_len = len(self.prefix) - self.prefix.rfind('\n')
        if last_line_len > 60:
            self.prefix = self.prefix[:-1] + '\n'


class Tester(object):
    """
    Получает на вход абстрактное AST (в виде объекта класса ASTParser), строит множества FIRST и FOLLOW,
    таблицу разбора, порождает набор позитивных и негативных тестов
    """

    INCORRECT_TEST = 1
    CORRECT_TEST = 0

    def __init__(self, parser, path_to_tests):
        self._parser = parser
        self._end_symbol = Symbol(Symbol.TYPE_TERMINAL, '$')
        self._eps = parser.get_epsilon()
        self._terminals = parser.get_terminals() + [self._end_symbol]
        self._non_terminals = parser.get_non_terminals()
        self._rules = parser.get_bnf_rules()
        # Для нетерминалов
        self._FIRST = {}
        self._FOLLOW = {}
        # Множество символов, которые не могут идти за нетерминалом
        self._inappropriate_symbols = {}
        # Множество символов, которые могут идти за терминалом
        self._appropriate_symbols = {}
        # Стек состояний вычислительной среды
        self._states_stack = []
        # Стек символов
        self._symbols_stack = []
        # Текущая выходная цепочка
        self._current_sequence = ''
        # Путь к файлам тестов
        self._path_to_tests = path_to_tests + '/tests'
        # Путь к позитивным тестам
        self._path_to_positive = self._path_to_tests + '/positive'
        # Путь к негативным тестам
        self._path_to_negative = self._path_to_tests + '/negative'
        # Используется для имени файла с позитивным тестом
        self._unique_id_positive = 0
        # Используется для имени файла с негативным тестом
        self._unique_id_negative = 0
        self._negative_count = 0

        #self.prepare_tests_directory()

        self.calculate_first_for_non_terminals()
        self.calculate_follow_for_non_terminals()

        # таблица предсказывающего анализатора представляет собой словарь словарей,
        # где первый ключ нетерминал, второй - терминал
        self._table = {}
        # Используется для проверки критерия покрытия всех пар
        self._visited = {}

        #self.build_table()

        #print self.print_table();

        print self.generate_json_table()

    # Вычисляет кратчайшие цепочки для всех нетрминалов
    def calculate_shortest_sequence(self):
        # Все правые части правил содержат только терминалы
        all_terminals = False
        # Длина рассматриваемой цепочки терминалов
        length = 0
        rules = self._rules

        while not all_terminals:
            new_rules = []
            changed = False

            if length == 1:
                pass

            for rule in rules:
                lhs = rule.get_lhs()
                rhs = rule.get_rhs()
                # В правой части правила содержится только eps
                only_epsilon = length == 0 and len(rhs) == 1 and rhs[0].is_epsilon()
                # В правой части правила содержится ровно length терминалов и больше ничего
                length_k = length == len(rhs) and Symbol.all_terminals(rhs)

                if only_epsilon or length_k:
                    for other_rule in rules:
                        if other_rule != rule:
                            other_rhs = other_rule.get_rhs()
                            other_lhs = other_rule.get_lhs()
                            new_rhs = []
                            for i, symb in enumerate(other_rhs):
                                if not (symb.is_non_terminal() and str(symb) == str(lhs)):
                                    new_rhs.append(symb)
                                else:
                                    changed = True
                                    if length_k:
                                        new_rhs += rhs

                            new_rules.append(Rule(other_lhs, new_rhs))
                        else:
                            new_rules.append(rule)

                if changed:
                    rules = new_rules
                    break
                else:
                    new_rules = []
            else:
                length += 1

            all_terminals = True
            for rule in rules:
                if not Symbol.all_terminals_or_epsilon(rule.get_rhs()):
                    all_terminals = False
                    break

        for rule in rules:
            lhs = rule.get_lhs()
            rhs = rule.get_rhs()
            # Не берем правые части, состоящие только из эпсилон
            if not (len(rhs) == 1 and rhs[0].is_epsilon()):
                if str(lhs) not in self._shortest_sequences:
                    self._shortest_sequences[str(lhs)] = rhs
                elif len(rhs) < len(self._shortest_sequences[str(lhs)]):
                    self._shortest_sequences[str(lhs)] = rhs

    # Считает множество FIRST для цепочки символов u
    def calculate_first(self, u):
        # Возможно, если длина 1 и символ нетерминал, стоит возвращать все мн-во FIRST
        if len(u) == 0:
            return set()

        if self._parser.is_terminal(u[0].get_image()):
            return {u[0]}

        if self._parser.is_non_terminal(u[0].get_image()):
            first = self._FIRST[str(u[0])]

            if len(u) == 1:
                return first
            else:
                if not ASTParser.contains_epsilon(first):
                    return first
                else:
                    return (first - {self._parser.get_epsilon()}) | self.calculate_first(u[1:])
            
        if len(u) == 1 and ASTParser.contains_epsilon(u):
            return {self._parser.get_epsilon()}
        
        raise ParserError('Can\'t calculate FIRST for %s' % u)

    def calculate_first_for_non_terminals(self):
        for nt in self._non_terminals:
            self._FIRST[str(nt)] = set()

        while True:
            changed = False
            for rule in self._rules:
                old_length = len(self._FIRST[str(rule.get_lhs())])
                self._FIRST[str(rule.get_lhs())] |= self.calculate_first(rule.get_rhs())
                if len(self._FIRST[str(rule.get_lhs())]) > old_length:
                    changed = True

            if not changed:
                break

    def calculate_follow_for_non_terminals(self):
        for i, nt in enumerate(self._non_terminals):
            self._FOLLOW[str(nt)] = set()
            if i == 0:
                self._FOLLOW[str(nt)].add(self._end_symbol)

        # X -> uYv
        for r in self._rules:
            rhs = r.get_rhs()
            for i, Y in enumerate(rhs[:-1]):
                if self._parser.is_non_terminal(Y.get_image()):
                    self._FOLLOW[str(Y)] |= self.calculate_first(rhs[i + 1:]) - {self._parser.get_epsilon()}

        while True:
            changed = False

            # X -> uY or X -> uYv, FIRST(V) содержит eps
            for r in self._rules:
                X = r.get_lhs()
                rhs = r.get_rhs()
                for i, Y in enumerate(rhs[:]):
                    if self._parser.is_non_terminal(Y.get_image()):
                        old_length = len(self._FOLLOW[str(Y)])
                        if i != len(rhs[:]) - 1:
                            first = self.calculate_first(rhs[i + 1:])
                            if ASTParser.contains_epsilon(first):
                                self._FOLLOW[str(Y)] |= self._FOLLOW[str(X)]
                        else:
                            self._FOLLOW[str(Y)] |= self._FOLLOW[str(X)]

                        if len(self._FOLLOW[str(Y)]) > old_length:
                            changed = True

            if not changed:
                break

    def build_table(self):
        for nt in self._non_terminals:
            self._table[str(nt)] = {}
            self._visited[str(nt)] = {}
            for t in self._terminals:
                self._table[str(nt)][str(t)] = []
                self._visited[str(nt)][str(t)] = None
            self._visited[str(nt)][str(self._eps)] = None

        for r in self._rules:
            X = r.get_lhs()
            u = r.get_rhs()
            first = self.calculate_first(u)
            for a in first:
                if not a.is_epsilon():
                    if len(self._table[str(X)][str(a)]) > 0:
                        raise TesterError('Cell for %s %s is not empty' % (str(X), str(a)))

                    self._table[str(X)][str(a)] += u

            if ASTParser.contains_epsilon(first):
                for b in self._FOLLOW[str(X)]:
                    if len(self._table[str(X)][str(b)]) > 0:
                        raise TesterError('Cell for %s %s is not empty' % (str(X), str(b)))
                    self._table[str(X)][str(b)] += u

    def generate_json_table(self):

        info = {}

        self._json_table = {}

        info["terminals"] = list(map(lambda x: x.toJSON(), self._terminals))
        info["axiom"] = self._non_terminals[0].toJSON()

        info["first"] = {}
        info["follow"] = {}

        for nt in self._non_terminals:
            self._json_table[nt.toJSON()] = {}

            for t in self._terminals:
                self._json_table[nt.toJSON()][t.toJSON()] = None

            info["first"][nt.toJSON()] = list(map(lambda x: None if x.is_epsilon() else x.toJSON(), self._FIRST[str(nt)]))
            info["follow"][nt.toJSON()] = list(map(lambda x: None if x.is_epsilon() else x.toJSON(), self._FOLLOW[str(nt)]))

        for r in self._rules:
            X = r.get_lhs()
            u = r.get_rhs()
            first = self.calculate_first(u)

            u_without_epsilon = filter(lambda x: not x.is_epsilon(), u)
            
            for a in first:
                if not a.is_epsilon():
                    self._json_table[X.toJSON()][a.toJSON()] = list(map(lambda x: x.toJSON(), u_without_epsilon))

            if ASTParser.contains_epsilon(first):
                for b in self._FOLLOW[str(X)]:
                    self._json_table[X.toJSON()][b.toJSON()] = list(map(lambda x: x.toJSON(), u_without_epsilon))

        for nt, line in self._json_table.iteritems():
            for t, val in line.iteritems():
                if val == None:
                    self._json_table[nt][t] = None

        info["table"] = self._json_table

        return json.dumps(info)

    def print_table(self):
        for nt, line in self._table.iteritems():
            for t, val in line.iteritems():
                str_repr = ''
                if len(val) > 0:
                    for s in val:
                        str_repr += str(s) + ' '
                else:
                    str_repr = 'ERROR'

                print '(%s, %s) %s' % (nt, t, str_repr)
        

    def create_tests(self):
        self.perform_open_actions(State('', [self._end_symbol, self._non_terminals[0]]))

    # Открытое состояние
    def perform_open_actions(self, state):
        current_symb = state.get_last_symbol_from_stack()
        if current_symb.is_terminal():
            state.remove_last_symbol_from_stack()
            if current_symb != self._end_symbol:
                state.append_symbol(current_symb)
                self.perform_open_actions(state)
            else:
                self.write_to_file(not state.negative, state.prefix)
        else:
            all_visited = True

            # Эпсилоны идут в конце, чтобы получить тесты максимальной длины
            def compare_function(x, y):
                if x.is_epsilon():
                    return -1
                elif y.is_epsilon():
                    return 1
                else:
                    return cmp(x, y)

            if not state.negative:
                correct_symb = None
                for a in self._appropriate_symbols[str(current_symb)]:
                    if not a.is_epsilon():
                        correct_symb = a
                        break
                else:
                    raise TesterError('No symbols except epsilon in FIRST for %s' % str(current_symb))

                for b in self._inappropriate_symbols[str(current_symb)]:
                    if self._visited[str(current_symb)][str(b)] is None:
                        if self._negative_count == 109:
                            pass
                        self._negative_count += 1
                        self._visited[str(current_symb)][str(b)] = True
                        negative_state = State(state.prefix, state.stack[:], correct_symb,
                                               State.NEGATIVE_INSERT_STATE)
                        if b != self._end_symbol:
                            negative_state.append_symbol(b)
                            self.perform_close_actions(negative_state)
                        else:
                            self.write_to_file(not negative_state.negative, negative_state.prefix)

                for a in self._appropriate_symbols[str(current_symb)]:
                    if self._visited[str(current_symb)][str(a)] is None:
                        all_visited = False
                        self._visited[str(current_symb)][str(a)] = True
                        self.perform_close_actions(State(state.prefix, state.stack[:], a))

            if all_visited or state.negative:
                state.remove_last_symbol_from_stack()
                for sym in self._shortest_sequences[str(current_symb)]:
                    if not sym.is_epsilon():
                        state.append_symbol(sym)
                self.perform_open_actions(state)

    # Закрытое состояние
    def perform_close_actions(self, state):
        current_symb = state.get_last_symbol_from_stack()
        if current_symb.is_terminal():
            state.remove_last_symbol_from_stack()
            if current_symb != self._end_symbol:
                state.append_symbol(current_symb)
                self.perform_open_actions(state)
            else:
                self.write_to_file(not state.negative, state.prefix)
        else:
            state.open_last_rule(self._table)
            self.perform_close_actions(state)

    def get_terminal_by_image(self, image):
        for t in self._terminals:
            if t.get_formatted_image_without_space() == image:
                return t

        raise TesterError('Can\'t find terminal by image %s' % image)

    # Проверка, является ли негативный тест действительно негативным
    def validate_test(self, seq):
        stack = [self._end_symbol, self._non_terminals[0]]
        terms = [] if seq == '' else [s for l in seq.split('\n')
                                        for s in l.split(' ')
                                        if s != '']
        terms += [self._end_symbol]
        a = terms[0]
        i = 1

        if self._unique_id_negative == 108:
            pass

        while True:
            X = stack[len(stack) - 1]

            if X == self._end_symbol:
                if X == self._end_symbol and a == self._end_symbol:
                    return Tester.CORRECT_TEST
                else:
                    return Tester.INCORRECT_TEST

            if X.is_terminal():
                if X.get_formatted_image_without_space() == a:
                    stack.pop()
                    a = terms[i]
                    i += 1
                else:
                    return Tester.INCORRECT_TEST
            else:
                if a != self._end_symbol:
                    t = self.get_terminal_by_image(a)
                else:
                    t = self._end_symbol

                symbs = self._table[str(X)][str(t)]
                if len(symbs) > 0:
                    stack.pop()
                    # Просто снимаем нетерминал со стека, если в ячейке eps
                    if not (len(symbs) == 1 and symbs[0].is_epsilon()):
                        stack += reversed(symbs)
                else:
                    return Tester.INCORRECT_TEST

    def write_to_file(self, positive, info):
        if positive:
            path_to_write = self._path_to_positive + '/positive' + str(self._unique_id_positive) + '.txt'
            self._unique_id_positive += 1
        else:
            valid = self.validate_test(info) == Tester.CORRECT_TEST

            if not valid:
                path_to_write = self._path_to_negative + '/negative' + str(self._unique_id_negative) + '.txt'
                self._unique_id_negative += 1
            else:
                return

        with open(path_to_write, 'a') as output:
            output.write(info)

    # Создаем нужные папки, очищаем от старых тестов
    def prepare_tests_directory(self):
        if not os.path.exists(self._path_to_tests):
            os.makedirs(self._path_to_tests)

        if not os.path.exists(self._path_to_positive):
            os.makedirs(self._path_to_positive)

        if not os.path.exists(self._path_to_negative):
            os.makedirs(self._path_to_negative)

        Tester.remove_files_from_directory(self._path_to_positive)
        Tester.remove_files_from_directory(self._path_to_negative)

    @staticmethod
    def remove_files_from_directory(path):
        for f in os.listdir(path):
            file_path = os.path.join(path, f)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)


class ParserError(Exception):
    """Ошибки, возникающие при работе парсера"""
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return repr(self._value)


class TesterError(Exception):
    """Ошибки, возникающие при работе тестера"""
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
        default='grammars/input.txt',
        help='path to file with a grammar',
        type=str,
        metavar=''
    )

    parser.add_argument(
        '-r',
        '--replacement',
        default='../table-builder/idents.json',
        help='path to file with replacements for idents',
        type=str,
        metavar=''
    )

    parser.add_argument(
        '-t',
        '--tests',
        default='.',
        help='path where to write tests',
        type=str,
        metavar=''
    )

    parser.add_argument(
        '--grammar-check',
        default=False,
        action='store_true',
        help='perform only parsing'
    )

    args = parser.parse_args()

    lexer = InputGrammarLexer(FileStream(args.input, encoding='utf-8'))
    stream = CommonTokenStream(lexer)
    # print_tokens(stream)
    parser = InputGrammarParser(stream)
    parser._listeners = [CustomErrorListener(args.grammar_check)]

    if args.grammar_check:
        f = open(os.devnull, 'w')
        sys.stdout = f
    try:
        tree = parser.sample()
        ast_parser = ASTParser(tree, args.replacement)
    except ParserError as e:
        if args.grammar_check:
            sys.exit(1)
        else:
            raise e

    if not args.grammar_check:
        tester = Tester(ast_parser, args.tests)

if __name__ == '__main__':
    main()
