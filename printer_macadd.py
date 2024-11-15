import socket
import uuid
import requests

# Constants
MIST_API_TOKEN = 'xh9oBdbYQllXCmCh5Ad63h3Y3enrewPWrDD37XpYA5f1ealYTPJQEb2FMkmo0DBi9vFIiLJpNlHd6fM95Zog8e0NldKTnOol'
ORG_ID = '15e7597e-9b06-4381-8443-16aba95c5e0d'
BASE_URL = 'https://api.eu.mist.com/api/v1'

# Get the system hostname
hostname = socket.gethostname()
print(f"Hostname: {hostname}")

# Get the system's MAC address
mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
print(f"MAC Address: {mac_address}")

# API endpoint for retrieving AP information for the organization
url = f"{BASE_URL}/orgs/{ORG_ID}/devices"

# Set headers for the API request
headers = {
    "Authorization": f"Token {MIST_API_TOKEN}",
    "Content-Type": "application/json"
}

# Make the API call to get information about connected APs
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check for request errors

    # Print information about connected APs
    ap_data = response.json()
    print("\nConnected Access Points:")
    for ap in ap_data:
        print(f"AP Name: {ap.get('name')}, MAC: {ap.get('mac')}, Model: {ap.get('model')}, Status: {ap.get('status')}")

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
