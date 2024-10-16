from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from llama_summarizer.chat import Chat

app = FastAPI()

chat = Chat()
summarizer = Chat("Your aim is to provide a concise summary of the user's article")


class Query(BaseModel):
    item: str


class ChatHistory(BaseModel):
    item: list[tuple[str, str]]


@app.post("/llm_on_cpu_stream")  # legacy route
@app.post("/summarize")
async def stream_summary(query: Query) -> StreamingResponse:
    """Request summary and stream the response.
    Uses a non persistent chat object with specific prompt for this.

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
        for token in summarizer.generate_summary(query.item):
            yield f"data: {token}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.post("/stream_chat")
async def stream_chat(hist: ChatHistory) -> StreamingResponse:
    """Simple chatbot

    Parameters
    ----------
    hist : ChatHistory
        Chat history that the AI will use to generate its next reply.

    Returns
    -------
    StreamingResponse
        Streaming response provided by the LLM.
    """

    async def generate():
        for token in chat.generate_chat_response(hist.item):
            yield f"data: {token}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


app.mount("/", StaticFiles(directory="static", html=True), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(path="/app/static/index.html", media_type="text/html")
