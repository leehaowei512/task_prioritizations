import time

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import OperationalError

from config import get_database_url
from models import Base, SessionLocal


class DatabaseManager:
    def __init__(self):
        self.database_url = get_database_url()
        self.engine = self._create_database_engine()
        SessionLocal.configure(bind=self.engine)
        self.session = SessionLocal()

    def _create_database_engine(self, echo=True, max_retries=3, retry_delay=2):
        """Create and return a database engine with retry logic"""
        for attempt in range(max_retries):
            try:
                engine = create_engine(self.database_url, echo=echo)
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                print("Successfully connected to database")
                return engine
            except OperationalError as e:
                if attempt < max_retries - 1:
                    print(f"Connection attempt {attempt + 1} failed. Retrying...")
                    time.sleep(retry_delay)
                else:
                    print("Failed to connect after multiple attempts")
                    raise

    def get_engine(self):
        return self.engine

    def get_session(self):
        return self.session

    def create_tables(self):
        try:
            inspector = inspect(self.engine)
            existing_tables = inspector.get_table_names()
            all_table_names = [table.name for table in Base.metadata.sorted_tables]
            tables_to_create = [
                table for table in all_table_names if table not in existing_tables
            ]

            if tables_to_create:
                print(f"Creating tables: {tables_to_create}")
                Base.metadata.create_all(self.engine)
                print("Tables created successfully!")
            else:
                print("All tables already exist")
            return True
        except Exception as e:
            print(f"Error creating tables: {e}")
            raise
