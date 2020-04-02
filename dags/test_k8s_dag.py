from datetime import datetime, timedelta
from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.utils.dates import days_ago

now = datetime.now()
now_to_the_hour = (
        now - timedelta(0, 0, 0, 0, 0, 3)
).replace(minute=0, second=0, microsecond=0)
START_DATE = now_to_the_hour
DAG_NAME = 'test_k8s_dag_v1'

default_args = {
    'owner': 'itay',
    'depends_on_past': True,
    'start_date': days_ago(2)
}
dag = DAG(DAG_NAME, schedule_interval='*/10 * * * *', default_args=default_args)
namespace = 'airflow'

with dag:
    k1 = KubernetesPodOperator(
        namespace=namespace,
        image="python:3.7-slim-buster",
        cmds=["bash", "-cx"],
        arguments=["echo", "10"],
        labels={"foo": "1"},
        name="test1",
        in_cluster=True,
        task_id="task1",
        is_delete_operator_pod=True,
        hostnetwork=False,
        priority_class_name="medium",
    )

with dag:
    k2 = KubernetesPodOperator(
        namespace=namespace,
        image="python:3.7-slim-buster",
        cmds=["bash", "-cx"],
        arguments=["echo", "20"],
        labels={"foo": "2"},
        name="test2",
        in_cluster=True,
        task_id="task2",
        is_delete_operator_pod=True,
        hostnetwork=False,
        priority_class_name="medium",
    )

with dag:
    k3 = KubernetesPodOperator(
        namespace=namespace,
        image="python:3.7-slim-buster",
        cmds=["bash", "-cx"],
        arguments=["echo", "30"],
        labels={"foo": "3"},
        name="test3",
        in_cluster=True,
        task_id="task3",
        is_delete_operator_pod=True,
        hostnetwork=False,
        priority_class_name="medium",
    )

k2.set_upstream(k1)
k3.set_upstream(k2)
