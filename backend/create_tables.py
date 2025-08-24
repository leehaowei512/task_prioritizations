from database_manager import DatabaseManager


def main():
    print("Creating database tables...")
    print("=" * 40)

    database_manager = DatabaseManager()
    database_manager.create_tables()


if __name__ == "__main__":
    main()
