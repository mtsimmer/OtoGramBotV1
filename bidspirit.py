import json
import logging as logger
from random import choice
from requests import request
from user_agents import android_ua
from plate_checks import query_gov_api
from config import BIDSPIRIT_HOST, BIDSPIRIT_ENDPOINTS, ISRAELI_PLATE_PATTERN

#Change log level accordingly
logger.basicConfig(level=logger.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

HEADERS = {
	'sec-ch-ua-platform': '"Android"',
	'Referer': 'https://cars.bidspirit.com/',
	'User-Agent': choice(android_ua),
	'Accept': 'application/json, text/plain, */*',
	'DNT': '1',
	'sec-ch-ua-mobile': '?0'
 }

class bidspirit_car_offer:
	def __init__(self, plate, **kwargs):
		self.plate = plate
		for key, value in kwargs.items():
			setattr(self, key, value)


def get_all_car_auctions():
	URL = BIDSPIRIT_HOST+BIDSPIRIT_ENDPOINTS['GET_ALL_CAR_AUCTIONS']
	logger.debug(f'Querying : {URL}')
	resp = request("GET", URL, headers=HEADERS).text
	all_auctions = json.loads(resp)
	logger.debug(f'retrieved  : {all_auctions}')
	return all_auctions

def get_auction_offers(intKey):
	URL = BIDSPIRIT_HOST + BIDSPIRIT_ENDPOINTS['GET_SPECIFIC_AUCTION'] + str(intKey)
	logger.debug(f'Querying : {URL}')
	resp = request("GET", URL, headers=HEADERS).text
	all_offers = json.loads(resp)
	logger.debug(f'retrieved  : {all_offers}')
	return all_offers

def get_all_auction_items(catalogKey):
	URL = BIDSPIRIT_HOST + BIDSPIRIT_ENDPOINTS['GET_SPECIFIC_ITEM'] + str(catalogKey)
	logger.debug(f'Querying : {URL}')
	resp = request("GET", URL, headers=HEADERS).text
	all_offers = json.loads(resp)
	logger.debug(f'retrieved  : {all_offers}')
	return all_offers

def get_plate_from_offer(offer):
	try:
		car_number = offer["carInfo"]["carNumber"]
	except (TypeError, KeyError) as e:
		logger.error("Couldnt retrieve car number")
		return None
	clean_car_number = car_number.replace(" ", "").replace("-", "")
	clean_car_number = ISRAELI_PLATE_PATTERN.match(clean_car_number)
	try:
		return clean_car_number.string
	except AttributeError as e:
		logger.info("Plate isnt ligal")
		return None
	
def get_all_plates_from_all_auction():
	all_plates = []
	all_auctions = get_all_car_auctions()
	try:
		upcoming_auctions = all_auctions["auctionsLists"]["UPCOMING"]
	except (TypeError, KeyError) as e:
		logger.error("Couldnt retrieve upcoming auction list")
	for auction in upcoming_auctions:
		all_offers = get_all_auction_items(auction["intKey"])
		for offer in all_offers:
			plate = get_plate_from_offer(offer)
			if plate != None:
				all_plates.append(plate)
	return all_plates

def get_all_bidspirit_offers(plates):
	bidspirit_enriched_offers = []
	for plate in plates:
		gov_query = query_gov_api(plate)[0]
		try: 
			gov_plate_enrich = gov_query['result']['records'][0]
		except (TypeError, KeyError, IndexError) as e:
			logger.error("Didnt get proper gov result")
		if gov_plate_enrich != [] and gov_plate_enrich != None and gov_plate_enrich != {}:
			bidspirit_enriched_offers.append(bidspirit_car_offer(plate, **gov_plate_enrich))
	return bidspirit_enriched_offers


def generate_offer_search(plate):
	#Return link that searches the plate
	pass