from ast_nodes import *

class Parser:
    def __init__(self,tokens):# the __init__ method is used to initialize the Parser class with a list of tokens. It sets the tokens and initializes the position to 0.
        self.tokens=tokens
        self.pos=0

    def current(self): # the current method is used to get the current token that the parser is looking at. It returns the token at the current position in the list of tokens.
        return self.tokens[self.pos]
    
    def eat(self,token_type): # the eat method is used to consume a token of a specific type. It checks if the current token matches the expected token type, and if it does, it advances the position to the next token. If the current token does not match the expected token type, it raises a SyntaxError.
        token=self.current() # the current token is stored in the variable token for further processing.
        if token.type !=token_type:
            raise Exception(f"expected {token_type},got{token.type}")
        self.pos+=1
        return token
    
    def parse_factor(self): # the parse_factor method is used to parse a factor in the expression. A factor can be a number, a variable, or an expression enclosed in parentheses. The method checks the type of the current token and returns the appropriate AST node based on the token type.
        token=self.current()
        
        if token.type=="NUM":
            self.eat("NUM")
            return Number(int(token.value))

        if token.type=="ID":
            self.eat("ID")
            return Variable(token.value)
        
        if token.type=="LPAREN":
            self.eat("LPAREN")
            node=self.parse_expr()
            self.eaat("RPAREN")
            return node

        
        raise Exception(f"Invalid factor: {token.type}")

    def parse_term(self):
        left=self.parse_factor()

        while self.current().type in ("STAR","SLASH"):
            op=self.current()
            if op.type=="STAR":
                self.eat("STAR")
            else:
                self.eat("SLASH")

            right=self.parse_factor()
            left=BinOp(left,op.value,right)
        return left

    def parse_expr(self):
        left=self.parse_term()
        

        while self.current().type in ("PLUS","MINUS"):
            op=self.current()
            if op.type=="PLUS":
                self.eat("PLUS")
            else:
                self.eat("MINUS")

            right=self.parse_term()
            left=BinOp(left,op.value,right) # the left variable is updated to a new BinOp node that represents the addition operation. The left operand of the BinOp node is the previously parsed left expression, the operator is the value of the PLUS token, and the right operand is the newly parsed right expression. This allows for chaining multiple addition operations
            # here we do the left recursion

        return left
    
    def parse_statement(self):

        if self.current().type =="INT": 
            self.eat("INT") # the eat method is called to consume the INT token, which indicates the start of a variable declaration statement.
            name=self.eat("ID").value # the eat method is called again to consume the ID token, which represents the name of the variable being declared. The value of the ID token is stored in the name variable for later use in creating a VarDec1 node in the abstract syntax tree (AST).
            self.eat("EQUALS")
            expr=self.parse_expr()
            self.eat("SEMI")
            return VarDec1(name,expr)
        

        elif self.current().type == "PRINT":
            self.eat("PRINT")
            self.eat("LPAREN")
            expr=self.parse_expr()
            self.eat("RPAREN")
            self.eat("SEMI")
            return Print(expr)
        else:
            raise Exception("Invalid statement")
        
    def parse(self):
        statements=[]

        while self.current().type!="EOF": # what is a EOF token? EOF stands for End Of File. It is a special token that is used to indicate the end of the input source code. When the parser encounters an EOF token, it knows that it has reached the end of the input and can stop parsing. In this implementation, we assume that an EOF token is added to the list of tokens after all the source code has been tokenized.
            statements.append(self.parse_statement()) # the parse method is used to parse the entire input source code and generate a list of statements in the abstract syntax tree (AST). It repeatedly calls the parse_statement method until it encounters an EOF token, which indicates that it has reached the end of the input. Each parsed statement is appended to the statements list, which is returned at the end of the parsing process.

        return statements