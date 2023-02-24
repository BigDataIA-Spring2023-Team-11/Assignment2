# import logging
#
# from dotenv import load_dotenv
# import re
#
# load_dotenv() # to load environments from .env file
# #
# aws_s3_client = boto3.client('s3',region_name = 'us-east-1',aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),aws_secret_access_key = os.environ.get('AWS_SECRET_KEY'))
# #
# app1 = FastAPI()
# def get_files_from_nexrad_bucket(dir):
#     files_from_nexrad_bucket = []
#     s3_client = boto3.client("s3",region_name="us-east-1",
#                       aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
#                       aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'))
#     paginator = s3_client.get_paginator('list_objects_v2')
#     nexrad_bucket = paginator.paginate(Bucket = "noaa-nexrad-level2",Prefix = dir) #,PaginationConfig  = {"PageSize":2}
#     for count,page in enumerate(nexrad_bucket):
#         files = page.get("Contents")
#         for file in files:
#             files_from_nexrad_bucket.append(file['Key'])
#             # print(file['Key'])
#             # f = open("output1.txt", "a")?\
#             # print(f"{file['Key']}",file = f)
#     # print(files_from_nexrad_bucket)
#     logging.info("Files extracted from Nexrad bucket")
#     return  files_from_nexrad_bucket
#



#
# def get_noaa_nexrad_url(filename):
#     static_url_nex = "https://noaa-nexrad-level2.s3.amazonaws.com"
#     generated_url = f"{static_url_nex}/{filename}"
#     # logging.info("Url extacted from S3")
#     return generated_url
#
# def get_my_s3_url_nex(filename):
#     # print(dir_to_nex)
#     # print(filename)
#     static_url = "https://damg7245-ass1.s3.amazonaws.com"
#     filename_alone = filename.split("/")[-1]
#     generated_url = f"{static_url}/{filename}"
#     return generated_url




#
# def copy_file_to_S3_and_return_my_s3_url(selected_file):
#     src_bucket = "noaa-nexrad-level2"
#     des_bucket = "damg7245-ass1"
#     my_s3_file_url = ""
#     # copying user selected file from AWS s3 bucket to our bucket
#     copied_flag = copy_s3_nexrad_file(src_bucket, selected_file, des_bucket, selected_file)
#     # getting url of user selected file from our s3 bucket
#     if copied_flag:
#         my_s3_file_url = get_my_s3_url_nex(selected_file)
#     return my_s3_file_url
#
#




# def get_dir_from_filename_nexrad(file_name):
#     ground_station = file_name[0:4]
#     year = file_name[4:8]
#     month = file_name[8:10]
#     day = file_name[10:12]
#     full_file_name = year+"/"+month+"/"+day+"/"+ground_station+"/"+file_name
#     # print(full_file_name,"ffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
#     return full_file_name
#
