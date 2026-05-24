# Imports the request module to assist in grabbing data from NASA's Asteroid NEO WS API
import requests

# Imports the os module to help read the hidden NASA API Key, done for safekeeping the API key
import os

#Reads the contents of .env
from dotenv import load_dotenv

import utils


#Loads hidden key into System Environment Variables
load_dotenv()

#Assigns api_key to hidden NASA API key
api_key_nasa = os.getenv("NASA_API_KEY")

#Url for NeoWs NASA API without search query parameters
url = "https://api.nasa.gov/neo/rest/v1/feed"

#Dictionary containing the search parameters for the API url (start_date, end_date, and api_key)
feedQuery_params = {
    "start_date": "2026-05-22",
    "end_date": "2026-05-27",
    "api_key": api_key_nasa
}

#Creates a response module object containing the raw data of the api call with the search params
api_response = requests.get(url, params=feedQuery_params)

#Converts the raw data to a parsable and extractable object 
asteroid_data = api_response.json()


#utils.printName_NeoID(asteroid_data)

#print(utils.prettyData(asteroid_data, 4))



#NEO Search UP

url = "https://api.nasa.gov/neo/rest/v1/neo/3837653"

lookQuery_params = {
    #"asteroid_id": "3837653",
    "api_key": api_key_nasa
}

asteroidLookUp = (requests.get(url, params=lookQuery_params)).json()

cleanData = asteroidLookUp["close"]

print(utils.prettyData(asteroidLookUp, 4))






