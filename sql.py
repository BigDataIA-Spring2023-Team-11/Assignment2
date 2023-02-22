import os
import logging
import sqlite3
import streamlit as st
import pandas as pd
from pathlib import Path
import boto3
import re
# from aws_geos import get_meta_data_for_db_population

# from aws_geos import get_files_from_noaa_bucket

LOGLEVEL  =  os.environ.get('LOGLEVEL','INFO').upper()

logging.basicConfig(
format='%(asctime)s %(levelname)-85 % (message)s',
level=LOGLEVEL,
datefmt='%Y-%m-%d %H:%M:%S')


#db name
database_file_name = "meta.db"
database_file_path  = os.path.join(os.path.dirname(__file__),database_file_name)



def create_df():
    data = get_meta_data_for_db_population()
    df = pd.DataFrame(data, columns = ['year', 'day', 'hour'])
    df = df.reset_index(drop=True)
    print("insidedf")
    return df

def create_table_in_db():
    conn = sqlite3.connect(database_file_path)
    # Insert data to table here

    df = create_df()
    df.to_sql("goes_meta", conn, if_exists = "replace")
    print(f"Data updated to table --> {df.shape}")
    # cursor.executescript(sql_script)
    conn.close()

def create_database():
    db = sqlite3.connect(database_file_path)
    cursor = db.cursor()
    db.commit()
    db.close()

def check_database_initilization():
    print(os.path.dirname(__file__))
    if not Path(database_file_path).is_file():
        logging.info(f"Database file not found, initilizing at: {database_file_path}")
        create_database()
        create_table_in_db()
    else:
        logging.info("Database file already exist")
        create_table_in_db()

@st.cache
def fetch_data_from_table_goes():
    conn = sqlite3.connect(database_file_path)
    df = pd.read_sql('SELECT * FROM goes_meta', conn)
    return df


"""
Arguments : Directory of the bucket
returns : list of all files from the dir
"""
def get_files_from_noaa_bucket(dir):
    files_from_bucket = []
    s3_client = boto3.client("s3",region_name="us-east-1",
                      aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
                      aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'))
    paginator = s3_client.get_paginator('list_objects_v2')
    noaa_bucket = paginator.paginate(Bucket = "noaa-goes18",Prefix = dir) #,PaginationConfig  = {"PageSize":2}
    for count,page in enumerate(noaa_bucket):
        files = page.get("Contents")
        for file in files:
            files_from_bucket.append(file['Key'])
            # print(file['Key'])
            # f = open("output.txt", "a")
            # print(f"{file['Key']}",file = f)
    # print(files_from_bucket)
    return  files_from_bucket

"""
takes file name and matches regex to get year,day and hour details of each file and returns list of [year,day,hour]
"""
def get_meta_data_for_db_population():
    meta_data_for_db = []
    files = get_files_from_noaa_bucket("ABI-L1b-RadC")
    for file in files:
        ydh = []
        match = re.findall(r"(\d{4})(\d{3})(\d{2})",file)
        # match = pattern.search(file)
        if match:
            year = match[0][0]
            day = match[0][1]
            hour = match[0][2]
            ydh.extend([year,day,hour])
            if ydh not in meta_data_for_db:
                meta_data_for_db.append(ydh)
    return meta_data_for_db


# if __name__ == "__main__":
#     # check_database_initilization