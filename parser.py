# -*- coding: utf-8 -*-
import antlr4
from antlr4 import *

from antlr_files.InputGrammarLexer import InputGrammarLexer
from antlr_files.InputGrammarParser import InputGrammarParser


class Symbol(object):
    """Представляет символ входного языка"""

    TOKEN_TERMINAL = 'terminal'

    TYPE_TERMINAL = 0
    TYPE_NON_TERMINAL = 1
    TYPE_SPECIAL_SYMBOL = 2
    TYPES = [TYPE_TERMINAL, TYPE_NON_TERMINAL, TYPE_SPECIAL_SYMBOL]

    SPECIAL_SYMBOLS = ['*', '+', '?', '|', '(', ')']

    def __init__(self, symbol_type, image):
        if symbol_type not in Symbol.TYPES:
            raise ParserError('Incorrect symbol type \'%s\'' % symbol_type)

        self._type = symbol_type
        self._image = image

    def get_type(self):
        return self._type

    def get_image(self):
        return self._image

    def __str__(self):
        if self._type == Symbol.TYPE_TERMINAL:
            return '<{0}>'.format(self._image)
        else:
            return '[{0}]'.format(self._image)

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
        # rhs - массив деревьев, каждое из которых является деревом РБНФ или символом
        self._rhs = rhs

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
        self._rules = []
        self._tree = tree
        self._header, self._main = list(self._tree.getChildren())
        # Выделяем терминалы и нетерминалы
        self.handle_header()
        # Выделяем правила
        self.handle_main()

    def get_terminals(self):
        return self._terminals

    def get_non_terminals(self):
        return self._non_terminals

    def get_rules(self):
        return self._rules

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
                    lhs = Symbol(Symbol.TYPE_NON_TERMINAL, lhs.getText())
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
                    descendants.append(Symbol(Symbol.TYPE_TERMINAL, child.getText()))
                elif self.is_non_terminal(child.getText()):
                    descendants.append(Symbol(Symbol.TYPE_NON_TERMINAL, child.getText()))

        # item (OP_OR item)+
        if node_type == EBNFStructure.TYPE_OR:
            # пропускаем |
            for i in range(0, len(children), 2):
                if ASTParser.is_antlr_terminal_node(children[i]):
                    if self.is_terminal(children[i].getText()):
                        descendants.append(Symbol(Symbol.TYPE_TERMINAL, children[i].getText()))
                    elif self.is_non_terminal(children[i].getText()):
                        descendants.append(Symbol(Symbol.TYPE_NON_TERMINAL, children[i].getText()))
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

    # Распечатать терминалы, нетерминалы и правила
    def print_abstract_ast(self):
        terminals = reduce(lambda x, y: x + ' ' + y, [str(t) for t in self._terminals])
        non_terminals = reduce(lambda x, y: x + ' ' + y, [str(nt) for nt in self._non_terminals])
        rules = reduce(lambda x, y: x + '\n' + y, [str(r) for r in self._rules])

        print 'terminals: ' + terminals
        print 'non-terminals: ' + non_terminals
        print 'rules:\n' + rules

    # Получает на вход узел AST antlr, возвращает True, если узел - терминал
    @staticmethod
    def is_antlr_terminal_node(node):
        return isinstance(node, antlr4.tree.Tree.TerminalNode)


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
    lexer = InputGrammarLexer(FileStream('input.txt', encoding='utf-8'))
    stream = CommonTokenStream(lexer)
    parser = InputGrammarParser(stream)
    tree = parser.sample()
    ast_parser = ASTParser(tree)
    ast_parser.print_abstract_ast()

if __name__ == '__main__':
    main()
