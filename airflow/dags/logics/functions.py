import requests

def get_motions(**context):
    try:
        url = "http://fastapi:8000/motion/"
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
            response = requests.post(url, json=motion)
            response.raise_for_status()
            result.append(response.json())
        
        return result
    except requests.exceptions.RequestException as e:
        print("Error occurred:", e)
        raise


def save_enhanced_nn(**context):
    enhanced_nn = context['ti'].xcom_pull(task_ids='enhance_nn')
    for item in enhanced_nn:
        try:
            url = f"http://fastapi:8000/motion?motion_id={item.get('id')}&label_id={item.get('label_id')}"
            response = requests.put(url)
            response.raise_for_status()  # Поднимет исключение для статусов ошибок
            result = response.json()
            return result
        except requests.exceptions.RequestException as e:
            print("Error occurred:", e)
            raise