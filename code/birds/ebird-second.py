import ebird.api as eb, json
from pprint import pprint

apiKey = ""

stateCodes = ["MA", "CT", "RI", "NY", "VT", "NH", "ME"]

for stateCode in stateCodes:
    countyNameToRecords = {}
    counties = eb.get_regions(apiKey, "subnational2", "US-" + stateCode)

    for county in counties:
        countyCode = county["code"]
        countyName = county["name"]
        records = eb.get_observations(apiKey, countyCode, back=7)
    #     pprint(records)
    #     print(f"{len(records)} species observed in {countyName} county.")

        totalObsCount = 0
        for r in records:
            if "howMany" not in r: r["howMany"] = 1
            totalObsCount += r["howMany"]
        print(f"{totalObsCount} observations in {stateCode} {countyName} county")

        recordsSortedByObsCount = sorted(records, key = lambda listElem: listElem["howMany"], reverse=True)
    #     for i in range(5):
    #         print("   ", recordsSortedByObsCount[i]["comName"], recordsSortedByObsCount[i]["howMany"])
        countyNameToRecords[countyName] = {}
        countyNameToRecords[countyName]["records"] = recordsSortedByObsCount
        countyNameToRecords[countyName]["totalObsCount"] = totalObsCount
        
    with open(stateCode.lower() + "CountyNameToRecords.json","w") as f:
        data = json.dumps(countyNameToRecords)
        f.write(data)
