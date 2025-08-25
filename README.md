# Virtual Env
- eval $(poetry env activate)
- poetry install

# Database
## Set Up Backend Database
- download postgresql
- set `.env` file for database login
- `cd database`
- `poetry run python main.py`

## Run Backend API
- `cd api_layer`
- `poetry run python main.py`