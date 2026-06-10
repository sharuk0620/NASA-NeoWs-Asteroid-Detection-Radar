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
        closeApproachDate = ""
        closeApproachTime = ""
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

        #Creates an array containing the calendar date and time of close asteroid approach
        closeApproachInfo = approachData["close_approach_date_full"].split()

        #Assigns date and time appropriately
        self.closeApproachDate = closeApproachInfo[0]
        self.closeApproachTime = closeApproachInfo[1]

        #The relative velocity in kilometers per second (km/s) of the asteroid during close approach
        self.relativeVelKmSeconds = float(approachData["relative_velocity"]["kilometers_per_second"])

        #A flag on whether or not asteroid is tracked by NASA's CNEOS for potential danger
        self.sentryObjectFlag = neoData.get("is_sentry_object", False)


    #Analyzes and determines the hazard score of a NEO using custom, developer-made criteria.
    #Criteria: Close Appr Dist, Size, and Speed follow a 60/30/10 hazard criteria
    def totalHazardAnalysis(self):
        
        #Temporary variables to store the hazard score of each criteria
        distScore = self.closeDistHazardAnalysis()
        sizeScore = self.sizeHazardAnalysis()
        speedScore = self.speedHazardAnalysis()

        #Assigns the hazardousRaating property of a given NEO with the 60/30/10 formula
        self.hazardousRating = round((0.6 * distScore) + (0.3 * sizeScore) + (0.1 * speedScore), 2)
        
 
    #Analyzes and returns the hazard score of NEO's close approach distance
    def closeDistHazardAnalysis(self):

        #Temporary variable to store the estimated close approach distance on a certain date
        dist = self.estApproachDistAU

        #Returns a corresponding score (0.0 - 1.0) depending on the approach distance of the NEO
        if(dist <= 0.05):
            return 1.0 #Maximum Hazard: Extremely close, marked as a "PHA"
        elif(dist <= 0.15):
            return 0.5 #Moderate Hazard: Moderately close
        elif(dist <= 0.30):
            return 0.1 #Low Hazard: Within 0.3 AU NEO neighborhood
        else:
            return 0 #No Hazard: Too far out to consider a NEO
        
    #Analyzes and returns the hazard score of NEO's size in meters
    def sizeHazardAnalysis(self):

        #Temporary variable to store the maximum estimated size of the NEO
        size = self.estSizeMetersMax

        #Returns a corresponding score (0.0 - 1.0) depending on the estimated max size of the NEO
        if(size >= 1000.0):
            return 1.0 #Maximum Hazard: Massive global threat!
        elif(size >= 300.0):
            return 0.5 #Moderate Hazard: Threat to cities/regions
        elif(size >= 140.0):
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
        if(self.hazardousRating >= 0.95):
            return "CRITICAL 🔴" #Extinction level threat
        elif(self.hazardousRating >= 0.80):
            return "SEVERE 🟠" #Major threat to humanity and life
        elif(self.hazardousRating >= 0.60):
            return "ELEVATED 🟡" #Potential to do massive damage to planet
        elif(self.hazardousRating >= 0.40):
            return "MODERATE 🟢" #Potential to level cities, countries, or whole regions
        else:
            return "LOW 🔵" #NEOs that will more than likely pose no threat to the planet
        
        #Prints out a special message whether the NEO is tracked by NASA's Center of Near Earth Object Studies
        if(self.sentryObjectFlag == True):
            print("‼️NEO IS ACTIVELY MONITORED BY NASA'S CNEOS‼️")









