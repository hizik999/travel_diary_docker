from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests


def get_labels(**context):
    try:
        response = requests.get("http://fastapi:8000/label/")
        response.raise_for_status()  # Поднимет исключение для статусов ошибок
        result = response.json()
        return result
    except requests.exceptions.RequestException as e:
        print("Error occurred:", e)
        raise

def print_labels(**context):
    labels = context['ti'].xcom_pull(task_ids='get_labels')
    print("RETURNED FROM GET LABELS: ", labels)

default_args = {
    'owner': 'andrey',
    'retries': 1,
    'retry_delay': timedelta(seconds=10),
}

with DAG(
    dag_id='test',
    default_args=default_args,
    description='Get labels from Postgres',
    schedule_interval=timedelta(minutes=10),
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:
    
    task_get_labels = PythonOperator(
        task_id='get_labels',
        python_callable=get_labels,
        provide_context=True
    )

    tasl_print_labels = PythonOperator(
        task_id='print_labels',
        python_callable=print_labels,
        provide_context=True
    )

    task_get_labels >> tasl_print_labels
