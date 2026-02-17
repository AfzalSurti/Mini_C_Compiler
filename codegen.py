class CodeGen:
    def generate(self,instructions):
        asm=[]

        for inst in instructions:
            op=inst[0]

            if op=="STORE":
                _,name,value=inst
                asm.append(f"MOV {name}, {value}")
                continue

            if op=="BINOP":
                _,dest,operator,left,right=inst

                asm.append(f"MOV {dest}, {left}")

                if operator=='+':
                    asm.append(f"ADD {dest}, {right}")

                elif operator=='-':
                    asm.append(f"SUB {dest}, {right}")

                elif operator=='*':
                    asm.append(f"MUL {dest}, {right}")

                elif operator=='/':
                    asm.append(f"DIV {dest}, {right}")

                else :
                    raise Exception(f"Unknown operator {operator}")
                
                continue

            if op=="PRINT":
                _,value=inst
                asm.append(f"PRINT {value}")
                continue

            raise Exception(f"unknown instruction {op}")
        
        return asm

