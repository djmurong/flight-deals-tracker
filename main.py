import requests
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

ORIGIN_CITY_IATA = "BHM"

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()

flight_search = FlightSearch()
for row in sheet_data:
    if row["IATA Code"] == "":
        row["IATA Code"] = flight_search.get_iata_code(row["City"])

data_manager.destination_data = sheet_data
data_manager.update_iata_codes()
emails_list = data_manager.get_customer_emails()

tomorrow = datetime.now() + timedelta(days=1)
six_months_later = datetime.now() + timedelta(days=(6 * 30))

# print(tomorrow, six_months_later)
# print(tomorrow.strftime("%Y-%m-%d"), six_months_later.strftime("%Y-%m-%d"))

notification_manager = NotificationManager()

for row in sheet_data:
    flight_offers = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        row["IATA Code"],
        six_months_later
    )
    # print(flight_offers)
    cheapest_flight_data = FlightData.find_cheapest_flight(flight_offers)
    if cheapest_flight_data.price != "N/A" and cheapest_flight_data.price < float(row["Lowest Price"]):
        msg = f"Low price alert! Only ${cheapest_flight_data.price} to fly from " \
              f"{cheapest_flight_data.origin_airport} to {cheapest_flight_data.destination_airport}, " \
              f"on {cheapest_flight_data.out_date} until {cheapest_flight_data.return_date}"

        print(f"Check your email. Lower price flight found to {row["City"]}!")

        notification_manager.send_whatsapp(msg_body=msg)

        notification_manager.send_email(customer_emails=emails_list, email_body=msg)
