# Imports the request module to assist in grabbing data from NASA's Asteroid NEO WS API
import requests

# Imports the os module to help read the hidden NASA API Key, done for safekeeping the API key
import os

#Reads the contents of .env
from dotenv import load_dotenv

import utils, radarInterface

from modules import NearEarthObject, NEOStorage

from datetime import date, timedelta

#Loads hidden key into System Environment Variables
load_dotenv()

#Assigns api_key to hidden NASA API key
#api_key_nasa = os.getenv("NASA_API_KEY")

#Url for NeoWs NASA API without search query parameters
#url = "https://api.nasa.gov/neo/rest/v1/feed"

#gets the current date in a YYYY-MM-DD format
#todayDate = str(date.today())

#Dictionary containing the search parameters for the API url (start_date, end_date, and api_key)
#feedQuery_params = {
    #"start_date": "2029-04-13", #todayDate,
    #"end_date": "2029-04-13", #date.today() + timedelta(days=7),
    #"api_key": api_key_nasa
#}

#Creates a response module object containing the raw data of the api call with the search params
#api_response = requests.get(url, params=feedQuery_params)

#Converts the raw data to a parsable and extractable object 
#asteroid_data = api_response.json()

#print("Asteroids between given dates: " + feedQuery_params["start_date"] + " to " + feedQuery_params["end_date"] + " (YYYY-MM-DD)")
#print("------------------------------")
#utils.listAsteroidNameID(asteroid_data)

#print(utils.prettyData(asteroid_data, 4))

#radarInterface.askUserMainChoice()

#radarInterface.askScanChoices()


#Asteroid Hazard Rating Tests
#asteroid_dict_test = asteroid_data["near_earth_objects"]["2026-05-24"][0]

#test_obj = NearEarthObject()

#test_obj.fillObj(asteroid_dict_test)

#print(vars(test_obj))

#test_obj.totalHazardAnalysis()

#print("----------------")

#print(test_obj.get_NEO_classification())



#radarInterface.scanNEOs(asteroid_data["near_earth_objects"], 1)


radarInterface.obtainAPIData()















