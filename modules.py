#NearEarthObject is a class that represents NEO and key data found and recieved NASA's NEOWs API calls.
class NearEarthObject:

    #Initializing/Constructor for NearEarthObject objects
    def __init__(self):
        
        #Initializes placeholder values for NEO's properties to help with eventual C transfer and strict memory management
        name = ""
        id = ""
        absMag = 0.0
        estSizeMeters = 0.0
        estApproachDistLD = 0.0
        closeApproachDate = ""
        closeApproachTime = ""
        relativeVelKmSeconds = 0.0
        hazardeousRating = 0.0
        sentryObjectFlag = False


    def fillObj(self, neoData):

        #Hydrates object properities from passed in data node corresponding to a certain asteroid of a given date
        self.name = neoData.get("name", "Unknown")
        self.id = neoData.get("id", "0000000")
        self.absMag = neoData.get("absolute_magnitude_h", 0.0)
        
        minNEOSize = float(neoData["estimated_diameter"]["meters"]["estimated_diameter_min"])
        maxNEOSize = float(neoData["estimated_diameter"]["meters"]["estimated_diameter_max"])

        self.estSizeMeters = round((minNEOSize + maxNEOSize) / 2, 3)
        
        approachData = neoData["close_approach_data"][0]

        self.estApproachDistLD = float(approachData["miss_distance"]["lunar"])

        closeApproachInfo = approachData["close_approach_date_full"].split()

        self.closeApproachDate = closeApproachInfo[0]

        self.closeApproachTime = closeApproachInfo[1]

        self.relativeVelKmSeconds = approachData["relative_velocity"]["kilometers_per_second"]

        self.sentryObjectFlag = neoData.get("is_sentry_object")


    #Analyzes and determines the hazard score of a NEO using custom, developer-made criteria.
    def hazardAnalysis(self):
        pass






