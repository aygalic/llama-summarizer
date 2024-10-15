from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse
from llama_summarizer.chat import Chat
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles


app = FastAPI()

chat = Chat()

class Query(BaseModel):
    item: str

class ChatHistory(BaseModel):
    item: list[tuple[str, str]]


@app.post("/llm_on_cpu")
def legacy_summary(query: Query) -> str:
    """Legacy function to ask for a summary without using token streaming.

    Parameters
    ----------
    query : Query
        Article to summarize

    Returns
    -------
    str
        Summary provided by the LLM
    """
    return chat.request_summary(query.item)


@app.post("/llm_on_cpu_stream")
async def stream_summary(query: Query) -> StreamingResponse:
    """Request summary and stream the response

    Parameters
    ----------
    query : Query
        Article to summarize

    Returns
    -------
    StreamingResponse
        Streaming summary provided by the LLM

    """
    async def generate():
        for token in chat.request_summary_stream(query.item):
            yield f"data: {token}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.post("/stream_misc_query")
async def stream_query(query: Query):
    async def generate():
        for token in chat.single_query_stream(query.item):
            yield f"data: {token}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.post("/stream_chat")
async def stream_chat(hist: ChatHistory):
    async def generate():
        for token in chat.stream_chat(hist.item):
            yield f"data: {token}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")





app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
def index() -> FileResponse:
    return FileResponse(path="/app/static/index.html", media_type="text/html")
