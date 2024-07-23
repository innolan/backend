from pydantic import BaseModel


class MatchDTO(BaseModel):
    primary_id: int
    secondary_id: int

    class Config:
        from_attributes = True
