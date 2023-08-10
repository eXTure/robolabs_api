import os
import sys
from unittest.mock import patch

import pytest
from requests.models import Response

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from robolabs_api.api import RoboLabsApi  # noqa: E402
from robolabs_api.app import app  # noqa: E402


@pytest.fixture
def robolabs_api():
    return RoboLabsApi()


@pytest.fixture
def job_id_response_model():
    response_model = Response()
    response_model._content = b'{"result": {"data": {"api_job_id": 1}}}'
    return response_model


@pytest.fixture
def job_response_model_failed():
    response_model = Response()
    response_model._content = b'{"result": {"data": {"state": "Vykdymas nepavyko", "response_message": "Error"}}}'
    return response_model


@pytest.fixture
def job_response_model_success():
    response_model = Response()
    response_model.status_code = 200
    response_model._content = (
        b'{"result": {"data": {"state": "Vykdymas pavyko",'
        b'"response_data": "[{\\"id\\": 1, \\"date\\": \\"2021-01-01\\", '
        b'\\"price\\": 100, \\"tax\\": 21, \\"total\\": 121}]"}}}'
    )
    return response_model


def test_home_page():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


@patch("robolabs_api.api.requests.post")
def test_get_invoice_list(mock_response, robolabs_api, job_id_response_model):
    mock_response.return_value = job_id_response_model
    job_id = robolabs_api.get_invoice_list("2021-01-01", "2021-01-01")
    assert isinstance(job_id, int)
    assert job_id == 1


@patch("robolabs_api.api.requests.post")
def test_get_job_response_data_fail(mock_response, robolabs_api, job_response_model_failed):
    mock_response.return_value = job_response_model_failed
    with pytest.raises(Exception) as e:
        robolabs_api.get_job_response_data(1)
        assert e == "Error"


@patch("robolabs_api.api.requests.post")
def test_get_job_response_data_success(mock_response, robolabs_api, job_response_model_success):
    mock_response.return_value = job_response_model_success
    job_data = robolabs_api.get_job_response_data(1)
    assert isinstance(job_data, dict)
    assert (
        job_data["result"]["data"]["response_data"]
        == '[{"id": 1, "date": "2021-01-01", "price": 100, "tax": 21, "total": 121}]'
    )


def test_extract_desired_data(robolabs_api):
    job_data = {
        "result": {
            "data": {
                "response_data": """[{"id": 1, "date_invoice": "2021-01-01",
                    "amount_total_invoice_currency": 100,
                    "number": 21, "partner_name": "asd"}]"""
            }
        }
    }
    desired_data = robolabs_api.extract_desired_data(job_data)
    assert isinstance(desired_data, list)
    assert desired_data == [{"date": "2021-01-01", "number": 21, "partner_name": "asd", "amount_total": 100}]
