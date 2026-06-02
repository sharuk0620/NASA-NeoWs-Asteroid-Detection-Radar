#Methods that provide the interface and user interactibilty of the radar application
# Imports the request module to assist in grabbing data from NASA's Asteroid NEO WS API
import requests

# Imports the os module to help read the hidden NASA API Key, done for safekeeping the API key
import os

#Reads the contents of .env
from dotenv import load_dotenv

#Imports the json request module to provide the json.dumps function to print the API data in a clean format
import json


#Asks the user to select an option upon initializition of the radar program
def askUserMainChoice():
    
    print("Welcome to the NEO Asteroid Radar! Please select an option below:\n"
          "-----------------------------------------------------------------")
    print("[1] SCAN FOR POTENTIALLY HAZARDEOUS ASTEROIDS")
    print("[2] BROWSE ASTEROIDS")
    print("[3] TERMINATE RADAR\n\n")
    
    while True:
        
        userChoice = input("Please enter the appropriate index corresponding to your choice: ")

        if userChoice in ["1", "2", "3"]:
            print(" ")
            break
        else:
            print("\nInvalid Choice! Please choose an option listed!\n")


#SCANNING OPTION METHODS/FUNCTIONS
# Background: API JSON Data is already called and formatted

def askScanChoices():
    #Agenda: Lay Out Options for user to choose on scanning asteroids 
    
    print("SCAN FOR POTENTIALLY HAZARDEOUS ASTEROIDS:\n"
          "-----------------------------------------------------------------")
    print("[a] SCAN TODAY")
    print("[b] SCAN TOMORROW")
    print("[c] DISPLAY TOP 10 HAZARDS IN THE NEXT 7 DAYS")

    while True:

        userChoice = input("Please enter the appropriate index corresponding to your choice: ")

        if userChoice in ["a", "b", "c"]:
            print(" ")
            break
        else:
            print("\nInvalid Choice! Please choose an option listed!\n")






