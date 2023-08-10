import json
import os
import time
from typing import Any

import requests
import structlog
from dotenv import load_dotenv

from robolabs_api import settings

logger = structlog.get_logger()


class RoboLabsApi:
    def __init__(self):
        load_dotenv()
        self.job_check_wait_time = settings.job_check_wait_time
        self.robolabs_api_secret = os.getenv("ROBOLABS_API_SECRET")
        self.robolabs_api_url = os.getenv("ROBOLABS_API_URL")

    def get_invoice_list(self, date_from: str, date_to: str) -> int:
        """Send post request to RoboLabs API and return job id"""
        logger.info("Getting invoice list", date_from=date_from, date_to=date_to)
        data = {
            "secret": self.robolabs_api_secret,
            "date_from": date_from,
            "date_to": date_to,
        }
        invoice_request = requests.post(f"{self.robolabs_api_url}get_invoice_list", json=data)
        job_id = invoice_request.json()["result"]["data"]["api_job_id"]
        logger.info("Job id received", job_id=job_id)
        return job_id

    def get_job_response_data(self, job_id: int) -> dict[str, Any]:
        """
        Send post request to RoboLabs API and return the data if the job is finished
        Strip down invoice list to desired data
        """
        while True:
            try:
                logger.info("Getting job response data", job_id=job_id)
                job_request = requests.post(
                    f"{self.robolabs_api_url}get_api_job",
                    json={"secret": self.robolabs_api_secret, "api_job_id": job_id},
                )
                job_request.raise_for_status()
                job_state = job_request.json()["result"]["data"]["state"]
                if job_state == "Laukiama vykdymo":
                    logger.info("Job is still running", job_id=job_id)
                    time.sleep(self.job_check_wait_time)
                    continue
                if job_state == "Vykdymas nepavyko":
                    raise Exception(job_request.json()["result"]["data"]["response_message"])
                break
            except Exception as e:
                logger.error("Job failed", job_id=job_id, error=e)
                raise e
        return job_request.json()

    def extract_desired_data(self, job_data: dict[str, Any]) -> list[dict[str, Any]]:
        """Strip down invoice data list to desired data"""
        invoice_list = json.loads(job_data["result"]["data"]["response_data"])
        data = [
            {
                "date": invoice["date_invoice"],
                "number": invoice["number"],
                "partner_name": invoice["partner_name"],
                "amount_total": invoice["amount_total_invoice_currency"],
            }
            for invoice in invoice_list
        ]
        logger.info("Job response data received successfully", data_length=len(data))
        return data


if __name__ == "__main__":
    robolabs_api = RoboLabsApi()
    job_id = robolabs_api.get_invoice_list("2023-06-01 00:00:00", "2023-08-09 00:00:00")
    data = robolabs_api.get_job_response_data(job_id)
    robolabs_api.extract_desired_data(data)
