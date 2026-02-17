class Optimizer:
    def optimize(self,instructions):
        out=[]

        for inst in instructions:
            op=inst[0]

            if op=="BINOP":
                _,dest,operator,left,right=inst

                if isinstance(left,int) and isinstance(right,int):
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
            return a//b
        
        raise Exception(f"Unknown operator {operator}")