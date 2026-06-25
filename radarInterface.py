#Methods that provide the interface and user interactibilty of the radar application
# Imports the request module to assist in grabbing data from NASA's Asteroid NEO WS API
import requests

# Imports the os module to help read the hidden NASA API Key, done for safekeeping the API key
import os

import itertools

#Reads the contents of .env
from dotenv import load_dotenv

from datetime import date, datetime, timedelta

#Imports the json request module to provide the json.dumps function to print the API data in a clean format
import json

#Imports modules
from modules import NearEarthObject, NEOStorage


#Global Constants:
currentDate = date.today() #Stores the current date in a YYYY-MM-DD date object

today_tomorrow_list = NEOStorage()

seven_day_list = NEOStorage()

testList = NEOStorage()





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

def obtainAPIData():

    #Assigns api_key to hidden NASA API key
    api_key_nasa = os.getenv("NASA_API_KEY")

    #Url for NeoWs NASA API without search query parameters
    url = "https://api.nasa.gov/neo/rest/v1/feed"

    #1 API CALL 

    #Dictionary containing the search parameters for the API url (start_date, end_date, and api_key)
    feedQuery_params = {
        "start_date": currentDate - timedelta(days=1),
        "end_date": currentDate + timedelta(days=2),
        "api_key": api_key_nasa
    }
    
    #Creates a response module object containing the raw data of the api call with the search params
    api_response = requests.get(url, params=feedQuery_params)

    #Converts the raw data to a parsable and extractable object 
    neo_data = api_response.json().get("near_earth_objects")

    ### LOGIC HERE TO PUT INTO TODAY/TMRW LIST

    iterable_data = itertools.chain.from_iterable(neo_data.values())

    for neo in iterable_data:
        curNEO = NearEarthObject()
        curNEO.fillObj(neo)
        today_tomorrow_list.neoCollection.append(curNEO)
    


    for neo in today_tomorrow_list.neoCollection:
        print(neo)
    
    
    #2ND API CALL

    feedQuery_params["start_date"] = currentDate + timedelta(days=3)
    feedQuery_params["end_date"] = currentDate + timedelta(days=7)

    #Creates a response module object containing the raw data of the api call with the search params
    api_response = requests.get(url, params=feedQuery_params)

    #Converts the raw data to a parsable and extractable object 
    neo_data = api_response.json().get("near_earth_objects")

    ### LOGIC HERE TO CREATE 7-DAY LIST

    seven_day_list.neoCollection = today_tomorrow_list.neoCollection.copy()

    iterable_data = itertools.chain.from_iterable(neo_data.values())

    for neo in iterable_data:
        curNEO = NearEarthObject()
        curNEO.fillObj(neo)
        seven_day_list.neoCollection.append(curNEO)



def filterAPIDataSingle(filter_date, neo_list):

    #Obtain date before and after filter date.

    prevDay = filter_date - timedelta(days=1)
    nextDay = filter_date + timedelta(days=1)

    filteredNEOs = []
    for neo in neo_list:
        neo_date =  datetime.strptime(neo.localApproachDate, "%Y-%m-%d").date()
        if(prevDay < neo_date < nextDay):
            filteredNEOs.append(neo)
            print(neo)
    today_tomorrow_list.neoCollection = filteredNEOs

def filterAPIDataWeek(neo_list):

    endOfSevenDays = date.today() + timedelta(days=6)

    filteredNEOs = []
    for neo in neo_list:
        neo_date =  datetime.strptime(neo.localApproachDate, "%Y-%m-%d").date()
        if(date.today <= neo_date <= endOfSevenDays):
            filteredNEOs.append(neo)
            print(neo)
        seven_day_list.neoCollection = filteredNEOs

        


        





    







#SCANNING OPTION METHODS/FUNCTIONS
# Background: API JSON Data is already called and formatted

def askScanChoices():
    #Agenda: Lay Out Options for user to choose on scanning asteroids 
    
    print("SCAN FOR POTENTIALLY HAZARDEOUS ASTEROIDS:\n"
          "-----------------------------------------------------------------")
    print("[a] SCAN TODAY")
    print("[b] SCAN TOMORROW")
    print("[c] DISPLAY TOP 10 HAZARDS IN THE NEXT 7 DAYS\n\n")

    while True:

        userChoice = input("Please enter the appropriate index corresponding to your choice: ")

        if userChoice in ["a", "b", "c"]:
            print(" ")
            break
        else:
            print("\nInvalid Choice! Please choose an option listed!\n")


def initializeNEOList():
    if(len(testList.neoCollection) != 0):
        testList.neoCollection = []
    for i in range(50):
        testList.neoCollection.append(NearEarthObject())
    #print(len(testList.neoCollection))

def evaluateHazRatings(hazScore, scoreList):
    if(hazScore >= 0.90):
        scoreList["critical"] += 1
    elif(hazScore >= 0.80):
        scoreList["severe"] += 1
    elif(hazScore >= 0.60):
        scoreList["elevated"] += 1
    elif(hazScore >= 0.40):
        scoreList["moderate"] += 1
    elif(hazScore >= 0.20):
        scoreList["low"] += 1
    else:
        scoreList["safe"] += 1


#Agenda: Evaluate close approaching 
def scanNEOs(nearEarthData, choice):
    #Attain Current Date


    initializeNEOList()

    threatCounts = {
        "critical": 0,
        "severe": 0,
        "elevated": 0,
        "moderate": 0,
        "low": 0,
        "safe": 0
    }

    index = 0

    #Today and Tomorrow Scans
    if(choice != 3):

        if(choice == 1):
            scanDate = currentDate
        else:
            scanDate = date.today() + timedelta(days=1)
    
        
        for asteroid in nearEarthData["2029-04-13"]:
            curNEO = testList.neoCollection[index]
            curNEO.fillObj(asteroid)
            print(curNEO)
            curHazScore = curNEO.hazardousRating

            evaluateHazRatings(curHazScore, threatCounts)
            index += 1
    else:
        dateList = nearEarthData.values()

        threatList = [neo for date in dateList for neo in date]

        for neo_data in threatList:
            curNEO = testList.neoCollection[index]
            curNEO.fillObj(neo_data)
            curHazScore = curNEO.hazardousRating

            evaluateHazRatings(curHazScore, threatCounts)
            index += 1
                
    print("SCAN COMPLETE! RESULTS:")
    print("-----------------------")
    print(f"CRITICAL THREATS: {threatCounts["critical"]}")
    print(f"SEVERE THREATS: {threatCounts["severe"]}")
    print(f"ELEVATED THREATS: {threatCounts["elevated"]}")
    print(f"MODERATE THREATS: {threatCounts["moderate"]}")
    print(f"LOW THREATS: {threatCounts["low"]}")
    print(f"SAFE NEOs : {threatCounts["safe"]}")





        