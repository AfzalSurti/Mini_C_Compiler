# it converts the abstarct trees into the tuples that we can use to generate the code
# so for  a int a = 5 + 3;
#print(a);
# [
#   ("BINOP", "t1", "+", 5, 3),
#   ("STORE", "a", "t1"),
#   ("PRINT", "a")
# ]

from ast_nodes import Number,StringLiteral,VarDec1,Assign,BinOp,Variable,ArrayAccess,Print

class IRGenerator:

    def __init__(self):
        self.instructions=[]# used to store the instructions generated during the IR generation phase. Each instruction is represented as a tuple that describes the operation to be performed, the operands involved, and any additional information needed for code generation.
        self.temp_count=0 # used to track of the number of temporary varibles cretae during IR geneartion phase


    def new_temp(self):
        self.temp_count+=1
        return f"t{self.temp_count}" # the new_temp method is used to generate a new temporary variable name. It increments the temp_count and returns a string in the format "t{temp_count}", which can be used as a temporary variable in the generated IR code. For example, if temp_count is 1, the method will return "t1", and if temp_count is 2, it will return "t2", and so on. This allows for the creation of unique temporary variable names during the IR generation process.
    
    def generate(self,program_ast):
        for stmt in program_ast:
            self.gen_stmt(stmt) # the generate method is used to generate IR code for a given program represented as an abstract syntax tree (AST). It iterates through each statement in the program AST and calls the gen_stmt method to generate IR code for each statement. This allows for the generation of IR code for the entire program by processing each statement in the AST sequentially.
        return self.instructions # the generate method returns the list of instructions generated during the IR generation phase. Each instruction is represented as a tuple that describes the operation to be performed, the operands involved, and any additional information needed for code generation. This list of instructions can then be used in subsequent phases of the compiler, such as optimization and code generation, to produce the final executable code.
    
    def gen_stmt(self,node):
        if isinstance(node,VarDec1): # node.__class__.__name___="VarDec1"
            if node.is_array:
                self.instructions.append(("DECL_ARRAY",node.name,node.var_type,node.array_size))
                return

            rhs=self.default_value(node.var_type) if node.expr is None else self.gen_expr(node.expr)
            self.instructions.append(("STORE",node.name,rhs))

            return

        if isinstance(node,Assign):
            rhs=self.gen_expr(node.expr)

            if isinstance(node.target,Variable):
                self.instructions.append(("STORE",node.target.name,rhs))
            elif isinstance(node.target,ArrayAccess):
                index_val=self.gen_expr(node.target.index)
                self.instructions.append(("STORE_INDEX",node.target.name,index_val,rhs))
            else:
                raise Exception(f"IR: Unknown assignment target:{type(node.target).__name__}")

            return
        
        if isinstance(node,Print):
            val=self.gen_expr(node.expr)
            self.instructions.append(("PRINT",val))
            return
        
        raise Exception(f"IR: Unknown Statement node:{type(node).__name__}")
    
    def gen_expr(self,node):
        if isinstance(node,Number):
            return node.value

        if isinstance(node,StringLiteral):
            return ("STR",node.value)
        
        if isinstance(node,Variable):
            return node.name

        if isinstance(node,ArrayAccess):
            index_val=self.gen_expr(node.index)
            temp=self.new_temp()
            self.instructions.append(("LOAD_INDEX",temp,node.name,index_val))
            return temp
        
        if isinstance(node,BinOp):
            left_val=self.gen_expr(node.left)
            right_val=self.gen_expr(node.right)

            temp=self.new_temp()
            self.instructions.append(("BINOP",temp,node.op,left_val,right_val))

            return temp
        
        raise Exception(f"IR::unknown expression node:{type(node).__name__}")

    def default_value(self,var_type):
        if var_type in ("float","double"):
            return 0.0
        if var_type=="string":
            return ("STR","")
        return 0
    
