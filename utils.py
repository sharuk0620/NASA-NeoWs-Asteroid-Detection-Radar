#Helper Functions to parse API data
# Imports the request module to assist in grabbing data from NASA's Asteroid NEO WS API
import requests

# Imports the os module to help read the hidden NASA API Key, done for safekeeping the API key
import os

#Reads the contents of .env
from dotenv import load_dotenv

#Imports the json request module to provide the json.dumps function to print the API data in a clean format
import json



def listAsteroidNameID(jsonData):
    #Creates a secondary dictonary of the "near_earth_objects" section
    neo_data = jsonData.get("near_earth_objects")

    #increment variable
    increment = 1

    #Nested For Loop: First loop parses through each date of api call, while second loop parses data for each asteroid for every date within search dates
    for date in neo_data:
        for asteroid in neo_data[date]:
            #Obtains the name and id for an asteroid of a certain date
            asteroid_name = asteroid.get("name")
            asteroid_id = asteroid.get("id")
                
            #prints out the asteroid's name and NEO id
            print(f"{increment}. {asteroid_name}, {asteroid_id}.")
            increment += 1
    return

#def analyzePlanetSafety(asteroidData):
    



def prettyData(jsonData, indentValue):

    return json.dumps(jsonData, indent=indentValue)



