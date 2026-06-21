from typing_extensions import Self

from pydantic import BaseModel, field_validator
from typing import Any, Literal, Optional

from nevara.agent.executor import executors

routes = {"DONE", *executors.keys()}

class RouterStruct(BaseModel):
    route: str
    prompt: Optional[str]
    
    @field_validator('route')
    @classmethod
    def validate_route(cls, value: Any):
        if value not in routes:
            raise ValueError(
                f"route must be one of {sorted(routes)}"
            )
        return value