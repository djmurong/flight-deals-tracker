import os
from dotenv import load_dotenv
import requests
import datetime

load_dotenv()

TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
OFFERS_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"


class FlightSearch:
    def __init__(self):
        self._api_key = os.getenv("AMADEUS_API_KEY")
        self._api_secret = os.getenv("AMADEUS_API_SECRET")
        self._token = self._get_new_token()

    def _get_new_token(self):
        header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        amadeus_body = {
            "grant_type": "client_credentials",
            "client_id": self._api_key,
            "client_secret": self._api_secret
        }
        response = requests.post(url=TOKEN_ENDPOINT, headers=header, data=amadeus_body)
        print(f"Your token is {response.json()['access_token']}")
        print(f"Your token expires in {response.json()['expires_in']} seconds")
        return response.json()['access_token']

    def get_iata_code(self, city):
        headers = {
            "Authorization": f"Bearer {self._token}"
        }
        query = {
            "keyword": city,
            "max": 2,
            "include": "AIRPORTS",
        }
        response = requests.get(url=IATA_ENDPOINT, params=query, headers=headers)

        print(f"Status code: {response.status_code}. Airplane Iata: {response.text}")

        try:
            code = response.json()["data"][0]["iataCode"]
        except IndexError:
            print(f"IndexError: No airport code found for {city['City']}")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city['City']}")
            return "Not Found"
        else:
            return code

    def check_flights(self, origin_city_code, destination_city_code, from_time):
        headers = {
            "Authorization": f"Bearer {self._token}"
        }
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "currencyCode": "USD"
        }
        response = requests.get(
            url=OFFERS_ENDPOINT,
            params=query,
            headers=headers
        )

        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print(f"Response body: {response.text}")
            return None

        return response.json()
