from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="test_python",
    schedule="0 0 * * *",
    start_date= datetime(2021, 1, 1),
    catchup=False,
) as dag:
    run_this = BashOperator(
        task_id="run_after_loop",
        bash_command="echo HELLO",
    )

    run_this1 = BashOperator(
        task_id="run_after_loop1",
        bash_command="echo HELLO",
    )

    run_this >> run_this1