import streamlit as st
import json
import requests
from streamlit_lottie import st_lottie

st.set_page_config(  # Alternate names: setup_page, page, layout
    layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
    initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
    page_title='Venkata_Bhargavi_Sikhakolli',  # String or None. Strings get appended with "• Streamlit".
    page_icon= None,  # String, anything supported by st.image, or None.
)
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
st.markdown("<h3 style='text-align: center'><span style='color: #2A76BE;'>Welcome to Data Exploration Application</span></h3>",unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center'>One stop to leverage data from NOAA Satellite and radars for analysis and extract insights.</h5>",unsafe_allow_html=True)
st.markdown("")
st.markdown("The 2 datasets available are: <span style='color: #2A76BE;'>[GOES](https://noaa-goes18.s3.amazonaws.com/index.html#ABI-L1b-RadC/)</span> and <span style='color: #2A76BE;'>[NEXRAD](https://noaa-nexrad-level2.s3.amazonaws.com/index.html)</span> ",unsafe_allow_html=True)
st.markdown("")
st.markdown("")
st.markdown("GOES (Geostationary Operational Environmental Satellite)These satellites assist meteorologists in observing and forecasting local weather phenomena such as thunderstorms, tornadoes, fog, hurricanes, flash floods, and other severe weather. GOES observations have also been useful in monitoring dust storms, volcanic eruptions, and forest fires.")
st.markdown("")
st.markdown("")
st.markdown("NEXRAD (Next Generation Radar)NEXRAD detects precipitation and atmospheric movement or wind. It returns data which when processed can be displayed in a mosaic map which shows patterns of precipitation and its movement. The radar system operates in two basic modes, selectable by the operator – a slow-scanning clear-air mode for analyzing air movements when there is little or no activity in the area, and a precipitation mode, with a faster scan for tracking active weather.")