from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from env import SERVER_TOKEN, MAPS_KEY
from ast import literal_eval
import requests

def format_coordinates(coord):
    temp = str(coord)
    lst = temp.split(".")
    ret = lst[0] + "." + lst[1][:3]
    return ret

def find_uberX_estimate(prices):
    for p in prices:
        if p["localized_display_name"] == "uberX":
            return p["estimate"]
    return "not found"

def get_uberX_info(start_lat, start_lng, end_lat, end_lng):
    session = Session(server_token=SERVER_TOKEN)
    client = UberRidesClient(session)

    response = client.get_price_estimates(
        start_latitude=start_lat,
        start_longitude=start_lng,
        end_latitude=end_lat,
        end_longitude=end_lng,
        seat_count=2
    )

    return find_uberX_estimate(response.json.get('prices'))

def main():
    start_loc = input("What is the starting address? ")
    end_loc = input("What is the ending address? ")

    start_info = requests.get(
        "https://maps.googleapis.com/maps/api/geocode/json?address=" + start_loc + "&key=" + MAPS_KEY)
    end_info = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + end_loc + "&key=" + MAPS_KEY)

    start_info = literal_eval(start_info.content.decode("utf-8"))
    end_info = literal_eval(end_info.content.decode("utf-8"))

    start_lat = format_coordinates(start_info["results"][0]["geometry"]["location"]["lat"])
    start_lng = format_coordinates(start_info["results"][0]["geometry"]["location"]["lng"])
    end_lat = format_coordinates(end_info["results"][0]["geometry"]["location"]["lat"])
    end_lng = format_coordinates(end_info["results"][0]["geometry"]["location"]["lng"])


    print(get_uberX_info(start_lat,start_lng,end_lat,end_lng))

main()