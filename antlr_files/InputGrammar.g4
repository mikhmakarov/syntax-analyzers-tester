/*
BSD License
Copyright (c) 2013, Tom Everett
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. Neither the name of Tom Everett nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

grammar InputGrammar;

sample
    : header main
    ;

header
    : KW_NT IDENT (OP_COM IDENT)* OP_SC KW_T IDENT (OP_COM IDENT)* OP_SC
    ;

main
    : grammar_rule+
    ;

grammar_rule
    : IDENT OP_EQ complex_item OP_SC
    ;

complex_item
    : item+ | item+ (OP_OR item+)+
    ;

item
    : (IDENT | EPS) | OP_LP item (OP_OR item)+ OP_RP | OP_LP item+ OP_RP | item (OP_MUL | OP_PLUS | OP_QUEST)
    ;

KW_NT
    : 'non-terminal'
    ;

KW_T
    : 'terminal'
    ;

    OP_EQ
    : '::='
    ;

OP_OR
    : '|'
    ;

OP_SC
    : ';'
    ;

OP_COM
    : ','
    ;

OP_MUL
    : '*'
    ;

OP_PLUS
    : '+'
    ;

OP_QUEST
    : '?'
    ;

OP_LP
    : '('
    ;

OP_RP
    : ')'
    ;

EPS
    : 'eps'
    ;

IDENT
   : [_a-zA-Z0-9/]+ | '\'' [?|_><\.;$%#&^=!@,{}:\[\]a-zA-Z0-9/'"()\+\-\*]+ '\''
   ;

WS
    : [ \r\n\t]+ -> skip
    ;