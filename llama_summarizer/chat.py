from llama_cpp import Llama
from . import MODELS_DIR
MODEL_PATH = str(MODELS_DIR / "Q4_K_M.gguf")

class Chat():
    def __init__(self):
        self.llm = Llama(model_path=MODEL_PATH, n_ctx=2048, n_threads=4, verbose=False)
        self.max_tokens = 500

    def single_query(self, message:str) -> str:
        messages = [
            {
                "role": "system",
                "content": "You are an AI assistant that respond to user request and is very concise in its answers."
            },
            {
                "role": "user",
                "content": message
            },
        ]
        return self._generate_response(messages)

    def _generate_response(self, query:str) -> str:

        # Convert messages to a single string prompt
        prompt = ""
        for message in query:
            role = message["role"]
            content = message["content"]
            prompt += f"{role}: {content}\n"
        prompt += "assistant: "

        # Generate response
        output = self.llm(prompt, max_tokens=self.max_tokens, stop=["user:", "system:", "\n"])
        return output['choices'][0]['text'].strip()

