#system imports
from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from dotenv import load_dotenv
import streamlit as st
import boto3
import os
import botocore
import logging

from utils_goes_API import goes_get_my_s3_url
from utils_nexrad_API import nexrad_get_my_s3_url

load_dotenv()
app = FastAPI()

#custom imports
from sql_goes import fetch_data_from_table_goes
from sql_nexrad import  fetch_data_from_table_nexrad


data_df_goes = fetch_data_from_table_goes()
data_df_nexrad = fetch_data_from_table_nexrad()









def copy_s3_file_if_exists(src_bucket_name, src_file_name, dst_bucket_name, dst_file_name):
    # session = boto3.Session(
    #     aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
    #     aws_secret_access_key=os.environ.get('AWS_SECRET_KEY')
    # )
    session = boto3.Session(
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
    session = boto3.Session(
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





# selected_file is a full filename with dir structure
@app.post("/get_goes_url")
async def goes_copy_file_to_S3_and_return_my_s3_url_Api(selected_file) -> dict:
    my_s3_file_url = ""
    src_bucket = "noaa-goes18"
    des_bucket = "damg7245-ass1"

    dir_list = str(selected_file).split("/")
    selected_station_code = dir_list[3]

    print(f"{selected_file} -- file with code")
    print(f"{selected_station_code} -- Station code")
    print(f"{dir_list[0]} {data_df_goes.year.unique().tolist()} -- year check")

    if dir_list[1] not in data_df_goes.year.unique().tolist():
        raise HTTPException(status_code=400, detail="Selected Year out of range")
    elif dir_list[2] not in data_df_goes[(data_df_goes.year == dir_list[1])].day.unique().tolist():
        raise HTTPException(status_code=400, detail="Selected Day out of range")
    elif dir_list[3] not in data_df_goes[(data_df_goes.year == dir_list[1]) & (data_df_goes.day == dir_list[2])].hour.unique().tolist():
        raise HTTPException(status_code=400, detail="Selected Hour out of range")
    else:
        # copying user selected file from AWS s3 bucket to our bucket
        copied_flag = copy_s3_file(src_bucket, selected_file, des_bucket, selected_file)

    # print(f"{copied_flag} -- flag")
    # copying user selected file from AWS s3 bucket to our bucket
    # copied_flag = copy_s3_file(src_bucket, selected_file, des_bucket, selected_file)
    # getting url of user selected file from our s3 bucket
    if copied_flag:
        my_s3_file_url = goes_get_my_s3_url(selected_file)
    else:
        raise HTTPException(status_code=404, detail="File not found")

    # return {'url': my_s3_file_url}
    return {'url':my_s3_file_url}








@app.post("/get_nexrad_rul")
async def nexrad_copy_file_to_S3_and_return_my_s3_url_API(selected_file) -> dict:
    # print(selected_file)

    src_bucket = "noaa-nexrad-level2"
    des_bucket = "damg7245-ass1"
    my_s3_file_url = ""

    dir_list = str(selected_file).split("/")
    selected_station_code = dir_list[3]

    print(f"{selected_file} -- file with code")
    print(f"{selected_station_code} -- Station code")
    print(f"{dir_list[0]} {data_df_nexrad.year.unique().tolist()} -- year check")

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
        copied_flag = copy_s3_file(src_bucket, selected_file, des_bucket, selected_file)

    print(f"{copied_flag} -- flag")
    # getting url of user selected file from our s3 bucket
    if copied_flag:
        my_s3_file_url = nexrad_get_my_s3_url(selected_file)
    else:
        raise HTTPException(status_code=404, detail="File not found")
    return  {'url':my_s3_file_url}
