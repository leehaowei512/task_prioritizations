# populate_fact_table.py
from datetime import datetime

from database.helpers.database_manager import DatabaseManager
from database.helpers.dimension_tables_mapper import DimensionTableMapper
from database.helpers.input_data_reader import InputDataReader
from database.models import Task


def populate_fact_table():
    """Import tasks from JSON file into the database"""

    session = DatabaseManager().get_session()
    dt_mapper = DimensionTableMapper(session)
    tasks_data = InputDataReader().get_tasks_data()

    imported_count = 0
    errors = []

    try:
        print(f"Processing {len(tasks_data)} tasks from JSON...")

        for task_data in tasks_data:
            try:
                user_name = task_data["name"]
                team_name = task_data["team"]
                priority_name = task_data["priority"]
                effort = task_data["effort"]

                print(
                    f"Processing task for: {user_name}, team: {team_name}, priority: {priority_name}"
                )

                # Get all required IDs with detailed error reporting
                team_id = dt_mapper.get_team_id(team_name)
                if team_id is None:
                    error_msg = f"Team '{team_name}' not found for user: {user_name}"
                    errors.append(error_msg)
                    print(f"❌ {error_msg}")
                    continue

                priority_id = dt_mapper.get_priority_id(priority_name)
                if priority_id is None:
                    error_msg = (
                        f"Priority '{priority_name}' not found for user: {user_name}"
                    )
                    errors.append(error_msg)
                    print(f"❌ {error_msg}")
                    continue

                user_id = dt_mapper.get_user_id(user_name)
                if user_id is None:
                    error_msg = f"User '{user_name}' not found in database"
                    errors.append(error_msg)
                    print(f"❌ {error_msg}")
                    continue

                # Check effort value
                effort = dt_mapper.get_valid_effort(effort)
                if effort is None:
                    error_msg = f"Effort '{effort}' is not valid Fibonacci number"
                    errors.append(error_msg)
                    print(f"❌ {error_msg}")
                    continue

                # Parse timestamp
                updated_timestamp = datetime.strptime(
                    task_data["updated_timestamp"], "%Y-%m-%d %H:%M:%S"
                )

                # Create new task
                new_task = Task(
                    user_id=user_id,
                    team_id=team_id,
                    priority_id=priority_id,
                    effort=task_data["effort"],
                    date_added=updated_timestamp.date(),
                    time_added=updated_timestamp.time(),
                    week_added=updated_timestamp.isocalendar()[1],
                    description=task_data["description"],
                )

                session.add(new_task)
                imported_count += 1
                print(f"✓ Successfully processed task for: {user_name}")

            except Exception as e:
                error_msg = f"Error processing task '{task_data.get('name', 'Unknown')}': {str(e)}"
                errors.append(error_msg)
                print(f"❌ {error_msg}")

        session.commit()
        print(f"\n✅ Import completed! Successfully imported {imported_count} tasks.")

        if errors:
            print(f"\n❌ Errors encountered ({len(errors)}):")
            for error in errors:
                print(f"  - {error}")
        else:
            print("🎉 No errors encountered!")

    except Exception as e:
        session.rollback()
        print(f"❌ Fatal error during import: {e}")
        raise
    finally:
        session.close()

    return imported_count, errors


def main():
    """Main function to import tasks from JSON"""

    print("Starting task import from JSON...")
    print("=" * 50)

    imported_count, errors = populate_fact_table()

    print("\n" + "=" * 50)
    print("FINAL RESULTS:")
    print(f"Tasks successfully imported: {imported_count}")
    print(f"Errors encountered: {len(errors)}")
    print("=" * 50)


if __name__ == "__main__":
    main()
