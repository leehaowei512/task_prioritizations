import logging
from typing import List, Optional

from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session

from database.models.task_view import TaskDetailsView
from schemas.task import TaskResponse

logger = logging.getLogger(__name__)


class TaskViewService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_tasks(self, team: Optional[str] = None) -> List[TaskResponse]:
        """Get all tasks from the materialized view"""
        try:
            query = self.db.query(TaskDetailsView)

            if team:
                query = query.filter(TaskDetailsView.team_name == team)
                logger.info(f"Filtering tasks for team: {team}")

            # Order by priority value (descending) and date added (ascending)
            tasks = query.order_by(
                desc(TaskDetailsView.priority_value), asc(TaskDetailsView.date_added)
            ).all()

            logger.info(f"Retrieved {len(tasks)} tasks from view")

            return [
                TaskResponse(
                    task_id=task.task_id,
                    user_name=task.user_name,
                    team_name=task.team_name,
                    priority_name=task.priority_name,
                    priority_value=task.priority_value,
                    effort=task.effort,
                    date_added=task.date_added,
                    time_added=task.time_added,
                    description=task.description,
                )
                for task in tasks
            ]

        except Exception as e:
            logger.error(f"Error retrieving tasks from view: {str(e)}")
            raise
