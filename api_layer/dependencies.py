from typing import Generator

from database.helpers.database_manager import DatabaseManager
from service_layer.allocation_service import AllocationService
from service_layer.task_service import TaskViewService
from service_layer.team_service import TeamService


def get_task_service() -> Generator[TaskViewService, None, None]:
    """Dependency for TaskService"""
    with DatabaseManager().get_session() as session:
        yield TaskViewService(session)


def get_team_service() -> Generator[TeamService, None, None]:
    """Dependency for TeamService"""
    with DatabaseManager().get_session() as session:
        yield TeamService(session)


def get_allocation_service() -> Generator[AllocationService, None, None]:
    """Dependency for AllocationService"""
    with DatabaseManager().get_session() as session:
        yield AllocationService(session)
