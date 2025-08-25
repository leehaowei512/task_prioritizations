from database.scripts.create_tables import create_tables
from database.scripts.populate_dimension_tables import populate_dimension_tables
from database.scripts.populate_fact_table import  populate_fact_table
from database.scripts.create_views import create_views


def main():
    create_tables()
    populate_dimension_tables()
    populate_fact_table()
    create_views()


if __name__ == "__main__":
    main()
