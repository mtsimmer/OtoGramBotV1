"""
General Info

This file contains all of the relevant config data
"""
"""
GOV Api works with resource IDs 
Regarding the resource_ID
registerd car numbers: 053cea08-09bc-40ec-8f7a-156f0677aff3
diregisterd cars: 851ecab1-0622-4dbe-a6c7-f950cf82abf9
self import: 03adc637-b6fe-402b-9937-7c3d3afc9140
MobileEye priceOff: 83bfb278-7be1-4dab-ae2d-40125a923da1

##Maybe Usefull for further implamintation
licensed resellers: eb74ad8c-ffcd-43bb-949c-2244fc8a8651
statistics regarding models on the market: 5e87a7a1-2f6f-41c1-8aec-7216d52a6cf6
Recalls:                                                                                                 

"""
import re

# Gov database query 
RESOURCE_IDS = ["053cea08-09bc-40ec-8f7a-156f0677aff3","851ecab1-0622-4dbe-a6c7-f950cf82abf9","03adc637-b6fe-402b-9937-7c3d3afc9140","83bfb278-7be1-4dab-ae2d-40125a923da1"]
GENERIC_URL = "https://data.gov.il/api/3/action/datastore_search?resource_id="
GENERIC_DATA = {'resource_id':None, #Contained in the url, depends on what API we are requesting
                'limit':1, #lmits the amount of answers.
                'q':None} #The Query (Pretty much what the user provides).
REQUEST_TYPE = "POST"

ISRAELI_PLATE_REGEX = '^\d{7,8}$'
ISRAELI_PLATE_PATTERN = re.compile(ISRAELI_PLATE_REGEX)

TELEGRAM_BOT_TOKEN = ""

# levi itzhak Query
LEVI_HOST = "https://s.leviitzhak.xyz"
LEVI_BTOKEN = ""
LEVI_ENDPOINTS = {
	"METADATA":"/main/get-by-licence-plate/",
	"PRICE_SUB":"/main/get-submodel/"
}
LEVI_REQUEST_TYPE = "POST"

# meshumashot Query
MESHUMASHOT_HOST = "https://meshumeshet.com"
MESHUMASHOT_ENDPOINTS = {
	"SEARCH":'/c/'
}
MESHUMASHOT_REQUEST_TYPE = "GET"

# Bidspirit Watch
BIDSPIRIT_HOST = 'https://bidspirit-portal.global.ssl.fastly.net'
BIDSPIRIT_ENDPOINTS = {
	"GET_ALL_CAR_AUCTIONS" : "/services/portal/getHomePageData?cdnSubDomain=cars&content=CARS&lang=he&region=IL",
	"GET_SPECIFIC_AUCTION" : "/services/portal/getAuctionPageData?cdnSubDomain=cars&lang=he&withHouseData=true&intKey=",
	"GET_SPECIFIC_ITEM" : "/services/catalogs/getItems?allowErotic=true&allowHidden=false&cdnSubDomain=cars&lang=he&catalogKey="	
}

BIDSPIRIT_SEARCH = 'https://cars.bidspirit.com/ui/search/FUTURE.%7B%7D.all.'