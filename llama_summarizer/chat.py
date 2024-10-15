from llama_cpp import Llama
from . import MODELS_DIR
MODEL_PATH = str(MODELS_DIR / "Q4_K_M.gguf")

class Chat():
    def __init__(self):
        self.llm = Llama(model_path=MODEL_PATH, n_ctx=2048, n_threads=4, verbose=False)
        self.max_tokens = 500

    def request_summary(self, message: str) -> str:
        messages = [
            {
                "role": "system",
                "content": "You aim is to summarize and article in the most concise way possible."
            },
            {
                "role": "user",
                "content": message
            },
        ]
        return self._generate_response(messages)

    def request_summary_stream(self, message: str):
        messages = [
            {
                "role": "system",
                "content": "You aim is to summarize and article in the most concise way possible."
            },
            {
                "role": "user",
                "content": message
            },
        ]
        yield from self._generate_response_stream(messages)


    def single_query_stream(self, message: str):
        messages = [
            {
                "role": "system",
                "content": "You are an AI assistant that responds to user requests and is very concise in its answers."
            },
            {
                "role": "user",
                "content": message
            },
        ]
        yield from self._generate_response_stream(messages)



    def stream_chat(self, messages: list[tuple[str, str]]):

        prompt = [
            {
                "role": "system",
                "content": "You are an AI assistant that responds to user requests and is very concise in its answers."
            }
        ]
        for role, content in messages:
            prompt.append(
                {
                    "role": role,
                    "content": content
                }
            )



        yield from self._generate_response_stream(prompt)    

    def _generate_response(self, query: list) -> str:
        prompt = self._create_prompt(query)
        output = self.llm(prompt, max_tokens=self.max_tokens, stop=["user:", "system:", "\n"])
        return output['choices'][0]['text'].strip()

    def _generate_response_stream(self, query: list):
        prompt = self._create_prompt(query)
        for output in self.llm(prompt, max_tokens=self.max_tokens, stop=["user:", "system:", "\n"], stream=True):
            yield output['choices'][0]['text']

    def _create_prompt(self, query: list) -> str:
        prompt = ""
        for message in query:
            role = message["role"]
            content = message["content"]
            prompt += f"{role}: {content}\n"
        prompt += "assistant: "
        return prompt