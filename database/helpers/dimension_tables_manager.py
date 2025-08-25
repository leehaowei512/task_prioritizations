from database.helpers.input_data_reader import InputDataReader
from database.models import Priority, Team, User


class DimensionTablesPopulator:
    def __init__(self, session):
        self.session = session

    def get_session(self):
        return self.session

    def populate_priority_dimension_table(self):
        default_priorities = [
            {"priority_name": "Low", "priority_value": 1},
            {"priority_name": "Medium", "priority_value": 2},
            {"priority_name": "High", "priority_value": 3},
        ]

        priorities_added = 0
        try:
            for priority_data in default_priorities:
                existing = (
                    self.session.query(Priority)
                    .filter_by(priority_name=priority_data["priority_name"])
                    .first()
                )
                if not existing:
                    self.session.add(Priority(**priority_data))
                    priorities_added += 1
                    print(f"✓ Added priority: {priority_data['priority_name']}")
            self.session.commit()
            print(f"Priorities added: {priorities_added}")
        except Exception as e:
            self.session.rollback()
            print(f"Fatal error during user import: {e}")
            raise
        finally:
            self.session.close()

    def populate_teams_dimension_table(self):
        default_teams = [
            {"team_name": "Grinders"},
            {"team_name": "Bean Selectors"},
            {"team_name": "Taste testing"},
            {"team_name": "Finance"},
        ]

        teams_added = 0
        try:
            for team_data in default_teams:
                existing = (
                    self.session.query(Team)
                    .filter_by(team_name=team_data["team_name"])
                    .first()
                )
                if not existing:
                    self.session.add(Team(**team_data))
                    teams_added += 1
                    print(f"✓ Added team: {team_data['team_name']}")

            self.session.commit()
            print(f"Teams added: {teams_added}")
        except Exception as e:
            self.session.rollback()
            print(f"Fatal error during user import: {e}")
            raise
        finally:
            self.session.close()

    def populate_users_dimension_table(self):
        def extract_unique_users_from_json():
            """Extract unique user names from JSON file"""
            tasks_data = InputDataReader().get_tasks_data()

            # Get unique user names
            unique_users = set()
            for task_data in tasks_data:
                unique_users.add(task_data["name"])

            return sorted(list(unique_users))

        unique_users = extract_unique_users_from_json()

        users_created = 0
        users_existing = 0
        errors = []

        try:
            print(f"Found {len(unique_users)} unique users in JSON file")

            for user_name in unique_users:
                try:
                    # Check if user already exists
                    existing_user = (
                        self.session.query(User).filter_by(user_name=user_name).first()
                    )

                    if existing_user:
                        users_existing += 1
                        print(
                            f"✓ User already exists: {user_name} (ID: {existing_user.user_id})"
                        )
                    else:
                        # Create new user
                        new_user = User(user_name=user_name)
                        self.session.add(new_user)
                        users_created += 1
                        print(f"✓ Creating new user: {user_name}")

                except Exception as e:
                    errors.append(f"Error processing user '{user_name}': {str(e)}")

            self.session.commit()
            print(f"\nUser import completed!")
            print(f"Users created: {users_created}")
            print(f"Users already existed: {users_existing}")
            print(f"Total users in database: {users_created + users_existing}")

            if errors:
                print(f"\nErrors encountered ({len(errors)}):")
                for error in errors:
                    print(f"  - {error}")

            return users_created, users_existing

        except Exception as e:
            self.session.rollback()
            print(f"Fatal error during user import: {e}")
            raise
        finally:
            self.session.close()
