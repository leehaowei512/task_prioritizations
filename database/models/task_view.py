# app/models/task_view.py
from sqlalchemy import Column, Date, Integer, String, Time, text

from .base import Base


class TaskDetailsView(Base):
    __tablename__ = "task_details_view"
    __table_args__ = {"info": dict(is_view=True)}  # Mark as view

    task_id = Column(Integer, primary_key=True)
    user_name = Column(String(50))
    team_name = Column(String(50))
    priority_name = Column(String(10))
    priority_value = Column(Integer)
    effort = Column(Integer)
    date_added = Column(Date)
    time_added = Column(Time)
    description = Column(String(500))

    @classmethod
    def create_view(cls, engine):
        """Create the database view"""
        view_sql = text(
            """
        CREATE OR REPLACE VIEW task_details_view AS
        SELECT 
            t.task_id,
            u.user_name,
            tm.team_name,
            p.priority_name,
            p.priority_value,
            t.effort,
            t.date_added,
            t.time_added,
            d.task_description as description
        FROM tasks t
        JOIN users u ON t.user_id = u.user_id
        JOIN teams tm ON t.team_id = tm.team_id
        JOIN priority p ON t.priority_id = p.priority_id
        JOIN task_descriptions d ON t.task_id = d.task_id
        """
        )

        with engine.connect() as conn:
            conn.execute(view_sql)
            conn.commit()
