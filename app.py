from fastapi import FastAPI, Form
import subprocess
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome internal-testing"}

@app.post("/execute")
def execute_command(command: str = Form(...)):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return {
            "command": command,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/files")
def list_files(path: str = "."):
    """
    Another vulnerable endpoint that allows directory traversal
    """
    try:
        files = os.listdir(path)
        return {"path": path, "files": files}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
