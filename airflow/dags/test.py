from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests


def get_motions(**context):
    try:
        url = "http://fastapi:8000/motion"
        response = requests.get(url)
        response.raise_for_status()  # Поднимет исключение для статусов ошибок
        result = response.json()
        return result
    except requests.exceptions.RequestException as e:
        print("Error occurred:", e)
        raise

def print_motions(**context):
    motions = context['ti'].xcom_pull(task_ids='get_motions')
    for item in motions:
        print(item)
    print("RETURNED FROM GET MOTIONS: ", motions)

def enhance_nn(**context):
    try:
        url = "http://host.docker.internal:8081/"
        motions = context['ti'].xcom_pull(task_ids='get_motions')
        result = []
        for motion in motions:
            # Удаляем поле id, если оно не требуется
            motion_data = {
                "user_imei": str(motion.get("user_imei", "default")),
                "acceleration_x": float(motion.get("acceleration_x", 0.0)),
                "acceleration_y": float(motion.get("acceleration_y", 0.0)),
                "acceleration_z": float(motion.get("acceleration_z", 0.0)),
                "gyro_x": float(motion.get("gyro_x", 0.0)),
                "gyro_y": float(motion.get("gyro_y", 0.0)),
                "gyro_z": float(motion.get("gyro_z", 0.0)),
                "magnetometer_x": float(motion.get("magnetometer_x", 0.0)),
                "magnetometer_y": float(motion.get("magnetometer_y", 0.0)),
                "magnetometer_z": float(motion.get("magnetometer_z", 0.0)),
                "pressure": float(motion.get("pressure", 0.0)),
                "label_id": int(motion.get("label_id", 0)),
                "time": int(motion.get("time", 0)),
            }
            response = requests.post(url, json=motion_data)
            response.raise_for_status()
            result.append(response.json())
        
        return result
    except requests.exceptions.RequestException as e:
        print("Error occurred:", e)
        raise


def save_enhanced_nn(**context):
    pass


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
    
    task_get_motions = PythonOperator(
        task_id='get_motions',
        python_callable=get_motions,
        provide_context=True
    )

    task_print_motions = PythonOperator(
        task_id='print_motions',
        python_callable=print_motions,
        provide_context=True
    )

    task_enhance_nn = PythonOperator(
        task_id='enhance_nn',
        python_callable=enhance_nn,
        provide_context=True
    )

    task_save_enhanced_nn = PythonOperator(
        task_id='save_enhanced_nn',
        python_callable=save_enhanced_nn,
        provide_context=True
    )

    task_get_motions >> task_print_motions >> task_enhance_nn
