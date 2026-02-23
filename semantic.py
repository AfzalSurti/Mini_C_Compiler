# symentic analyse check the meaning of the code, such as type check, variable check, function check, etc.
# it cretas  teh symbol table , ceheck the varible scope , and error checking 

from ast_nodes import Number,StringLiteral,Variable,ArrayAccess,BinOp,VarDec1,Assign,Print

NUMERIC_TYPES={"int","float","double"}

class SemanticAnalyzer:

    def __init__(self):
        self.symbol_table={} # the symbol table is a dictionary that stores the variables and their values. It is used to keep track of the variables that have been declared and their corresponding values during the semantic analysis phase of the compiler.
        self.used_types=set()

    def _error(self,message,pos):
        raise Exception(f"Semantic error at pos {pos}: {message}")

    def _declare(self,name,var_type,is_array,size,pos):
        if name in self.symbol_table:
            self._error(f"variable '{name}' already declared",pos)

        if is_array:
            if size is None or size <= 0:
                self._error(f"array '{name}' must have positive size",pos)

        self.symbol_table[name]={
            "type": var_type,
            "is_array": is_array,
            "size": size,
        }

    def _get_symbol(self,name,pos):
        if name not in self.symbol_table:
            self._error(f"variable '{name}' not declared",pos)
        return self.symbol_table[name]

    def _is_assignable(self,target_type,value_type):
        if target_type==value_type:
            return True

        if target_type in ("float","double") and value_type in NUMERIC_TYPES:
            return True

        if target_type=="double" and value_type=="float":
            return True

        return False

    def _numeric_result(self,left_type,right_type,pos):
        if left_type not in NUMERIC_TYPES or right_type not in NUMERIC_TYPES:
            self._error("binary operator requires numeric operands",pos)

        if "double" in (left_type,right_type):
            return "double"
        if "float" in (left_type,right_type):
            return "float"
        return "int"

    def get_expr_type(self,node):
        if isinstance(node,Number):
            self.used_types.add(node.value_type)
            return node.value_type

        if isinstance(node,StringLiteral):
            self.used_types.add("string")
            return "string"

        if isinstance(node,Variable):
            sym=self._get_symbol(node.name,node.pos)
            if sym["is_array"]:
                self._error(f"array '{node.name}' used without index",node.pos)
            self.used_types.add(sym["type"])
            return sym["type"]

        if isinstance(node,ArrayAccess):
            sym=self._get_symbol(node.name,node.pos)
            if not sym["is_array"]:
                self._error(f"variable '{node.name}' is not an array",node.pos)

            index_type=self.get_expr_type(node.index)
            if index_type != "int":
                self._error("array index must be int",node.pos)

            self.used_types.add(sym["type"])
            return sym["type"]

        if isinstance(node,BinOp):
            left_type=self.get_expr_type(node.left)
            right_type=self.get_expr_type(node.right)
            result_type=self._numeric_result(left_type,right_type,node.pos)
            self.used_types.add(result_type)
            return result_type

        self._error(f"unknown expression {type(node).__name__}",getattr(node,"pos",0))

    def visit(self,node): # it used to traverse the whole abstact syntax tree(ast) and check all the nodes wheather they are correct or not

        if isinstance(node,VarDec1):
            self._declare(node.name,node.var_type,node.is_array,node.array_size,node.pos)

            if node.expr is not None:
                expr_type=self.get_expr_type(node.expr) # the visit method is called recursively to check the expression on the right side of the variable declaration. This allows the semantic analyzer to ensure that the expression is valid and does not contain any errors before adding the variable to the symbol table.
                if not self._is_assignable(node.var_type,expr_type):
                    self._error(f"cannot assign {expr_type} to {node.var_type}",node.pos)

        elif isinstance(node,Assign):
            if isinstance(node.target,Variable):
                sym=self._get_symbol(node.target.name,node.target.pos)
                if sym["is_array"]:
                    self._error(f"array '{node.target.name}' must be indexed",node.target.pos)
                target_type=sym["type"]
            elif isinstance(node.target,ArrayAccess):
                sym=self._get_symbol(node.target.name,node.target.pos)
                if not sym["is_array"]:
                    self._error(f"variable '{node.target.name}' is not an array",node.target.pos)
                index_type=self.get_expr_type(node.target.index)
                if index_type != "int":
                    self._error("array index must be int",node.target.pos)
                target_type=sym["type"]
            else:
                self._error("invalid assignment target",node.pos)

            expr_type=self.get_expr_type(node.expr)
            if not self._is_assignable(target_type,expr_type):
                self._error(f"cannot assign {expr_type} to {target_type}",node.pos)

        elif isinstance(node,Print):
            self.get_expr_type(node.expr) # the visit method is called recursively to check the expression that is being printed. This allows the semantic analyzer to ensure that the expression is valid and does not contain any errors before allowing it to be printed.

        elif isinstance(node,BinOp):
            self.get_expr_type(node)

        elif isinstance(node,(Variable,ArrayAccess,Number,StringLiteral)):
            self.get_expr_type(node)

        else:
            self._error(f"unknown statement {type(node).__name__}",getattr(node,"pos",0))

