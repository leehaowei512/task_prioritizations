from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Priority(Base):
    __tablename__ = "priority"

    priority_id = Column(Integer, primary_key=True, autoincrement=True)
    priority_name = Column(
        String(10), nullable=False, unique=True
    )  # 'Low', 'Medium', 'High'
    priority_value = Column(Integer, nullable=False, unique=True)  # 1, 2, 3

    # Relationship to tasks
    tasks = relationship("Task", back_populates="priority")
