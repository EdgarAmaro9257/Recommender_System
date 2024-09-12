from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import psycopg2

def extract_data():
    conn = psycopg2.connect("dbname=recommendations user=airflow password=airflow")
    query = "SELECT * FROM interactions"
    df = pd.read_sql(query, conn)
    return df

def transform_data(df):
    # Realiza transformación de datos (por ejemplo, normalización de ratings)
    df['rating'] = df['rating'] / df['rating'].max()
    return df

def load_data(df):
    # Guardar datos transformados de vuelta en PostgreSQL
    conn = psycopg2.connect("dbname=recommendations user=airflow password=airflow")
    df.to_sql('interactions_transformed', conn, if_exists='replace')

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 9, 1),
}

with DAG('etl_pipeline', default_args=default_args, schedule_interval='@daily') as dag:
    extract_task = PythonOperator(task_id='extract_data', python_callable=extract_data)
    transform_task = PythonOperator(task_id='transform_data', python_callable=transform_data)
    load_task = PythonOperator(task_id='load_data', python_callable=load_data)

    extract_task >> transform_task >> load_task
