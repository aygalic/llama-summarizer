from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse
from llama_summarizer.chat import Chat
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles


app = FastAPI()

chat = Chat()

class Query(BaseModel):
    item: str

# Legacy route - keeps existing behavior
@app.post("/llm_on_cpu")
def legacy_query(query: Query):
    return chat.single_query(query.item)

# New streaming route
@app.post("/llm_on_cpu_stream")
async def stream_query(query: Query):
    async def generate():
        for token in chat.single_query_stream(query.item):
            yield f"data: {token}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
def index() -> FileResponse:
    return FileResponse(path="/app/static/index.html", media_type="text/html")



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