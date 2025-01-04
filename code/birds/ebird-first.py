import ebird.api as eb
from pprint import pprint

apiKey = ""

# Getting a list of dictionaries, each of which describes a county in MA.
#   Each dictionary contains a county's code (county ID) and name. 
#   "subnational2" means counties.
counties = eb.get_regions(apiKey, "subnational2", "US-MA")
# pprint(counties)
    # US-MA-017 is the county code for Middlesex conty

# Getting a list of dictionaries, each of which describes a species observed.
#   "back=7" means the last 7 days. 
records = eb.get_observations(apiKey, "US-MA-017", back=7)
# pprint(records)
print(f"{len(records)} species observed.")

for r in records:
    if "howMany" not in r: r["howMany"] = 1

recordsSortedByObsCount = sorted(records, key = lambda listElem: listElem["howMany"], reverse=True)
for i in range(5):
    print("   ", recordsSortedByObsCount[i]["comName"], recordsSortedByObsCount[i]["howMany"])



