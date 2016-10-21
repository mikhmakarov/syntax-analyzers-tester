# -*- coding: utf-8 -*-
from antlr4 import *

from InputGrammarLexer import InputGrammarLexer
from InputGrammarParser import InputGrammarParser

# Константы
TOKEN_TERMINAL = 'terminal'
SYMBOL_TYPE_TERMINAL = 0
SYMBOL_TYPE_NON_TERMINAL = 1


class Symbol(object):
    """Представляет символ входного языка"""
    def __init__(self, symbol_type, image):
        self._type = symbol_type
        self._image = image

    def get_type(self):
        return self._type

    def get_image(self):
        return self._image

    def __str__(self):
        if self._type == SYMBOL_TYPE_TERMINAL:
            return '<{0}>'.format(self._image)
        else:
            return '[{0}]'.format(self._image)


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

    def handle_header(self):
        # Описание терминалов и нетерминалов грамматики
        items = list(self._header.getChildren())
        terminal_index = 0
        # Идем по header'у, пропуская токен "non-terminal" и запятые и сохраняя нетерминалы,
        # пока не найдем токен "terminal"
        for i in range(1, len(items), 2):
            if items[i].getText() == TOKEN_TERMINAL:
                terminal_index = i
                break
            else:
                self._non_terminals.append(Symbol(SYMBOL_TYPE_NON_TERMINAL, items[i].getText()))

        # Идем по header'у, пропуская токен "terminal" и запятые и сохраняя терминалы
        for i in range(terminal_index + 1, len(items), 2):
            self._terminals.append(Symbol(SYMBOL_TYPE_TERMINAL, items[i].getText()))


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

if __name__ == '__main__':
    main()
