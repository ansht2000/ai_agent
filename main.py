import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from typing import List, Callable

class UserInput:
    def __init__(self, input: str) -> None:
        self.tokens: List[str] = []
        self.flags: List[str] = []
        self.parse_args_and_flags(input)

    def parse_args_and_flags(self, toks: List[str]) -> None:
        for tok in toks:
            if tok[0:2] == "--":
                self.flags.append(tok[2:])
            else:
                self.tokens.append(tok)

def print_verbose_response(input: UserInput) -> Callable[[types.GenerateContentResponse], None]:
    print(f"Working on: {" ".join(input.tokens)}")
    print("=============================================================")
    def print_res(res: types.GenerateContentResponse):
        print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {res.usage_metadata.candidates_token_count}")
        print_short_response(res)
    return print_res

def print_short_response(res: types.GenerateContentResponse):
    print("Response:")
    print(res.text)

def print_response(res: types.GenerateContentResponse, input: UserInput):
    res_printer: Callable[[types.GenerateContentResponse], None] = print_short_response
    for flag in input.flags:
        if flag == "verbose":
            res_printer = print_verbose_response(input)
    res_printer(res)

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
    res: types.GenerateContentResponse = client.models.generate_content(
                                            model="gemini-2.0-flash-001",
                                            contents=messages
                                        )
    print_response(res=res, input=input)

if __name__ == "__main__":
    main()