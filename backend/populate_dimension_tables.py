from database_manager import DatabaseManager
from dimension_tables_manager import DimensionTablesPopulator


def populate_dimension_tables():
    """Populate database with default teams and priorities"""

    session = DatabaseManager().get_session()
    dimension_tbl_manager = DimensionTablesPopulator(session)

    try:
        print("Populating default data...")

        dimension_tbl_manager.populate_priority_dimension_table()

        dimension_tbl_manager.populate_teams_dimension_table()

        dimension_tbl_manager.populate_users_dimension_table()

        print(f"\nData population completed!")

    except Exception as e:
        session.rollback()
        print(f"Error populating data: {e}")
        raise
    finally:
        session.close()


def main():
    """Main function to populate default data"""

    print("Populating database with default data...")
    print("=" * 50)

    populate_dimension_tables()

    print("\nData population completed!")
    print("Run 'python import_tasks.py' to import tasks from JSON.")


if __name__ == "__main__":
    main()
