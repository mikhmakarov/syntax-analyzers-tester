# Generated from java-escape by ANTLR 4.5
# encoding: utf-8
from __future__ import print_function
from antlr4 import *
from io import StringIO


def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\2")
        buf.write(u"\17X\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write(u"\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t")
        buf.write(u"\r\4\16\t\16\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2")
        buf.write(u"\3\2\3\2\3\2\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\4")
        buf.write(u"\3\4\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t")
        buf.write(u"\3\n\3\n\3\13\3\13\3\f\3\f\3\r\6\rI\n\r\r\r\16\rJ\3\r")
        buf.write(u"\3\r\3\r\5\rP\n\r\3\16\6\16S\n\16\r\16\16\16T\3\16\3")
        buf.write(u"\16\2\2\17\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25")
        buf.write(u"\f\27\r\31\16\33\17\3\2\5\5\2\61\61C\\c|\t\2$$)-//\61")
        buf.write(u"\61C\\^^c|\5\2\13\f\17\17\"\"Z\2\3\3\2\2\2\2\5\3\2\2")
        buf.write(u"\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2")
        buf.write(u"\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2")
        buf.write(u"\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\3\35\3\2\2\2\5")
        buf.write(u"*\3\2\2\2\7\63\3\2\2\2\t\67\3\2\2\2\139\3\2\2\2\r;\3")
        buf.write(u"\2\2\2\17=\3\2\2\2\21?\3\2\2\2\23A\3\2\2\2\25C\3\2\2")
        buf.write(u"\2\27E\3\2\2\2\31O\3\2\2\2\33R\3\2\2\2\35\36\7p\2\2\36")
        buf.write(u"\37\7q\2\2\37 \7p\2\2 !\7/\2\2!\"\7v\2\2\"#\7g\2\2#$")
        buf.write(u"\7t\2\2$%\7o\2\2%&\7k\2\2&\'\7p\2\2\'(\7c\2\2()\7n\2")
        buf.write(u"\2)\4\3\2\2\2*+\7v\2\2+,\7g\2\2,-\7t\2\2-.\7o\2\2./\7")
        buf.write(u"k\2\2/\60\7p\2\2\60\61\7c\2\2\61\62\7n\2\2\62\6\3\2\2")
        buf.write(u"\2\63\64\7<\2\2\64\65\7<\2\2\65\66\7?\2\2\66\b\3\2\2")
        buf.write(u"\2\678\7~\2\28\n\3\2\2\29:\7=\2\2:\f\3\2\2\2;<\7.\2\2")
        buf.write(u"<\16\3\2\2\2=>\7,\2\2>\20\3\2\2\2?@\7-\2\2@\22\3\2\2")
        buf.write(u"\2AB\7A\2\2B\24\3\2\2\2CD\7*\2\2D\26\3\2\2\2EF\7+\2\2")
        buf.write(u"F\30\3\2\2\2GI\t\2\2\2HG\3\2\2\2IJ\3\2\2\2JH\3\2\2\2")
        buf.write(u"JK\3\2\2\2KP\3\2\2\2LM\7)\2\2MN\t\3\2\2NP\7)\2\2OH\3")
        buf.write(u"\2\2\2OL\3\2\2\2P\32\3\2\2\2QS\t\4\2\2RQ\3\2\2\2ST\3")
        buf.write(u"\2\2\2TR\3\2\2\2TU\3\2\2\2UV\3\2\2\2VW\b\16\2\2W\34\3")
        buf.write(u"\2\2\2\6\2JOT\3\b\2\2")
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


