import pytest
from fastapi.testclient import TestClient
from API import app

client = TestClient(app)
def test_nexrad_url():
    response = client.post(
        url="/get_nexrad_url",
        json={
            'filename_with_dir': '2022/04/08/TDFW/TDFW20220408_022326_V08'
        }
    )
    assert response.status_code == 200
    message = response.json()["url"]
    assert message == 'https://damg7245-ass1.s3.amazonaws.com/2022/04/08/TDFW/TDFW20220408_022326_V08'
