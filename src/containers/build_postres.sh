#!/bin/bash

# Criando a Rede

# Remove rede se já existir
docker network rm pg-network

# Cria rede
docker network create pg-network

# Remove containers com o mesmo nome
sudo docker rm pg-database --force
sudo docker rm pgadmin --force

# Subindo o servidor Postgres
sudo docker run -d \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB='ny_taxi' \
    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
    --network=pg-network \
    --name pg-database \
    -p 5432:5432 \
    postgres:13


echo "* Servidor Postgres inicializado com sucesso"

# Subindo o PgAdmin
sudo docker run -d \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=pg-network \
    --name pgadmin \
    dpage/pgadmin4

echo "* PgAdmin Inicializado com sucesso"