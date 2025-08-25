from sqlalchemy import create_engine, inspect, text

from database.helpers.database_manager import DatabaseManager
from database.models import Base


def create_tables():
    try:
        engine = DatabaseManager().get_engine()
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()

        # Filter out views from the tables to create
        # Only include tables that are NOT marked as views
        tables_to_create = []
        for table in Base.metadata.sorted_tables:
            # Check if this table is actually a view (using the info dict)
            is_view = table.info.get('is_view', False)
            if not is_view and table.name not in existing_tables:
                tables_to_create.append(table)

        if tables_to_create:
            table_names = [table.name for table in tables_to_create]
            print(f"Creating tables: {table_names}")

            # Create only the non-view tables
            for table in tables_to_create:
                table.create(engine)

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
