# Servidor Postgress com Docker Container

Este documento exemplifica como implementar um servidor postgress através de um container Docker. 

## Criando o container Postgress

    docker run -it \
        -e POSTGRES_USER="root" \        
        -e POSTGRES_PASSWORD="root" \
        -e POSTGRES_DB="ny_taxi" \
        -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
        -p 5432:5432 postgres:13

Após a criação do container abra um novo terminal e acese o servidor. Para isso vamos instalar o pacote pgcli do python para nos ajudar.

    pip install pgcli


Após a instalação do pgcli, abra um novo terminal e digite:

    pgcli -h <host> -U <username> -d <database_name>

Pronto agora estamos conectados ao servidor postgres. Para testar a conexão digite:

    \d  lista todos os bancos de dados no postgres


## Conectando o Postgres ao PgAdmin

Subindo o pgadmin docker container:

    docker run -it \
        -e PGADMIN_DEFAULT_EMAIL='admin@admin.com" \
        -e PGADMIN_DEFAULT_PASSWORD="root" \
        -p 8080:80 dpage/pgadmin4

