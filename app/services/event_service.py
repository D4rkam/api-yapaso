from collections import deque

from app.schemas.event_schema import EventSchema


class SSEEvent:
    EVENTS = deque()

    @staticmethod
    def add_event(event: EventSchema) -> None:
        SSEEvent.EVENTS.append(event)

    @staticmethod
    def get_event() -> EventSchema | None:
        if len(SSEEvent.EVENTS) == 0:
            return None
        return SSEEvent.EVENTS.popleft()

    @staticmethod
    def count():
        return len(SSEEvent.EVENTS)
