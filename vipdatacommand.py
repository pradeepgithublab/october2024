import requests
import json
import pandas as pd

# Define your Mist API credentials and organization/site IDs
api_token = 'xh9oBdbYQllXCmCh5Ad63h3Y3enrewPWrDD37XpYA5f1ealYTPJQEb2FMkmo0DBi9vFIiLJpNlHd6fM95Zog8e0NldKTnOol'
org_id = '15e7597e-9b06-4381-8443-16aba95c5e0d'
site_id = '7ddd12b8-7ecf-451f-9f52-88b3b7ae30c3'

# Headers for the API requests
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Token {api_token}'
}

# Function to load hostnames from an Excel file
def load_hostnames_from_excel(file_path):
    df = pd.read_excel(file_path)  # Assuming 'hostname' is the column header
    return df['hostname'].tolist()

# Function to filter client data based on the provided hostname
def get_wifi_metrics_for_vip_hostnames(vip_hostnames):
    vip_metrics = []
    missing_hostnames = []

    # Fetch client connection details from the Mist API
    response = requests.get(
        f'https://api.eu.mist.com/api/v1/sites/{site_id}/stats/clients',
        headers=headers
    )
    
    if response.status_code == 200:
        client_data = response.json()
        if client_data:
            matched_hostnames = [client_info.get('hostname') for client_info in client_data]
            for hostname in vip_hostnames:
                if hostname in matched_hostnames:
                    # Get metrics for matching hostnames
                    for client_info in client_data:
                        if client_info.get('hostname') == hostname:
                            vip_metrics.append({
                                'hostname': client_info.get('hostname', 'N/A'),
                                'mac': client_info.get('mac', 'N/A'),
                                'ip': client_info.get('ip', 'N/A'),
                                'ssid': client_info.get('ssid', 'N/A'),
                                'band': client_info.get('band', 'N/A'),
                                'channel': client_info.get('channel', 'N/A'),
                                'vlan_id': client_info.get('vlan_id', 'N/A'),
                                'rssi': client_info.get('rssi', 'N/A'),
                                'snr': client_info.get('snr', 'N/A')
                            })
                else:
                    # If hostname is missing from the client data, add to missing list
                    missing_hostnames.append(hostname)
        else:
            print("No client data available.")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        
    return vip_metrics, missing_hostnames

# Function to display the available and missing Wi-Fi metrics
def display_wifi_metrics(vip_metrics, missing_hostnames):
    if vip_metrics:
        # Create a DataFrame to display the data in a single row format
        df = pd.DataFrame(vip_metrics)
        print("Consolidated Data for Hostnames with Available Metrics:")
        print(df.to_string(index=False))
    else:
        print("No available metrics for any of the hostnames.")
    
    if missing_hostnames:
        # Display hostnames without available data
        print("\nData is not Available for the following Hostnames:")
        df_missing = pd.DataFrame(missing_hostnames, columns=['hostname'])
        print(df_missing.to_string(index=False))
    else:
        print("\nAll hostnames have available metrics.")

def main():
    # Load hostnames from Excel file
    vip_hostnames = load_hostnames_from_excel('C:\\mist\\hostname.xlsx')  # Replace with your file path
    vip_metrics, missing_hostnames = get_wifi_metrics_for_vip_hostnames(vip_hostnames)
    
    # Display the consolidated Wi-Fi metrics and missing hostnames
    display_wifi_metrics(vip_metrics, missing_hostnames)

if __name__ == '__main__':
    main()
