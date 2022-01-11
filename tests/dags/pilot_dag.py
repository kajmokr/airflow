from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.docker_operator import DockerOperator

from datetime import datetime

default_args = {
    'start_date': datetime(2019, 1, 1),
    'owner': 'Airflow',
    'email': 'owner@test.com'
}

def process_init(p1):
    print(p1)
    return 'init'

def process_done(p2):
    print(p2)
    return 'done'

with DAG(dag_id='parallel_dag', schedule_interval='0 0 * * *', default_args=default_args, catchup=False) as dag:
    
    # Tasks dynamically generated 
    task_1 = BashOperator(task_id='task_1', bash_command='echo "DAG Started"')

    task_2 = PythonOperator(task_id='task_2', python_callable=process_init, op_args=['my super parameter'])

    task_3 = BashOperator(task_id='task_3', bash_command='echo "init done"')

    task_4 = DockerOperator(
        task_id='task_4',
        image='kajmokr/airflow:220105a',#'harbor.accuinsight.net/aiip/aiip-tuning/modeler-common:aiip-dev',
        api_version='auto',
        auto_remove=True,
        command="/bin/sleep 30",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge"
    )

    task_5 = PythonOperator(task_id='task_2', python_callable=process_done, op_args=['my super parameter'])

    task_1 >> task_2 >> task_3 >> task_4 >> task_5
        