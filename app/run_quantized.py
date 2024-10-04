from fastapi import FastAPI
from llama_summarizer.chat import Chat
from pydantic import BaseModel

app = FastAPI()

chat = Chat()

class Query(BaseModel):
    item: str


@app.post("/llm_on_cpu")
async def stream(query: Query):
    return chat.single_query(query.item)

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