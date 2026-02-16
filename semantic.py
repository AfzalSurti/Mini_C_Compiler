# symentic analyse check the meaning of the code, such as type check, variable check, function check, etc.
# it cretas  teh symbol table , ceheck the varible scope , and error checking 

class SemanticAnalyzer:

    def __init__(self):
        self.symbol_table={} # the symbol table is a dictionary that stores the variables and their values. It is used to keep track of the variables that have been declared and their corresponding values during the semantic analysis phase of the compiler.


    def visit(self,node): # it used to traverse the whole abstact syntax tree(ast) and check all the nodes wheather they are correct or not

        if node.__class__.__name__=="VarDec1":

            if node.name in self.symbol_table:
                raise Exception(f"variable '{node.name}' already declared")
            
            self.symbol_table[node.name]="int"
            self.visit(node.expr) # the visit method is called recursively to check the expression on the right side of the variable declaration. This allows the semantic analyzer to ensure that the expression is valid and does not contain any errors before adding the variable to the symbol table.

        elif node.__class__.__name__=="Print":
            self.visit(node.expr) # the visit method is called recursively to check the expression that is being printed. This allows the semantic analyzer to ensure that the expression is valid and does not contain any errors before allowing it to be printed.


        elif node.__class__.__name__=="BinOp":
            self.visit(node.left) # it recursively visits the left operand of the binary operation to check for any semantic errors in that part of the expression. This allows the semantic analyzer to ensure that the left operand is valid and does not contain any errors before proceeding to check the right operand.
            self.visit(node.right)

        elif node.__class__.__name__=="Variable":
            
            if node.name not in self.symbol_table:
                raise Exception(f"variable '{node.name}' not declared")
            

        elif node.__class__.__name__=="Number":
            pass # 
        
        