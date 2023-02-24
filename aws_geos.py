import os
import boto3

from dotenv import load_dotenv

load_dotenv() # to load environments from .env file


aws_s3_client = boto3.client('s3',region_name = 'us-east-1',aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),aws_secret_access_key = os.environ.get('AWS_SECRET_KEY'))

# files_from_bucket = []

# def get_files_from_noaa_bucket(dir):
#     # s3 = boto3.client("s3",
#     #                   aws_access_key_id= None,
#     #                   aws_secret_access_key=None)
#     """
#     This function will list down all files in a folder from S3 bucket
#     :return: None
#     """
#
#     print(dir,"ddddddddddddddddddddd")
#     s3_client = boto3.client("s3",
#                       aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
#                       aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'))
#     bucket_name = "noaa-goes18"
#     response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=dir)
#     files = response.get("Contents")
#     print("---------------------------------------------------------------------")
#     print(type(files))
#     files_from_bucket =[]
#     for file in files:
#         files_from_bucket.append(file['Key'])
#         # f = open("output.txt", "a")
#         # print(file['Key'])
#         print(f"file_name: {file['Key']}, size: {file['Size']}")
#         # f.close()
#     return files_from_bucket

# """
# Arguments : Directory of the bucket
# returns : list of all files from the dir
# """
# def get_files_from_noaa_bucket(dir):
#     files_from_bucket = []
#     s3_client = boto3.client("s3",region_name="us-east-1",
#                       aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
#                       aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'))
#     paginator = s3_client.get_paginator('list_objects_v2')
#     noaa_bucket = paginator.paginate(Bucket = "noaa-goes18",Prefix = dir) #,PaginationConfig  = {"PageSize":2}
#     for count,page in enumerate(noaa_bucket):
#         files = page.get("Contents")
#         for file in files:
#             files_from_bucket.append(file['Key'])
#             # print(file['Key'])
#             # f = open("output.txt", "a")
#             # print(f"{file['Key']}",file = f)
#     # print(files_from_bucket)
#     return  files_from_bucket



# """
# takes file name and matches regex to get year,day and hour details of each file and returns list of [year,day,hour]
# """
# def get_meta_data_for_db_population():
#     meta_data_for_db = []
#     files = get_files_from_noaa_bucket("ABI-L1b-RadC")
#     for file in files:
#         ydh = []
#         match = re.findall(r"(\d{4})(\d{3})(\d{2})",file)
#         # match = pattern.search(file)
#         if match:
#             year = match[0][0]
#             day = match[0][1]
#             hour = match[0][2]
#             ydh.extend([year,day,hour])
#             if ydh not in meta_data_for_db:
#                 meta_data_for_db.append(ydh)
#     return meta_data_for_db
#

# def get_noaa_geos_url(filename):
#     static_url_12 = "https://noaa-goes18.s3.amazonaws.com"
#     generated_url = f"{static_url_12}/{filename}"
#     return generated_url

# class UserInput(BaseModel):
# #     filename_with_dir:str
# test = "ABI-L1b-RadC/2022/209/01/OR_ABI-L1b-RadC-M6C01_G18_s20222090111140_e20222090113513_c20222090113553.nc"
#
# #filename here is with dir
# async def get_my_s3_url_api(filename) -> dict:
#     # print(filename)
#     static_url = "https://damg7245-ass1.s3.amazonaws.com"
#     generated_url = f"{static_url}/{filename}"
#     return {"url":generated_url}


#--------------------------------------replicated in API------------------------------------------------
# # selected_file is a full filename with dir structure
# def copy_file_to_S3_and_return_my_s3_url(selected_file):
#     my_s3_file_url = ""
#     src_bucket = "noaa-goes18"
#     des_bucket = "damg7245-ass1"
#     # copying user selected file from AWS s3 bucket to our bucket
#     copied_flag = copy_s3_file(src_bucket, selected_file, des_bucket, selected_file)
#     # getting url of user selected file from our s3 bucket
#     if copied_flag:
#         my_s3_file_url = get_my_s3_url(selected_file)
#     return  my_s3_file_url






# def get_my_s3_url(filename):
#     # print(dir_to_geos)
#     print(filename)
#     static_url = "https://damg7245-ass1.s3.amazonaws.com"
#     filename_alone = filename.split("/")[-1]
#     generated_url = f"{static_url}/{filename}"
#     return generated_url
# #
# def copy_s3_file_if_exists(src_bucket_name, src_file_name, dst_bucket_name, dst_file_name):
#     session = boto3.Session(
#         aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
#         aws_secret_access_key=os.environ.get('AWS_SECRET_KEY')
#     )
#
#     s3 = session.resource('s3')
#     src_bucket = s3.Bucket(src_bucket_name)
#
#     copy_source = {
#         'Bucket': src_bucket_name,
#         'Key': src_file_name
#     }
#     dst_bucket = s3.Bucket(dst_bucket_name)
#
#     try:
#         dst_bucket.Object(dst_file_name).load()
#         # print(f"Object {dst_file_name} already exists in destination bucket {dst_bucket_name}.")
#         #already copied so flag 1
#         flag = 1
#     except botocore.exceptions.ClientError as e:
#
#         if e.response['Error']['Code'] == "404":
#             # st.markdown(f"File NOT found in dst bucket {e.response['Error']['Code']}")
#             dst_bucket.copy(copy_source, dst_file_name)
#             print(f"Object {src_file_name} copied from source bucket {src_bucket_name} to destination bucket {dst_bucket_name}.")
#             #now copied so flat = 1
#             flag = 1
#         else:
#             st.error("No Such File")
#             #so such file to copy , so flag =0
#             flag = 0
#     return flag
#
# def copy_s3_file(src_bucket_name, src_file_name, dst_bucket_name, dst_file_name):
#     # s3 = boto3.client("s3",
#     #                   aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
#     #                   aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'))
#
#     # Creating Session With Boto3.
#     session = boto3.Session(
#         aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
#         aws_secret_access_key=os.environ.get('AWS_SECRET_KEY')
#     )
#     flag = 0
#
#     s3 = session.resource('s3')
#     src_bucket = s3.Bucket(src_bucket_name)
#
#     try:
#         src_bucket.Object(src_file_name).load()
#         st.markdown(f"Here {src_bucket.Object(src_file_name).load()}")
#         flag = copy_s3_file_if_exists(src_bucket_name, src_file_name, dst_bucket_name, dst_file_name)
#         st.markdown(flag)
#         return flag
#
#     except botocore.exceptions.ClientError as e:
#         st.markdown("EXCEPTION")
#         if e.response['Error']['Code'] == "404":
#             st.error(f"File {src_file_name} not found in source bucket {src_bucket_name}.")
#             # flag = 0
#             return 0
#         # else:
#         #     raise
#
#------------------------------replicated in API till here-----------------------------------------------
# """
# takes just filename as input and extracts file directory from it and return the filename with directory
# """
#
#
# def get_dir_from_filename_geos(file_name):
#   # static_url_12 = "https://noaa-goes18.s3.amazonaws.com"
#   full_file_name = ""
#   try:
#       lis = file_name.split("_")
#       mode_lis = lis[1].split("-")
#       mode = "-".join(mode_lis[0:3])
#       if mode[-1].isdigit():
#           mode = mode[:len(mode)-1]
#       file_text = lis[0]+"_"+lis[1]
#       year = lis[3][1:5]
#       day_of_year = lis[3][5:8]
#       day = lis[3][8:10]
#       full_file_name = mode+"/"+year+"/"+day_of_year+"/"+day+"/"+file_name
#       # print(full_file_name,"ffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
#   except:
#       logging.debug("exception_occured_in_goes while making directory")
#   return full_file_name
#



# if __name__ == "__main__":
#     # main()
#
#     # get_files_from_noaa_bucket("ABI-L1b-RadC/2022")
#     # meta_data = get_meta_data_for_db_population()
#     copy_s3_file("noaa-goes18","")
#     # print(meta_data)
#     # piyush_func()