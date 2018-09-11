# Generated from java-escape by ANTLR 4.5
# encoding: utf-8
from __future__ import print_function
from antlr4 import *
from io import StringIO
package = globals().get("__package__", None)
ischild = len(package)>0 if package is not None else False
if ischild:
    from .InputGrammarListener import InputGrammarListener
else:
    from InputGrammarListener import InputGrammarListener
def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3")
        buf.write(u"\20b\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write(u"\3\2\3\2\3\2\3\3\3\3\3\3\3\3\7\3\26\n\3\f\3\16\3\31\13")
        buf.write(u"\3\3\3\3\3\3\3\3\3\3\3\7\3 \n\3\f\3\16\3#\13\3\3\3\3")
        buf.write(u"\3\3\4\6\4(\n\4\r\4\16\4)\3\5\3\5\3\5\3\5\3\5\3\6\6\6")
        buf.write(u"\62\n\6\r\6\16\6\63\3\6\3\6\6\68\n\6\r\6\16\69\7\6<\n")
        buf.write(u"\6\f\6\16\6?\13\6\3\7\3\7\3\7\3\7\3\7\3\7\6\7G\n\7\r")
        buf.write(u"\7\16\7H\6\7K\n\7\r\7\16\7L\3\7\3\7\3\7\3\7\6\7S\n\7")
        buf.write(u"\r\7\16\7T\3\7\3\7\5\7Y\n\7\3\7\3\7\7\7]\n\7\f\7\16\7")
        buf.write(u"`\13\7\3\7\2\3\f\b\2\4\6\b\n\f\2\4\3\2\16\17\3\2\t\13")
        buf.write(u"g\2\16\3\2\2\2\4\21\3\2\2\2\6\'\3\2\2\2\b+\3\2\2\2\n")
        buf.write(u"\61\3\2\2\2\fX\3\2\2\2\16\17\5\4\3\2\17\20\5\6\4\2\20")
        buf.write(u"\3\3\2\2\2\21\22\7\3\2\2\22\27\7\17\2\2\23\24\7\b\2\2")
        buf.write(u"\24\26\7\17\2\2\25\23\3\2\2\2\26\31\3\2\2\2\27\25\3\2")
        buf.write(u"\2\2\27\30\3\2\2\2\30\32\3\2\2\2\31\27\3\2\2\2\32\33")
        buf.write(u"\7\7\2\2\33\34\7\4\2\2\34!\7\17\2\2\35\36\7\b\2\2\36")
        buf.write(u" \7\17\2\2\37\35\3\2\2\2 #\3\2\2\2!\37\3\2\2\2!\"\3\2")
        buf.write(u"\2\2\"$\3\2\2\2#!\3\2\2\2$%\7\7\2\2%\5\3\2\2\2&(\5\b")
        buf.write(u"\5\2\'&\3\2\2\2()\3\2\2\2)\'\3\2\2\2)*\3\2\2\2*\7\3\2")
        buf.write(u"\2\2+,\7\17\2\2,-\7\5\2\2-.\5\n\6\2./\7\7\2\2/\t\3\2")
        buf.write(u"\2\2\60\62\5\f\7\2\61\60\3\2\2\2\62\63\3\2\2\2\63\61")
        buf.write(u"\3\2\2\2\63\64\3\2\2\2\64=\3\2\2\2\65\67\7\6\2\2\668")
        buf.write(u"\5\f\7\2\67\66\3\2\2\289\3\2\2\29\67\3\2\2\29:\3\2\2")
        buf.write(u"\2:<\3\2\2\2;\65\3\2\2\2<?\3\2\2\2=;\3\2\2\2=>\3\2\2")
        buf.write(u"\2>\13\3\2\2\2?=\3\2\2\2@A\b\7\1\2AY\t\2\2\2BC\7\f\2")
        buf.write(u"\2CJ\5\f\7\2DF\7\6\2\2EG\5\f\7\2FE\3\2\2\2GH\3\2\2\2")
        buf.write(u"HF\3\2\2\2HI\3\2\2\2IK\3\2\2\2JD\3\2\2\2KL\3\2\2\2LJ")
        buf.write(u"\3\2\2\2LM\3\2\2\2MN\3\2\2\2NO\7\r\2\2OY\3\2\2\2PR\7")
        buf.write(u"\f\2\2QS\5\f\7\2RQ\3\2\2\2ST\3\2\2\2TR\3\2\2\2TU\3\2")
        buf.write(u"\2\2UV\3\2\2\2VW\7\r\2\2WY\3\2\2\2X@\3\2\2\2XB\3\2\2")
        buf.write(u"\2XP\3\2\2\2Y^\3\2\2\2Z[\f\3\2\2[]\t\3\2\2\\Z\3\2\2\2")
        buf.write(u"]`\3\2\2\2^\\\3\2\2\2^_\3\2\2\2_\r\3\2\2\2`^\3\2\2\2")
        buf.write(u"\r\27!)\639=HLTX^")
        return buf.getvalue()


class InputGrammarParser ( Parser ):

    grammarFileName = "java-escape"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ u"<INVALID>", u"'non-terminal'", u"'terminal'", u"'::='", 
                     u"'|'", u"';'", u"','", u"'*'", u"'+'", u"'?'", u"'('", 
                     u"')'", u"'eps'" ]

    symbolicNames = [ u"<INVALID>", u"KW_NT", u"KW_T", u"OP_EQ", u"OP_OR", 
                      u"OP_SC", u"OP_COM", u"OP_MUL", u"OP_PLUS", u"OP_QUEST", 
                      u"OP_LP", u"OP_RP", u"EPS", u"IDENT", u"WS" ]

    RULE_sample = 0
    RULE_header = 1
    RULE_main = 2
    RULE_grammar_rule = 3
    RULE_complex_item = 4
    RULE_item = 5

    ruleNames =  [ u"sample", u"header", u"main", u"grammar_rule", u"complex_item", 
                   u"item" ]

    EOF = Token.EOF
    KW_NT=1
    KW_T=2
    OP_EQ=3
    OP_OR=4
    OP_SC=5
    OP_COM=6
    OP_MUL=7
    OP_PLUS=8
    OP_QUEST=9
    OP_LP=10
    OP_RP=11
    EPS=12
    IDENT=13
    WS=14

    def __init__(self, input):
        super(InputGrammarParser, self).__init__(input)
        self.checkVersion("4.5")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class SampleContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(InputGrammarParser.SampleContext, self).__init__(parent, invokingState)
            self.parser = parser

        def header(self):
            return self.getTypedRuleContext(InputGrammarParser.HeaderContext,0)


        def main(self):
            return self.getTypedRuleContext(InputGrammarParser.MainContext,0)


        def getRuleIndex(self):
            return InputGrammarParser.RULE_sample

        def enterRule(self, listener):
            if isinstance( listener, InputGrammarListener ):
                listener.enterSample(self)

        def exitRule(self, listener):
            if isinstance( listener, InputGrammarListener ):
                listener.exitSample(self)




    def sample(self):

        localctx = InputGrammarParser.SampleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_sample)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 12
            self.header()
            self.state = 13
            self.main()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class HeaderContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(InputGrammarParser.HeaderContext, self).__init__(parent, invokingState)
            self.parser = parser

        def KW_NT(self):
            return self.getToken(InputGrammarParser.KW_NT, 0)

        def IDENT(self, i=None):
            if i is None:
                return self.getTokens(InputGrammarParser.IDENT)
            else:
                return self.getToken(InputGrammarParser.IDENT, i)

        def OP_SC(self, i=None):
            if i is None:
                return self.getTokens(InputGrammarParser.OP_SC)
            else:
                return self.getToken(InputGrammarParser.OP_SC, i)

        def KW_T(self):
            return self.getToken(InputGrammarParser.KW_T, 0)

        def OP_COM(self, i=None):
            if i is None:
                return self.getTokens(InputGrammarParser.OP_COM)
            else:
                return self.getToken(InputGrammarParser.OP_COM, i)

        def getRuleIndex(self):
            return InputGrammarParser.RULE_header

        def enterRule(self, listener):
            if isinstance( listener, InputGrammarListener ):
                listener.enterHeader(self)

        def exitRule(self, listener):
            if isinstance( listener, InputGrammarListener ):
                listener.exitHeader(self)




    def header(self):

        localctx = InputGrammarParser.HeaderContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_header)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 15
            self.match(InputGrammarParser.KW_NT)
            self.state = 16
            self.match(InputGrammarParser.IDENT)
            self.state = 21
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==InputGrammarParser.OP_COM:
                self.state = 17
                self.match(InputGrammarParser.OP_COM)
                self.state = 18
                self.match(InputGrammarParser.IDENT)
                self.state = 23
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 24
            self.match(InputGrammarParser.OP_SC)
            self.state = 25
            self.match(InputGrammarParser.KW_T)
            self.state = 26
            self.match(InputGrammarParser.IDENT)
            self.state = 31
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==InputGrammarParser.OP_COM:
                self.state = 27
                self.match(InputGrammarParser.OP_COM)
                self.state = 28
                self.match(InputGrammarParser.IDENT)
                self.state = 33
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 34
            self.match(InputGrammarParser.OP_SC)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class MainContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(InputGrammarParser.MainContext, self).__init__(parent, invokingState)
            self.parser = parser

        def grammar_rule(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(InputGrammarParser.Grammar_ruleContext)
            else:
                return self.getTypedRuleContext(InputGrammarParser.Grammar_ruleContext,i)


        def getRuleIndex(self):
            return InputGrammarParser.RULE_main

        def enterRule(self, listener):
            if isinstance( listener, InputGrammarListener ):
                listener.enterMain(self)

        def exitRule(self, listener):
            if isinstance( listener, InputGrammarListener ):
                listener.exitMain(self)




    def main(self):

        localctx = InputGrammarParser.MainContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_main)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 36
                self.grammar_rule()
                self.state = 39 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==InputGrammarParser.IDENT):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Grammar_ruleContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(InputGrammarParser.Grammar_ruleContext, self).__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(InputGrammarParser.IDENT, 0)

        def OP_EQ(self):
            return self.getToken(InputGrammarParser.OP_EQ, 0)

        def complex_item(self):
            return self.getTypedRuleContext(InputGrammarParser.Complex_itemContext,0)


        def OP_SC(self):
            return self.getToken(InputGrammarParser.OP_SC, 0)

        def getRuleIndex(self):
            return InputGrammarParser.RULE_grammar_rule

        def enterRule(self, listener):
            if isinstance( listener, InputGrammarListener ):
                listener.enterGrammar_rule(self)

        def exitRule(self, listener):
            if isinstance( listener, InputGrammarListener ):
                listener.exitGrammar_rule(self)




    def grammar_rule(self):

        localctx = InputGrammarParser.Grammar_ruleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_grammar_rule)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 41
            self.match(InputGrammarParser.IDENT)
            self.state = 42
            self.match(InputGrammarParser.OP_EQ)
            self.state = 43
            self.complex_item()
            self.state = 44
            self.match(InputGrammarParser.OP_SC)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Complex_itemContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(InputGrammarParser.Complex_itemContext, self).__init__(parent, invokingState)
            self.parser = parser

        def item(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(InputGrammarParser.ItemContext)
            else:
                return self.getTypedRuleContext(InputGrammarParser.ItemContext,i)


        def OP_OR(self, i=None):
            if i is None:
                return self.getTokens(InputGrammarParser.OP_OR)
            else:
                return self.getToken(InputGrammarParser.OP_OR, i)

        def getRuleIndex(self):
            return InputGrammarParser.RULE_complex_item

        def enterRule(self, listener):
            if isinstance( listener, InputGrammarListener ):
                listener.enterComplex_item(self)

        def exitRule(self, listener):
            if isinstance( listener, InputGrammarListener ):
                listener.exitComplex_item(self)




    def complex_item(self):

        localctx = InputGrammarParser.Complex_itemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_complex_item)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 47 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 46
                self.item(0)
                self.state = 49 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << InputGrammarParser.OP_LP) | (1 << InputGrammarParser.EPS) | (1 << InputGrammarParser.IDENT))) != 0)):
                    break

            self.state = 59
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==InputGrammarParser.OP_OR:
                self.state = 51
                self.match(InputGrammarParser.OP_OR)
                self.state = 53 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 52
                    self.item(0)
                    self.state = 55 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << InputGrammarParser.OP_LP) | (1 << InputGrammarParser.EPS) | (1 << InputGrammarParser.IDENT))) != 0)):
                        break

                self.state = 61
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ItemContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(InputGrammarParser.ItemContext, self).__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(InputGrammarParser.IDENT, 0)

        def EPS(self):
            return self.getToken(InputGrammarParser.EPS, 0)

        def OP_LP(self):
            return self.getToken(InputGrammarParser.OP_LP, 0)

        def item(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(InputGrammarParser.ItemContext)
            else:
                return self.getTypedRuleContext(InputGrammarParser.ItemContext,i)


        def OP_RP(self):
            return self.getToken(InputGrammarParser.OP_RP, 0)

        def OP_OR(self, i=None):
            if i is None:
                return self.getTokens(InputGrammarParser.OP_OR)
            else:
                return self.getToken(InputGrammarParser.OP_OR, i)

        def OP_MUL(self):
            return self.getToken(InputGrammarParser.OP_MUL, 0)

        def OP_PLUS(self):
            return self.getToken(InputGrammarParser.OP_PLUS, 0)

        def OP_QUEST(self):
            return self.getToken(InputGrammarParser.OP_QUEST, 0)

        def getRuleIndex(self):
            return InputGrammarParser.RULE_item

        def enterRule(self, listener):
            if isinstance( listener, InputGrammarListener ):
                listener.enterItem(self)

        def exitRule(self, listener):
            if isinstance( listener, InputGrammarListener ):
                listener.exitItem(self)



    def item(self, _p=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = InputGrammarParser.ItemContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 10
        self.enterRecursionRule(localctx, 10, self.RULE_item, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 86
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.state = 63
                _la = self._input.LA(1)
                if not(_la==InputGrammarParser.EPS or _la==InputGrammarParser.IDENT):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()
                pass

            elif la_ == 2:
                self.state = 64
                self.match(InputGrammarParser.OP_LP)
                self.state = 65
                self.item(0)
                self.state = 72 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 66
                    self.match(InputGrammarParser.OP_OR)
                    self.state = 68 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while True:
                        self.state = 67
                        self.item(0)
                        self.state = 70 
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << InputGrammarParser.OP_LP) | (1 << InputGrammarParser.EPS) | (1 << InputGrammarParser.IDENT))) != 0)):
                            break

                    self.state = 74 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==InputGrammarParser.OP_OR):
                        break

                self.state = 76
                self.match(InputGrammarParser.OP_RP)
                pass

            elif la_ == 3:
                self.state = 78
                self.match(InputGrammarParser.OP_LP)
                self.state = 80 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 79
                    self.item(0)
                    self.state = 82 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << InputGrammarParser.OP_LP) | (1 << InputGrammarParser.EPS) | (1 << InputGrammarParser.IDENT))) != 0)):
                        break

                self.state = 84
                self.match(InputGrammarParser.OP_RP)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 92
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,10,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = InputGrammarParser.ItemContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_item)
                    self.state = 88
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 89
                    _la = self._input.LA(1)
                    if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << InputGrammarParser.OP_MUL) | (1 << InputGrammarParser.OP_PLUS) | (1 << InputGrammarParser.OP_QUEST))) != 0)):
                        self._errHandler.recoverInline(self)
                    else:
                        self.consume() 
                self.state = 94
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,10,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx



    def sempred(self, localctx, ruleIndex, predIndex):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[5] = self.item_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def item_sempred(self, localctx, predIndex):
            if predIndex == 0:
                return self.precpred(self._ctx, 1)
         



