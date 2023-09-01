from datetime import datetime
from airflow import DAG
from airflow.operators.pyton_operator import PythonOperator

#define work function
def print_hw():
    print("hello")
def print_gb():
    print("Goodbye")

#prepare dag
test_dag = DAG("test_DAG", 
               schedule_interval = None,
               start_date = datetime(2023,9,1))

#prepare task id
TASK_ONE = 'task_one'
TASK_TWO = 'task_two'

with test_dag:
    first_task = PythonOperator(
        task_id = TASK_ONE,
        python_callable = print_hw
    )
    second_task = PythonOperator(
        task_id = TASK_TWO,
        python_callable = print_gb
    )
    #task direction
    first_task >> second_task