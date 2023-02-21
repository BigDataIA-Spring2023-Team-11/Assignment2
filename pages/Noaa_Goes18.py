import logging

import streamlit as st
import os
import json
import requests
from streamlit_lottie import st_lottie

from sql import fetch_data_from_table
from aws_geos import get_files_from_noaa_bucket, get_noaa_geos_url, copy_s3_file, get_my_s3_url, \
    get_dir_from_filename_geos

path = os.path.dirname(__file__)
from dotenv import load_dotenv

load_dotenv()


data_df = fetch_data_from_table()


# """
# returns values from df of selected column
# """

def extract_values_from_df(df, key, value, col):
    # Extract the rows where key is equal to value
    filtered_df = df[df[key] == value]

    # Return all the values from the specified column
    return filtered_df[col].unique().tolist()


def load_lottiefile(filepath:str):
    with open(filepath,"r") as f:
        return json.load(f)
def load_lottieurl(url:str):
    r = requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()
lottie_satellite = "https://assets3.lottiefiles.com/private_files/lf30_cmdcmgh0.json"

with st.sidebar:
    lottie_pro = load_lottieurl(f"{lottie_satellite}")
    st_lottie(
        lottie_pro,
        speed=1,
        reverse=False,
        loop=True,
        height="450px",
        width=None,
        key=None,
    )
st.markdown("<h1 style='text-align: center'>Data Explorator</h1>",unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center'>GOES</h2>",unsafe_allow_html=True)
selected_year_geos = ""
selected_day_geos = ""
selected_hour_geos = ""

#creating columns to show year, day, hour to user to select
year,day,hour = st.columns([1,1,1])

with year:
    yl = data_df.year.unique().tolist()
    yl.insert(0, "Select Year")
    year = st.selectbox('Year', yl)
    # year = st.selectbox('Year', range(2020, 2023))
    selected_year_geos = year
days_of_selected_year = extract_values_from_df(data_df[data_df.year==selected_year_geos],"year",selected_year_geos,"day")

with day:
    dsyl = days_of_selected_year
    dsyl.insert(0, "Select Day")
    day = st.selectbox('Day',dsyl)
    selected_day_geos = day
hours_of_selected_day = extract_values_from_df(data_df[(data_df.year==selected_year_geos) & (data_df.day==selected_day_geos)],"day",selected_day_geos,"hour")

with hour:
    hsdl = hours_of_selected_day
    hsdl.insert(0,"Select Hour")
    hour = st.selectbox("Hour",hsdl)
    selected_hour_geos = hour

    # """
    # takes geos dir as input and returns al the files in that dir as list
    # """
def return_list(dir_to_check_geos):
    noaa_files_list = []

    noaa_files_list = get_files_from_noaa_bucket(dir_to_check_geos)

    return noaa_files_list

#creating dir based on user input
dir_to_check_geos = ""
if (selected_hour_geos != "Select Hour") and (selected_day_geos != "Select Day") and (selected_year_geos != "Select Year"):
    dir_to_check_geos = f"ABI-L1b-RadC/{selected_year_geos}/{selected_day_geos}/{selected_hour_geos}"
# st.markdown(dir_to_check_geos)


fetching, image = st.columns([3, 1])

#     not_empty_selection = all(map(bool, [selected_year_geos, selected_day_geos, selected_hour_geos])) #returns a bool on checking if all fields are empty

#Takes list of files from user selected directory and showing them in selectbox
noaa_files_list = return_list(dir_to_check_geos) if dir_to_check_geos != "" else []
selected_file = st.selectbox("Select a file", noaa_files_list)



#retrieving url from AWS s3 bucket for selected file
geos_file_url = get_noaa_geos_url(f"{dir_to_check_geos}/{selected_file}")
get_url_btn = st.button("Get Url")
my_s3_file_url = ""
# empty_selection = all(map(bool, [selected_year_geos, selected_day_geos, selected_hour_geos])) #returns a bool on checking if all fields are empty

if get_url_btn:
    if ((selected_hour_geos != "Select Hour") and (selected_day_geos != "Select Day") and (selected_year_geos != "Select Year")):
        src_bucket = "noaa-goes18"
        des_bucket = "damg7245-ass1"
        # copying user selected file from AWS s3 bucket to our bucket
        copy_s3_file(src_bucket, selected_file, des_bucket, selected_file)
        # getting url of user selected file from our s3 bucket
        my_s3_file_url = get_my_s3_url(selected_file)
        st.success(f"Download link has been generated!\n [URL]({my_s3_file_url})")
        with st.expander("Expand for URL"):
            text2 = f"<p style='font-size: 20px; text-align: center'><span style='color: #15b090; font-weight:bold ;'>{my_s3_file_url}</span></p>"
            st.markdown(f"[{text2}]({my_s3_file_url})", unsafe_allow_html=True)
            logging.info("URL has been generated")
    else:
        st.error("Please select all fields!")




st.markdown("----------------------------------------------------------------------------------------------------")
st.markdown("<h2 style='text-align: center'>Download Using FileName</h2>",unsafe_allow_html=True)
given_file_name = st.text_input("Enter File Name")
button_url = st.button("Get url")

if button_url:
    if given_file_name != "":
        src_bucket = "noaa-goes18"
        des_bucket = "damg7245-ass1"
        # copying user selected file from AWS s3 bucket to our bucket
        full_file_name = get_dir_from_filename_geos(given_file_name)
        # st.markdown(f"full file name is {full_file_name}")
        if full_file_name != "":
            copied_flag = copy_s3_file(src_bucket, full_file_name, des_bucket, full_file_name)
            # getting url of user selected file from our s3 bucket
            dir_to_check = f"ABI-L1b-RadC/{selected_year_geos}/{selected_day_geos}/{selected_hour_geos}"
            if copied_flag:
                my_s3_file_url = get_my_s3_url( full_file_name)
                # displaying url through expander
                st.success(f"Download link has been generated!\n [URL]({my_s3_file_url})")
                with st.expander("Expand for URL"):
                    text2 = f"<p style='font-size: 20px; text-align: center'><span style='color: #15b090; font-weight:bold ;'>{my_s3_file_url}</span></p>"
                    st.markdown(f"[{text2}]({my_s3_file_url})", unsafe_allow_html=True)
                    logging.info("URL has been generated")
            else:
                logging.DEBUG("File not found in NOAA database")
                st.error("File not found in NOAA database, Please enter a valid filename!")

        else:
            st.error("File not found in NOAA database, Please enter a valid filename")
    else:
        st.error("Please Enter a file name")

