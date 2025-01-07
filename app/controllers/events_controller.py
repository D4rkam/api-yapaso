import asyncio

from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse

from app.schemas.event_schema import EventSchema
from app.services.event_service import SSEEvent

router = APIRouter(prefix="/events", tags=["Eventos"])


@router.post("/emit")
async def new_event(event: EventSchema):
    SSEEvent.add_event(event)
    return {"message": "Event added", "count": SSEEvent.count()}


@router.get("/stream")
async def stream_events(req: Request):
    async def stream_generator():
        while True:
            if await req.is_disconnected():
                break
            event = SSEEvent.get_event()
            if event:
                yield f"data: {event.model_dump_json()}"
            await asyncio.sleep(1)

    return EventSourceResponse(stream_generator())
