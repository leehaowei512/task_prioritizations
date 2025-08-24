from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Team(Base):
    __tablename__ = "teams"

    team_id = Column(Integer, primary_key=True, autoincrement=True)
    team_name = Column(String(50), nullable=False, unique=True)

    # Relationship to tasks
    tasks = relationship("Task", back_populates="team")
