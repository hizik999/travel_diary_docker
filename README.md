чтобы перезапустить контейнер и подтянуть новые значения из .env
```bash
docker-compose down --volumes --remove-orphans
docker-compose up -d
```
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