
import boto3
import botocore
import os
import streamlit as st
"""
returns a concatenated url from AWS bucket
"""
def get_noaa_nexrad_url(filename):
    static_url_nex = "https://noaa-nexrad-level2.s3.amazonaws.com"
    generated_url = f"{static_url_nex}/{filename}"
    return generated_url


"""
return concatenated url of our s3 bucket
"""
def nexrad_get_my_s3_url(filename):
    static_url = "https://damg7245-ass1.s3.amazonaws.com"
    filename_alone = filename.split("/")[-1]
    generated_url = f"{static_url}/{filename}"
    return generated_url







"""
returns full filename of nexrad with dir structure
"""
def get_dir_from_filename_nexrad(file_name):
    ground_station = file_name[0:4]
    year = file_name[4:8]
    month = file_name[8:10]
    day = file_name[10:12]
    full_file_name = year+"/"+month+"/"+day+"/"+ground_station+"/"+file_name
    return full_file_name







def nexrad_copy_file_to_S3_and_return_my_s3_url(selected_file):
    src_bucket = "noaa-nexrad-level2"
    des_bucket = "damg7245-ass1"
    my_s3_file_url = ""
    # copying user selected file from AWS s3 bucket to our bucket
    copied_flag = copy_s3_file(src_bucket, selected_file, des_bucket, selected_file)
    # getting url of user selected file from our s3 bucket
    if copied_flag:
        my_s3_file_url = nexrad_get_my_s3_url(selected_file)
    return my_s3_file_url





def copy_s3_file_if_exists(src_bucket_name, src_file_name, dst_bucket_name, dst_file_name):
    session = boto3.Session(
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_KEY')
    )

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
    # s3 = boto3.client("s3",
    #                   aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
    #                   aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'))

    # Creating Session With Boto3.
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
        # st.markdown("EXCEPTION")
        if e.response['Error']['Code'] == "404":
            st.error(f"File {src_file_name} not found in source bucket {src_bucket_name}.")
            # flag = 0
            return 0
        # else:
        #     raise


