#Helper Functions to parse API data

import json

def printName_NeoID(jsonData):
    #Creates a secondary dictonary of the "near_earth_objects" section
    neo_data = jsonData.get("near_earth_objects")

    #Nested For Loop: First loop parses through each date of api call, while second loop parses data for each asteroid for every date within search dates
    for date in neo_data:
        for asteroid in neo_data[date]:
            #Obtains the name and id for an asteroid of a certain date
            asteroid_name = asteroid.get("name")
            asteroid_id = asteroid.get("id")
                
            #prints out the asteroid's name and NEO id
            print(asteroid_name + ", " + asteroid_id)
    return


def prettyData(jsonData, indentValue):

    return json.dumps(jsonData, indent=indentValue)