
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

