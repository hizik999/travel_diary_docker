from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Функция, которую мы будем запускать в задаче
def print_hello():
    print("Hello from Airflow!")

# Определяем параметры DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Создаем DAG
with DAG(
    'test_bash',
    default_args=default_args,
    description='A simple hello world DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    # Создаем задачу, которая вызывает функцию print_hello
    hello_task = PythonOperator(
        task_id='hello_task',
        python_callable=print_hello,
    )

    hello_task
