from pydantic import BaseModel


class EventSchema(BaseModel):
    type: str
    message: str
