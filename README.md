# Book-store-transaction-data-pipeline
This project was created as part of R2DE's course 

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
