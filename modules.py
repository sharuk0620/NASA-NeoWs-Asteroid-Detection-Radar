from datetime import datetime


#NearEarthObject is a class that represents NEO and key data found and recieved NASA's NEOWs API calls.
class NearEarthObject:

    #Initializing/Constructor for NearEarthObject objects
    def __init__(self):
        
        #Initializes placeholder values for NEO's properties to help with eventual C transfer and strict memory management
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
        hazardeousRating = 0.0
        sentryObjectFlag = False


    #Hydrates object properities from passed in data node corresponding to a certain asteroid of a given date
    def fillObj(self, neoData):

    

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

        #Evaluates and updates the localApproachDate and localApproachTime for the NEO based off of the users timezone
        self.attainLocalApproachTime()

        


    def attainLocalApproachTime(self):
        #Attains the approach date and time of the NEO in their local timezone
        approach_date_full = str(datetime.fromtimestamp(self.rawApproachTime / 1000))[:16]

        #An array containing the calendar date and military-time clock approach time
        dateParts = approach_date_full.split()

        #Creates a datetime object to contain the military time of the NEO
        localTime = datetime.strptime(dateParts[1], "%H:%M")

        self.militaryApproachTime = dateParts[1]

        #Assigns the local approach date to the first dateParts element (Local Calendar Date)
        self.localApproachDate = dateParts[0]

        #Converts the datetime object into a string containing the standard approach time of the NEO
        self.localApproachTime = localTime.strftime("%I:%M %p")

    def __str__(self):
        return f"NEO Target: {self.name} \nID: {self.id} \nAbsolute Magnitude: {self.absMag} \nEstimated Minimum Size: {self.estSizeMetersMin} meters \nEstimated Maximum Size: {self.estSizeMetersMax} meters \nApproach Distance: {self.estApproachDistAU} Astronomical Units \nLocal Approach Date: {self.localApproachDate} \nLocal Approach Time: {self.localApproachTime} \nRelative Velocity Upon Approach: {self.relativeVelKmSeconds} km/s \nHazard Score: {self.hazardousRating}/1.00 \nHazard Rating: {self.get_NEO_classification()} \nCurrently Tracked by NASA CNEOS Facility: {self.sentryObjectFlag} \n------------------------------------------\n"

    #Analyzes and determines the hazard score of a NEO using custom, developer-made criteria.
    #Criteria: Close Appr Dist, Size, and Speed follow a 60/30/10 hazard criteria
    def totalHazardAnalysis(self):
        
        #Temporary variables to store the hazard score of each criteria
        distScore = self.closeDistHazardAnalysis()
        sizeScore = self.sizeHazardAnalysis()
        speedScore = self.speedHazardAnalysis()

        #Assigns the hazardousRaating property of a given NEO with the 60/30/10 formula
        self.hazardousRating = round((0.6 * distScore) + (0.3 * sizeScore) + (0.1 * speedScore), 2)

        #If the NEO is a sentry object, add 0.25 to the hazardousRating and ensure exceeding over 1.00
        if(self.sentryObjectFlag == True):
            self.hazardousRating = min(1.00, self.hazardousRating + 0.25)

        
    #Analyzes and returns the hazard score of NEO's close approach distance
    def closeDistHazardAnalysis(self):

        #Temporary variable to store the estimated close approach distance on a certain date
        dist = self.estApproachDistAU

        #Returns a corresponding score (0.0 - 1.0) depending on the approach distance of the NEO
        if(dist <= 0.0026):
            return 1.0 #Maximum Hazard: Closer than the moon is!
        elif(dist <= 0.015):
            return 0.5 #Moderate Hazard: Very close to earth, far within PHA boundaries
        elif(dist <= 0.05):
            return 0.2 #Low Hazard: Offically marked as a "PHA"
        else:
            return 0 #No Hazard: Too far out to consider a NEO
        
    #Analyzes and returns the hazard score of NEO's size in meters
    def sizeHazardAnalysis(self):

        #Temporary variable to store the maximum estimated size of the NEO
        size = self.estSizeMetersMax

        #Returns a corresponding score (0.0 - 1.0) depending on the estimated max size of the NEO
        if(size >= 140):
            return 1.0 #Maximum Hazard: Massive global threat!
        elif(size >= 70):
            return 0.5 #Moderate Hazard: Threat to cities/regions
        elif(size >= 20):
            return 0.2 #Low Hazard: Major damage possible, marked as a "PHA"
        else:
            return 0 #No Hazard: Will burn up in earth's atmosphere if in contact

    #Analyzes and returns the hazard score of NEO's relative speed in kilometers per second

    def speedHazardAnalysis(self):

        #Temporary variable to store the relative velocity of a NEO on a given approach date
        speed = self.relativeVelKmSeconds

        #Returns a corresponding score (0.0 - 1.0) depending on the estimated relative velocity of the NEO
        if(speed >= 30.0):
            return 1.0 #Maximum Hazard: Extremely fast and major threat to planet!
        elif(speed >= 20.0):
            return 0.5 #Moderate Hazard: Oddly fast, and holds potential do major damage
        elif(speed >= 11.0):
            return 0.1 #Low Hazard: Typical/average speed of NEOs
        else:
            return 0 #No Hazard: Slower than usual NEOs
    
    #Returns a classification/label for a given NEO object based on it's hazard rating property
    def get_NEO_classification(self):
        if(self.hazardousRating >= 0.90):
            return "CRITICAL 🔴" #Extinction level threat
        elif(self.hazardousRating >= 0.80):
            return "SEVERE 🟠" #Major threat to humanity and life
        elif(self.hazardousRating >= 0.60):
            return "ELEVATED 🟡" #Potential to do massive damage to planet
        elif(self.hazardousRating >= 0.40):
            return "MODERATE 🟢" #Potential to level cities, countries, or whole regions
        elif(self.hazardousRating >= 0.20):
            return "LOW 🔵" #Potential to do some damage, but unlikely
        else:
            return "SAFE ⚪" #NEOs that are highly unlikely to come in conflict with Earth
        



class NEOStorage:
    def __init__(self):
        self.neoCollection = []
    
    def initializeNEOList(self):
        self.neoCollection = [None] * 50
        self.neoCount = 0

    def printList(self):

        print("\nNAVAGATION MASTER LIST") 
        print("----------------------")

        neoList = [neo for neo in self.neoCollection if type(neo) is NearEarthObject]
        neoList.sort(key=lambda neo: (neo.hazardousRating), reverse=True)
        
        totalItems = len(neoList)


        totalRows = 10 if totalItems > 10 else totalItems

        for i in range(totalRows):
            row_strings = []

            for space in range(0, 60, 10):
                index = i + space

                if index < totalItems:
                    curNeo = neoList[index]
                    cell_text = f"{index+1:2}. [{curNeo.name}] {curNeo.get_NEO_classification()}"
                    row_strings.append(f"{cell_text:37}")
                else:
                    row_strings.append(" " * 37)
        
            print("".join(row_strings))



    









