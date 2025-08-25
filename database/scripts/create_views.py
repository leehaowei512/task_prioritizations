from database.helpers.database_manager import DatabaseManager
from database.models.task_view import TaskDetailsView


def create_views():
    """Create database views"""
    try:
        engine = DatabaseManager().get_engine()
        TaskDetailsView.create_view(engine)
        print("✅ Database views created successfully!")
    except Exception as e:
        print(f"❌ Error creating views: {e}")
        raise


def main():
    print("Creating database views...")
    print("=" * 40)

    create_views()


if __name__ == "__main__":
    main()
