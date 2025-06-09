import os
from google.genai import types

from config import MAX_CHARS

def get_file_content(working_directory: os.PathLike, file_path: os.PathLike) -> str:
    target_file: str = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_dir: str = os.path.abspath(working_directory)

    if not target_file.startswith(abs_working_dir):
        return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"
    
    if not os.path.isfile(target_file):
        return f"Error: File not found or is not a regular file: '{file_path}'"
    
    content = ""
    try:
        with open(target_file, "r") as f:
            content = f.read(MAX_CHARS)
            extra = len(f.read(1)) > 0
            if extra:
                content += f"\nFile '{file_path}' truncated at 10000 characters"
        return content
    except Exception as e:
        return f"Error: Error reading file: {e}"
    
schema_get_file_content: types.FunctionDeclaration = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
    ),
)

if __name__ == "__main__":
    print(get_file_content("calculator", "bin/cat"))
