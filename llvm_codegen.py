class LLVMCodeGen:
    def __init__(self):
        self.lines=[] # list to store the generated LLVM IR code lines
        self.reg=0 # register counter to generate unique register names

        self.var_ptr={} # dictionary to map variable names to their corresponding LLVM IR register names

        self.temp_val={} # dictionary to map temporary variable names to their corresponding LLVM IR register names


    def new_reg(self):
        self.reg+=1
        return f"%{self.reg}" # the new_reg method is used to generate a new register name in LLVM IR. It increments the reg counter and returns a string in the format "%{reg}", which can be used as a register name in the generated LLVM IR code. For example, if reg is 1, the method will return "%1", and if reg is 2, it will return "%2", and so on. This allows for the creation of unique register names during the code generation process.

    def llvm_val(self,x): # the llvm_val method is used to convert a value into its corresponding LLVM IR representation. It checks the type of the value and handles it accordingly. If the value is an integer, it simply returns the string representation of the integer. If the value is a string, it checks if it is a temporary variable name (starting with "t") or a regular variable name. For temporary variable names, it looks up the corresponding LLVM IR register name in the temp_val dictionary. For regular variable names, it looks up the corresponding LLVM IR register name in the var_ptr dictionary and generates a load instruction to retrieve the value from memory. If the variable name is not found in either dictionary, it raises an exception indicating that the variable is used before its definition.
        if isinstance(x,int):
            return str(x) # the llvm_val method is used to convert a value into its corresponding LLVM IR representation. If the value is an integer, it simply returns the string representation of the integer. This allows for the direct use of integer literals in the generated LLVM IR code.
        
        if isinstance(x,str):

            if x.startswith("t"):
                if x not in self.temp_val:
                    raise Exception(f"LLVM: temp '{x}' used before definition")
                
                return self.temp_val[x]
            
            if x not in self.var_ptr:
                raise Exception(f"LLVM: variable '{x}' used before definition")
            
            r=self.new_reg()
            self.lines.append(f"{r}=load i32,i32*{self.var_ptr[x]}") 
            return r
        
        raise Exception(f"LLVM: unsupported value {x} of type {type(x)}")
    
    def header(self):
        self.lines.append('; --- MiniC LLVM IR ---')
        self.lines.append('declare i32 @printf(i8*,...)') # the header method is used to add a declaration for the printf function in the generated LLVM IR code. It appends the string 'declare i32 @printf(i8*,...)' to the lines list, which declares the printf function as an external function that takes a format string (i8*) and a variable number of arguments (...). This allows the generated LLVM IR code to use the printf function for output, which is commonly used in C programs for printing to the console. By declaring it in the header, we ensure that the generated code can call printf without any issues during linking or execution.
        self.lines.append('@.fmt = private unnamed_addr constant [4 x i8] c"%d\\0A\\00"')
        self.lines.append('') # the header method adds an empty line to the generated LLVM IR code for better readability and separation between the header declarations and the main function definition. This helps to visually distinguish the different sections of the generated code, making it easier to read and understand.
        self.lines.append('define i32 @main(){') # the header method is used to add the function definition for the main function in the generated LLVM IR code. It appends the string 'define i32 @main(){' to the lines list, which defines a function named main that returns an integer (i32). This serves as the entry point for the generated code, as the main function is typically where the execution of a C program begins. By defining it in the header, we ensure that the generated LLVM IR code has a proper structure and can be executed correctly when compiled and linked.
        self.lines.append('entry:')


    def footer(self):
        self.lines.append('  ret i32 0') # the footer method is used to add a return statement to the generated LLVM IR code. It appends the string '  ret i32 0' to the lines list, which indicates that the main function should return an integer value of 0. This is a common convention in C programs, where returning 0 from the main function typically indicates successful execution. By including this return statement in the footer, we ensure that the generated LLVM IR code has a proper exit point and can be executed without any issues.
        self.lines.append('}')

    def ensure_var(self,name):
        if name not in self.var_ptr:
            ptr=f"%{name}" 
            self.var_ptr[name]=ptr
            self.lines.append(f"  {ptr}=alloca i32") # the ensure_var method is used to ensure that a variable is allocated in memory and has a corresponding LLVM IR register name. If the variable name is not already present in the var_ptr dictionary, it generates a new register name (ptr) for the variable and adds an entry to the var_ptr dictionary mapping the variable name to the register name. It then appends an allocation instruction to the lines list, which allocates memory for the variable on the stack. This ensures that the variable can be used in subsequent instructions and that its value can be stored and retrieved correctly during code generation.


    def generate(self,ir):
        self.header()

        for inst in ir:
            op=inst[0]

            if op=="STORE":
                _,name,value=inst

                if isinstance(name,str) and  name.startswith("t"):
                    v=self.llvm_val(value)
                    self.temp_val[name]=v
                    continue

                self.ensure_var(name)# the ensure_var method is called to ensure that the variable being stored has a corresponding memory allocation in the generated LLVM IR code. This is necessary because variables need to be allocated in memory before they can be used in LLVM IR instructions. By calling ensure_var, we ensure that the variable is properly set up for storage and can be accessed correctly in subsequent instructions.
                v=self.llvm_val(value)
                self.lines.append(f"store i32 {v}, i32* {self.var_ptr[name]}") # the generate method is used to generate LLVM IR code for a given list of IR instructions. When it encounters a STORE instruction, it first ensures that the variable being stored has a corresponding memory allocation by calling the ensure_var method. Then, it retrieves the LLVM IR representation of the value being stored using the llvm_val method. Finally, it appends a store instruction to the lines list, which stores the value into the allocated memory location for the variable. This allows for proper handling of variable storage in the generated LLVM IR code.
                continue

            if op=="BINOP":
                _,dest,operator,left,right=inst
                l=self.llvm_val(left)
                r=self.llvm_val(right)

                out=self.new_reg()

                if operator=='+':
                    self.lines.append(f"{out}=add i32 {l},{r}")

                elif operator =='-':
                    self.lines.append(f"{out}=sub i32 {l},{r}")

                elif operator=='*':
                    self.lines.append(f"{out}=mul i32 {l},{r}")

                elif operator=='/':
                    self.lines.append(f"{out}=sdiv i32 {l},{r}")

                else:
                    raise Exception(f"LLVM:unknown operator {operator}")

                self.temp_val[dest]=out
                continue


            if op=="PRINT":
                _,value=inst
                v=self.llvm_val(value)
                r=self.new_reg()
                self.lines.append(
                    f"  {r} = call i32 (i8*, ...) @printf("
                    f"i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.fmt, i32 0, i32 0), "
                    f"i32 {v})"
                )
                continue

            raise Exception(f"LLVM: unknown instruction {op}   ")
        
        self.footer()
        return "\n".join(self.lines)
