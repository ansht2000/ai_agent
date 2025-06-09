from typing import List, Dict
from google.genai import types

class UserInput:
    def __init__(self, input: str) -> None:
        self.tokens: List[str] = []
        self.flags: Dict[str, bool] = {}
        self.parse_args_and_flags(input)

    def parse_args_and_flags(self, toks: List[str]) -> None:
        for tok in toks:
            if tok[0:2] == "--":
                self.flags[tok[2:]] = True
            else:
                self.tokens.append(tok)

class LLMResponse:
    def __init__(self, res: types.GenerateContentResponse) -> None:
        self.text: str = ""
        self.function_calls: List[types.FunctionCall] = []
        self.executable_code: str = ""
        self.code_execution_result: str = ""
        self.function_call_results: Dict[str, types.Content] = {}
        self.populate_fields(res)

    def populate_fields(self, res: types.GenerateContentResponse) -> None:
        self.text = res.text
        self.function_calls = res.function_calls
        self.executable_code = res.executable_code
        self.code_execution_results = res.code_execution_result
