import os
import requests
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

# //for sheety api
# sheet_id = "1hZlxWuJXFyVVQa71YzTmUt5HtbjFUEFF9PbP8Ets_Yg"
# sheet = client.open_by_key(sheet_id)

load_dotenv()

SHEETDB_PRICES_ENDPOINT = "https://sheetdb.io/api/v1/7qoxp4nvri10q"
sheetdb_header = {
    "Authorization": f"Bearer {os.getenv('SHEETDB_TOKEN')}"
}


class DataManager:

    def __init__(self):
        self.destination_data = {}
        self.customer_data = {}

    def get_destination_data(self):
        data = {
            'sheet': "prices"
        }
        response = requests.get(
            url=SHEETDB_PRICES_ENDPOINT,
            json=data,
            headers=sheetdb_header)
        data = response.json()
        # print(data)
        self.destination_data = data
        return self.destination_data

    def update_iata_codes(self):
        for city in self.destination_data:
            new_data = {
                'sheet': "prices",
                'data': {
                    'IATA Code': city["IATA Code"],
                }
            }
            response = requests.patch(
                url=f"{SHEETDB_PRICES_ENDPOINT}/City/{city["City"]}",
                json=new_data,
                headers=sheetdb_header
            )
            print(f"Response code: {response.status_code}. Body: {response.text}")

    def get_customer_emails(self):
        data = {
            'sheet': "users"
        }
        response = requests.get(
            url=SHEETDB_PRICES_ENDPOINT,
            json=data,
            headers=sheetdb_header)
        self.customer_data = response.json()
        # print(self.customer_data)
        email_list = []
        for customer in self.customer_data:
            email_list.append(customer["What is your email?"])
        return email_list
