import os
import logging
import sqlite3
from pathlib import Path

import pandas as pd
# from pathlib import Path
# from aws_nexrad import get_meta_data_for_db_population
import boto3
import streamlit as st
from dotenv import load_dotenv

#
# from dotenv import load_dotenv
#
# aws_client = boto3.client('s3',region_name = 'us-east-1',aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),aws_secret_access_key = os.environ.get('AWS_SECRET_KEY'))
#
# bucket = "noaa-nexrad-level2"
#
# # from aws_nexrad import get_meta_data_for_db_population
#
# LOGLEVEL  =  os.environ.get('LOGLEVEL','INFO').upper()
#
# logging.basicConfig(
# format='%(asctime)s %(levelname)-85 % (message)s',
# level=LOGLEVEL,
# datefmt='%Y-%m-%d %H:%M:%S')
#
#
load_dotenv() # to load environments from .env file
#
#
database_file_name = "meta.db"
# # ddl_file_name = ""
database_file_path  = os.path.join(os.path.dirname(__file__),database_file_name)
# # ddl_file_path  = os.path.join(os.path.dirname(__file__),ddl_file_name)
#
# years = []
# months = []
# days = []
# station = set()
#
# prefix = ""
# result = aws_client.list_objects(Bucket=bucket, Prefix=prefix, Delimiter="/")
# for o in result.get("CommonPrefixes"):
#     years.append(o.get("Prefix"))
#
# for year in years:
#     prefix = year
#     result = aws_client.list_objects(Bucket=bucket, Prefix=prefix, Delimiter="/")
#     for o in result.get("CommonPrefixes"):
#         months.append(o.get("Prefix"))
#
# for month in months:
#     prefix = month
#     result = aws_client.list_objects(Bucket=bucket, Prefix=prefix, Delimiter="/")
#     for o in result.get("CommonPrefixes"):
#         days.append(o.get("Prefix"))
#
# for day in days:
#     prefix = day
#     result = aws_client.list_objects(Bucket=bucket, Prefix=prefix, Delimiter="/")
#     for o in result.get("CommonPrefixes"):
#         meta_data = o.get("Prefix").split("/")
#         station.add(
#             (meta_data[0], meta_data[1], meta_data[2], meta_data[3])
#         )
#
# conn = sqlite3.connect("meta.db")
# cursor = conn.cursor()
# cursor.execute("DROP TABLE IF EXISTS nexrad")
# # Create a new table
# cursor.execute(
#     "CREATE TABLE IF NOT EXISTS nexrad (year text, month text, day text, station text)"
# )
# for data in station:
#     year, month, day, station = data
#     cursor.execute(
#         "INSERT INTO nexrad VALUES (?, ?, ?, ?)",
#         (year, month, day, station),
#     )
# conn.commit()
# conn.close()
#

def create_df():
    # year = [2022] * 51 * 24 + [2023] * 32 * 24
    # days_with_leading_zeros = []
    # for i in range(1,33):
    #     days_with_leading_zeros.append(str(i).zfill(3))
    # day = list(range(209, 260)) * 24 + days_with_leading_zeros * 24
    # first_ten_hours = []
    # for i in range(0,10):
    #     first_ten_hours.append(str(i).zfill(2))
    # hour =  (first_ten_hours + list(range(10, 24))) * 83
    # data = {"year": year, "day": day, "hour": hour}
    # data = get_meta_data_for_db_population()
    # df = pd.DataFrame(data, columns = ['year', 'month', 'day', 'stationid'])
    # df = df.reset_index(drop=True)
    # print("insidedf")
    # return df
    return


def create_table_in_db():
    conn = sqlite3.connect(database_file_path)
    # Insert data to table here

    df = create_df()
    print(df,"dddddddddddddddddddddddddddddddddddddddd")
    df.to_sql("nexrad", conn, if_exists = "replace")
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











def get_files_from_nexrad_bucket(dir):
    files_from_nexrad_bucket = []
    s3_client = boto3.client("s3",region_name="us-east-1",
                      aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
                      aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'))
    paginator = s3_client.get_paginator('list_objects_v2')
    nexrad_bucket = paginator.paginate(Bucket = "noaa-nexrad-level2",Prefix = dir) #,PaginationConfig  = {"PageSize":2}
    for count,page in enumerate(nexrad_bucket):
        files = page.get("Contents")
        for file in files:
            files_from_nexrad_bucket.append(file['Key'])
            # print(file['Key'])
            # f = open("output1.txt", "a")?\
            # print(f"{file['Key']}",file = f)
    # print(files_from_nexrad_bucket)
    logging.info("Files extracted from Nexrad bucket")
    return  files_from_nexrad_bucket




@st.cache
def fetch_data_from_table_nexrad():
    conn = sqlite3.connect(database_file_path)
    df = pd.read_sql('SELECT * FROM nexrad', conn)
    logging.info("Data Loaded")
    return df
#
# #     df = create_df()
# #     df.to_sql("nexrad_metadata", conn, if_exists = "replace")
# #     print(f"Data updated to table --> {df.shape}")
# #     # cursor.executescript(sql_script)
# #     conn.close()
#
# # def create_database():
# #     db = sqlite3.connect(database_file_path)
# #     cursor = db.cursor()
# #     db.commit()
# #     db.close()
#
# # def check_database_initilization():
# #     print(os.path.dirname(__file__))
# #     if not Path(database_file_path).is_file():
# #         logging.info(f"Database file not found, initilizing at: {database_file_path}")
# #         create_database()
# #         create_table_in_db()
# #     else:
# #         logging.info("Database file already exist")
# #         create_table_in_db()
#
# # if __name__ == "__main__":
# #     check_database_initilization()