# 📘 Mini C Compiler — From Source Code to CPU Execution

> A step-by-step educational compiler that transforms a small C-like language into **LLVM IR**, compiles it to native code, and runs it on the CPU.

---

## 🚀 Project Goal

This project demonstrates the **complete compiler pipeline**:

```
Mini C Source Code
        ↓
Lexical Analysis (Tokens)
        ↓
Parsing (AST Construction)
        ↓
Semantic Analysis (Validation)
        ↓
Intermediate Representation (IR)
        ↓
Optimization
        ↓
LLVM Code Generation
        ↓
Native Machine Code (clang)
        ↓
CPU Execution
```

Unlike toy compilers that stop at parsing, this project **goes all the way to real execution**.

---

## 🧠 What This Project Teaches

✔ How compilers understand source code
✔ How syntax becomes structure (AST)
✔ How semantic checks prevent errors
✔ How IR simplifies compilation
✔ How optimization improves performance
✔ How LLVM turns IR into machine code
✔ How programs actually run on a CPU

---

# 🏗️ Compiler Architecture

## 🔎 Overall Flow

```
        Source Code
             ↓
         [ LEXER ]
     Characters → Tokens
             ↓
         [ PARSER ]
       Tokens → AST
             ↓
   [ SEMANTIC ANALYZER ]
   AST + Symbol Table Checks
             ↓
       [ IR GENERATOR ]
        AST → IR (tuples)
             ↓
        [ OPTIMIZER ]
      Improve IR Efficiency
             ↓
     [ LLVM CODE GENERATOR ]
        IR → LLVM IR
             ↓
          clang (LLVM)
             ↓
      Machine Code (.exe)
             ↓
             CPU
```

---

# ⚙️ Phase 1 — Lexical Analysis (Lexer)

### Purpose

Convert raw text into **tokens**.

### Input

```c
int a = 5 + 3;
print(a);
```

### Output Tokens

```
INT  ID(a)  =  NUM(5)  +  NUM(3)  ;  PRINT ( ID(a) ) ;
```

### Why Needed?

The compiler cannot understand characters — it needs **structured units**.

### Implementation Highlights

* Recognizes keywords (`int`, `print`)
* Reads identifiers and numbers
* Tracks source position
* Emits EOF token

---

# 🌳 Phase 2 — Parsing (AST Construction)

### Purpose

Turn tokens into a **tree structure** representing program meaning.

### Example AST

```
        VarDecl(a)
            |
          BinOp(+)
          /     \
      Number(5)  BinOp(*)
                  /     \
             Number(3)  Number(2)
```

### Why Tree?

Tokens are flat. Programs are hierarchical.
The AST preserves precedence and relationships.

---

# 📐 Phase 3 — Semantic Analysis

### Purpose

Check **meaning**, not just syntax.

### What It Validates

| Check               | Example           |
| ------------------- | ----------------- |
| Undeclared variable | `print(x);` ❌     |
| Redeclaration       | `int a; int a;` ❌ |
| Valid expressions   | `a = 5 + 3;` ✔    |

### Symbol Table Example

```
Name   Type
------------
a      int
```

### Why Needed?

Parser says code is *grammatically correct*.
Semantic phase ensures it’s *logically correct*.

---

# 🔧 Phase 4 — Intermediate Representation (IR)

### Purpose

Convert AST into **simple instructions** easy to optimize.

### Example IR

```python
('BINOP', 't1', '+', 5, 3)
('STORE', 'a', 't1')
('PRINT', 'a')
```

This removes syntax complexity and creates a machine-friendly form.

---

# ⚡ Phase 5 — Optimization

### Constant Folding Example

Before:

```
t1 = 3 * 2
```

After:

```
t1 = 6
```

The compiler computes values **at compile time** to reduce runtime work.

---

# 🧬 Phase 6 — LLVM Code Generation

### Purpose

Translate IR into **LLVM IR**, an industry-grade backend language.

### Example Generated LLVM IR

```llvm
%1 = add i32 5, 3
store i32 %1, i32* %a
call i32 @printf(...)
```

LLVM then handles:

* Register allocation
* Calling conventions
* Machine code emission
* Platform targeting

---

# 💻 Phase 7 — Native Compilation (clang)

We use clang to convert LLVM IR → real machine code:

```bash
clang out.ll -o program.exe
```

Now the program runs directly on the CPU.

---

# 📂 Project Structure

```
Mini_C_Compiler/
│
├── lexer.py          # Tokenization
├── parser.py         # AST builder
├── semantic.py       # Meaning validation
├── ir_gen.py         # AST → IR
├── optimizer.py      # IR optimization
├── llvm_codegen.py   # IR → LLVM IR
├── main.py           # Driver pipeline
└── out.ll            # Generated LLVM
```

---

# ▶️ How to Run

### 1️⃣ Generate LLVM IR

```bash
python main.py
```

### 2️⃣ Compile to Native Code

First Download This - https://aka.ms/vs/17/release/vs_BuildTools.exe
After Installing it - ✔ Select Desktop development with C++.

### For windows
```bash
clang out.ll -o program.exe
```

### For Linux
```bash
clang --target=x86_64-linux-gnu out.ll -o program
```

### For ARM(Mac M1)
```bash
clang --target=arm64-apple-macos out.ll -o program
```

### 3️⃣ Execute

```bash
program.exe
```

---

# 📊 Example End-to-End Transformation

Input:

```c
int a = 5 + 3 * 2;
print(a);
```

Compiler Output Flow:

```
Tokens → AST → IR → Optimized IR → LLVM IR → Machine Code → CPU Output
```

Program Output:

```
11
```

---

# 🎯 Why This Matters (Real-World Relevance)

This is the same architecture used by modern languages:

| Language | Backend |
| -------- | ------- |
| Rust     | LLVM    |
| Swift    | LLVM    |
| Clang    | LLVM    |
| Julia    | LLVM    |

You built a **realistic compiler pipeline**, not a toy.

---

