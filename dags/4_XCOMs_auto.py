from airflow.sdk import dag, task 


@dag(
        dag_id="xcoms_dag_auto",
)
def xcoms_dag_auto():

    @task.python
    def first_task():
        print("Extracting data... This is the first task")
        fetched_data = {"data": [1, 2, 3, 4, 5]}
        return fetched_data


    @task.python
    def second_task(data:dict):
        fetched_data = data['data']
        transformed_data = fetched_data*2
        transformed_data_dict = {"transf_data":transformed_data}
        return transformed_data_dict


    @task.python
    def third_task(data:dict):
        load_data = data
        return load_data 
        
    
    # Defining task dependencies
    first = first_task()
    second = second_task(first)
    third = third_task(second)
    


# Instantiating the DAG
xcoms_dag_auto()