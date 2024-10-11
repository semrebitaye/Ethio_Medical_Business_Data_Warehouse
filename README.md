 ### Ethiopian Medical Business Data Warehouse

 #### Overview
This project involves the development of a robust data warehouse to store and analyze data from Ethiopian medical businesses. It includes data scraping from various sources including Telegram channels, data cleaning, object detection using YOLO, and API exposure using FastAPI. The goal is to facilitate comprehensive data analysis and decision-making in the healthcare sector.

#### Business Need
Kara Solutions aims to centralize data on Ethiopian medical businesses to enable stakeholders to derive valuable insights through advanced analytics. The data warehouse enhances operational efficiency and strategic planning by providing a unified platform for data integration and analysis.

#### Project Components
#### Data Scraping and Collection Pipeline

    Telegram Scraping: Utilize Telegram API and custom scripts to extract data from relevant channels such as DoctorsET, Chemed, lobelia4cosmetics, yetenaweg, and others listed on et.tgstat.com/medicine.
    Image Scraping: Collect images from specified Telegram channels for object detection.
    Storing Raw Data: Store scraped data in a temporary storage location (e.g., local database) before further processing.
    Monitoring and Logging: Implement logging to track scraping progress, errors, and monitor pipeline performance.

##### Setup Instructions Data Scraping
##### 1, Clone the Repository:
git clone https://github.com/juniorworku/ethiopian-medical-business-data-warehouse.git
cd ethiopian-medical-business-data-warehouse
##### 2, Install Dependencies:-
pip install -r requirements.txt
##### 3, Telegram Scraping Setup:-
    Create a Telegram API account and generate API credentials. -Update telegram_scraper.py with your API credentials and channels to scrape.
##### 4, Image Scraping Setup:-
    Ensure Python packages like telethon are installed for Telegram image scraping. -Modify download_images.py to specify image collection from relevant Telegram channels.
##### 5, Logging Setup:-
    Implement logging in telegram_scraping.py and image_scraping.py to monitor scraping processes.

#### Data Cleaning and Transformation
##### Data Cleaning:
    Remove duplicates, handle missing values, standardize formats, and validate data integrity.
##### Database Storage:
    Design database schemas for cleaned data and use DBT for transformation tasks.
##### DBT for Data Transformation:
    Define SQL models to transform data and ensure quality using testing and documentation features.
##### Monitoring and Logging:
    ontinue logging practices to monitor cleaning and transformation processes.

#### Setup Instructions for Data Cleaning and Transformation
##### 1, Ensure Database Setup: 
    Configure database.py with your database connection URL (e.g., PostgreSQL). 
    DATABASE_URL = "postgresql://user:password@localhost/dbname"
##### 2, Install DBT (Data Build Tool):
    pip install dbt
    dbt init ethiopian_medical_project
##### 3, Define DBT Models:
    Create SQL files in the models directory for data transformations. -Use dbt run to execute transformations and load data into the data warehouse.
##### 4, Testing and Documentation:
    Implement tests (dbt test) and generate documentation (dbt docs generate) for transformed data.

#### Object Detection Using YOLO
