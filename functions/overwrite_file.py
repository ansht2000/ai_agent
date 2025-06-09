import os
from google.genai import types

def overwrite_file(working_directory: os.PathLike, file_path: os.PathLike, content: str) -> str:
    target_file: str = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_dir: str = os.path.abspath(working_directory)

    if not target_file.startswith(abs_working_dir):
        return f"Error: Cannot write to '{file_path}' as it is outside the permitted working directory"
    
    try:
        if not os.path.exists(target_file):
            target_file_dir: str = "/".join(target_file.split("/")[0:-1])
            os.makedirs(name=target_file_dir, exist_ok=True)

        if os.path.exists(target_file) and os.path.isdir(target_file):
            return f"Error: '{file_path}' is a directory, not a file"

        with open(target_file, "w") as f:
            num_w: int = f.write(content)
            if num_w != len(content):
                return f"Error: Not all characters written to file: {file_path}"
        return f"Successfully wrote to '{file_path}' ({len(content)} bytes written)"
    except Exception as e:
        return f"Error: Error writing to file: {e}"

schema_overwrite_file: types.FunctionDeclaration = types.FunctionDeclaration(
    name="overwrite_file",
    description="""
        Overwrite a file specified by a file path with new content,
        if the file does not exist, create a new file with the specified content,
        constrained to the working directory
    """,
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to overwrite or create, relative to the working directory"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write the file"
            ),
        },
    ),
)

if __name__ == "__main__":
    print(overwrite_file("calculator", "/tmp/temp.txt", "this should not be allowed"))