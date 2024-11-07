from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta



default_args = {
    'owner': 'andrew',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id="my_first_dag_v2",
    description="My First DAG",
    start_date=datetime(2023, 11, 6),
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command="echo 'hello, world!'"
    )

    task2 = BashOperator(
        task_id='second_task',
        bash_command="echo 'hello, again!'"
    )

    task1 >> task2