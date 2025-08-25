from sqlalchemy import create_engine, inspect, text

from database.helpers.database_manager import DatabaseManager
from database.models import Base


def create_tables():
    try:
        engine = DatabaseManager().get_engine()
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        all_table_names = [table.name for table in Base.metadata.sorted_tables]
        tables_to_create = [
            table for table in all_table_names if table not in existing_tables
        ]

        if tables_to_create:
            print(f"Creating tables: {tables_to_create}")
            Base.metadata.create_all(engine)
            print("Tables created successfully!")
        else:
            print("All tables already exist")
        return True
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise


def main():
    print("Creating database tables...")
    print("=" * 40)

    create_tables()


if __name__ == "__main__":
    main()
