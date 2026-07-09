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


#Start of Program

while True:

    radarInterface.askUserMainChoice()      
    userChoice = input("Please enter the appropriate index corresponding to your choice: ")

    if userChoice in ["1", "2", "3"]:
        print(" ")
        break
    else:
        print("\nInvalid Choice! Please choose an option listed!\n")



#radarInterface.obtainInitialData()

#radarInterface.scanWeek()















