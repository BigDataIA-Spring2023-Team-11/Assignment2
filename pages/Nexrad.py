import pandas as pd
import os
import json
import requests

import streamlit as st
import logging
import folium
# from aws_nexrad import get_files_from_nexrad_bucket, get_noaa_nexrad_url, copy_s3_nexrad_file, get_my_s3_url_nex, \
#     get_dir_from_filename_nexrad, copy_file_to_S3_and_return_my_s3_url
# from aws_nexrad import get_dir_from_filename_nexrad, get_files_from_nexrad_bucket, get_noaa_nexrad_url
from sql_nexrad import fetch_data_from_table_nexrad
# from aws_geos import get_files_from_noaa_bucket, get_noaa_geos_url, copy_s3_file, get_my_s3_url, \
#     get_dir_from_filename_geos
from streamlit_folium import folium_static
from utils_nexrad_API import get_dir_from_filename_nexrad

path = os.path.dirname(__file__)
from dotenv import load_dotenv

load_dotenv()

logout_btn = False



if 'login_status' not in st.session_state:
    st.session_state.login_status = False

if 'login_submit' not in st.session_state:
    st.session_state.login_submit = False

if 'logout_submit' not in st.session_state:
    st.session_state.logout_submit = True

if 'username' not in st.session_state:
    st.session_state.username = False

if 'password' not in st.session_state:
    st.session_state.password = False

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'valid_user_flag' not in st.session_state:
    st.session_state.valid_user_flag = False

if 'login_btn' not in st.session_state:
    st.session_state.login_btn = False


if 'logout_btn' not in st.session_state:
    st.session_state.logout_btn = False


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

# with st.sidebar:
#     lottie_pro = load_lottieurl(f"{lottie_satellite}")
#     st_lottie(
#         lottie_pro,
#         speed=1,
#         reverse=False,
#         loop=True,
#         height="450px",
#         width=None,
#         key=None,
#     )

selected_year_nexrad = ""
selected_month_nexrad = ""
selected_day_nexrad = ""
selected_station_nexrad = ""

def nexrad_enabled():


    #creating columns to show year, day, hour to user to select
    year, month, day, station_code = st.columns([1, 1, 1, 1])

    data_df = fetch_data_from_table_nexrad()

    with year:
        yl = data_df.year.unique().tolist()
        # yl = [int(item) for item in yl]
        # yl.sort()
        # yl = [str(item) for item in yl]
        yl.insert(0, "Select Year")
        year = st.selectbox('Year', yl)
        # year = st.selectbox('Year', range(2020, 2023))
        selected_year_nexrad = year
    month_of_selected_year = extract_values_from_df(data_df[data_df.year==selected_year_nexrad], "year", selected_year_nexrad, "month")
    with month:
        msyl = month_of_selected_year
        # msyl = [int(item) for item in msyl]
        # msyl.sort()
        # msyl=[str(item) for item in msyl]
        msyl.insert(0, "Select Month")
        month = st.selectbox('Month', msyl)
        selected_month_nexrad = month
    day_of_selected_month = extract_values_from_df(data_df[(data_df.year==selected_year_nexrad) & (data_df.month==selected_month_nexrad)], "month", selected_month_nexrad, "day")

    with day:
        dsml = day_of_selected_month
        # dsml = [int(item) for item in dsml]
        # dsml.sort()
        # dsml = [str(item) for item in dsml]
        dsml.insert(0, "Select Day")
        day = st.selectbox("Day", dsml)
        selected_day_nexrad = day
    station_code_of_selected_hour = extract_values_from_df(data_df[(data_df.year==selected_year_nexrad) & (data_df.month==selected_month_nexrad) & (data_df.day==selected_day_nexrad)],"day", selected_day_nexrad, "station")

    with station_code:
        scshl = station_code_of_selected_hour
        # scshl = [int(item) for item in scshl]
        # scshl.sort()
        # scshl = [str(item) for item in scshl]
        scshl.insert(0,"Select station")
        station = st.selectbox("Station Code",scshl)
        selected_station_nexrad = station



    #
    # # """
    # # takes nexrad dir as input and returns al the files in that dir as list
    # # """
    # def return_list(dir_to_check_nexrad):
    #     noaa_files_list = []
    #
    #     noaa_files_list = get_files_from_nexrad_bucket(dir_to_check_nexrad)
    #
    #     return noaa_files_list
    #


    # if st.button("Retreive"):
    dir_to_check_nexrad = ""
    if ((selected_year_nexrad != "Select Year") and (selected_month_nexrad != "Select Month") and (
            selected_day_nexrad != "Select Day") and (selected_station_nexrad != "Select station")):

            url = 'http://api:8000/get_nexrad_files'
            data = {
                "year": int(selected_year_nexrad),
                "month": selected_month_nexrad,
                "day":selected_day_nexrad,
                "station_code":selected_station_nexrad
            }
            response = requests.post(url=url, json=data)
            noaa_files_list = response.json().get('files')

            # response = requests.post(url, data = dir_to_check_geos)
            # files_from_api = response.json()
            # st.markdown(files_from_api['files'])
            selected_file = st.selectbox("Select a file", noaa_files_list)
    else:
        st.error("Please select all fields")





        dir_to_check_nexrad = f"{selected_year_nexrad}/{selected_month_nexrad}/{selected_day_nexrad}/{selected_station_nexrad}"
    # st.markdown(dir_to_check_nexrad)


    fetching, image = st.columns([3, 1])


    # #Takes list of files from user selected directory and showing them in selectbox
    # noaa_files_list = return_list(dir_to_check_nexrad) if dir_to_check_nexrad != "" else []
    # selected_file = st.selectbox("Select a file", noaa_files_list)



    #retrieving url from AWS s3 bucket for selected file
    # nexrad_file_url = get_noaa_nexrad_url(f"{dir_to_check_nexrad}/{selected_file}")
    get_url_btn = st.button("Get Url")
    my_s3_file_url = ""


    #through user inputs
    if get_url_btn:
        if((selected_year_nexrad != "Select Year") and (selected_month_nexrad != "Select Month") and (selected_day_nexrad != "Select Day") and (selected_station_nexrad != "Select station")):
        # if ((selected_day_nexrad != "Select Hour") and (selected_month_nexrad != "Select Day") and (selected_year_nexrad != "Select Year")):
        #     my_s3_file_url = asyncio.run(nexrad_copy_file_to_S3_and_return_my_s3_url_API(selected_file)) #------for API-----
        #     my_s3_file_url = nexrad_copy_file_to_S3_and_return_my_s3_url(selected_file)

            get_nexrad_url = 'http://api:8000/get_nexrad_url'
            nexrad_data = {
                "filename_with_dir": selected_file
            }
            response = requests.post(url=get_nexrad_url, json=nexrad_data)
            my_s3_file_url = response.json().get('url')

            if my_s3_file_url != "":
                st.success(f"Download link has been generated!\n [URL]({my_s3_file_url})")
                with st.expander("Expand for URL"):
                    text2 = f"<p style='font-size: 20px; text-align: center'><span style='color: #15b090; font-weight:bold ;'>{my_s3_file_url}</span></p>"
                    st.markdown(f"[{text2}]({my_s3_file_url})", unsafe_allow_html=True)
                    logging.info("URL has been generated")
            else:
                st.error("File not found in NEXRAD Dataset, Please enter a valid filename")
        else:
            st.error("Please select all fields!")




    st.markdown("----------------------------------------------------------------------------------------------------")
    st.markdown("<h2 style='text-align: center'>Download Using FileName</h2>",unsafe_allow_html=True)
    given_file_name = st.text_input("Enter File Name")
    button_url = st.button("Get url")


    # through file input
    if button_url:
        if given_file_name != "":
            src_bucket = "noaa-nexrad-level2"
            des_bucket = "damg7245-ass1"

            #generating filename with dir structure
            full_file_name = get_dir_from_filename_nexrad(given_file_name)

            #getting my s3 bucket url giving full file name with dir as input
            # my_s3_file_url = asyncio.run(nexrad_copy_file_to_S3_and_return_my_s3_url_API(full_file_name))  #---for API-----
            # my_s3_file_url = nexrad_copy_file_to_S3_and_return_my_s3_url(full_file_name)
            get_nexrad_url = 'http://api:8000/get_nexrad_url'
            nexrad_data = {
                "filename_with_dir": full_file_name
            }
            response = requests.post(url=get_nexrad_url, json=nexrad_data)
            my_s3_file_url = response.json().get('url')
            # st.markdown(my_s3_file_url)

            if my_s3_file_url != None:  #checks if the file url is not empty
                st.success(f"Download link has been generated!\n [URL]({my_s3_file_url})")
                logging.info("Download link generated")

                # displaying url through expander
                with st.expander("Expand for URL"):
                    text2 = f"<p style='font-size: 20px; text-align: center'><span style='color: #15b090; font-weight:bold ;'>{my_s3_file_url}</span></p>"
                    st.markdown(f"[{text2}]({my_s3_file_url})", unsafe_allow_html=True)
                    logging.info("URL has been generated")
            else:
                st.error("File not found in NEXRAD Dataset, Please enter a valid filename")

        else:
            st.error("Please Enter a file name")



    DATA_URL = ('nexrad.csv')
    @st.cache(persist=True)
    def load_data(nrows):
        data = pd.read_csv(DATA_URL, nrows=nrows)
        # lowercase = lambda x:str(x).lower()
        return data
    data = load_data(10000)
    df = pd.DataFrame({'name': data['NAME'],'lat': data['LAT'],'lon':data['LON']})

    m = folium.Map(location=[20,0], tiles="OpenStreetMap", zoom_start=2)
    # st.map(df)
    for i in range(0,len(data)):
       folium.Marker(
          location=[df.iloc[i]['lat'], df.iloc[i]['lon']],
          popup=df.iloc[i]['name'],
       ).add_to(m)
    # st.markdown()
    folium_static(m)


if st.session_state["authenticated"] == True:

    c1, c2, c3, c4, c5 = st.columns(5)
    with c5:
        logout_btn = st.button("Logout!")

    st.markdown("<h1 style='text-align: center'>Data Explorator - NEXRAD</h1>", unsafe_allow_html=True)

    nexrad_enabled()
else:
    st.error("Please login through login page to view session ")


if logout_btn:
    st.session_state.authenticated = False
    st.success("User Logged-OUT")
    # home_page_layout(st.session_state.authenticated)


# if logout_btn:
#     st.session_state.authenticated = False
#     st.success("User Logged-OUT")
#     home_page_layout(st.session_state.authenticated)
