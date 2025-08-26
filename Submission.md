# Assumptions
Functional and non-functional requirements are directly inferred from README 
### Functional Requirements
- Database
  - Source: cumbersome to maintain as new tasks are added manually directly to the json file
- Data consistency
  - Source: Often there's a mistake made which may interfere with prioritising the tasks.
  - Certain rows have certain accepted values, rows that contain columns that do not adhere will be dropped
- Printing all lists of tasks ordered by priority, then date added
  - Assumption, data added does not include time, just date
- Weekly task allocation
  - Given the tasks in the database, return tasks that most fully utilize the resource provided

### Non-functional Requirements
- This is a POC
  - Hence, not production ready, no emphasis on scalability, robustness, testing, ...
  - Emphasis is on getting a working product, functionality
- Development timeframe: Time limit

# Design
## Database layer
- Filtering done at the layer
- Foreign key constraint
- Star schema
  - Fact Table = tasks
  - Dimension Tables = teams, priority, users
- ORM use: SQLAlchemy with PostgreSQL database 
- Reasoning:
  - Splitting out the table makes it easy to query filter all query values all at once (e.g. teams)
  - Foreign key constraint, to ensure that team and effort values belong to the set of allowed values
  - ORM used to provide layer of abstraction on top of database, speeding up development as low level implementation at postgresSQL level is not needed
## Service Layer
- Python logic used
- Contains all the business logic
  - weekly task allocation (given tasks and resource, figure out the optimal tasks)
  - get all tasks (contains the order by logic that is specific to the business)
## Api Layer
- FastAPI
- Fast development
- Automatic documentation generation
- In built data validation
## Frontend
- NextJS
- Faster development that React
- For the current requirements, could not justify React's complexity
- Out of the box routing (as I wanted to separate the functionality into 2 different pages)
- Could have went with something even more light-weight like Flask

## Mistakes
- Over-engineered database layer, should have went for a single table at first to save time
- Over-engineered frontend layer, should have went with something more lightweight like Flask

## Extensions
- Database Layer
  - Data Ingestion (batching/streaming), currently only deals with single file and populating databse with that
  - Database Index, possibly increasing the speed of the queries
  - Read replicas
  - Scalability
- Frontend
  - Possible interaction between team filter and allocation functionality but would need to confirm with users
  - Increase styling
  - Possible security
  - Dockerization to possible increase scalability
- Testing
  - Unit testing for components
- Security
  - Login functionality
- Hosting
  - Not locally, but possibly through cloud for scalability

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
- `npm dev run`
