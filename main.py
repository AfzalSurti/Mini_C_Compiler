from lexer import tokenize
from parser import Parser
from semantic import SemanticAnalyzer
from ir_generation import IRGenerator
from ir_vm import IRVM
from optimizer import Optimizer
from codegen import CodeGen

source_code = """ int a = 5 + 3 * 2;
print(a);"""

# why we erite here in """ instead of "" because we want to write multiple lines of code and using """ allows us to do that without having to use \n for new lines. It also makes the code more readable and easier to maintain.
tokens=tokenize(source_code)
for token in tokens:
    print(f"{token.type:8} {token.value!r} (pos={token.pos})") # this line is used to print the type, value and position of each token in a formatted way. The !r is used to get the string representation of the value, which is useful for debugging purposes.

parser=Parser(tokens)

ast=parser.parse()

analyzer=SemanticAnalyzer()

print(ast)

for stmt in ast:
    analyzer.visit(stmt)

print("Semantic phase is passed")

ir=IRGenerator().generate(ast)

print("IR code: ")

for instruction in ir:
    print(instruction)

opt=Optimizer()

optimized_ir=opt.optimize(ir)

print("optimized ir code:")
for instruction in optimized_ir:
    print(instruction)

cg=CodeGen()

assembly_code=cg.generate(optimized_ir)

print("assembly code:")

for line in assembly_code:
    print(line)

vm=IRVM()

vm.run(optimized_ir)