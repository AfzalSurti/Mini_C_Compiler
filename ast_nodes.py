from dataclass import dataclass

@dataclass
class Number:
    value:int

@dataclass
class Variable:
    name:str

@dataclass

class BinOp: # BinOp stands for Binary Operation, which is an operation that takes two operands and applies an operator to them. For example, in the expression "5 + 3", the left operand is "5", the operator is "+", and the right operand is "3". The BinOp class is used to represent such expressions in the abstract syntax tree (AST) of the compiler.
    left:any
    op:str
    right:any

class VarDec1: # The VarDec1 class is used to represent a variable declaration in the abstract syntax tree (AST) of the compiler. It has two attributes: name, which is a string representing the name of the variable being declared, and expr, which can be any expression that represents the initial value of the variable. For example, if we have a variable declaration like "int a = 5 + 3;", the name attribute would be "a" and the expr attribute would represent the expression "5 + 3" as a BinOp node in the AST.
    name:str
    expr:any

@dataclass
class Print: # The Print class is used to represent a print statement in the abstract syntax tree (AST) of the compiler. It has a single attribute, expr, which can be any expression that we want to print. For example, if we have a print statement like "print(a + b);", the expr attribute would represent the expression "a + b" as a BinOp node in the AST.
    expr:any