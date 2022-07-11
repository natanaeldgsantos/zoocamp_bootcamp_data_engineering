#!/bin/bash


# Remove containers com o mesmo nome, se existirem.
sudo docker rm pg-database --force
sudo docker rm pgadmin --force

# Criando a Rede, se ainda não existir.
docker network create pg-network


# Subindo o servidor Postgres
sudo docker run -d \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB='ny_taxi' \
    -v $(pwd)/src/data/ny_taxi_postgres_data:/var/lib/postgresql/data \
    --network=pg-network \
    --name pg-database \
    -p 5432:5432 \
    postgres:13

echo
echo "* Servidor Postgres inicializado com sucesso"
echo

# Subindo o PgAdmin
sudo docker run -d \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=pg-network \
    --name pgadmin \
    dpage/pgadmin4

echo
echo "* PgAdmin Inicializado com sucesso"
echo

URL="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet"

: '
python src/data_upload.py \
 --user=root \
 --password=root \
 --host=localhost \
 --port=5432 \
 --db=ny_taxi \
 --table=tb_yellow_taxis \
 --url=${URL}
'

 # Construindo o container python 
 sudo docker build -t taxi_ingest:01 -f $PWD/src/containers/Dockerfile_python_machine .

echo
echo "* Container Python inicializado com sucesso"
echo

# Subindo o container python
 docker run -it \
   --network=pg-network \
   taxi_ingest:01 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table=tb_yellow_taxis \
    --url=${URL}
