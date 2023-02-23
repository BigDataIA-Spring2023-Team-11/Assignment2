from utils_nexrad_API import get_dir_from_filename_nexrad, get_noaa_nexrad_url

team1 = "KBGM20110612_003045_V03.gz"
team2 = "KARX20100512_014240_V03.gz"
team3 = "KABX20130902_002911_V06.gz"
team4 = "KBIS20001222_090728.gz"
team5 = "KCCX20120203_013605_V03.gz"
team6 = "KCBW20011213_002358.gz"
team7 = "KBYX20150804_000940_V06.gz"
team8 = "KAPX20120717_013219_V06.gz"
team9 = "KAPX20140907_010223_V06.gz"
team10 = "KCBW20080819_012424_V03.gz"
team11 = "KLWX19931112_005128.gz"
team12 = "KBOX20030717_014732.gz"




team1_url ="https://noaa-nexrad-level2.s3.amazonaws.com/2011/06/12/KBGM/KBGM20110612_003045_V03.gz"
team2_url ="https://noaa-nexrad-level2.s3.amazonaws.com/2010/05/12/KARX/KARX20100512_014240_V03.gz"
team3_url ="https://noaa-nexrad-level2.s3.amazonaws.com/2013/09/02/KABX/KABX20130902_002911_V06.gz"
team4_url ="https://noaa-nexrad-level2.s3.amazonaws.com/2000/12/22/KBIS/KBIS20001222_090728.gz"
team5_url ="https://noaa-nexrad-level2.s3.amazonaws.com/2012/02/03/KCCX/KCCX20120203_013605_V03.gz"

team7_url ="https://noaa-nexrad-level2.s3.amazonaws.com/2015/08/04/KBYX/KBYX20150804_000940_V06.gz"
team8_url ="https://noaa-nexrad-level2.s3.amazonaws.com/2012/07/17/KAPX/KAPX20120717_013219_V06.gz"
team9_url ="https://noaa-nexrad-level2.s3.amazonaws.com/2014/09/07/KAPX/KAPX20140907_010223_V06.gz"
team10_url ="https://noaa-nexrad-level2.s3.amazonaws.com/2008/08/19/KCBW/KCBW20080819_012424_V03.gz"
team11_url ="https://noaa-nexrad-level2.s3.amazonaws.com/1993/11/12/KLWX/KLWX19931112_005128.gz"
team12_url ="https://noaa-nexrad-level2.s3.amazonaws.com/2003/07/17/KBOX/KBOX20030717_014732.gz"




def test_team_1():
    full_file_name = get_dir_from_filename_nexrad(team1)
    print(team1_url,"///////////////////////////////////////////////////////")
    print(get_noaa_nexrad_url(full_file_name))
    assert get_noaa_nexrad_url(full_file_name) == team1_url
def test_team_2():
    full_file_name = get_dir_from_filename_nexrad(team2)
    assert get_noaa_nexrad_url(full_file_name) == team2_url
def test_team_3():
    full_file_name = get_dir_from_filename_nexrad(team3)
    assert get_noaa_nexrad_url(full_file_name) == team3_url
def test_team_4():
    full_file_name = get_dir_from_filename_nexrad(team4)
    assert get_noaa_nexrad_url(full_file_name) == team4_url
def test_team_5():
    full_file_name = get_dir_from_filename_nexrad(team5)
    assert get_noaa_nexrad_url(full_file_name) == team5_url


# def test_team_6():
#     full_file_name = get_dir_from_filename_nexrad(team6)
#     assert get_noaa_nexrad_url(full_file_name) == team6_url
def test_team_7():
    full_file_name = get_dir_from_filename_nexrad(team7)
    assert get_noaa_nexrad_url(full_file_name) == team7_url
def test_team_8():
    full_file_name = get_dir_from_filename_nexrad(team8)
    assert get_noaa_nexrad_url(full_file_name) == team8_url

def test_team_9():
    full_file_name = get_dir_from_filename_nexrad(team9)
    assert get_noaa_nexrad_url(full_file_name) == team9_url

def test_team_10():
    full_file_name = get_dir_from_filename_nexrad(team10)
    assert get_noaa_nexrad_url(full_file_name) == team10_url

def test_team_11():
    full_file_name = get_dir_from_filename_nexrad(team11)
    assert get_noaa_nexrad_url(full_file_name) == team11_url

def test_team_12():
    full_file_name = get_dir_from_filename_nexrad(team12)
    assert get_noaa_nexrad_url(full_file_name) == team12_url













