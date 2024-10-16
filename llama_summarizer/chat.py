from llama_cpp import Llama
from . import MODELS_DIR
MODEL_PATH = str(MODELS_DIR / "Q4_K_M.gguf")

class Chat():
    def __init__(self, init_prompt : str | None = None):
        self.llm = Llama(model_path=MODEL_PATH, n_ctx=2048, n_threads=4, verbose=False)
        self.max_tokens = 500
        self.prompt_history : list[dict[str, str]] = []

        self.prompt_history += [{
            "role": "system",
            "content":[init_prompt, "You are an AI assistant that responds to user requests."][init_prompt is None]
        }]

    def generate_summary(self, message: str):
        """Generate Summary for the user.

        Parameters
        ----------
        message : str
            Article tu summarize

        Yields
        ------
        str
            Summary
        """
        messages = self.prompt_history + [
            {
                "role": "user",
                "content": message
            },
        ]
        yield from self._generate_response_stream(messages)


    def generate_chat_response(self, messages: list[tuple[str, str]]):
        """Generate chat response

        Parameters
        ----------
        messages : list[tuple[str, str]]
            Chat history

        Yields
        ------
        str
            new LLM response.
        """
        prompt = self.prompt_history
        for role, content in messages:
            prompt.append(
                {
                    "role": role,
                    "content": content
                }
            )

        yield from self._generate_response_stream(prompt)


    def _generate_response_stream(self, query: list):
        """Streaming interface with the model.

        Parameters
        ----------
        query : list
            List of messages

        Yields
        ------
        str
            LLM response
        """
        prompt = self._create_prompt(query)
        for output in self.llm(prompt, max_tokens=self.max_tokens, stop=["user:", "system:", "\n"], stream=True):
            yield output['choices'][0]['text']

    def _create_prompt(self, query: list) -> str:
        """Create a valid prompt

        Parameters
        ----------
        query : list
            List of messages

        Returns
        -------
        str
            Formatted prompt
        """
        prompt = ""
        for message in query:
            role = message["role"]
            content = message["content"]
            prompt += f"{role}: {content}\n"
        prompt += "assistant: "
        return prompt