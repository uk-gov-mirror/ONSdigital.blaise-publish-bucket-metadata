import requests
import os

def patch(payload, fileName):
    try:
        baseUrl = os.getenv("DDS_URL")
        url = f"{baseUrl}/v1/state/{fileName}"
        request = requests.patch(url, json=payload)
        print(f"Updated DDS for {fileName} with the state {payload}")
    except Exception as error:
        print(f"Unable to send patch request: {error}")

def error(fileName, state, error_message):
    try:
        payload = { "state":state, "error_info": error_message }
        patch(payload, fileName)
    except Exception as error:
        print(f"Unable to update state for {fileName}, error: {error}")

def update(fileName, state):
    try:
        payload = { "state":state }
        patch(payload, fileName)
    except Exception as error:
        print(f"Unable to update state for {fileName}, error: {error}")
