чтобы перезапустить контейнер и подтянуть новые значения из .env
```bash
docker-compose down --volumes --remove-orphans
docker-compose up -d
```