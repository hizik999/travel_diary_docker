from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logics.functions as f


default_args = {
    'owner': 'andrey',
    'retries': 1,
    'retry_delay': timedelta(seconds=10),
}

def create_task(task_id, python_callable):
    return PythonOperator(
        task_id=task_id,
        python_callable=python_callable,
        trigger_rule='all_success',
        provide_context=True
    )

with DAG(
    dag_id='update_labels_dag',
    default_args=default_args,
    description='Get labels from Postgres',
    schedule_interval=timedelta(minutes=10),
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:
    
    task_get_motions = create_task('get_motions', f.get_motions)
    task_enhance_nn = create_task('enhance_nn', f.enhance_nn)
    task_save_enhanced_nn = create_task('save_enhanced_nn', f.save_enhanced_nn)
    
    task_get_motions >> task_enhance_nn >> task_save_enhanced_nn
