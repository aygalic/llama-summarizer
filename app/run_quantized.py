from fastapi import FastAPI
from llama_summarizer.chat import Chat

app = FastAPI()

chat = Chat()

@app.post("/llm_on_cpu")
async def stream(item: str):
    return chat.single_query(item)

'''
from llama_summarizer.random_article import get_random_wikipedia_article

title, content = get_random_wikipedia_article()


print(f"Title: {title}")
print(f"Content:\n{content}")


breakpoint()

summary_prompt = f"can you summarize the following article? \n {title=} {content=}"

response = chat.single_query(summary_prompt)


print(f"assistant: {response}")






breakpoint()

'''