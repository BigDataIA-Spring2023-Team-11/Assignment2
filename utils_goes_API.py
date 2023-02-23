import logging
import boto3
import botocore
import os
import streamlit as st

# takes full file name with dir and returns full noaa bucket url
def get_noaa_geos_url(filename):
    static_url_12 = "https://noaa-goes18.s3.amazonaws.com"
    generated_url = f"{static_url_12}/{filename}"
    return generated_url


"""
Takes full filename with dir and returns my s3 bucket url
"""
def goes_get_my_s3_url(filename):
    # print(dir_to_geos)
    print(filename)
    static_url = "https://damg7245-ass1.s3.amazonaws.com"
    filename_alone = filename.split("/")[-1]
    generated_url = f"{static_url}/{filename}"
    return generated_url



"""
takes just filename as input and extracts file directory from it and return the filename with directory
"""


def get_dir_from_filename_geos(file_name):
  # static_url_12 = "https://noaa-goes18.s3.amazonaws.com"
  full_file_name = ""
  try:
      lis = file_name.split("_")
      mode_lis = lis[1].split("-")
      mode = "-".join(mode_lis[0:3])
      if mode[-1].isdigit():
          mode = mode[:len(mode)-1]
      file_text = lis[0]+"_"+lis[1]
      year = lis[3][1:5]
      day_of_year = lis[3][5:8]
      day = lis[3][8:10]
      full_file_name = mode+"/"+year+"/"+day_of_year+"/"+day+"/"+file_name
      # print(full_file_name,"ffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
  except:
      logging.debug("exception_occured_in_goes while making directory")
  return full_file_name
























# selected_file is a full filename with dir structure
def goes_copy_file_to_S3_and_return_my_s3_url(selected_file):
    my_s3_file_url = ""
    src_bucket = "noaa-goes18"
    des_bucket = "damg7245-ass1"
    # copying user selected file from AWS s3 bucket to our bucket
    copied_flag = copy_s3_file(src_bucket, selected_file, des_bucket, selected_file)
    # getting url of user selected file from our s3 bucket
    if copied_flag:
        my_s3_file_url = goes_get_my_s3_url(selected_file)
    return  my_s3_file_url

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



