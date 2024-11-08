чтобы перезапустить контейнер и удалить все данные из бд
```bash
docker-compose down --volumes --remove-orphans
docker-compose up -d
```

## Гайд как запустить приложение
1. собираю образ fastapi 
```bash
cd fastapi_app
docker build -t fastapi .
cd ..
```
проверяю что он нормально встал
`docker images`
2. запускаю композ
```bash
docker compose down -v
docker compose up --build --force-recreate -d
```

чтобы эт все работало, нужно еще добавить ./init.sql такого вида
```sql
-- обязательно должно быть синхронизироано с .env
CREATE DATABASE airflow_db;
CREATE DATABASE travel_diary;
CREATE USER airflow WITH PASSWORD 'password123';
CREATE USER travel_diary_user WITH PASSWORD 'password123';
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow;
GRANT ALL PRIVILEGES ON DATABASE travel_diary TO travel_diary_user;
```
и ./.env
```.env
AIRFLOW_UID=YOUR_AIRFLOW_UID
AIRFLOW_IMAGE_NAME=apache/airflow:2.10.3
AIRFLOW__CORE__FERNET_KEY=YOUR_FERNET_KEY
_AIRFLOW_WWW_USER_USERNAME=admin
_AIRFLOW_WWW_USER_PASSWORD=admin

POSTGRES_HOST_PORT=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres

aPOSTGRES_USER=airflow
aPOSTGRES_PASSWORD=password123
aPOSTGRES_DB=airflow_db

fPOSTGRES_USER=travel_diary_user
fPOSTGRES_PASSWORD=password123
fPOSTGRES_DB=travel_diary

```
_AIRFLOW_WWW_USER_USERNAME и _AIRFLOW_WWW_USER_USERNAME это для входа в веб админку, остальное вроде понятно)
