import datetime
import os
from time import sleep

import requests

token = "<Add Your JWT Token>"


def get_reponse(data):
    response = []
    for center in data.get("centers"):
        sessions = center.get('sessions')
        center_name = center.get("name")
        for session in sessions:
            available_capacity = session.get("available_capacity")
            min_age_limit = session.get("min_age_limit")
            slots = session.get("slots")
            date = session.get("date")
            if available_capacity and int(available_capacity) >= 1 and int(min_age_limit) <= 18:
                response.append({'center_name': center_name, "available_capacity": available_capacity, "slots": slots,
                                 "date": date})
            else:
                pass
    return response


loop_condition = True
count = 0
while loop_condition:
    today = datetime.datetime.now().date().strftime("%d-%m-%Y")
    URL = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=770&date={today}"
    TOKEN = "Bearer {token}"
    HEADERS = {'Authorization': TOKEN}
    request = requests.get(url=URL, headers=HEADERS)
    # request = requests.get(url=URL)
    print(request.status_code)
    if request.status_code == 200:
        data = get_reponse(request.json())
        if data:
            for x in data:
                center_name = x.get("center_name")
                available_capacity = x.get("available_capacity")
                slots = x.get("slots")
                date = x.get("date")
                print(
                    f"Center Name = {center_name} \nAvailable Capacity = {available_capacity}"
                    f"\nSlots: {slots}\nDate: {date}\n")
        sleep(5)
        count += 1
        if count > 6:
            os.system('cls' if os.name == 'nt' else 'clear')
            count = 0

    elif request.status_code == 304:
        sleep(10)
    elif request.status_code == 403:
        exit(0)
    elif request.status_code == 401:
        sleep(20)
    else:
        sleep(20)
