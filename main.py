import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from typing import List, Callable
from config import SYSTEM_PROMPT
from classes import UserInput, LLMResponse
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.overwrite_file import schema_overwrite_file
from functions.run_python import schema_run_python_file
from call_function import call_function

def process_llm_response(res: types.GenerateContentResponse, verbose: bool = False) -> LLMResponse:
    llm_res = LLMResponse(res=res)

    if llm_res.text:
        print("Text response:")
        print(llm_res.text)

    if llm_res.function_calls:
        print("Function calls:")
        for call in llm_res.function_calls:
            function_res: types.Content = call_function(call=call, verbose=verbose)
            llm_res.function_call_results[call.id] = function_res
            if not function_res.parts[0].function_response.response:
                raise ValueError
            elif verbose:
                print(f"-> {function_res.parts[0].function_response.response}")
    
    if llm_res.executable_code:
        # TODO: figure out how to handle this
        pass

    if llm_res.code_execution_result:
        # TODO: figure out how to handle this
        pass

    return llm_res

def main() -> None:
    load_dotenv() 
    api_key: str = os.environ.get("GEMINI_API_KEY")
    client: genai.Client = genai.Client(api_key=api_key)
    
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <prompt>")
        exit(1)
    
    input: UserInput = UserInput(sys.argv[1:])
    messages: List[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=" ".join(input.tokens))])
    ]
    available_functions: types.Tool = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_overwrite_file,
            schema_run_python_file,
        ]
    )

    res: types.GenerateContentResponse = client.models.generate_content(
                                            model="gemini-2.0-flash-001",
                                            contents=messages,
                                            config=types.GenerateContentConfig(
                                                tools=[available_functions],
                                                system_instruction=SYSTEM_PROMPT
                                            )
                                        )
    
    verbose = "verbose" in input.flags
    if verbose:
        text: str = f"Working on: {" ".join(input.tokens)}"
        print(f"Working on: {" ".join(input.tokens)}")
        print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {res.usage_metadata.candidates_token_count}")
        print('=' * len(text))

    llm_res: LLMResponse = process_llm_response(res, verbose=verbose)
    # print_response(res=res, input=input)

if __name__ == "__main__":
    main()