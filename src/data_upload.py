import os
from time import time

import pandas as pd
import pyarrow.parquet as pa 


from sqlalchemy import create_engine, exc

from dotenv import load_dotenv
load_dotenv()

# DIRETÓRIOS PRINCIPAIS
WORK_DIR = os.getcwd()
DATA_DIR = os.path.join(WORK_DIR, 'src/data')


# CONECTANDO AO SERVIDOR POSTGRES
user     = os.environ.get('USER_DB') 
password = os.environ.get('PASSWORD')

engine = create_engine( f'postgresql://{user}:{password}@localhost:5432/ny_taxi' )
try:
    engine.connect()
    print('* Conexão realizada com sucesso')
except exc.SQLAlchemyError: 
    pass


# CRIANDO SCHEMA E TABELA

file_path =  os.path.join(DATA_DIR,'yellow_tripdata_2022-01.parquet')

df = pd.read_parquet(file_path)
print('* Numbers of rows in parquet file {}'.format( df.shape[0]) )

# Cria a tabela ou subscreve se já existir.
df.head(n=0).to_sql(name='tb_yellow_taxis', con=engine, if_exists='replace')


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

    batch_df.to_sql( name='tb_yellow_taxis', con=engine, if_exists='append')

    t_end = time() # end upload     


    print('* ... Upload number {:02d} with {} rows, loaded in {:.3f} seconds'.format(count,batch_df.shape[0] , (t_end - t_start)))

    # Log Geral
    count_rows += batch_df.shape[0]
    count_seconds += t_end - t_start

print('Carga executada em {:.3f} segundos com total de {}'.format(count_seconds, count_rows))


