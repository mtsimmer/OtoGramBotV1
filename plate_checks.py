"""
Gets Exact make and model from GOV api
"""

import json, requests
from config import RESOURCE_IDS, GENERIC_URL, GENERIC_DATA, REQUEST_TYPE

def query_gov_api(car_plate):
    replies = [] #list of the returned jsons (a list of dicts)
    for resource_id in RESOURCE_IDS:
        url = GENERIC_URL + resource_id
        data = GENERIC_DATA
        data['resource_id'] = resource_id
        data['q'] = car_plate
        raw_reply = requests.request(REQUEST_TYPE,url,data=data)
        replies.append(json.loads(raw_reply.text))
    return replies

def compose_message(car_plate):
    if car_plate.isdigit():
        if len(car_plate) > 6 and len(car_plate) < 9:
            api_reply = query_gov_api(car_plate)
            composed_message = json.dumps(api_reply[0]["result"]["records"],indent=2,ensure_ascii=False)
            print(composed_message) #DEBUG
            return composed_message
    else:
        return "Invalid Input"

