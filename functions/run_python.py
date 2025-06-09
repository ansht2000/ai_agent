import os
import subprocess
from google.genai import types

def run_python_file(working_directory: os.PathLike, file_path: os.PathLike) -> str:
    target_file: str = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_dir: str = os.path.abspath(working_directory)
    
    if not target_file.startswith(abs_working_dir):
        return f"Error: Cannot execute '{file_path}' as it is outside the permitted working directory"
    
    if not os.path.exists(target_file):
        return f"Error: File '{file_path}' not found."
    
    if target_file.split("/")[-1].split(".")[-1] != "py":
        return f"Error: '{file_path}' is not a python file."
    
    try:
        process: subprocess.CompletedProcess = subprocess.run(args=["python3", target_file],
                                                              capture_output=True,
                                                              timeout=30,
                                                              cwd=abs_working_dir,
                                                              text=True)
        stdout: str = process.stdout if len(process.stdout) > 0 else "No output"
        stderr: str = process.stderr if len(process.stderr) > 0 else "No output"
        return_code: int = process.returncode
        if len(stdout) and len(stderr) == 0:
            return "No output produced."
        content = f"STDOUT: {stdout}\nSTDERR: {stderr}\n"
        if return_code != 0:
            content += f"Process exited with code {return_code}"
        return content
    except Exception as e:
        return f"Error: Error executing python file: {e}"
    
schema_run_python_file: types.FunctionDeclaration = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a python file specified by its path, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the python file to run, relative to the working directory"
            ),
        },
    ),
)

if __name__ == "__main__":
    print(run_python_file("calculator", "tests.py"))