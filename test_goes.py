from utils_goes_API import get_dir_from_filename_geos, get_noaa_geos_url

team1 = "OR_ABI-L2-ACMM1-M6_G18_s20230090504262_e20230090504319_c20230090505026.nc"
team2 = "OR_ABI-L2-ACTPM1-M6_G18_s20230090408262_e20230090408319_c20230090409174.nc"
team3 = "OR_ABI-L2-DSIM1-M6_G18_s20230110608251_e20230110608308_c20230110609126.nc"
team4 = "OR_ABI-L2-ACHTM1-M6_G18_s20223560805242_e20223560805300_c20223560806526.nc"
team5 = "OR_ABI-L2-BRFF-M6_G18_s20223150230207_e20223150239515_c20223150241087.nc"
team6 = "OR_ABI-L2-ADPM2-M6_G18_s20230061310557_e20230061311015_c20230061311402.nc"
team7 = "OR_ABI-L1b-RadM1-M6C01_G18_s20230030201252_e20230030201311_c20230030201340.nc"
team8 = "OR_ABI-L2-ACHTF-M6_G18_s20223532240210_e20223532249518_c20223532252164.nc"
team9 = "OR_ABI-L2-DSRC-M6_G18_s20223180501179_e20223180503552_c20223180508262.nc"
team10 = "OR_ABI-L2-DMWVM1-M6C08_G18_s20223552050271_e20223552050328_c20223552122197.nc"
team11 = "OR_ABI-L2-ACMC-M6_G18_s20222800931164_e20222800933537_c20222800934574.nc"
team12 = "OR_ABI-L2-DMWC-M6C07_G18_s20223510516174_e20223510518559_c20223510527449.nc"


team1_url = "https://noaa-goes18.s3.amazonaws.com/ABI-L2-ACMM/2023/009/05/OR_ABI-L2-ACMM1-M6_G18_s20230090504262_e20230090504319_c20230090505026.nc"
team2_url = "https://noaa-goes18.s3.amazonaws.com/ABI-L2-ACTPM/2023/009/04/OR_ABI-L2-ACTPM1-M6_G18_s20230090408262_e20230090408319_c20230090409174.nc"
team3_url = "https://noaa-goes18.s3.amazonaws.com/ABI-L2-DSIM/2023/011/06/OR_ABI-L2-DSIM1-M6_G18_s20230110608251_e20230110608308_c20230110609126.nc"
team4_url = "https://noaa-goes18.s3.amazonaws.com/ABI-L2-ACHTM/2022/356/08/OR_ABI-L2-ACHTM1-M6_G18_s20223560805242_e20223560805300_c20223560806526.nc"
team5_url = "https://noaa-goes18.s3.amazonaws.com/ABI-L2-BRFF/2022/315/02/OR_ABI-L2-BRFF-M6_G18_s20223150230207_e20223150239515_c20223150241087.nc"
team6_url = "https://noaa-goes18.s3.amazonaws.com/ABI-L2-ADPM/2023/006/13/OR_ABI-L2-ADPM2-M6_G18_s20230061310557_e20230061311015_c20230061311402.nc"
team7_url = "https://noaa-goes18.s3.amazonaws.com/ABI-L1b-RadM/2023/003/02/OR_ABI-L1b-RadM1-M6C01_G18_s20230030201252_e20230030201311_c20230030201340.nc"
team8_url = "https://noaa-goes18.s3.amazonaws.com/ABI-L2-ACHTF/2022/353/22/OR_ABI-L2-ACHTF-M6_G18_s20223532240210_e20223532249518_c20223532252164.nc"
team9_url = "https://noaa-goes18.s3.amazonaws.com/ABI-L2-DSRC/2022/318/05/OR_ABI-L2-DSRC-M6_G18_s20223180501179_e20223180503552_c20223180508262.nc"
team10_url = "https://noaa-goes18.s3.amazonaws.com/ABI-L2-DMWVM/2022/355/20/OR_ABI-L2-DMWVM1-M6C08_G18_s20223552050271_e20223552050328_c20223552122197.nc"
team11_url = "https://noaa-goes18.s3.amazonaws.com/ABI-L2-ACMC/2022/280/09/OR_ABI-L2-ACMC-M6_G18_s20222800931164_e20222800933537_c20222800934574.nc"
team12_url = "https://noaa-goes18.s3.amazonaws.com/ABI-L2-DMWC/2022/351/05/OR_ABI-L2-DMWC-M6C07_G18_s20223510516174_e20223510518559_c20223510527449.nc"






def test_team_1():
    full_file_name = get_dir_from_filename_geos(team1)
    f = get_noaa_geos_url(full_file_name)
    assert get_noaa_geos_url(full_file_name) == team1_url
def test_team_2():
    full_file_name = get_dir_from_filename_geos(team2)
    assert get_noaa_geos_url(full_file_name) == team2_url
def test_team_3():
    full_file_name = get_dir_from_filename_geos(team3)
    assert get_noaa_geos_url(full_file_name) == team3_url
def test_team_4():
    full_file_name = get_dir_from_filename_geos(team4)
    assert get_noaa_geos_url(full_file_name) == team4_url
def test_team_5():
    full_file_name = get_dir_from_filename_geos(team5)
    assert get_noaa_geos_url(full_file_name) == team5_url


def test_team_6():
    full_file_name = get_dir_from_filename_geos(team6)
    assert get_noaa_geos_url(full_file_name) == team6_url
def test_team_7():
    full_file_name = get_dir_from_filename_geos(team7)
    assert get_noaa_geos_url(full_file_name) == team7_url
def test_team_8():
    full_file_name = get_dir_from_filename_geos(team8)
    assert get_noaa_geos_url(full_file_name) == team8_url

def test_team_9():
    full_file_name = get_dir_from_filename_geos(team9)
    assert get_noaa_geos_url(full_file_name) == team9_url

def test_team_10():
    full_file_name = get_dir_from_filename_geos(team10)
    assert get_noaa_geos_url(full_file_name) == team10_url

def test_team_11():
    full_file_name = get_dir_from_filename_geos(team11)
    assert get_noaa_geos_url(full_file_name) == team11_url

def test_team_12():
    full_file_name = get_dir_from_filename_geos(team12)
    assert get_noaa_geos_url(full_file_name) == team12_url
