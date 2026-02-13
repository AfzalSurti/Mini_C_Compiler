from dataclasses import dataclass
from typing import List , Optional # list and optional is used for type hinting

KEYWORDS={"int":"INT","print":"PRINT"}

SINGLE_CHAR_TOKENS={
    "(":"LPAREN",
    ")" :"RPAREN",
    "{" :"LBRACE",
    "}" :"RBRACE",
    ";" :"SEMI",
    "+" :"PLUS",
    "*" : "STAR",
    "/": "SLASH",
    "=": "EQUALS"

}

@dataclass # dataclass is used to create a class that is mainly used to store data and automatically generates special methods like __init__() and __repr__()

class Token:
    type :str
    value:Optional[str]
    pos:int

def tokenize(src: str) ->List[Token]:
    tokens: List[Token]=[]
    i=0
    n=len(src)

    while i<n:
        ch=src[i]

        if ch.isspace():
            i+=1
            continue

        if ch.isalpha(): #  .isalpha() is used to check if the character is a letter
            start=i
            i+=1
            while i<n and(src[i].isalnum() or src[i]=="_"): # .isalnum() is used to check if the character is either a letter or a digit
                i+=1

            word=src[start:i]    

            if word in KEYWORDS:
                tokens.append(Token(type=KEYWORDS[word], value=word, pos=start))
            else:
                tokens.append(Token("ID",word,start))

            continue


        if ch.isdigit():
            start=i
            i+=1
            while i<n and src[i].isdigit():
                i+=1

            num=src[start:i]
            tokens.append(Token("NUM",num,i))
            continue
        
        if ch in SINGLE_CHAR_TOKENS:
            tokens.append(Token(SINGLE_CHAR_TOKENS[ch],ch,i))
            i+=1
            continue


        raise SyntaxError(f"Unexpected character '{ch}' at position {i}")
    
    tokens.append(Token("EOF",None,n))

    return tokens