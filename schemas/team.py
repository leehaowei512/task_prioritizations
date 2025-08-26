# app/schemas/team.py
from pydantic import BaseModel


class TeamResponse(BaseModel):
    team_name: str

    class Config:
        from_attributes = True
