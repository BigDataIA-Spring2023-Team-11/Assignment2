#system imports
import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import streamlit as st
import boto3
import os
import botocore
import logging
import pandas as pd
# from sql_credentials import verify_password
import hashlib

# from utils_goes_API import goes_get_my_s3_url
# from utils_nexrad_API import nexrad_get_my_s3_url

load_dotenv()
app = FastAPI()
#
# #custom imports
# from sql_goes import fetch_data_from_table_goes
# from sql_nexrad import  fetch_data_from_table_nexrad



database_file_name = "meta.db"
database_file_path  = os.path.join(os.path.dirname(__file__),database_file_name)

def hash_text(text):
    # Convert the text to bytes using UTF-8 encoding
    text_bytes = text.encode('utf-8')

    # Create a SHA-256 hash object
    sha256_hash = hashlib.sha256()

    # Update the hash object with the text bytes
    sha256_hash.update(text_bytes)

    # Get the hexadecimal representation of the hash
    hex_digest = sha256_hash.hexdigest()

    # Return the hexadecimal hash digest
    return hex_digest

def verify_password(db_password,given_password):
    flag = 0
    if str(hash_text(given_password)) == str(db_password):
        flag = 1
    return flag

# secret_key = "bullshit"
def goes_get_my_s3_url(filename):
    # print(dir_to_geos)
    print(filename)
    static_url = "https://damg7245-ass1.s3.amazonaws.com"
    filename_alone = filename.split("/")[-1]
    generated_url = f"{static_url}/{filename}"
    return generated_url


"""
return concatenated url of our s3 bucket
"""
def nexrad_get_my_s3_url(filename):
    static_url = "https://damg7245-ass1.s3.amazonaws.com"
    filename_alone = filename.split("/")[-1]
    generated_url = f"{static_url}/{filename}"
    return generated_url




@st.cache
def fetch_data_from_table_nexrad():
    conn = sqlite3.connect(database_file_path)
    df = pd.read_sql('SELECT * FROM nexrad', conn)
    logging.info("Data Loaded")
    return df
#
@st.cache
def fetch_data_from_table_goes():
    conn = sqlite3.connect(database_file_path)
    df = pd.read_sql('SELECT * FROM goes_meta', conn)
    return df

data_df_goes = fetch_data_from_table_goes()
data_df_nexrad = fetch_data_from_table_nexrad()

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





def copy_s3_file_if_exists(src_bucket_name, src_file_name, dst_bucket_name, dst_file_name):
    # session = boto3.Session(
    #     aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
    #     aws_secret_access_key=os.environ.get('AWS_SECRET_KEY')
    # )
    session = boto3.Session(region_name="us-east-1",
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_KEY')
    )
    print(os.environ.get('AWS_ACCESS_KEY'), "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

    s3 = session.resource('s3')
    src_bucket = s3.Bucket(src_bucket_name)

    copy_source = {
        'Bucket': src_bucket_name,
        'Key': src_file_name
    }
    dst_bucket = s3.Bucket(dst_bucket_name)

    try:
        dst_bucket.Object(dst_file_name).load()
        # print(f"Object {dst_file_name} already exists in destination bucket {dst_bucket_name}.")
        #already copied so flag 1
        flag = 1
    except botocore.exceptions.ClientError as e:

        if e.response['Error']['Code'] == "404":
            # st.markdown(f"File NOT found in dst bucket {e.response['Error']['Code']}")
            dst_bucket.copy(copy_source, dst_file_name)
            print(f"Object {src_file_name} copied from source bucket {src_bucket_name} to destination bucket {dst_bucket_name}.")
            #now copied so flat = 1
            flag = 1
        else:
            st.error("No Such File")
            #so such file to copy , so flag =0
            flag = 0
    return flag



def copy_s3_file(src_bucket_name, src_file_name, dst_bucket_name, dst_file_name):
    session = boto3.Session(region_name="us-east-1",
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_KEY')
    )
    flag = 0

    s3 = session.resource('s3')
    src_bucket = s3.Bucket(src_bucket_name)

    try:
        src_bucket.Object(src_file_name).load()
        # st.markdown(f"Here {src_bucket.Object(src_file_name).load()}")
        flag = copy_s3_file_if_exists(src_bucket_name, src_file_name, dst_bucket_name, dst_file_name)
        # st.markdown(flag)
        return flag

    except botocore.exceptions.ClientError as e:
        st.markdown("EXCEPTION")
        if e.response['Error']['Code'] == "404":
            st.error(f"File {src_file_name} not found in source bucket {src_bucket_name}.")
            # flag = 0
            return 0




class GoesUserInput(BaseModel):
    filename_with_dir:str
#

# selected_file is a full filename with dir structure
@app.post("/get_goes_url")
async def goes_copy_file_to_S3_and_return_my_s3_url_Api(selected_file:GoesUserInput):

    my_s3_file_url = ""
    src_bucket = "noaa-goes18"
    des_bucket = "damg7245-ass1"

    dir_list = str(selected_file.filename_with_dir).split("/")


    if dir_list[1] not in data_df_goes.year.unique().tolist():
        raise HTTPException(status_code=400, detail="Selected Year out of range")
    elif dir_list[2] not in data_df_goes[(data_df_goes.year == dir_list[1])].day.unique().tolist():
        raise HTTPException(status_code=400, detail="Selected Day out of range")
    elif dir_list[3] not in data_df_goes[(data_df_goes.year == dir_list[1]) & (data_df_goes.day == dir_list[2])].hour.unique().tolist():
        raise HTTPException(status_code=400, detail="Selected Hour out of range")
    else:
        # copying user selected file from AWS s3 bucket to our bucket
        copied_flag = copy_s3_file(src_bucket, selected_file.filename_with_dir, des_bucket, selected_file.filename_with_dir)

    # print(f"{copied_flag} -- flag")
    # copying user selected file from AWS s3 bucket to our bucket
    # copied_flag = copy_s3_file(src_bucket, selected_file, des_bucket, selected_file)
    # getting url of user selected file from our s3 bucket
    if copied_flag:
        my_s3_file_url = goes_get_my_s3_url(selected_file.filename_with_dir)
    else:
        raise HTTPException(status_code=404, detail="File not found")

    # return {'url': my_s3_file_url}
    return {'url':my_s3_file_url}






class NexradUserInput(BaseModel):
    filename_with_dir:str
#

@app.post("/get_nexrad_url")
async def nexrad_copy_file_to_S3_and_return_my_s3_url_API(selected_file:NexradUserInput):

    src_bucket = "noaa-nexrad-level2"
    des_bucket = "damg7245-ass1"
    my_s3_file_url = ""

    dir_list = str(selected_file.filename_with_dir).split("/")

    if dir_list[0] not in data_df_nexrad.year.unique().tolist():
        raise HTTPException(status_code = 400,detail="Selected Year out of range")
    elif dir_list[1] not in data_df_nexrad[(data_df_nexrad.year == dir_list[0])].month.unique().tolist():
        raise HTTPException(status_code=400, detail="Selected Month out of range")
    elif dir_list[2] not in data_df_nexrad[(data_df_nexrad.year == dir_list[0]) & (data_df_nexrad.month == dir_list[1])].day.unique().tolist():
        raise HTTPException(status_code=400, detail="Selected day out of 3range")
    elif dir_list[3] not in data_df_nexrad[(data_df_nexrad.year == dir_list[0]) & (data_df_nexrad.month == dir_list[1]) & (data_df_nexrad.day == dir_list[2])].station.unique().tolist():
        raise HTTPException(status_code = 404,detail="StationCode not found")
    else:
        # copying user selected file from AWS s3 bucket to our bucket
        copied_flag = copy_s3_file(src_bucket, selected_file.filename_with_dir, des_bucket, selected_file.filename_with_dir)

    print(f"{copied_flag} -- flag")
    # getting url of user selected file from our s3 bucket
    if copied_flag:
        my_s3_file_url = nexrad_get_my_s3_url(selected_file.filename_with_dir)
    else:
        raise HTTPException(status_code=404, detail="File not found")
    return  {'url':my_s3_file_url}




class GoesInputs(BaseModel):
    year:int
    day:str
    hour:str
"""
takes geos dir (only directory structure) as input and returns all the files in that dir as list
"""
@app.post("/get_goes_files")
async def return_goes_files_list(dir_to_check_geos:GoesInputs):
    goes_files_list = []
    dir = f"ABI-L1b-RadC/{dir_to_check_geos.year}/{dir_to_check_geos.day}/{dir_to_check_geos.hour}"

    goes_files_list = get_files_from_noaa_bucket(dir)

    return {'files':goes_files_list}







class NexradInputs(BaseModel):
    year:int
    month:str
    day:str
    station_code:str
"""
takes nexrad dir as input and returns all the files in that dir as list 
"""
@app.post("/get_nexrad_files")
async def return_nexrad_files_list(dir_to_check_nexrad:NexradInputs):
    noaa_files_list = []
    dir_to_check_nexrad = f"{dir_to_check_nexrad.year}/{dir_to_check_nexrad.month}/{dir_to_check_nexrad.day}/{dir_to_check_nexrad.station_code}"

    noaa_files_list = get_files_from_nexrad_bucket(dir_to_check_nexrad)

    return {'files':noaa_files_list}


class CredInputs(BaseModel):
    un:str
    pwd:str
@app.post("/autheticate_user")
def verify_user(credentials:CredInputs):
    conn = sqlite3.connect('meta.db')
    c = conn.cursor()

    query = f"SELECT password FROM cred  WHERE username = '{credentials.un}'"
    # try:
    #     p = c.execute(query)
    #     db_pwd = p.fetchall()[0][0]
    #     if verify_password(db_pwd, credentials.pwd):
    #         user_data = {"username": credentials.un}
    #         expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    #         token = jwt.encode({"user": user_data, "exp": expiration_time}, secret_key, algorithm="HS256")
    #         return {"token": token}
    #     else:
    #         return {"error": "Invalid credentials"}
    # except IndexError:
    #     return {"error": "Invalid credentials"}
    try:
        p=c.execute(query)
        db_pwd = p.fetchall()[0][0]
        return {"matched":verify_password(db_pwd, credentials.pwd)}
    except IndexError:
        return {"matched": 0}

# @app.get("/protected_resource")
# def protected_resource(token: str):
#     if is_token_valid(token):
#         # Grant access to the protected resource
#         return {"message": "Access granted"}
#     else:
#         # Return an error message or redirect to the login page
#         return {"error": "Invalid or expired token"}
#

