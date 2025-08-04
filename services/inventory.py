import json

import httpx
import os
from dotenv import load_dotenv
import logging

from schemas.models import InventoryItemInsert, InventoryItemUpdate, InventoryItemUpdateStock

logger = logging.getLogger(__name__)
load_dotenv()

headers = {
    "AUTH_KEY": os.getenv("API_KEY"),
    "Content-Type": os.getenv("API_CONTENT_TYPE"),
}

endpoint = os.getenv("API_URL") + "/inventory"

async def fetchInventoryItems():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                endpoint,
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            logging.info(f"Fetched inventory items successfully: {response.status_code}")
            return response.json()

        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            return json.dumps({"error": f"HTTP error occurred: {e.response.status_code} - {e.response.text}"})

        except httpx.TimeoutException:
            logging.info("Request timed out")
            return json.dumps({"error": "Request timed out"})


async def addInventoryItem(item: InventoryItemInsert):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                endpoint,
                headers=headers,
                json=item.model_dump(),
                timeout=30.0
            )
            response.raise_for_status()
            logging.info(f"Inventory item added successfully: {response.status_code}")
            return response.json()

        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            return json.dumps({"error": f"HTTP error occurred: {e.response.status_code} - {e.response.text}"})

        except httpx.TimeoutException:
            logging.info("Request timed out")
            return json.dumps({"error": "Request timed out"})


async def updateInventoryItem(item: InventoryItemUpdate):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(
                endpoint,
                headers=headers,
                json=item.model_dump(),
                timeout=30.0
            )
            response.raise_for_status()
            logging.info(f"Inventory item updated successfully: {response.status_code}")
            return response.json()

        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            return json.dumps({"error": f"HTTP error occurred: {e.response.status_code} - {e.response.text}"})

        except httpx.TimeoutException:
            logging.info("Request timed out")
            return json.dumps({"error": "Request timed out"})


async def updateInventoryItemStock(item: InventoryItemUpdateStock):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.patch(
                endpoint,
                headers=headers,
                json=item.model_dump(),
                timeout=30.0
            )
            response.raise_for_status()
            logging.info(f"Inventory new_stock updated successfully: {response.status_code}")
            return response.json()

        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            return json.dumps({"error": f"HTTP error occurred: {e.response.status_code} - {e.response.text}"})

        except httpx.TimeoutException:
            logging.info("Request timed out")
            return json.dumps({"error": "Request timed out"})
