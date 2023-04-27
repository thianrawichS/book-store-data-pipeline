# Book store transaction Data pipeline
The transaction's data of customers who purchased the book.
- This data pipeline built to find the specific of data like :
  - What is the best selling book and category?
  - Which country do most customers come from?
- most of the process in this pipeline uses GCP's environment.
## Data Pipeline Architecture 
<img src="https://github.com/chinxtd/book-store-data-pipeline/blob/main/image/BOOK%20STORE%20DATA%20PIPELINE.png" alt="data_architecture">

## Technology Stack
- Data Lake: Google Cloud Storage(GCS) 
- Data Warehouse: Google BigQuery
- Workflow Orchestration: Apache Airflow/ Google Cloud Composer(fully managed workflow orchestration service built on Apache Airflow)
- Transformation: Pandas
- Visualization: Looker Studio

## Data Description
| Column Name | Description |  
| :--- | :--- |  
| user_id | This field represents the identifier for user that purchased the book |			
| country	| This field represents the country of origin or location for the customers |
| Book_ID	|	This field represents the identifier for each book in the store |	
| Book_Title	|	The title of the book	|
| Book_Subtitle	|	The subtitle of the book, provides additional context or detail about the content of the book. |
| Book_Author	|	Author of the book |
| Book_Narrator	| Narrator of the audiobook	|
| Audio_Runtime	|	This field represents the total duration of the audiobook |		
| Audiobook_Type | This field represents the type of audiobook |
| Categories	|	This field represents the categories that the book belongs to |
| Rating	|	This field represents the average rating of the book |	
| Total_No__of_Ratings	|	This field represents the total number of ratings that the book has received. |
| Price	|	The price of the book in the local currency	(USD) |
| date	|	The date the book has been purchased |		
| conversion_rate	|	the conversion rate of [ USD - THB ] changed by the date of purchasing |
| THBPrice | The price of the book in Thai baht |

## Replication
- to perform the same output you need to:
  - First, go to GCP and create the account to get Free credits
  - Go to Cloud Composer
    - create Airflow environments (This step will automatically create bucket in Google Cloud Storage)
  - Open Cloud Shell Editor, then upload the DAGs.py 
  - Open Cloud Shell Terminal, cd to DAGs.py's directory
    - uses command " gsutil cp DAGs.py gs://***your bucketname***/dags "
  - Go to BigQuery and create dataset (make sure the path in the ***t4*** of DAGs.py is set to this dataset.)
  - Go to Cloud Composer
    - Go to ***your composer environment's name***
      - Go to PYPI Packages
      - add modules : pandas, pymysql, requests (leave the "extra version" blanked)
    - open the Airflow
      - set the connection of "my_sql_default" (host,user_id,password,...)
  - if nothing wrong, your dags's graph view will look like picture below
  <img src="https://github.com/chinxtd/book-store-data-pipeline/blob/main/image/DAGs%20Graph%20view.png" alt="dags_graph_view">
  
  ### ***don't forget to delete the Cloud Composer Environment after finished, the price is quite high.***
  

## Dashboard / Visualization
To visualize this data with looker studio:
- go to https://lookerstudio.google.com/
- Create Datasource > link your table/view from BigQuery
- Create a Blank Report and design your own's dashboard

### Overview
<img src="https://github.com/chinxtd/book-store-data-pipeline/blob/main/dashboard/Overview.png" alt="overview_data">

### Book by Revenue 
<img src="https://github.com/chinxtd/book-store-data-pipeline/blob/main/dashboard/Book-by-Revenue.png" alt="book_revenue_data">
