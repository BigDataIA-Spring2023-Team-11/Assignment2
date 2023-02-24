import os
import logging
import sqlite3
import pandas as pd
from pathlib import Path

LOGLEVEL  =  os.environ.get('LOGLEVEL','INFO').upper()

logging.basicConfig(
format='%(asctime)s %(levelname)-85 % (message)s',
level=LOGLEVEL,
datefmt='%Y-%m-%d %H:%M:%S')



database_file_name ="meta.db"
# ddl_file_name = ""
database_file_path  = os.path.join(os.path.dirname(__file__),database_file_name)
# ddl_file_path  = os.path.join(os.path.dirname(__file__),ddl_file_name)

def create_df():
    df = pd.read_csv("nexrad1.csv")
    print(df)
    return df

def create_table_in_db():
    conn = sqlite3.connect(database_file_path)
    # Insert data to table here

    df = create_df()
    df.to_sql("latlong", conn, if_exists = "replace")
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


def fetch_data_from_table():
    conn = sqlite3.connect(database_file_path)
    df = pd.read_sql('SELECT * FROM latlong', conn)
    return df


if __name__ == "__main__":
    check_database_initilization()