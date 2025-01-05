# import gecoder
from geopy.geocoders import Nominatim
import requests, csv, usstates

geolocator = Nominatim(user_agent="spaceapps24")

def downloadUsdmDroughtSeverityGeoJson(fileName):
    url = "https://droughtmonitor.unl.edu/data/json/" + fileName
    response = requests.get(url)
    if response.status_code == 200:
        open(fileName, "wb").write(response.content)
        print(f"Successfully downloaded and saved {fileName}.")
        return fileName
    else:
        raise RuntimeError(f"Failed to download {fileName} from USDM: {response.status_code}")


def cityStateToCountyFips(cityName, stateCode):
    queryParams = {"city" : cityName,
                   "state" : stateCode,
                   "country" : "United States" }
    location = geolocator.geocode(query=queryParams, timeout=1000)
    if location == None:
        raise RuntimeError(f"Nominatim failed to find (lat, lon) for {cityState}.")
    else:
#         print(type(location))
#         print(location.raw)
#         print(location.address) # "Boston, Suffolk County, Massachusetts, United States"
        countyFullName = location.address.split(",")[1].lstrip().rstrip()
        with open("uscounties.csv") as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                if row[2] == countyFullName and row[4] == stateCode:
                    return row[3]

# Takes "cityName, stateCode" as cityState (e.g. "Boston, MA") and
#   return (cityName, stateName); e.g. ("Boston", "MA")
#
def separateCityNameStateName(cityState):
    return (cityState.split(",")[0].lstrip().rstrip(),
            cityState.split(",")[1].lstrip().rstrip())
    

# def cityStateToCountyFips(cityName, stateCode):
#     osm = geocoder.osm(cityName + ", " + usstates.stateCodeToState[stateCode] + ", US")
#     countyFullName = osm.county
# 
#     with open("uscounties.csv") as csvFile:
#         reader = csv.reader(csvFile)
#         for row in reader:
#             if row[2] == countyFullName and row[4] == stateCode:
#                 return row[3]

def getDroughtSeverity(csvFileName):
    date = None
    severityIndex = -1
    with open(csvFileName, "r") as f:
        csvReader = csv.reader(f)
        for rowindex, row in enumerate(csvReader):
            if not row[0].startswith("MapDate"):
                d0To4List = row[5:10]
                if d0To4List.count("100.00") == len(d0To4List):
                    severityIndex = 4
                else:
                    maxVal = 0                
                    for elem in d0To4List:
                        elemF = float(elem)
                        if elemF != 0 and elemF != 100 and elemF > maxVal:
                            maxVal = elemF
                    if maxVal == 0:
                        severityIndex = 0
                    else:
                        severityIndex = d0To4List.index(str(maxVal))
                date = row[rowindex][0]
                return (severityIndex, date)

def downloadUsdmData(city, stateCode, startDate, endDate):
    countyFips = cityStateToCountyFips(city, stateCode)
    fileName = "usdm" + startDate + "-" + endDate + ".csv"
    usdmStartDate = startDate[4:6] + "/" + startDate[6:8] + "/" + startDate[0:4]
    usdmEndDate = endDate[4:6] + "/" + endDate[6:8] + "/" + endDate[0:4]
 
    url = "https://usdmdataservices.unl.edu/api/" + \
          "CountyStatistics/GetDroughtSeverityStatisticsByAreaPercent?" + \
          "aoi=" + str(countyFips) + "&startdate=" + usdmStartDate + \
          "&enddate=" + usdmEndDate + "&statisticsType=1"
    headers = {"Accept" : "text/csv"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        open(fileName, "wb").write(response.content)
        print("Successfully downloaded data from USDM. Saved it in ", fileName)
    else:
        print("Failed to download data from USDM", response.status_code)
        print(response.text)
        
    severityIndex, date = getDroughtSeverity(fileName)
    return severityIndex

    
    
if __name__ == "__main__":
    print( cityStateToCountyFips("Boston", "MA") )
    
    waCities = ["Seattle, WA", "Bellevue, WA", "Renton, WA", "Issaquah, WA", "North Bend, WA",
                "Easton, WA", "Cle Elum, WA", "Quincy, WA", "George, WA", "Ritzville, WA",
                "Ellensburg, WA", "Sprague, WA", "Cheney, WA", "Spokane, WA", "Liberty Cake, WA"]
    for cityState in waCities:
        cityName, stateName = separateCityNameStateName(cityState)
        print( cityStateToCountyFips(cityName, stateName) )    
# Test
#print( cityStateToCountyFips("Bedford","MA") )
#print( downloadUsdmData("Bedford", "MA", "20220101", "20221231"))
