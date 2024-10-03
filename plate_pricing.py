"""
Levi itzhak Price checks
"""
import json
from random import choice
from requests import request
from user_agents import android_ua
from config import LEVI_HOST, LEVI_REQUEST_TYPE, LEVI_BTOKEN, LEVI_ENDPOINTS

HEADERS = {
	"Accept-Language": "en-US,en;q=0.9",
	"Content-Length": "22",
	"Authorization": LEVI_BTOKEN,
	"User-Agent": choice(android_ua),
	"Accept": "application/json",
	"Content-Type": "application/json",
	"Origin": "https://s.leviitzhak.xyz",
	"X-Requested-With": "com.levinew.app",
	"Sec-Fetch-Site": "cross-site",
	"Sec-Fetch-Mode": "cors",
	"Sec-Fetch-Dest": "empty",
	"Referer": "https://s.leviitzhak.xyz/",
	"Accept-Encoding": "gzip, deflate, br"
}

#{"plate":18734101}

def get_plate_metadata(plate):
	#print(LEVI_REQUEST_TYPE, LEVI_HOST+LEVI_ENDPOINTS["METADATA"], HEADERS, {"plate":int(plate)})
	bplates = b'{\r\n"plate":'+ plate.encode("utf8") +b'\r\n}'
	HEADERS['Content-Length'] = str(len(bplates))
	#add exception handling
	metadata_resp = request(LEVI_REQUEST_TYPE, LEVI_HOST+LEVI_ENDPOINTS["METADATA"], headers=HEADERS, data=bplates)
	#try:
	return(json.loads(metadata_resp.text)['data'])

def get_price_submodel(manuf, model, car_submodel, owner_type):
	search_meta = {"type":owner_type,"manufacturer":manuf,"model":model,"subModel":car_submodel}
	HEADERS['Content-Length'] = str(len(search_meta))
	metadata_resp = request(LEVI_REQUEST_TYPE, LEVI_HOST+LEVI_ENDPOINTS["PRICE_SUB"], headers=HEADERS, data=json.dumps(search_meta))
	return(json.loads(metadata_resp.text)['data']['Year0'])


def levi_price(plate):
	meta = get_plate_metadata(plate)
	get_price_submodels_per_year = get_price_submodel(meta['search']['manufacturer']['id'], meta['search']['model']['id'], meta['car']['id'], meta['car']['type']['id'])
	for year_price in get_price_submodels_per_year:
		if meta['car']['year'][0] == year_price['$']['Year0']:
			print(year_price['$']['Cost'])
			return year_price['$']['Cost']
