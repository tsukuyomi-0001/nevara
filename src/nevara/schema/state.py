from pydantic import BaseModel

class GlobalState(BaseModel):
    userInput: str