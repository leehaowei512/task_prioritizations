from datetime import datetime

from sqlalchemy import Column, Date, ForeignKey, Integer, Time, String
from sqlalchemy.orm import relationship

from .base import Base


class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(f"users.user_id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.team_id"), nullable=False)
    priority_id = Column(Integer, ForeignKey("priority.priority_id"), nullable=False)
    effort = Column(Integer, nullable=False)
    description = Column(String(200), nullable=False)
    date_added = Column(Date, default=datetime.utcnow().date)
    time_added = Column(Time, default=datetime.utcnow().time)
    week_added = Column(Integer)  # Week number of the year

    # Relationships
    user = relationship("User", back_populates="tasks")
    team = relationship("Team", back_populates="tasks")
    priority = relationship("Priority", back_populates="tasks")
