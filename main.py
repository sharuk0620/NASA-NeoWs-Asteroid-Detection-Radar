# Imports the request module to assist in grabbing data from NASA's Asteroid NEO WS API
import requests
# Imports the os module to help read the hidden NASA API Key, done for safekeeping the API key
import os

#Reads the contents of .env
from dotenv import load_dotenv

#Loads hidden key into System Environment Variables
load_dotenv()

#Assigns api_key to hidden NASA API key
api_key_nasa = os.getenv("NASA_API_KEY")

#Url for NeoWs NASA API without search query parameters
url = "https://api.nasa.gov/neo/rest/v1/feed"

#Dictionary containing the search parameters for the API url (start_date, end_date, and api_key)
query_params = {
    "start_date": "2026-05-22",
    "end_date": "2026-05-27",
    "api_key": api_key_nasa
}

#Creates a response module object containing the raw data of the api call with the search params
api_response = requests.get(url, params=query_params)

#Converts the raw data to a parsable and extractable object 
asteroid_data = api_response.json()

#Creates a secondary dictonary of the "near_earth_objects" section
neo_data = asteroid_data.get("near_earth_objects")

#Nested For Loop: First loop parses through each date of api call, while second loop parses data for each asteroid for every date within search dates
for date in neo_data:
    for asteroid in neo_data[date]:
        #Obtains the name and id for an asteroid of a certain date
        asteroid_name = asteroid.get("name")
        asteroid_id = asteroid.get("id")
        
        #prints out the asteroid's name and NEO id
        print(asteroid_name + ", " + asteroid_id)
