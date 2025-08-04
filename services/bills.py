import json

from dotenv import load_dotenv
import os
import httpx
import logging

from schemas.models import IssueBill, BillItemAddOrUpdate, BillItemDelete, DraftBill

logger = logging.getLogger(__name__)
load_dotenv()

headers = {
    "AUTH_KEY": os.getenv("API_KEY"),
    "Content-Type": os.getenv("API_CONTENT_TYPE"),
}

endpoint_bill = os.getenv("API_URL") + "/bills"
endpoint_bill_archive = os.getenv("API_URL") + "/billarchive"

# Operations on Bill Records

async def fetchBillRecords():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                endpoint_bill,
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            logging.info(f"Fetched bill records successfully: {response.status_code}")
            return response.json()

        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            return json.dumps({"error": f"HTTP error occurred: {e.response.status_code} - {e.response.text}"})

        except httpx.TimeoutException:
            logging.info("Request timed out")
            return json.dumps({"error": "Request timed out"})

async def fetchBillRecordsByCashier(cashier_id: int):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                endpoint_bill,
                headers=headers,
                json={"cashier_id": cashier_id},
                timeout=30.0
            )
            response.raise_for_status()

            if response.status_code == 200:
                logging.info(f"Fetched bills successfully with status code: {response.status_code}")
            else:
                logging.error(f"Fetch Bills Request Failed with status code: {response.status_code} - {response.text}")

            return response.json()

        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            return json.dumps({"error": f"HTTP error occurred: {e.response.status_code} - {e.response.text}"})

        except httpx.TimeoutException:
            logging.info("Request timed out")
            return json.dumps({"error": "Request timed out"})

async def issueBill(bill: IssueBill):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.patch(
                endpoint_bill,
                headers=headers,
                json=bill.model_dump(),
                timeout=30.0
            )
            response.raise_for_status()

            if response.status_code == 200:
                logging.info(f"Issue Bill Successfully with status code: {response.status_code}")
            else:
                logging.info(f"Issue Bill Request Failed with status code: {response.status_code} - {response.text}")

            return response.json()

        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            return json.dumps({"error": f"HTTP error occurred: {e.response.status_code} - {e.response.text}"})

        except httpx.TimeoutException:
            logging.info("Request timed out")
            return json.dumps({"error": "Request timed out"})

async def discardBill(invoice_no: int):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                "DELETE",
                endpoint_bill,
                headers=headers,
                content=json.dumps({"invoice_no": invoice_no}),
                timeout=30.0
            )
            response.raise_for_status()
            if response.status_code == 200:
                logging.info(f"Discard Bill Successfully with status code: {response.status_code}")
            else:
                logging.info(f"Discard Bill Request Failed with status code: {response.status_code}")

            return response.json()

        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            return json.dumps({"error": f"HTTP error occurred: {e.response.status_code} - {e.response.text}"})

        except httpx.TimeoutException:
            logging.info("Request timed out")
            return json.dumps({"error": "Request timed out"})


# Operations inside a bill entry (BillArchive)

async def createDraftBill(draft_bill: DraftBill):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                endpoint_bill_archive,
                headers=headers,
                json=draft_bill.model_dump(),
                timeout=30.0
            )
            response.raise_for_status()
            if response.status_code == 200 or response.status_code == 207:
                logging.info(f"Created bill successfully with status code: {response.status_code}")
            else:
                logging.error(f"Bill archive request failed: {response.status_code}")

            return response.json()

        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            return json.dumps({"error": f"HTTP error occurred: {e.response.status_code}", "request": f"{draft_bill.model_dump_json()}"})

        except httpx.TimeoutException:
            logging.info("Request timed out")
            return json.dumps({"error": "Request timed out"})


async def openBill(invoice_no: int):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                endpoint_bill_archive + "/" + str(invoice_no),
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()

            if response.status_code == 200:
                logging.info(f"Opened bill successfully with status code: {response.status_code}")
            else:
                logging.error(f"Bill archive request failed: {response.status_code}")

            return response.json()

        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            return json.dumps({"error": f"HTTP error occurred: {e.response.status_code}"})

        except httpx.TimeoutException:
            logging.info("Request timed out")
            return json.dumps({"error": "Request timed out"})


async def addToExistingBill(entry: BillItemAddOrUpdate):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(
                endpoint_bill_archive,
                headers=headers,
                json=entry.model_dump(),
                timeout=30.0
            )
            response.raise_for_status()

            return response.json()

        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            return json.dumps({"error": f"HTTP error occurred: {e.response.status_code}", "request": f"{draft_bill.model_dump_json()}"})

        except httpx.TimeoutException:
            logging.info("Request timed out")
            return json.dumps({"error": "Request timed out"})


async def editProductQty(entry: BillItemAddOrUpdate):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.patch(
                endpoint_bill_archive,
                headers=headers,
                json=entry.model_dump(),
                timeout=30.0
            )
            response.raise_for_status()

            if response.status_code == 200:
                logging.info(f"Updated bill successfully with status code: {response.status_code}")
            else:
                logging.error(f"Bill archive request failed: {response.status_code}")

            return response.json()

        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            return json.dumps({"error": f"HTTP error occurred: {e.response.status_code} - {e.response.text}"})

        except httpx.TimeoutException:
            logging.info("Request timed out")
            return json.dumps({"error": "Request timed out"})


async def deleteBillItem(entry: BillItemDelete):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                "DELETE",
                endpoint_bill_archive,
                headers=headers,
                content=entry.model_dump_json(),
                timeout=30.0
            )
            response.raise_for_status()
            if response.status_code == 200:
                logging.info(f"Deleted bill successfully with status code: {response.status_code}")
            else:
                logging.error(f"Bill archive request failed: {response.status_code} - {response.text}")
            return response.json()

        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            return json.dumps({"error": f"HTTP error occurred: {e.response.status_code} - {e.response.text}"})

        except httpx.TimeoutException:
            logging.info("Request timed out")
            return json.dumps({"error": "Request timed out"})
