# Imports the request module to assist in grabbing data from NASA's Asteroid NEO WS API
import requests

# Imports the os module to help read the hidden NASA API Key, done for safekeeping the API key
import os

import sys

#Reads the contents of .env
from dotenv import load_dotenv

import utils, radarInterface

from modules import NearEarthObject, NEOStorage

from datetime import date, timedelta

import time

#Loads hidden key into System Environment Variables
load_dotenv()


#Start of Program

def main():

    radarInterface.obtainInitialData()

    while True:
        #Starts radar and asks user for their option
    
        choice = userMainSelection()
        match choice:

            case "1":
                scan = userScanChoice()

                if scan == "d":
                    continue
                else:
                    evaluateScanChoice(scan)
                
                    postChoice = postScanChoice()

                    if postChoice == "2":
                        continue
                    else: 
                        printNEOList()
                


                

                


                    
                    
            case "2":
                browse = userBrowseChoice()

                if browse == "d":
                    continue
                else:
                    pass

            case "3":
                sys.exit()
            case _:
                print("\nINVALID CHOICE! PLEASE CHOOSE A LISTED OPTION!\n")
            






def userMainSelection():

    while(True):

        radarInterface.clearInterface()

        radarInterface.askUserMainChoice()      
        userChoice = input("PLEASE ENTER THE APPROPRIATE INDEX CORRESPONDING TO YOUR CHOICE: ")

        if userChoice in ["1", "2", "3"]:
            return userChoice
        
        print("\nINVALID CHOICE! PLEASE CHOOSE A LISTED OPTION!\n")
        time.sleep(2.0)

def userScanChoice():

    while(True):

        radarInterface.clearInterface()

        radarInterface.askScanChoices()
        scanChoice = (input("PLEASE CHOOSE A SCANNING OPTION (a, b, c, d): ")).lower()

        if scanChoice in ["a", "b", "c", "d"]:  
            return scanChoice

        print("\nINVALID CHOICE! PLEASE CHOOSE A LISTED OPTION!\n")
        time.sleep(2.0)

def evaluateScanChoice(choice):

    radarInterface.clearInterface()

    match choice:

        case "a":
            radarInterface.scanToday()
        case "b":
            radarInterface.scanTomorrow()
        case "c":
            radarInterface.scanWeek()

def postScanChoice():

    radarInterface.neoBrowseChoices()

    while True:
        postChoice = input("\nENTER YOUR CHOICE: ")

        if postChoice in ["1", "2"]:
            return postChoice
        else:
            print("\nINVALID CHOICE! PLEASE CHOOSE A LISTED OPTION!")
            time.sleep(2.0)
            radarInterface.clearInput()



def printNEOList():

    while True:

        radarInterface.clearInterface()

        radarInterface.masterList.printList()

        radarInterface.top10Choices()
        try:
        
            listChoice = input("\nENTER CHOICE: ")

            if listChoice.upper() == "EXIT":
                return
            elif  0 >= int(listChoice) or len(radarInterface.masterList.neoCollection) < int(listChoice):
                print("\nINVALID CHOICE! PLEASE ENTER A VALID NEO INDEX!")
                time.sleep(2.0)
                radarInterface.clearInput()
            else:
                radarInterface.clearInterface()
                print(radarInterface.masterList.neoCollection[int(listChoice) - 1])

                radarInterface.postBrowseChoices()


                postChoice = input("PLEASE CHOOSE YOUR OPTION: ")

                if postChoice == "1":
                    continue
                else: 
                    return
        
        except ValueError:

            print("\nINVALID CHOICE! PLEASE ENTER A LISTED OPTION! ")
            time.sleep(2.0)




  


        


            
                


def userBrowseChoice():

    radarInterface.clearInterface()

    radarInterface.askBrowseChoices()

    browseChoice = (input("PLEASE CHOOSE A BROWSING OPTION (a, b, c): ")).lower()


    if browseChoice in ["a", "b", "c", "d"]:  
        return browseChoice
    
    print("\nINVALID CHOICE! PLEASE CHOOSE A LISTED OPTION!\n")
    time.sleep(2.0)







#Allows python to run the main() function upon running "python main.py" in the terminal
if __name__ == "__main__":
    main()



    















