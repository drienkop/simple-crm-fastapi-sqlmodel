# simple-crm-fastapi-sqlmodel
Simple CRM based on FastAPI and SQLModel

## Configuration
Configure the following environment variables:

```bash
DATABASE_URL=postgresql+asyncpg://sample_user:sample_pass@db:5432/db_name
SECRET_KEY=random_hash
POSTGRES_USER=sample_user
POSTGRES_PASSWORD=sample_pass
POSTGRES_DB=db_name
```

## Run the services
```bash
docker-compose up -d --build
```
## Initial db migration
```bash
docker-compose run backend alembic upgrade head
```
