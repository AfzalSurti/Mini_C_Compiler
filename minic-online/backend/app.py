from fastapi import FastAPI
from pydantic import BaseModel

from compiler_pipeline import run_pipeline

app = FastAPI()

SUPPORTED = {
    "language": "Mini C (educational subset)",
    "features": [
        "Data type: int",
        "Statements: int declaration with initialization, print(expr);",
        "Expressions: +, -, *, / with precedence",
        "Parentheses supported: ( ... )",
    ],
    "not_supported_yet": [
        "if / while",
        "functions",
        "strings",
        "arrays",
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
    return run_pipeline(code, mode=req.mode)