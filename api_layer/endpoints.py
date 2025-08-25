import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from api_layer.dependencies import (get_allocation_service, get_task_service,
                                    get_team_service)
from schemas.allocation import AllocationResult
from schemas.task import TaskResponse
from schemas.team import TeamResponse
from service_layer.allocation_service import AllocationService
from service_layer.task_service import TaskViewService
from service_layer.team_service import TeamService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/tasks", response_model=List[TaskResponse])
async def get_tasks(
    team: Optional[str] = Query(None, description="Filter by team name"),
    task_service: TaskViewService = Depends(get_task_service),
):
    try:
        tasks = task_service.get_all_tasks(team=team)
        return tasks
    except Exception as e:
        logger.error(f"Error in get_tasks endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving tasks: {str(e)}")


@router.get("/teams", response_model=List[TeamResponse])
async def get_teams(team_service: TeamService = Depends(get_team_service)):
    """
    Get all available team names.
    Useful for populating dropdowns and filters in the UI.
    """
    try:
        teams = team_service.get_all_teams()
        return teams
    except Exception as e:
        logger.error(f"Error in get_teams endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving teams: {str(e)}")


@router.get("/allocate-tasks/", response_model=AllocationResult)
async def allocate_tasks_get(
    available_effort: int = Query(
        ..., ge=1, description="Available effort points for the week"
    ),
    allocation_service: AllocationService = Depends(get_allocation_service),
):
    """
    GET version of task allocation endpoint.

    Find the optimal set of tasks to work on given available effort points.
    Useful for quick testing and manual allocation.

    - **available_effort**: Number of effort points available for the week (min: 1)
    - **returns**: Optimal task allocation with efficiency metrics
    """
    try:
        result = allocation_service.get_optimal_allocation(available_effort)
        return result
    except Exception as e:
        logger.error(f"Error in task allocation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error allocating tasks: {str(e)}")
