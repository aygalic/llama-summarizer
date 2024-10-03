from llama_cpp import Llama
from llama_summarizer.random_article import get_random_wikipedia_article
# Path to your quantized model

model_path = "/Users/aygalic/github/llama-summarizer/models/Q4_K_M.gguf"

# Initialize the model
llm = Llama(model_path=model_path, n_ctx=2048, n_threads=4, verbose=False)

# Function to generate text
def generate_chat_response(messages, max_tokens=500):
    # Convert messages to a single string prompt
    prompt = ""
    for message in messages:
        role = message["role"]
        content = message["content"]
        prompt += f"{role}: {content}\n"
    prompt += "assistant: "

    # Generate response
    output = llm(prompt, max_tokens=max_tokens, stop=["user:", "system:", "\n"])
    return output['choices'][0]['text'].strip()

# Example usage
messages = [
    {"role": "system", "content": "You are an AI assistant that is very concise in its answer and your purpose is to summarize inputs!"},
    {"role": "user", "content": "Who are you?"},
]

response = generate_chat_response(messages)
print("Chat:")
for message in messages:
    print(f"{message['role']}: {message['content']}")

print(f"assistant: {response}")


# Usage
title, content = get_random_wikipedia_article()


print(f"Title: {title}")
print(f"Content:\n{content}")


breakpoint()

# Example usage
messages = [
    {"role": "system", "content": "You are an AI assistant that is very concise in its answer and your purpose is to summarize inputs!"},
    {"role": "user", "content": f"can you summarize the following article? \n {title=} {content=}"},
]

response = generate_chat_response(messages)
print("Chat:")
for message in messages:
    print(f"{message['role']}: {message['content']}")

print(f"assistant: {response}")






breakpoint()