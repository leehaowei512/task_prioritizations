# Design
## Assumptions
- This is a POC
- Hence, not production ready, no emphasis on scalability, robustness, testing, ...
- Emphasis is on getting a working product, functionality

## Extensions
- Data Ingestion (batching/streaming), currently only deals with single file and populating databse with that
- Database Index, possibly increasing the speed of the queries
- Read replicas
- Scalability

# How to Run
## Virtual Env
- eval $(poetry env activate)
- poetry install

## Database
### Set Up Backend Database
- download postgresql
- set `.env` file for database login
- `cd database`
- `poetry run python main.py`

### Run Backend API
- `cd api_layer`
- `poetry run python main.py`

## Frontend

