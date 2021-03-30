import requests
import os

def patch(payload):
    try:
        baseUrl = os.getenv("DDS_URL")
        url = f"{baseUrl}/v1/state/{fileName}"
        request = requests.patch(url, json=payload)
    except:
        print(f"Unable to send patch request")

def errorDataDeliveryStatus(fileName, state, error_message):
    try:
        payload = { "state":state, "error_info": error_message }
        patch(payload)
    except Exception:
        print(f"Unable to update state for {fileName}")

def updateDataDeliveryStatus(fileName, state):
    try:
        payload = { "state":state }
        patch(payload)
    except Exception:
        print(f"Unable to update state for {fileName}")
