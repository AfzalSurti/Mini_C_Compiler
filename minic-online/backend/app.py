from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import importlib

import compiler_pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPPORTED = {
    "language": "Mini C (educational subset)",
    "features": [
        "Data types: int, float, double, string",
        "Statements: declaration, assignment, print(expr);",
        "Arrays: T name[N], indexing name[i]",
        "Expressions: +, -, *, / with precedence",
        "Parentheses supported: ( ... )",
    ],
    "not_supported_yet": [
        "if / while",
        "functions",
        "input",
    ],
}

class RunRequest(BaseModel):
    code: str
    mode: str = "irvm"   # "irvm" or "native"

@app.get("/api/info")
def info():
    return SUPPORTED

@app.post("/api/run")
def run(req: RunRequest):
    code = req.code.strip()
    if len(code) > 10_000:
        return {"ok": False, "phase": "validation", "stderr": "Code too large."}

    modules_to_reload = [
        "ast_nodes",
        "parser",
        "semantic",
        "ir_generation",
        "optimizer",
        "llvm_codegen",
        "ir_vm",
        "compiler_pipeline",
    ]

    for module_name in modules_to_reload:
        module = __import__(module_name)
        importlib.reload(module)

    return compiler_pipeline.run_pipeline(code, mode=req.mode)