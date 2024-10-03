import json
import logging as logger
from random import choice
from requests import request
from user_agents import android_ua
from config import BIDSPIRIT_HOST, BIDSPIRIT_ENDPOINTS


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

def get_auction_item_by_catalog(catalogKey)
	URL = BIDSPIRIT_HOST + BIDSPIRIT_ENDPOINTS['GET_SPECIFIC_ITEM'] + str(catalogKey)
	logger.debug(f'Querying : {URL}')
	resp = request("GET", URL, headers=HEADERS).text
	all_offers = json.loads(resp)
	logger.debug(f'retrieved  : {all_offers}')
	return all_offers
	


#Rename later
def main():
	all_auctions = get_all_car_auctions()
	upcoming_auctions = all_auctions['auctionsLists']['UPCOMING']
	for auction in upcoming_auctions:
		all_offers = get_auction_offers(auction['intKey'])
		for offer in all_offers:
			get_auction_item(offer[''])

