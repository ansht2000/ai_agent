import os
from google.genai import types

def get_files_info(working_directory: os.PathLike, directory: os.PathLike = None) -> str:
    target_dir: str = os.path.abspath(working_directory)
    abs_working_dir: str = target_dir
    if directory:
        target_dir = os.path.abspath(os.path.join(target_dir, directory))

    if not target_dir.startswith(abs_working_dir):
        return f"Error: Cannot list '{directory}' as it is outside the permitted working directory"

    if not os.path.isdir(target_dir):
        return f"Error: '{directory}' is not a directory"

    content = []
    dirs = os.listdir(target_dir)
    try:
        for item in dirs:
            file_size = 0
            is_dir = True
            item_path = os.path.join(target_dir, item)
            if os.path.isfile(item_path):
                file_size = os.path.getsize(item_path)
                is_dir = False
            content.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(content)
    except Exception as e:
        return f"Error: Error listing directory items: {e}"
    
schema_get_files_info: types.FunctionDeclaration = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

if __name__ == "__main__":
    print(get_files_info("calculator", "pkg"))