from typing import Union

from database.models import Priority, Team, User
from database.helpers.dimension_effort_checker import EffortChecker


class DimensionTableMapper:
    def __init__(self, session):
        self.session = session
        self._users_map = self._get_user_id_map()
        self.effort_checker = EffortChecker()

    def get_team_id(self, team_name: str) -> Union[int, None]:
        team = self.session.query(Team).filter_by(team_name=team_name).first()
        if not team:
            return None
        return team.team_id

    def get_priority_id(self, priority_value: str) -> Union[int, None]:
        priority_value = priority_value.lower()
        priority = (
            self.session.query(Priority)
            .filter(Priority.priority_name.ilike(priority_value))
            .first()
        )

        if not priority:
            return None
        return priority.priority_id

    def _get_user_id_map(self) -> dict:
        users = self.session.query(User).all()
        user_id_map = {user.user_name: user.user_id for user in users}
        return user_id_map

    def get_user_id(self, user_name: str) -> Union[int, None]:
        user_id = self._users_map.get(user_name)

        if user_id is None:
            return None
        return user_id

    def get_valid_effort(self, effort: int) -> Union[int, None]:
        if self.effort_checker.effort_is_valid(effort):
            return effort
        else:
            return None
