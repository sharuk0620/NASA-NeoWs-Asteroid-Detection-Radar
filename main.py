"""
main.py
-------
Main file for housing helper methods and main() function for initializing
and establishing the NEO Radar System.

Author:  Sai Sharuk Lakshmi Narayanan
Created: May 22nd, 2026
Last Updated: July 20th, 2026
Version: 1.0 (Prototype)
License: MIT
"""


# ==========================================================
# 1. IMPORTS
# ==========================================================

# Built-in python modules
import sys
import time

# Custom module 
import radarInterface


# ==========================================================
# 2. main(): RADAR INITIALIZATION
# ==========================================================
def main() -> None:
    """
    Initializes NEO radar terminal, establishes UI interface,
    and loops through radar functionality until terminated by user
    """

    # Handles API call for all necessary data to be used within the radar
    radarInterface.obtainInitialData()

    #Primary interface loop
    while True:
    
        # Asks user for their initial choice (scan, browse, terminate radar)
        choice = userMainSelection()
        match choice:

            # User chooses to scan for NEOs
            case "1":

                #Asks user for their scan choice (today, tomorrow, top 10 threats in the week, back to main menu)
                scan = userScanChoice()

                # Resets loop if back to menu was chosen, otherwise calls and undergoes chosen scanning process
                if scan == "d": 
                    continue
                else:
                    #Displays scanning results, such as # of NEOs within time frame as well as their hazard levels
                    evaluateScanChoice(scan)
                
                    #Asks user for their choice after scanning for NEOs (browse scanned NEOs or back to main menu)
                    postUserChoice = postChoice("scan")

                    # Resets loop if back to menu was chosen, otherwise prints out master list and allows for browsing
                    if postUserChoice == "2":
                        continue
                    else: 
                        printNEOList()
            
            # User chooses to browse scanned NEOs
            case "2":

                # Asks user to choose their browsing option (today, tomorrow, week), or terminate radar 
                browse = userBrowseChoice()

                # Resets loop if terminate was chosen, otherwise undergoes chosen browsing process
                if browse == "d":
                    continue
                else:
                    #Displays master list of NEOs within chosen time frame and allows user to browse specific NEO data
                    evaluateBrowseChoice(browse)

                    #Asks user for their choice after choosing to browse NEOs (go forward with browsing or back to main menu)
                    postUserChoice = postChoice(browse)

                    # Resets loop if back to menu was chosen, otherwise prints out the list of NEOs and allows for browsing of NEO data
                    if postUserChoice == "2":
                        continue
                    else: 
                        printNEOList()

            # User chooses to terminate radar 
            case "3":
                sys.exit()

            # User does not choose a listed option
            case _:
                print("\nINVALID CHOICE! PLEASE CHOOSE A LISTED OPTION!\n")         


# ==========================================================
# 3. General Helper Methods
# ==========================================================

def userMainSelection() -> str:
    """
    Handles user input for choosing their primary radar function 
    (scan, browse, or terminate)
    
    Returns: 
        userChoice: String containing user's radar function of choice
    """

    # Displays primary radar options to user 
    radarInterface.clearInterface()
    radarInterface.askUserMainChoice()    

    # Continuous loop until valid input is given
    while(True):

        # Asks for user choice
        userChoice = input("PLEASE ENTER THE APPROPRIATE INDEX CORRESPONDING TO YOUR CHOICE: ")

        # if valid, return userChoice to main() and exit
        if userChoice in ["1", "2", "3"]:
            return userChoice
        
        # if invalid, restart loop until valid input is given
        print("INVALID CHOICE! PLEASE CHOOSE A LISTED OPTION!")
        time.sleep(2.0)
        radarInterface.clearInput()

def postChoice(choice) -> str:
    """
    Handles user input for choosing an option after scanning or browsing NEOs
    (Go forward with browsing NEOs or back to main menu)

    Parameters:
        choice: A string used to determine whether scanning or browsing is the primary function
    
    Returns: 
        postChoice: String containing user's choice to browse or exit to main menu
    """

    # If primary choice was browse, immediately print the master list of NEOs within previously chosen time frame
    if choice.upper() == "BROWSE":
        radarInterface.MASTER_LIST.printList()

    # Prints out options
    radarInterface.neoBrowseChoices()

    #Continuous loop until valid input given
    while True:

        # Asks user for their choice on browsing NEOs after the primary function or exitting to main menu
        postChoice = input("ENTER YOUR CHOICE: ")

        # Returns input to main() if valid, else passes an error message and resets input
        if postChoice in ["1", "2"]:
            return postChoice
        else:
            print("INVALID CHOICE! PLEASE CHOOSE A LISTED OPTION!")

            # Sleeps the terminal for 2 seconds to allow user to read display message before clearing
            time.sleep(2.0)
            radarInterface.clearInput()

def printNEOList() -> None:
    """
    Handles user input for pulling up data of a chosen NEO
    (Go forward with browsing NEOs or back to main menu)
    
    Returns: 
        None: Returns a None type object if back to main menu option was chosen
    """

    # Continuous loop until valid input is given
    while True:

        # Displays master list of NEOs based on previously chosen time frame of scan/browse and displays options 
        radarInterface.clearInterface()
        print("NAVAGATION MASTER LIST (BY HAZARD RATING)")
        print("-----------------------------------------")
        radarInterface.MASTER_LIST.printList()
        radarInterface.curBrowseChoices()

        # Try-Catch to catch ValueErrors exceptions: user inputs a completely invalid input
        try:
        
            listChoice = input("ENTER CHOICE: ")

            # Returns to main menu
            if listChoice.upper() == "EXIT":
                return
            
            # If user desires to browse a NEO but inputs an invalid index value, prints error message and clears input 
            elif  0 >= int(listChoice) or radarInterface.MASTER_LIST.neoCount < int(listChoice):
                print("INVALID CHOICE! PLEASE ENTER A VALID NEO INDEX!")
                time.sleep(2.0)
            
            #If user does input a valid index 
            else:

                # Prints the NEOs attributes in a clean format
                radarInterface.clearInterface()
                print(radarInterface.MASTER_LIST.neoCollection[int(listChoice) - 1])

                # Displays option to return to main NEO list
                radarInterface.postBrowseChoices()
                reBrowseChoice()

        # If the user inputs neither the "exit" keyword or an index value
        except ValueError:

            # Prints an error message if input is neither an int or the str "exit", loop is reset
            print("INVALID CHOICE! PLEASE ENTER A LISTED OPTION!")

            # Sleeps the terminal for 2 seconds to allow user to read display message before clearing
            time.sleep(2.0)
            radarInterface.clearInput()


# ==========================================================
# 4. NEO Scanning Helper Methods
# ==========================================================

def userScanChoice() -> str:
    """
    Handles user input for choosing their scanning option
    (scan NEOs today, tomorrow, or display the 10 most hazardous threats in the upcoming 7 days)
    
    Returns: 
        scanChoice: String designating the user's chosen scanning option
    """

    # Displays the scanning functions
    radarInterface.clearInterface()
    radarInterface.askScanChoices()

    #Continuous loop until a valid input is given
    while(True):

        # Asks user for their choice
        scanChoice = (input("PLEASE CHOOSE A SCANNING OPTION (a, b, c, d): ")).lower()

        # Return input back to main() if valid, otherwise prints an error message and resets loop
        if scanChoice in ["a", "b", "c", "d"]:  
            return scanChoice
        print("INVALID CHOICE! PLEASE CHOOSE A LISTED OPTION!")

        # Sleeps the terminal for 2 seconds to allow user to read display message before clearing
        time.sleep(2.0) 
        radarInterface.clearInput()

def evaluateScanChoice(choice) -> None:
    """
    Runs scanning logic based on user's chosen time frame of NEO scan
    (today, tomorrow, or top 10 threats)
    
    Parameters:
        choice: String that contains the letter corresponding to the scanning choice displayed to user.
            Used to run the correct scanning logic.
    """

    radarInterface.clearInterface()

    # Switch-Case statement to run correct scanning logic based on user input
    match choice:

        # Scan today
        case "a":
            radarInterface.todayOption("scan")
        
        # Scan tomorrow
        case "b":
            radarInterface.tomorrowOption("scan")

        #Display top 10 threats in next 7 days
        case "c":
            radarInterface.weekOption("scan")


# ==========================================================
# 5. NEO Browsing Helper Methods
# ==========================================================

def userBrowseChoice() -> str:
    """
    Handles user input for choosing their browsing option
    (browse NEOs today, tomorrow, in the week (next 7 days), or terminate)
    
    Returns: 
        scanChoice: String designating the user's chosen scanning option
    """

    # Displays browsing functionalities
    radarInterface.clearInterface()
    radarInterface.askBrowseChoices()

    # Continuous loop until a valid input is given
    while(True):

        # Asks user for their choice
        browseChoice = (input("PLEASE CHOOSE A BROWSING OPTION (a, b, c, d): ")).lower()

        # Return input back to main() if valid, otherwise prints an error message and resets loop
        if browseChoice in ["a", "b", "c", "d"]:  
            return browseChoice
        print("INVALID CHOICE! PLEASE CHOOSE A LISTED OPTION!")

        # Sleeps the terminal for 2 seconds to allow user to read display message before clearing
        time.sleep(2.0)
        radarInterface.clearInput()

def evaluateBrowseChoice(choice) -> None:
    """
    Runs browsing logic based on user's chosen time frame of browsing NEOs
    (today, tomorrow, or full week browsing)
    
    Parameters:
        choice: String that contains the letter corresponding to the browsing choice displayed to user.
            Used to run the correct browsing logic.
    """

    radarInterface.clearInterface()

    # Switch-case to run correct browsing logic based off of user input
    match choice:

        # Browse today
        case "a":
            radarInterface.todayOption("browse")

        # Browse tomorrow
        case "b":
            radarInterface.tomorrowOption("browse")

        # Browse week (next 7 days)
        case "c":
            radarInterface.weekOption("browse")

def reBrowseChoice() -> None:
    """
    Prompts user if they would like to return to the main NEO master list once done viewing
    a browsed NEO
    """

    # Continuous loop until valid input given
    while(True):    

        # Asks user if they'd like to return to NEO list
        postChoice = input("PLEASE CHOOSE YOUR OPTION: ")

        # Returns back to master list of NEOs to continue browsing data 
        if postChoice == "1":
            return

        # Otherwise, displays error, clears previous input, and asks again
        print("INVALID INPUT! PLEASE ENTER A LISTED OPTION!")
        time.sleep(2.0)
        radarInterface.clearInput()


# ==========================================================
# 6. MISC.
# ==========================================================

#Allows python to run the main() function upon running "python main.py" in the terminal
if __name__ == "__main__":
    main()