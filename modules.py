"""
modules.py
-------
File containing two major classes utilized in radar implementation:

    NearEarthObject: Allows for object instantiation for individual NEOs, containing defining data and attributes

    NEOStorage: Creates lists that contain several NearEarthObject instances to be used for analysis and UI needs

Author:  Sai Sharuk Lakshmi Narayanan
Created: June 4th, 2026
Last Updated: July 20th, 2026
Version: 1.0 (Prototype)
License: MIT
"""


# ==========================================================
# 1. IMPORTS
# ==========================================================

# Built-in python module
from datetime import datetime


# ==========================================================
# 2. NearEarthObject CLASS
# ==========================================================

class NearEarthObject:
    """
    Allows for object instantiaton for individual NEO entries, allowing for 
    efficient NEO data organization and analysis

    Attributes:
        name (str): Official Name of NEO desigated by NASA
        id (str): Identification tag used within NASA's NEO Database
        absMag (float): Estimated Absolute Magnitude (brightness) measurement of NEO
        estSizeMetersMin (float): Lower bound of estimated size of NEO in meters
        estSizeMetersMax (float): Upper bound of estimated size of NEO in meters
        estApproachDistAU (float): Estimated approach distance of NEO to Earth in Astronomical Units (AU)
        rawApproachTime (str): Near approach time of NEO measured in epoch milliseconds, used for local time conversion
        localApproachDate (str): Near approach calendar date of NEO based on user's local time zone in YYYY-MM-DD format
        militaryApproachTime (str): Near approach, 24 hour time format of NEO in user's local time zone, used for NEO comparision
        localApproachTime (str): Near approach, 12 hour format time of NEO in user's local time zone
        relativeVelKmSeconds (float): Estimated relative velocity of NEO measured in kilometers per second upon approach
        hazardousRating (float): Hazard rating of NEO based off of a custom engineered scale, out of a 1.00 rating
        sentryObjectFlag (bool): Label weather NEO is actively tracked by NASA's Center for Near Earth Object Studies 
    """


    # -------------------------------------------------------------------------
    # CONSTUCTOR AND MAGIC METHODS
    # -------------------------------------------------------------------------

    def __init__(self) -> None:
        """Initializes NEO with placeholder values to assist in eventual C transfer and strict memory management"""
        
        name = ""
        id = ""
        absMag = 0.0
        estSizeMetersMin = 0.0
        estSizeMetersMax = 0.0
        estApproachDistAU = 0.0
        rawApproachTime = ""
        localApproachDate = ""
        militaryApproachTime = ""
        localApproachTime = ""
        relativeVelKmSeconds = 0.0
        hazardousRating = 0.0
        sentryObjectFlag = False

    def __str__(self) -> str:
        """Prints out a NEO's attributes in a clean, multi-line format"""

        return f"""NEO Target: {self.name}
            ------------------------------------------
            ID: {self.id}
            Absolute Magnitude: {self.absMag}
            Estimated Minimum Size: {self.estSizeMetersMin} meters
            Estimated Maximum Size: {self.estSizeMetersMax} meters
            Approach Distance: {self.estApproachDistAU} Astronomical Units
            Local Approach Date: {self.localApproachDate}
            Local Approach Time: {self.localApproachTime}
            Relative Velocity Upon Approach: {self.relativeVelKmSeconds} km/s
            Hazard Score: {self.hazardousRating}/1.00
            Hazard Rating: {self.get_NEO_classification()}
            Currently Tracked by NASA CNEOS Facility: {self.sentryObjectFlag}
            ------------------------------------------"""


    # -------------------------------------------------------------------------
    # ATTRIBUTE HYDRATE/FILL METHODS
    # -------------------------------------------------------------------------
    
    def fillObj(self, neoData) -> None:
        """
        Hydrates object properities from parsed dictionary corresponding to a specified NEO of a given date
        
        Parameters:
            neoData: A individual dict (dictionary) instance containing data of a specified NEO, obtained from NASA's NEOWS API
        """

        #Identification Data of the asteroid
        self.name = neoData.get("name", "Unknown")
        self.id = neoData.get("id", "0000000")

        #Absolute Magnitude rating of the asteroid
        self.absMag = neoData.get("absolute_magnitude_h", 0.0)
    
        #Min and Max asteroid size (diameters; meters)
        self.estSizeMetersMin = float(neoData["estimated_diameter"]["meters"]["estimated_diameter_min"])
        self.estSizeMetersMax = float(neoData["estimated_diameter"]["meters"]["estimated_diameter_max"])
        
        #Pulls up the first close_approach_data instance for a given asteroid
        approachData = neoData["close_approach_data"][0]

        #The near approach distance of the asteroid in Astronomical Units (AU)
        self.estApproachDistAU = float(approachData["miss_distance"]["astronomical"])

        #Assigns the epoch date in milliseconds, which later converts to local time
        self.rawApproachTime = approachData["epoch_date_close_approach"]

        #The relative velocity in kilometers per second (km/s) of the asteroid during close approach
        self.relativeVelKmSeconds = float(approachData["relative_velocity"]["kilometers_per_second"])

        #A flag on whether or not asteroid is tracked by NASA's CNEOS for potential danger
        self.sentryObjectFlag = neoData.get("is_sentry_object", False)

        #Evaluates and updates hazardousRating score
        self.totalHazardAnalysis()

        #Evaluates and updates the localApproachDate and localApproachTime for the NEO based off of the users time zone
        self.attainLocalApproachTime()

    def attainLocalApproachTime(self) -> None:
        """
        Converts the raw approach date of NEO in epoch millisecond to calculate its local approach calendar
        date and time based on the user's local time zone
        """

        # Attains the approach date and time of the NEO in their local timezone
        approach_date_full = str(datetime.fromtimestamp(self.rawApproachTime / 1000))[:16]

        # A list containing the local calendar approach date and military-time clock approach time
        dateParts = approach_date_full.split()

        # Creates a datetime object to contain the military time of the NEO
        localTime = datetime.strptime(dateParts[1], "%H:%M")

        # Assigns the local calendar approach date
        self.localApproachDate = dateParts[0]

        # Assigns the military approach time
        self.militaryApproachTime = dateParts[1]

        # Converts the datetime object into a string containing the standard approach time of the NEO
        self.localApproachTime = localTime.strftime("%I:%M %p")


    # -------------------------------------------------------------------------
    # HAZARD ANALYSIS/CALCULATION METHODS
    # -------------------------------------------------------------------------

    def totalHazardAnalysis(self) -> None:
        """
        Analyzes and determines the hazard rating of a NEO using a developer-made scale. Hazard ratings are a
        value assigned out of 1.00, and follow a 60/30/10 weighting based off of the NEO's close approach distance,
        size, and velocity respectively
        """
        
        # Obtains score of NEO in each scale catagory
        distScore = self.closeDistHazardAnalysis()
        sizeScore = self.sizeHazardAnalysis()
        speedScore = self.speedHazardAnalysis()

        # Assigns the hazardousRaating property of a given NEO with the 60/30/10 formula
        self.hazardousRating = round((0.6 * distScore) + (0.3 * sizeScore) + (0.1 * speedScore), 2)

        # If the NEO is a sentry object, add 0.25 to the hazardousRating and ensure exceeding over 1.00
        if(self.sentryObjectFlag == True):
            self.hazardousRating = min(1.00, self.hazardousRating + 0.25)

    def closeDistHazardAnalysis(self) -> int:
        """Analyzes NEOs approach distance (AU) and assigns a threat score out of 1.0 based on it's proximity"""
        
        dist = self.estApproachDistAU

        if(dist <= 0.0026):
            return 1.0 #High Hazard: Closer than the moon is to Earth!
        elif(dist <= 0.015):
            return 0.5 #Moderate Hazard: Very close to earth, far within "Potentially Hazardous Asteroid" boundaries
        elif(dist <= 0.05):
            return 0.2 #Low Hazard: Offically marked as a "Potentially Hazardous Asteroid"
        else:
            return 0 #No Hazard: Too far out to be considered a NEO
        
    
    def sizeHazardAnalysis(self) -> int:
        """Analyzes NEOs estimated upper bound size (meters) to establish a worst case scenario and assigns a threat 
        score out 1.0 based on it's magnitude"""

        size = self.estSizeMetersMax
        
        if(size >= 140):
            return 1.0 #High Hazard: Massive global threat!
        elif(size >= 70):
            return 0.5 #Moderate Hazard: Threat to cities/regions
        elif(size >= 20):
            return 0.2 #Low Hazard: Major damage possible, marked as a "PHA"
        else:
            return 0 #No Hazard: Will burn up in earth's atmosphere if in contact

    def speedHazardAnalysis(self) -> int:
        """Analyzes NEOs relative velocity (km/s) and assigns a threat score out 1.0 based on it's speed"""

        speed = self.relativeVelKmSeconds

        if(speed >= 30.0):
            return 1.0 #High Hazard: Extremely fast and major threat to planet if in contact!
        elif(speed >= 20.0):
            return 0.5 #Moderate Hazard: Oddly fast for a NEO, and holds potential do major damage
        elif(speed >= 11.0):
            return 0.1 #Low Hazard: Typical/average speed of NEOs
        else:
            return 0 #No Hazard: Slower than usual NEOs
    
    #Returns a classification/label for a given NEO object based on it's hazard rating property
    def get_NEO_classification(self) -> str:
        """Analyzes NEOs relative velocity (km/s) and assigns a threat score out 1.0 based on it's speed"""

        if(self.hazardousRating >= 0.90):
            return "CRITICAL 🔴" #Extinction level threat
        elif(self.hazardousRating >= 0.80):
            return "SEVERE 🟠" #Major threat to humanity and life
        elif(self.hazardousRating >= 0.60):
            return "ELEVATED 🟡" #Potential to do massive damage to planet
        elif(self.hazardousRating >= 0.40):
            return "MODERATE 🟢" #Potential to level cities, countries, or whole regions
        elif(self.hazardousRating >= 0.20):
            return "LOW 🔵" #Potential to do some damage, but unlikely for impact
        else:
            return "SAFE ⚪" #NEOs that are highly unlikely to come in physical contact with Earth

        
# ==========================================================
# 3. NEOStorage CLASS
# ==========================================================

class NEOStorage:
    """
    Allows instantiation of storage objects containing lists that can contain up to 50 NEO instances, which can then be
    used to display and access NEOs in a memory efficient manner.

    Attributes:
        neoCollection (list): Contains memory allocated spots for up to 50 NEO instances
        neoCount (int): A counter that stores how many NEO instances are in a NEOStorage object
    """

    # -------------------------------------------------------------------------
    # CONSTUCTOR AND INTIALIZER
    # -------------------------------------------------------------------------

    def __init__(self) -> None:
        """Initializes with an empty list as a placeholder for memory management purposes"""

        self.neoCollection = []
    
    def initializeNEOList(self) -> None:
        """Assigns a NEOStorage object a refreshed list of 50 allocated memory spots"""

        self.neoCollection = [None] * 50
        self.neoCount = 0

    # -------------------------------------------------------------------------
    # PRINT METHOD
    # -------------------------------------------------------------------------

    def printList(self) -> None:
        """
        Custom print method to display a NEOStorage object's list in a user-friendly grid format,
        making it easy to navigate and view individual NEO instances within the list.
        """

        # Temporary list that omits any remaining None type objects within the list
        neoList = [neo for neo in self.neoCollection if type(neo) is NearEarthObject]

        totalItems = len(neoList)

        # Intializes grid to 10 rows unless there are less than 10 items
        totalRows = 10 if totalItems > 10 else totalItems

        # Iterates through each individual row
        for i in range(totalRows):

            # List containing strings for each printable row
            rowStrings = []

            # Increments by 10 to organize each NEO's index on the same row to be 10 apart
            for space in range(0, 60, 10):

                index = i + space

                # If the index value is valid, append it's name and classification to row_strings
                if index < totalItems:
                    curNeo = neoList[index]

                    # index value is increment by 1 (to not start at 0) and is able to take up 2 spaces to center every index label
                    cell_text = f"{index+1:2}. [{curNeo.name}] {curNeo.get_NEO_classification()}"

                    # ensures cell_text is at least 37 characters wide (adds empty characters if needed) to format columns properly
                    rowStrings.append(f"{cell_text:37}")

                # Otherwise, append 37 empty characters to position last empty spot
                else:
                    rowStrings.append(" " * 37)

            # Combines rows together
            print("".join(rowStrings))