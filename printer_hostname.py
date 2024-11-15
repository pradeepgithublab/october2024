import socket
import uuid
import requests

# Constants
MIST_API_TOKEN = 'xh9oBdbYQllXCmCh5Ad63h3Y3enrewPWrDD37XpYA5f1ealYTPJQEb2FMkmo0DBi9vFIiLJpNlHd6fM95Zog8e0NldKTnOol'
ORG_ID = '15e7597e-9b06-4381-8443-16aba95c5e0d'
BASE_URL = 'https://api.eu.mist.com/api/v1'

# Get the system hostname
hostname = socket.gethostname()
print(f"User's Hostname: {hostname}")

# Get the system's MAC address
mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
print(f"User's MAC Address: {mac_address}")

# API endpoint for retrieving connected clients in the organization
url = f"{BASE_URL}/orgs/{ORG_ID}/clients"

# Set headers for the API request
headers = {
    "Authorization": f"Token {MIST_API_TOKEN}",
    "Content-Type": "application/json"
}

# Make the API call to get information about connected clients
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check for request errors

    # Parse JSON response
    client_data = response.json()

    # Initialize a variable to track if a matching AP is found
    connected_ap = None

    # Filter the list of clients to find the one that matches the MAC address
    for client in client_data:
        # Check if the client MAC matches the user's MAC address
        if client.get('mac') == mac_address:
            connected_ap = client.get('connected_ap_name')  # Store the AP hostname
            break  # Exit loop once we find the connected AP

    # Display the result
    if connected_ap:
        print(f"\nConnected Access Point Hostname: {connected_ap}")
    else:
        print("\nNo matching access point found for the user's MAC address.")

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
