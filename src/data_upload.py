import os
import pandas as pd
import argparse
import pyarrow.parquet as pa 

from time import time
from sqlalchemy import create_engine, exc

# DIRETÓRIOS PRINCIPAIS
WORK_DIR = '/app'
DATA_DIR = os.path.join(WORK_DIR, 'data')
print("* ", DATA_DIR)

parser = argparse.ArgumentParser(description = ' Ingestão do arquivo parquet para o Postgres')


def main(params):

    user      = params.user
    password  = params.password
    host      = params.host
    port      = params.port
    db        = params.db
    table     = params.table
    url       = params.url
    file_name = 'yellow_tripdata_2022-01.parquet'
    file_path =  os.path.join(DATA_DIR,file_name)

    # BAIXANDO O ARQUIVO FONTE
    os.system(f"wget {url} -O {file_path}")

    # CONECTANDO AO SERVIDOR POSTGRES    
    engine = create_engine( f'postgresql://{user}:{password}@{host}:{port}/{db}' )
    try:
        engine.connect()
        print('* Conexão realizada com sucesso')
    except exc.SQLAlchemyError: 
        pass


    # CRIANDO SCHEMA E TABELA
    df = pd.read_parquet(file_path)
    print('* Numbers of rows in parquet file {}'.format( df.shape[0]) )

    # Cria a tabela ou subscreve se já existir.
    df.head(n=0).to_sql(name= table, con=engine, if_exists='replace')


    # UPLOAD DE DADOS
    parquet_file = pa.ParquetFile(file_path)

    # Carregando dados na tabela em chunks

    count = 0            # Acumulador, computa o número de chunks a cada rodada.
    count_rows = 0       # Acumulador, computa o total de linhas carregadas.
    count_seconds = 0    # Acumulador, computa o tempo em segundos de cada carga.

    for batch in parquet_file.iter_batches():

        t_start = time() # start upload
        
        count +=1

        batch_df = batch.to_pandas()

        batch_df.to_sql( name= table, con=engine, if_exists='append')

        t_end = time() # end upload     


        print('* ... Upload number {:02d} with {} rows, loaded in {:.3f} seconds'.format(count,batch_df.shape[0] , (t_end - t_start)))

        # Log Geral
        count_rows += batch_df.shape[0]
        count_seconds += t_end - t_start

    print('Carga executada em {:.3f} segundos com total de {}'.format(count_seconds, count_rows))

if __name__ == "__main__":

    parser.add_argument('--user',     help='usuário dpara o postgres')
    parser.add_argument('--password', help='password para o postgres')
    parser.add_argument('--host',     help='host para postgres')
    parser.add_argument('--port',     help='porta do banco de dados postgres')
    parser.add_argument('--db',       help='nome do banco de dados no postgres')
    parser.add_argument('--table',    help='tabela do banco de dados postgres')
    parser.add_argument('--url',      help='url do arquivo parquet fonte')

    args = parser.parse_args()
    
    main(args)
