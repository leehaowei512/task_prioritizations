# app/services/allocation_service.py
import logging
from typing import List, Tuple, Union

from database.models.task_view import TaskDetailsView
from sqlalchemy.orm import Session

from schemas.allocation import AllocationResult
from schemas.task import TaskResponse

logger = logging.getLogger(__name__)


class AllocationService:
    def __init__(self, db: Session):
        self.db = db

    def get_optimal_allocation(self, available_effort: int) -> AllocationResult:
        """
        Find the optimal set of tasks to maximize effort utilization while considering priority.
        Uses a knapsack-like algorithm with priority as value and effort as weight.
        """
        try:
            # Get all tasks ordered by priority (high first) then effort (ascending)
            tasks_data = self._get_task_data()

            if tasks_data is None:
                return AllocationResult(
                    allocated_tasks=[],
                    total_effort_used=0,
                    total_effort_available=available_effort,
                    efficiency=0.0,
                )

            # Find optimal allocation
            selected_tasks = _solve_knapsack(tasks_data, available_effort)

            # Calculate metrics
            total_effort_used = sum(task.effort for task in selected_tasks)

            # Convert to response model
            allocated_tasks = [
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
                for task in selected_tasks
            ]

            return AllocationResult(
                allocated_tasks=allocated_tasks,
                total_effort_used=total_effort_used,
                total_effort_available=available_effort,
            )

        except Exception as e:
            logger.error(f"Error in task allocation: {str(e)}")
            raise

    def _get_task_data(self) -> Union[List[tuple], None]:
        all_tasks = (
            self.db.query(TaskDetailsView)
            .order_by(
                TaskDetailsView.priority_value.desc(),  # High priority first
                TaskDetailsView.effort.asc(),  # Then smaller efforts first
            )
            .all()
        )

        if not all_tasks:
            return None

        tasks_data = []
        for task in all_tasks:
            tasks_data.append((task.effort, task.priority_value, task))

        return tasks_data


def _solve_knapsack(data: List[Tuple[int, int, any]], capacity: int) -> List:
    """
    Solve the knapsack problem to maximize priority value while staying within effort capacity.
    Uses dynamic programming approach.
    """
    n = len(data)

    # Create DP table: dp[i][w] = max total value using first i items with capacity w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    # Fill DP table
    for i in range(1, n + 1):
        effort, priority_value, task = data[i - 1]
        for w in range(capacity + 1):
            if effort <= w:
                # Max of including or excluding current item
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - effort] + priority_value)
            else:
                dp[i][w] = dp[i - 1][w]

    # Backtrack to find selected items
    selected_tasks = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            effort, priority_value, task = data[i - 1]
            selected_tasks.append(task)
            w -= effort

    # Return tasks in priority order (high first)
    return sorted(selected_tasks, key=lambda x: (-x.priority_value, x.effort))
