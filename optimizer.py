class Optimizer:
    def optimize(self,instructions):
        out=[]

        for inst in instructions:
            op=inst[0]

            if op=="BINOP":
                _,dest,operator,left,right=inst

                if isinstance(left,(int,float)) and isinstance(right,(int,float)):
                    result=self.eval_const(operator,left,right)
                    out.append(("STORE",dest,result))

                else:
                    out.append(inst)

            else:
                out.append(inst)


        return out
    
    def eval_const(self,operator,a,b):
        if operator =='+':
            return a+b
        
        if operator =='-':
            return a-b
        
        if operator =='*':
            return a*b
        
        if operator =='/':
            if isinstance(a,float) or isinstance(b,float):
                return a/b
            return a//b
        
        raise Exception(f"Unknown operator {operator}")