# This file, connects the invmgmt api and is used to manage users.

import json
import httpx
from dotenv import load_dotenv
import os
import logging

from schemas.models import User

logger = logging.getLogger(__name__)
load_dotenv()

headers = {
    "AUTH_KEY": os.getenv("API_KEY"),
    "Content-Type": os.getenv("API_CONTENT_TYPE"),
}

async def fetchUsers(): 
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                os.getenv("API_URL") + "/users",
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            logging.info(f"Fetched users successfully: {response.status_code}")
            return response.json()

        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            return json.dumps({"error": f"HTTP error occurred: {e.response.status_code}"})

        except httpx.TimeoutException:
            logging.info("Request timed out")
            return json.dumps({"error": "Request timed out"})


async def addUser(user: User):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                os.getenv("API_URL") + "/users",
                headers=headers,
                json=user.model_dump(),
                timeout=30.0
            )
            response.raise_for_status()
            logging.info(f"User added successfully: {response.status_code}")
            return response.json()

        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            return json.dumps({"error": f"HTTP error occurred: {e.response.status_code}"})

        except httpx.TimeoutException:
            logging.info("Request timed out")
            return json.dumps({"error": "Request timed out"})