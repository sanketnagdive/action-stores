from pydantic import BaseModel

class SimpleResponse(BaseModel):
    message: str
