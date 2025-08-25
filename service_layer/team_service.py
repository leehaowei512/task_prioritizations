# app/services/team_service.py
import logging
from typing import List

from database.models import Team
from sqlalchemy.orm import Session

from schemas.team import TeamResponse

logger = logging.getLogger(__name__)


class TeamService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_teams(self) -> List[TeamResponse]:
        """Get all available teams"""
        try:
            teams = self.db.query(Team).order_by(Team.team_name).all()
            logger.info(f"Retrieved {len(teams)} teams")

            return [TeamResponse(team_name=team.team_name) for team in teams]

        except Exception as e:
            logger.error(f"Error retrieving teams: {str(e)}")
            raise
