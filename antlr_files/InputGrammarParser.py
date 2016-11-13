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
        buf.write(u"\20Q\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\3\2\3\2")
        buf.write(u"\3\2\3\3\3\3\3\3\3\3\7\3\24\n\3\f\3\16\3\27\13\3\3\3")
        buf.write(u"\3\3\3\3\3\3\3\3\7\3\36\n\3\f\3\16\3!\13\3\3\3\3\3\3")
        buf.write(u"\4\6\4&\n\4\r\4\16\4\'\3\5\3\5\3\5\6\5-\n\5\r\5\16\5")
        buf.write(u".\3\5\3\5\3\6\3\6\6\6\65\n\6\r\6\16\6\66\3\6\3\6\6\6")
        buf.write(u";\n\6\r\6\16\6<\3\6\3\6\5\6A\n\6\3\6\3\6\3\6\6\6F\n\6")
        buf.write(u"\r\6\16\6G\3\6\3\6\7\6L\n\6\f\6\16\6O\13\6\3\6\2\3\n")
        buf.write(u"\7\2\4\6\b\n\2\3\3\2\t\13U\2\f\3\2\2\2\4\17\3\2\2\2\6")
        buf.write(u"%\3\2\2\2\b)\3\2\2\2\n@\3\2\2\2\f\r\5\4\3\2\r\16\5\6")
        buf.write(u"\4\2\16\3\3\2\2\2\17\20\7\3\2\2\20\25\7\17\2\2\21\22")
        buf.write(u"\7\b\2\2\22\24\7\17\2\2\23\21\3\2\2\2\24\27\3\2\2\2\25")
        buf.write(u"\23\3\2\2\2\25\26\3\2\2\2\26\30\3\2\2\2\27\25\3\2\2\2")
        buf.write(u"\30\31\7\7\2\2\31\32\7\4\2\2\32\37\7\17\2\2\33\34\7\b")
        buf.write(u"\2\2\34\36\7\17\2\2\35\33\3\2\2\2\36!\3\2\2\2\37\35\3")
        buf.write(u"\2\2\2\37 \3\2\2\2 \"\3\2\2\2!\37\3\2\2\2\"#\7\7\2\2")
        buf.write(u"#\5\3\2\2\2$&\5\b\5\2%$\3\2\2\2&\'\3\2\2\2\'%\3\2\2\2")
        buf.write(u"\'(\3\2\2\2(\7\3\2\2\2)*\7\17\2\2*,\7\5\2\2+-\5\n\6\2")
        buf.write(u",+\3\2\2\2-.\3\2\2\2.,\3\2\2\2./\3\2\2\2/\60\3\2\2\2")
        buf.write(u"\60\61\7\7\2\2\61\t\3\2\2\2\62\64\b\6\1\2\63\65\7\17")
        buf.write(u"\2\2\64\63\3\2\2\2\65\66\3\2\2\2\66\64\3\2\2\2\66\67")
        buf.write(u"\3\2\2\2\67A\3\2\2\28:\7\f\2\29;\5\n\6\2:9\3\2\2\2;<")
        buf.write(u"\3\2\2\2<:\3\2\2\2<=\3\2\2\2=>\3\2\2\2>?\7\r\2\2?A\3")
        buf.write(u"\2\2\2@\62\3\2\2\2@8\3\2\2\2AM\3\2\2\2BE\f\5\2\2CD\7")
        buf.write(u"\6\2\2DF\5\n\6\2EC\3\2\2\2FG\3\2\2\2GE\3\2\2\2GH\3\2")
        buf.write(u"\2\2HL\3\2\2\2IJ\f\3\2\2JL\t\2\2\2KB\3\2\2\2KI\3\2\2")
        buf.write(u"\2LO\3\2\2\2MK\3\2\2\2MN\3\2\2\2N\13\3\2\2\2OM\3\2\2")
        buf.write(u"\2\f\25\37\'.\66<@GKM")
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
    RULE_item = 4

    ruleNames =  [ u"sample", u"header", u"main", u"grammar_rule", u"item" ]

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
            self.state = 10
            self.header()
            self.state = 11
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
            self.state = 13
            self.match(InputGrammarParser.KW_NT)
            self.state = 14
            self.match(InputGrammarParser.IDENT)
            self.state = 19
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==InputGrammarParser.OP_COM:
                self.state = 15
                self.match(InputGrammarParser.OP_COM)
                self.state = 16
                self.match(InputGrammarParser.IDENT)
                self.state = 21
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 22
            self.match(InputGrammarParser.OP_SC)
            self.state = 23
            self.match(InputGrammarParser.KW_T)
            self.state = 24
            self.match(InputGrammarParser.IDENT)
            self.state = 29
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==InputGrammarParser.OP_COM:
                self.state = 25
                self.match(InputGrammarParser.OP_COM)
                self.state = 26
                self.match(InputGrammarParser.IDENT)
                self.state = 31
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 32
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
            self.state = 35 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 34
                self.grammar_rule()
                self.state = 37 
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

        def OP_SC(self):
            return self.getToken(InputGrammarParser.OP_SC, 0)

        def item(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(InputGrammarParser.ItemContext)
            else:
                return self.getTypedRuleContext(InputGrammarParser.ItemContext,i)


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
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 39
            self.match(InputGrammarParser.IDENT)
            self.state = 40
            self.match(InputGrammarParser.OP_EQ)
            self.state = 42 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 41
                self.item(0)
                self.state = 44 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==InputGrammarParser.OP_LP or _la==InputGrammarParser.IDENT):
                    break

            self.state = 46
            self.match(InputGrammarParser.OP_SC)
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

        def IDENT(self, i=None):
            if i is None:
                return self.getTokens(InputGrammarParser.IDENT)
            else:
                return self.getToken(InputGrammarParser.IDENT, i)

        def OP_LP(self):
            return self.getToken(InputGrammarParser.OP_LP, 0)

        def OP_RP(self):
            return self.getToken(InputGrammarParser.OP_RP, 0)

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
        _startState = 8
        self.enterRecursionRule(localctx, 8, self.RULE_item, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 62
            token = self._input.LA(1)
            if token in [InputGrammarParser.IDENT]:
                self.state = 50 
                self._errHandler.sync(self)
                _alt = 1
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 49
                        self.match(InputGrammarParser.IDENT)

                    else:
                        raise NoViableAltException(self)
                    self.state = 52 
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,4,self._ctx)


            elif token in [InputGrammarParser.OP_LP]:
                self.state = 54
                self.match(InputGrammarParser.OP_LP)
                self.state = 56 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 55
                    self.item(0)
                    self.state = 58 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==InputGrammarParser.OP_LP or _la==InputGrammarParser.IDENT):
                        break

                self.state = 60
                self.match(InputGrammarParser.OP_RP)

            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 75
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,9,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 73
                    la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
                    if la_ == 1:
                        localctx = InputGrammarParser.ItemContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_item)
                        self.state = 64
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 67 
                        self._errHandler.sync(self)
                        _alt = 1
                        while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                            if _alt == 1:
                                self.state = 65
                                self.match(InputGrammarParser.OP_OR)
                                self.state = 66
                                self.item(0)

                            else:
                                raise NoViableAltException(self)
                            self.state = 69 
                            self._errHandler.sync(self)
                            _alt = self._interp.adaptivePredict(self._input,7,self._ctx)

                        pass

                    elif la_ == 2:
                        localctx = InputGrammarParser.ItemContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_item)
                        self.state = 71
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 72
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << InputGrammarParser.OP_MUL) | (1 << InputGrammarParser.OP_PLUS) | (1 << InputGrammarParser.OP_QUEST))) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self.consume()
                        pass

             
                self.state = 77
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,9,self._ctx)

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
        self._predicates[4] = self.item_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def item_sempred(self, localctx, predIndex):
            if predIndex == 0:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 1)
         



