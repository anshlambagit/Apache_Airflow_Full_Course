from airflow.sdk import dag, task 


@dag(
        dag_id="xcoms_dag_kwargs",
)
def xcoms_dag_kwargs():

    @task.python
    def first_task(**kwargs):

        # Extracting 'ti' from kwargs to push XComs manually
        ti = kwargs['ti']
        
        print("Extracting data... This is the first task")
        fetched_data = {"data": [1, 2, 3, 4, 5]}
        ti.xcom_push(key='return_result', value=fetched_data)


    @task.python
    def second_task(**kwargs):
        
        ti = kwargs['ti']

        # Pulling XComs pushed by the first task
        fetched_data = ti.xcom_pull(task_ids='first_task', key='return_result')['data']
        print("Transforming data... This is the second task")

        transformed_data = fetched_data*2
        transformed_data_dict = {"transf_data":transformed_data}
        
        ti.xcom_push(key='return_result', value=transformed_data_dict)


    @task.python
    def third_task(**kwargs):
        ti = kwargs['ti']
        load_data = ti.xcom_pull(task_ids='second_task', key='return_result')
        return load_data 
        
    
    # Defining task dependencies
    first = first_task()
    second = second_task()
    third = third_task()

    first >> second >> third
    


# Instantiating the DAG
xcoms_dag_kwargs()