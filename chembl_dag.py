from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow import DAG
from datetime import datetime, timedelta

# Define the DAG
chembl_data_dag = DAG(dag_id='chembl_traning_data_update',
                         description='Get Hlm activities data from chembl',
                         schedule_interval='@daily',
                         start_date=datetime(2024,10,13))

# Define the tasks
task1 = BashOperator(task_id='get data',
                     bash_command='python '+'crawler.py',
                     dag= chembl_data_dag)

task2 = BashOperator(task_id='Create_dataset_Table',
                       bash_command='python '+'data.py',
                       dag= chembl_data_dag)


task1>>task2
    
print('Done')