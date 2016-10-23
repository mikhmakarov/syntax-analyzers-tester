# Generated from java-escape by ANTLR 4.5
# encoding: utf-8
from __future__ import print_function
from antlr4 import *
from io import StringIO


def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\2")
        buf.write(u"\17\\\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write(u"\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t")
        buf.write(u"\r\4\16\t\16\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2")
        buf.write(u"\3\2\3\2\3\2\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\4")
        buf.write(u"\3\4\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t")
        buf.write(u"\3\n\3\n\3\13\3\13\3\f\3\f\3\r\6\rI\n\r\r\r\16\rJ\3\r")
        buf.write(u"\3\r\6\rO\n\r\r\r\16\rP\3\r\5\rT\n\r\3\16\6\16W\n\16")
        buf.write(u"\r\16\16\16X\3\16\3\16\2\2\17\3\3\5\4\7\5\t\6\13\7\r")
        buf.write(u"\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\3\2\5\5\2\61")
        buf.write(u"\61C\\c|\t\2$$)-//\61\61C\\^^c|\5\2\13\f\17\17\"\"_\2")
        buf.write(u"\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3")
        buf.write(u"\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2")
        buf.write(u"\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2")
        buf.write(u"\2\2\3\35\3\2\2\2\5*\3\2\2\2\7\63\3\2\2\2\t\67\3\2\2")
        buf.write(u"\2\139\3\2\2\2\r;\3\2\2\2\17=\3\2\2\2\21?\3\2\2\2\23")
        buf.write(u"A\3\2\2\2\25C\3\2\2\2\27E\3\2\2\2\31S\3\2\2\2\33V\3\2")
        buf.write(u"\2\2\35\36\7p\2\2\36\37\7q\2\2\37 \7p\2\2 !\7/\2\2!\"")
        buf.write(u"\7v\2\2\"#\7g\2\2#$\7t\2\2$%\7o\2\2%&\7k\2\2&\'\7p\2")
        buf.write(u"\2\'(\7c\2\2()\7n\2\2)\4\3\2\2\2*+\7v\2\2+,\7g\2\2,-")
        buf.write(u"\7t\2\2-.\7o\2\2./\7k\2\2/\60\7p\2\2\60\61\7c\2\2\61")
        buf.write(u"\62\7n\2\2\62\6\3\2\2\2\63\64\7<\2\2\64\65\7<\2\2\65")
        buf.write(u"\66\7?\2\2\66\b\3\2\2\2\678\7~\2\28\n\3\2\2\29:\7=\2")
        buf.write(u"\2:\f\3\2\2\2;<\7.\2\2<\16\3\2\2\2=>\7,\2\2>\20\3\2\2")
        buf.write(u"\2?@\7-\2\2@\22\3\2\2\2AB\7A\2\2B\24\3\2\2\2CD\7*\2\2")
        buf.write(u"D\26\3\2\2\2EF\7+\2\2F\30\3\2\2\2GI\t\2\2\2HG\3\2\2\2")
        buf.write(u"IJ\3\2\2\2JH\3\2\2\2JK\3\2\2\2KT\3\2\2\2LN\7)\2\2MO\t")
        buf.write(u"\3\2\2NM\3\2\2\2OP\3\2\2\2PN\3\2\2\2PQ\3\2\2\2QR\3\2")
        buf.write(u"\2\2RT\7)\2\2SH\3\2\2\2SL\3\2\2\2T\32\3\2\2\2UW\t\4\2")
        buf.write(u"\2VU\3\2\2\2WX\3\2\2\2XV\3\2\2\2XY\3\2\2\2YZ\3\2\2\2")
        buf.write(u"Z[\b\16\2\2[\34\3\2\2\2\7\2JPSX\3\b\2\2")
        return buf.getvalue()


class InputGrammarLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]


    KW_NT = 1
    KW_T = 2
    OP_EQ = 3
    OP_OR = 4
    OP_SC = 5
    OP_COM = 6
    OP_MUL = 7
    OP_PLUS = 8
    OP_QUEST = 9
    OP_LP = 10
    OP_RP = 11
    IDENT = 12
    WS = 13

    modeNames = [ u"DEFAULT_MODE" ]

    literalNames = [ u"<INVALID>",
            u"'non-terminal'", u"'terminal'", u"'::='", u"'|'", u"';'", 
            u"','", u"'*'", u"'+'", u"'?'", u"'('", u"')'" ]

    symbolicNames = [ u"<INVALID>",
            u"KW_NT", u"KW_T", u"OP_EQ", u"OP_OR", u"OP_SC", u"OP_COM", 
            u"OP_MUL", u"OP_PLUS", u"OP_QUEST", u"OP_LP", u"OP_RP", u"IDENT", 
            u"WS" ]

    ruleNames = [ u"KW_NT", u"KW_T", u"OP_EQ", u"OP_OR", u"OP_SC", u"OP_COM", 
                  u"OP_MUL", u"OP_PLUS", u"OP_QUEST", u"OP_LP", u"OP_RP", 
                  u"IDENT", u"WS" ]

    grammarFileName = u"InputGrammar.g4"

    def __init__(self, input=None):
        super(InputGrammarLexer, self).__init__(input)
        self.checkVersion("4.5")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


