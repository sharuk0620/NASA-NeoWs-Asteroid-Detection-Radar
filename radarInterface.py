"""
radarInterface.py
-------
File containing radar logic and primary functions to filter, parse, analyze, and display NEO data 
for the user's disposal.

Author:  Sai Sharuk Lakshmi Narayanan
Created: June 1st, 2026
Last Updated: July 20th, 2026
Version: 1.0 (Prototype)
License: MIT
"""

# ==========================================================
# 1. IMPORTS
# ==========================================================

# Built-in python modules
import os
import sys
import subprocess
import itertools
from datetime import date, datetime, timedelta
import json
import time

# 3rd-party modules installed via pip
from dotenv import load_dotenv
import requests

# Custom modules
from modules import NearEarthObject, NEOStorage


# ==========================================================
# 2. GLOBAL CONSTANTS
# ==========================================================

# Stores raw, unfilitered NEO data used for today or tomorrow scans/browsing
TODAY_TOMORROW_LIST = NEOStorage()

# Stores raw, unfilitered NEO data used for full week scan/browsing
SEVEN_DAY_LIST = NEOStorage()

# Manages filtered NEOs of interest based on user's radar choices 
MASTER_LIST = NEOStorage()



# =============================================================================
# 3. API DATA ACQUISITION: 2-CALL OVERLAPPING FETCH (10-DAY TOTAL WINDOW)
# =============================================================================
# PROBLEM: 
# NASA's NeoWS API acts upon UTC (Coordinated Universal Time). Because of this, 
# an NEO approaching on a certain date/time in the user's local timezone may not appear 
# in an explicit API call with the same date if UTC has rolled over to the next day.
# In addition, NASA's API call time frame boundaries are limited to 7 days at most.
#
# SOLUTION:
# Allow for a day before and after the week's worth of data to catch NEOs that are omitted
# due to UTC rolling over before local time zone, and to avoid time frame boundary, split
# API call into 2 separate calls that obtain a collective 10-day window of NEOs. Finally,
# combine both lists together for the entire week's worth of NEO data.
#
# LOGIC:
# Calls NASA NeoWS API across two queries to fetch data from Yesterday 
# (Yesterday = -1 Day) through 8 Days Ahead (+8 Days).
#
#
#                  [CALL 1: 4 Days]                  [CALL 2: 6 Days]
#         |<------------------------------>| |<------------------------------>|
#
# DAYS:  [Day -1]  [Day 0]  [Day +1]  [Day +2]  [Day +3] ... [Day +7]  [Day +8]
#           ^         ^                            ^                      ^
#           |         |                            |                      |
#        Yesterday  Today                        Mid-Week             Day After Week
#        (UTC Pad)                                                      (UTC Pad)
#
# -----------------------------------------------------------------------------
# WHY THIS WORKS:
# 1. Day -1 covers local "yesterday evening" events that fell into early UTC Today.
# 2. Day +8 covers local "late evening" events on Day +7 that fall into UTC Day +8.
# 3. Splitting into 2 smaller date chunks avoids exceeding NASA's rate/range boundary.
# =============================================================================
    
def obtainInitialData() -> None: 
    """
    Obtains full week's worth of data from NASA's NEO Web Service API to be used in the 3 primary
    radar functionality time frames (today, tomorrow, full week). 
    
        1st Scan: Obtains NEOs from day before today's date to 2 days after today's date
            (Day -1 to Day +2)

        2nd Scan: Obtains NEOs from 3 days after today's date to 8 days after today's date
            (Day +3 to Day +8)
    """

    # -------------------------------------------------------------------------
    # API KEY & CALL URL
    # -------------------------------------------------------------------------
 
    # Assigns api_key to hidden NASA API key in .env file
    load_dotenv()
    api_key_nasa = os.getenv("NASA_API_KEY")

    url = "https://api.nasa.gov/neo/rest/v1/feed"


    # -------------------------------------------------------------------------
    # API CALL #1: (Day -1 to Day +2)
    # -------------------------------------------------------------------------

    #Dictionary containing the search parameters for the API url (start_date, end_date, and api_key)
    feedQuery_params = {
        "start_date": (getTodayDate() - timedelta(days=1)).isoformat(),
        "end_date": (getTodayDate() + timedelta(days=2)).isoformat(),
        "api_key": api_key_nasa
    }
    
    #Creates a response module object containing the raw data of the api call with the search params
    api_response = requests.get(url, params=feedQuery_params)

    #Converts the raw data to a parsable and extractable object 
    neo_data = api_response.json().get("near_earth_objects")

    # Utilizes itertools module to create an iterable list of NEO data values
    iterable_data = itertools.chain.from_iterable(neo_data.values())

    # Parses through each NEO data dict to create and fill a corresponding NEO Object into TODAY_TOMORROW_LIST
    for neo in iterable_data:
        curNEO = NearEarthObject()
        curNEO.fillObj(neo)
        TODAY_TOMORROW_LIST.neoCollection.append(curNEO)

    # Sorts NEOs firstly by calendar approach date, and then sorts same-date NEOs by approach time 
    TODAY_TOMORROW_LIST.neoCollection.sort(key=lambda neo: (neo.localApproachDate, neo.militaryApproachTime))


    # -------------------------------------------------------------------------
    # API CALL #2: (Day +3 to Day +8)
    # -------------------------------------------------------------------------

    # Changes feedQuery's start and end date params to the new call boundaries
    feedQuery_params["start_date"] = getTodayDate() + timedelta(days=3)
    feedQuery_params["end_date"] = getTodayDate() + timedelta(days=8)

    # Re-grabs NEO data values 
    api_response = requests.get(url, params=feedQuery_params)
    neo_data = api_response.json().get("near_earth_objects")
    iterable_data = itertools.chain.from_iterable(neo_data.values())

    # Initially sets SEVEN_DAY_LIST to the first call's collection of NEO data
    SEVEN_DAY_LIST.neoCollection = TODAY_TOMORROW_LIST.neoCollection.copy()

    # Grabs 2nd call NEO data from iterable_data, creates and hydrates NEO into object, and adds to SEVEN_DAY_LIST
    for neo in iterable_data:
        curNEO = NearEarthObject()
        curNEO.fillObj(neo)
        SEVEN_DAY_LIST.neoCollection.append(curNEO)

# ==========================================================
# 4. NEO DATA FILTERING METHODS
# ==========================================================

def filterAPIDataSingle(filter_date, neo_list) -> None:
    """
    Filters an inputted list of NEO objects by a specified, singular calendar date. Assigns
    filtered NEOs into radar's NEO master list.

    Parameters:
        filter_date: date object containing the calendar date to filter inputted list of NEOs by
        neo_list: list containing NEO objects 
    """

    # Index utilized to access nodes in MASTER_LIST
    index = 0

    # Parses through every NEO object
    for neo in neo_list:

        # Grabs the current NEO object's date (string; YYYY-MM-DD format) and creates a corresponding date object
        neo_date =  datetime.strptime(neo.localApproachDate, "%Y-%m-%d").date()

        #If the NEO's date matches with the filters date, appends to the next open node in NEO master list
        if(neo_date == filter_date):
            MASTER_LIST.neoCollection[index] = neo
            MASTER_LIST.neoCount += 1
            index += 1
    
def filterAPIDataWeek(neo_list) -> None:
    """
    Filters an inputted list of NEO objects between today's date inclusive and 7 days later incluive.
    Assigns filtered NEOs into radar's NEO master list.

    Parameters:
        neo_list: list containing NEO objects 
    """

    # Calculates and instantiates a date object with a date 7 days after current date
    endOfSevenDays = getTodayDate() + timedelta(days=7)

    # Index utilized to access nodes in MASTER_LIST
    index = 0

    # Parses through every NEO object
    for neo in neo_list:

        # Grabs the current NEO object's date (string; YYYY-MM-DD format) and creates a corresponding date object
        neo_date =  datetime.strptime(neo.localApproachDate, "%Y-%m-%d").date()

        # if the NEOs date falls between (including) the current date or 7 days later, appends to NEO master list
        if(getTomorrowDate() <= neo_date <= endOfSevenDays):
            MASTER_LIST.neoCollection[index] = neo
            MASTER_LIST.neoCount += 1
            index += 1

# ==========================================================
# 5. SCAN/BROWSE LOGIC METHODS
# ==========================================================
        
def todayOption(choice) -> None:
    """
    Combines radar logic and calculations to allow user to scan/browse NEOs within current date

    Parameters:
        choice: a string that determines whether the radar should scan or browse NEOs within current date
    """

    # Disposes of any stored NEOs in MASTER_LIST 
    MASTER_LIST.initializeNEOList()

    # Filters NEO data in TODAY_TOMORROW_LIST by today's date to fill MASTER_LIST
    filterAPIDataSingle(getTodayDate(), TODAY_TOMORROW_LIST.neoCollection)

    # If user is browsing, simply print the list and exit
    if choice.upper() == "BROWSE":
        print("NAVAGATION MASTER LIST (BY APPROACH TIME)")
        print("-----------------------------------------")
        MASTER_LIST.printList()
        return

    # Dictionary to track number of NEO hazard variety during scan
    threatCounts = {
        "critical": 0,
        "severe": 0,
        "elevated": 0,
        "moderate": 0,
        "low": 0,
        "safe": 0
    }

    # Parses every filtered NEO added to MASTER_LIST
    for neo in MASTER_LIST.neoCollection:

        # Ensures accessed node is a NEO object, stopping at end of list or when first None type object is reached
        if(type(neo) is NearEarthObject):

            # Grabs current NEO's hazard rating and increments corresponding value in threatCounts
            curHazScore = neo.hazardousRating
            evaluateHazRatings(curHazScore, threatCounts)

    # Displays hazard variety of all scanned NEOs to user
    printResults(threatCounts)

    # Descendingly sorts all NEO objects (excluding None type nodes) by hazard rating for user to browse if chosen
    MASTER_LIST.neoCollection[:MASTER_LIST.neoCount] = sorted(
        MASTER_LIST.neoCollection[:MASTER_LIST.neoCount],
        key=lambda neo: (neo.hazardousRating),
        reverse=True
    )

def tomorrowOption(choice) -> None:
    """
    Combines radar logic and calculations to allow user to scan/browse NEOs within tomorrow's date

    Parameters:
        choice: a string that determines whether the radar should scan or browse NEOs within tomorrows date
    """

    # Disposes of any stored NEOs in MASTER_LIST 
    MASTER_LIST.initializeNEOList()

    # Filters NEO data in TODAY_TOMORROW_LIST by tomorrow's date to fill MASTER_LIST
    filterAPIDataSingle(getTomorrowDate(), TODAY_TOMORROW_LIST.neoCollection)

    # If user is browsing, simply print the list and exit
    if choice.upper() == "BROWSE":
        print("NAVAGATION MASTER LIST (BY APPROACH TIME)")
        print("-----------------------------------------")
        MASTER_LIST.printList()
        return

    # Dictionary to track number of NEO hazard variety during scan
    threatCounts = {
        "critical": 0,
        "severe": 0,
        "elevated": 0,
        "moderate": 0,
        "low": 0,
        "safe": 0
    }

    # Parses every filtered NEO added to MASTER_LIST
    for neo in MASTER_LIST.neoCollection:

        # Ensures accessed node is a NEO object, stopping at end of list or when first None type object is reached
        if(type(neo) is NearEarthObject):

            # Grabs current NEO's hazard rating and increments corresponding value in threatCounts
            curHazScore = neo.hazardousRating
            evaluateHazRatings(curHazScore, threatCounts)

    # Displays hazard variety of all scanned NEOs to user
    printResults(threatCounts)

    # Descendingly sorts all NEO objects (excluding None type nodes) by hazard rating for user to browse if chosen
    MASTER_LIST.neoCollection[:MASTER_LIST.neoCount] = sorted(
        MASTER_LIST.neoCollection[:MASTER_LIST.neoCount],
        key=lambda neo: (neo.hazardousRating),
        reverse=True
    )


def weekOption(choice) -> None:
    """
    Combines radar logic and calculations to scan the week and display top 10 threats or browse NEOs within the week

    Parameters:
        choice: a string that determines whether the radar should scan or browse NEOs within the week
    """

    # Disposes of any stored NEOs in MASTER_LIST 
    MASTER_LIST.initializeNEOList()

    # Filters NEO data in SEVEN_DAY_LIST between current date and next 7 days to fill MASTER_LIST
    filterAPIDataWeek(SEVEN_DAY_LIST.neoCollection)

    # If user is browsing, simply print the list and exit
    if choice.upper() == "BROWSE":
        print("NAVAGATION MASTER LIST (BY APPROACH TIME)")
        print("-----------------------------------------")
        MASTER_LIST.printList()
        return

    # Dictionary to track number of NEO hazard variety during scan
    threatCounts = {
        "critical": 0,
        "severe": 0,
        "elevated": 0,
        "moderate": 0,
        "low": 0,
        "safe": 0
    }

    # Parses every filtered NEO added to MASTER_LIST
    for neo in SEVEN_DAY_LIST.neoCollection:

        # Ensures accessed node is a NEO object, stopping at end of list or when first None type object is reached
        if(type(neo) is NearEarthObject):

            # Grabs current NEO's hazard rating and increments corresponding value in threatCounts
            curHazScore = neo.hazardousRating
            evaluateHazRatings(curHazScore, threatCounts)

    # Displays hazard variety of all scanned NEOs to user
    printResults(threatCounts)

    # Descendingly sorts all NEO objects (excluding None type nodes) by hazard rating for user to browse if chosen
    MASTER_LIST.neoCollection[:MASTER_LIST.neoCount] = sorted(
        MASTER_LIST.neoCollection[:MASTER_LIST.neoCount],
        key=lambda neo: (neo.hazardousRating),
        reverse=True
    )

    # If scan was chosen, assigns MASTER_LIST to the first 10 highest hazard NEOs
    MASTER_LIST.neoCollection = MASTER_LIST.neoCollection[:10]
    MASTER_LIST.neoCount = 10

    #Prints out the top 10 hazardeous NEOs to user 
    print("\nTOP 10 HAZARDS IN THIS WEEK: ")
    print("-----------------------------")
    MASTER_LIST.printList()

def evaluateHazRatings(hazScore, scoreList):
    """
    Updates a hazard count dictionary accordingly from the inputted NEO hazard rating

    Parameters:
        hazScore: float that represents the hazard score of a certain NEO 
        scoreList: a dictionary containing the spread of scanned hazards within a single scan
    """

    # Accesses and increments the corresponding key:value pair based on the inputted NEO's hazard rating
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


# ==========================================================
# 6. DATE HELPER METHODS
# ==========================================================

def getTodayDate():
    """Returns a date object containing today's date"""

    return date.today()

def getTomorrowDate():
    """Returns a date object containing tomorrows's date"""

    return date.today() + timedelta(days=1)


# ==========================================================
# 7. RADAR UI DISPLAY METHODS
# ==========================================================

def askUserMainChoice() -> None:
    """Displays primary options upon radar boot up"""
    
    print("Welcome to the NEO Asteroid Radar! Please select an option below:\n"
          "-----------------------------------------------------------------")
    print("[1] SCAN FOR POTENTIALLY HAZARDEOUS ASTEROIDS")
    print("[2] BROWSE ASTEROIDS")
    print("[3] TERMINATE RADAR\n")

def askScanChoices() -> None:
    """Displays scanning choices if the user likes to scan for NEOs"""
    
    print("SCAN FOR POTENTIALLY HAZARDEOUS NEOs:\n"
          "-----------------------------------------------------------------")
    print("[a] SCAN TODAY")
    print("[b] SCAN TOMORROW")
    print("[c] DISPLAY TOP 10 HAZARDS IN THE NEXT 7 DAYS")
    print("[d] GO BACK TO MAIN MENU\n")

def printResults(hazCounts) -> None:
    """Displays scan results if a type of scanning was chosen"""

    print("SCAN COMPLETE! RESULTS:")
    print("-----------------------")
    
    print(f"CRITICAL THREATS: {hazCounts["critical"]}")
    print(f"SEVERE THREATS: {hazCounts["severe"]}")
    print(f"ELEVATED THREATS: {hazCounts["elevated"]}")
    print(f"MODERATE THREATS: {hazCounts["moderate"]}")
    print(f"LOW THREATS: {hazCounts["low"]}")
    print(f"SAFE NEOs : {hazCounts["safe"]}")

def askBrowseChoices() -> None:
    """Displays browsing choices if the user is wanting to browse NEOs"""

    print("BROWSE NEOs:\n"
          "-----------------------------------------------------------------")
    print("[a] BROWSE TODAY'S NEOs")
    print("[b] BROWSE TOMORROW'S NEOs")
    print("[c] BROWSE IN THE NEXT 7 DAYS")
    print("[d] GO BACK TO MAIN MENU\n")

def neoBrowseChoices() -> None:
    """Displays options to user after initially scanning/browsing NEOs"""

    print("\nOPTIONS:")
    print("----------------")
    print("[1] BROWSE NEOs")
    print("[2] BACK TO MAIN MENU\n")


def curBrowseChoices() -> None:
    """Displays options if a user decides to browse NEOs as a primary choice or after a scan"""

    print("\nOPTIONS:")
    print("----------------")
    print("[#] BROWSE NEO AT SPECIFIED INDEX")
    print("[exit] BACK TO MAIN MENU\n")

def postBrowseChoices() -> None:
    "If a user does decide to browse a NEO, displays option to return to main NEO list"

    print("\n\nOPTIONS:")
    print("----------------")
    print("[1] BACK TO NEO LIST\n")

def clearInterface() -> None:
    """Clears all printed items in terminal to avoid scrolling through a large terminal during radar instantiation"""

    # If the user's OS is Windows
    if os.name == "nt":

        # Uses Windows Shell to run the command "cls" to clear terminal
        subprocess.run(['cls'], shell=True)

    # If user is running on Linux/macOS
    else:

        #Users "clear" command in to clear terminal
        subprocess.run(['clear'])

def clearInput() -> None:
    """Clears user input if an invalid input is given with ANSI escape codes"""

    # \x1b[1A moves terminal cursor up 1 line (back to input line) while \x1b[2K clears the line completely, repeats again
    sys.stdout.write("\x1b[1A\x1b[2K" * 2)

    # Pushes python to erase the line to eliminate buffer
    sys.stdout.flush()