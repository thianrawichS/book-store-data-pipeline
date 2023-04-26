from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.utils.dates import days_ago
from airflow.decorators import task,dag
from airflow.operators.bash import BashOperator
import pandas as pd
import requests


MYSQL_CONNECTION = "mysql_default"
CONVERSION_RATE_URL = "https://r2de2-workshop-vmftiryt6q-ts.a.run.app/usd_thb_conversion_rate"
default_args = {}


#OUTPUT PATH
mysql_output_path = "/home/airflow/gcs/data/audible_data_merged.csv"
conversion_rate_output_path = "/home/airflow/gcs/data/conversion_rate.csv"
final_output_path = "/home/airflow/gcs/data/output.csv"


@task()
def get_data_from_mysql(data_target_path):

    #get the data from DATABASE
    mysqlserver = MySqlHook(MYSQL_CONNECTION)
    audible_data = mysqlserver.get_pandas_df(sql="SELECT * FROM audible_data")
    audible_transaction = mysqlserver.get_pandas_df(sql="SELECT * FROM audible_transaction")
    
    #merge both table
    df = audible_transaction.merge(audible_data,how="left", left_on="book_id", right_on="Book_ID")

    #load to csv
    df.to_csv(data_target_path, index=False)
    print(f"output to {data_target_path}")


@task()
def get_conversion_rate(conversion_target_path):

    #get data from api
    response_data = requests.get(CONVERSION_RATE_URL).json()
    df = pd.DataFrame(response_data)

    #change index name to "date" column
    df = df.reset_index().rename(columns={"index":"date"})

    #load to csv
    df.to_csv(conversion_target_path, index=False)
    print(f"output to {conversion_target_path}")


@task()
def get_merge_data(data_target_path, conversion_target_path, output_path):
    #get both table
    transaction = pd.read_csv(data_target_path)
    conversion_rate = pd.read_csv(conversion_target_path)

    #convert the timestamp to date(yyyy-MM-dd) so it can join with conversion rate's date
    #create new column "date"
    transaction['date'] = transaction['timestamp']
    transaction['date'] = pd.to_datetime(transaction['date']).dt.date
    conversion_rate['date'] = pd.to_datetime(conversion_rate['date']).dt.date

    #merge both table
    final_df = transaction.merge(conversion_rate, how="left", left_on="date", right_on="date")

    # remove '$' from price and covert to float so it can convert by conversion rate
    final_df['Price'] = final_df['Price'].str.replace('$','').astype('float64')

    #drop previous date column (timestamp)
    final_df.drop(['timestamp','book_id'], axis=1, inplace=True)

    #ADD COLUMN 'THBPrice' by multiply price by conversion rate
    final_df['THBPrice'] = final_df['Price']*final_df['conversion_rate']

    #load to csv
    final_df.to_csv(output_path, index=False)
    print(f"output to {output_path}")


@dag(default_args=default_args, start_date=days_ago(1), schedule_interval="@once", tags=["workshop"])
def dag_taskflow():
    
    t1 = get_data_from_mysql(mysql_output_path)
    t2 = get_conversion_rate(conversion_rate_output_path)
    t3 = get_merge_data(mysql_output_path,conversion_rate_output_path,final_output_path)    
    t4 = BashOperator(
        bash_command="bq load \
            --source_format=CSV \
            --autodetect \
            workshop5.audible_data \
            gs://asia-southeast1-ws5-8cccf362-bucket/data/output.csv",
        task_id="upload_to_bq"
    )
    #task dependencies
    [t1,t2] >> t3 >> t4


dag_execute = dag_taskflow()