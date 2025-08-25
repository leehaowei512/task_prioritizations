# Set Up Backend Database

- download postgresql
- set `.env` file for database login
- `pip install -e .`
- `cd database`
- eval $(poetry env activate)
- poetry install
- `cd scripts`
- `python create_tables.py`
- `python populate_dimension_tables.py`
- `python populate_fact_table.py`
