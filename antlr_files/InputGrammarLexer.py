# Generated from java-escape by ANTLR 4.5
# encoding: utf-8
from __future__ import print_function
from antlr4 import *
from io import StringIO


def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\2")
        buf.write(u"\20b\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write(u"\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t")
        buf.write(u"\r\4\16\t\16\4\17\t\17\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3")
        buf.write(u"\2\3\2\3\2\3\2\3\2\3\2\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3")
        buf.write(u"\3\3\3\3\4\3\4\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3")
        buf.write(u"\b\3\t\3\t\3\n\3\n\3\13\3\13\3\f\3\f\3\r\3\r\3\r\3\r")
        buf.write(u"\3\16\6\16O\n\16\r\16\16\16P\3\16\3\16\6\16U\n\16\r\16")
        buf.write(u"\16\16V\3\16\5\16Z\n\16\3\17\6\17]\n\17\r\17\16\17^\3")
        buf.write(u"\17\3\17\2\2\20\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23")
        buf.write(u"\13\25\f\27\r\31\16\33\17\35\20\3\2\5\6\2\61\61\63;C")
        buf.write(u"\\c|\n\2$$)-//\61\61\63;C\\^^c|\5\2\13\f\17\17\"\"e\2")
        buf.write(u"\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3")
        buf.write(u"\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2")
        buf.write(u"\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2")
        buf.write(u"\2\2\2\35\3\2\2\2\3\37\3\2\2\2\5,\3\2\2\2\7\65\3\2\2")
        buf.write(u"\2\t9\3\2\2\2\13;\3\2\2\2\r=\3\2\2\2\17?\3\2\2\2\21A")
        buf.write(u"\3\2\2\2\23C\3\2\2\2\25E\3\2\2\2\27G\3\2\2\2\31I\3\2")
        buf.write(u"\2\2\33Y\3\2\2\2\35\\\3\2\2\2\37 \7p\2\2 !\7q\2\2!\"")
        buf.write(u"\7p\2\2\"#\7/\2\2#$\7v\2\2$%\7g\2\2%&\7t\2\2&\'\7o\2")
        buf.write(u"\2\'(\7k\2\2()\7p\2\2)*\7c\2\2*+\7n\2\2+\4\3\2\2\2,-")
        buf.write(u"\7v\2\2-.\7g\2\2./\7t\2\2/\60\7o\2\2\60\61\7k\2\2\61")
        buf.write(u"\62\7p\2\2\62\63\7c\2\2\63\64\7n\2\2\64\6\3\2\2\2\65")
        buf.write(u"\66\7<\2\2\66\67\7<\2\2\678\7?\2\28\b\3\2\2\29:\7~\2")
        buf.write(u"\2:\n\3\2\2\2;<\7=\2\2<\f\3\2\2\2=>\7.\2\2>\16\3\2\2")
        buf.write(u"\2?@\7,\2\2@\20\3\2\2\2AB\7-\2\2B\22\3\2\2\2CD\7A\2\2")
        buf.write(u"D\24\3\2\2\2EF\7*\2\2F\26\3\2\2\2GH\7+\2\2H\30\3\2\2")
        buf.write(u"\2IJ\7g\2\2JK\7r\2\2KL\7u\2\2L\32\3\2\2\2MO\t\2\2\2N")
        buf.write(u"M\3\2\2\2OP\3\2\2\2PN\3\2\2\2PQ\3\2\2\2QZ\3\2\2\2RT\7")
        buf.write(u")\2\2SU\t\3\2\2TS\3\2\2\2UV\3\2\2\2VT\3\2\2\2VW\3\2\2")
        buf.write(u"\2WX\3\2\2\2XZ\7)\2\2YN\3\2\2\2YR\3\2\2\2Z\34\3\2\2\2")
        buf.write(u"[]\t\4\2\2\\[\3\2\2\2]^\3\2\2\2^\\\3\2\2\2^_\3\2\2\2")
        buf.write(u"_`\3\2\2\2`a\b\17\2\2a\36\3\2\2\2\7\2PVY^\3\b\2\2")
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
    EPS = 12
    IDENT = 13
    WS = 14

    modeNames = [ u"DEFAULT_MODE" ]

    literalNames = [ u"<INVALID>",
            u"'non-terminal'", u"'terminal'", u"'::='", u"'|'", u"';'", 
            u"','", u"'*'", u"'+'", u"'?'", u"'('", u"')'", u"'eps'" ]

    symbolicNames = [ u"<INVALID>",
            u"KW_NT", u"KW_T", u"OP_EQ", u"OP_OR", u"OP_SC", u"OP_COM", 
            u"OP_MUL", u"OP_PLUS", u"OP_QUEST", u"OP_LP", u"OP_RP", u"EPS", 
            u"IDENT", u"WS" ]

    ruleNames = [ u"KW_NT", u"KW_T", u"OP_EQ", u"OP_OR", u"OP_SC", u"OP_COM", 
                  u"OP_MUL", u"OP_PLUS", u"OP_QUEST", u"OP_LP", u"OP_RP", 
                  u"EPS", u"IDENT", u"WS" ]

    grammarFileName = u"InputGrammar.g4"

    def __init__(self, input=None):
        super(InputGrammarLexer, self).__init__(input)
        self.checkVersion("4.5")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


