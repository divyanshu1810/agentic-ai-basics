from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()

async def llm_stream(question: str):
    response = f"Answer for: {question}"

    for word in response.split():
        yield word + " "
        await asyncio.sleep(0.1)

@app.get("/ask")
async def ask(question: str):
    return StreamingResponse(
        llm_stream(question),
        media_type="text/plain"
    )