# Font choices: https://fontawesome.com/
#
# Boundarires of MA counties (shepefiles):
#   https://www.mass.gov/info-details/massgis-data-counties
#
# Shapefile -> GeoJson conversion: 
#   https://mapshaper.org/
#   https://github.com/mbloch/mapshaper/wiki/Command-Reference
#     mapshaper -proj wgs84 -simplify dp 20% -o COUNTIES_POLYM.json
#   GDAL's ogr2ogr command:
#     ogr2ogr -f GeoJSON -t_srs crs:84 COUNTIES_POLYM.geojson COUNTIES_POLYM.shp
#    
# US counties database: https://simplemaps.com/data/us-counties
#
# Style choices in folium follows CSS style properties.
#   https://www.w3schools.com/cssref/index.php
#   Font name choices (predefined names): https://www.w3.org/wiki/CSS/Properties/color/keywords
#

import csv, json, folium, folium.plugins, branca
from pprint import pprint

# maCenter = (42.4072, -71.3824)
mapCenter = (43.86965971392195, -73.46419566567673)
maCountyCenters = {}
ctCountyCenters = {}
riCountyCenters = {}
nyCountyCenters = {}
vtCountyCenters = {}
nhCountyCenters = {}
meCountyCenters = {}

with open("uscounties.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header
    for row in reader:
        if row[5] == "Massachusetts":
            maCountyCenters[row[1]] = (row[6],row[7])
            continue
        if row[5] == "Connecticut":
            ctCountyCenters[row[1]] = (row[6],row[7])
            continue
        if row[5] == "Rhode Island":
            riCountyCenters[row[1]] = (row[6],row[7])
            continue
        if row[5] == "New York":
            nyCountyCenters[row[1]] = (row[6],row[7])
            continue
        if row[5] == "Vermont":
            vtCountyCenters[row[1]] = (row[6],row[7])
            continue
        if row[5] == "New Hampshire":
            nhCountyCenters[row[1]] = (row[6],row[7])
            continue
        if row[5] == "Maine":
            meCountyCenters[row[1]] = (row[6],row[7])
            continue
countyCentersList = [maCountyCenters, ctCountyCenters, riCountyCenters, nyCountyCenters,
                     vtCountyCenters, nhCountyCenters, meCountyCenters]

maMap = folium.Map(location = mapCenter, zoom_start = 7)

folium.GeoJson(
    "ma-counties.json",
    style_function = lambda geoJsonFeatures: {
        "color": "darkblue",
        "weight": 2,
        "fillOpacity": 0},
).add_to(maMap)

folium.GeoJson(
    "us-states.json",
    style_function = lambda geoJsonFeatures: {
        "color": "darkblue",
        "weight": 2,
        "fillOpacity": 0},
).add_to(maMap)

stateCodes = ["MA", "CT", "RI", "NY", "VT", "NH", "ME"]

for i, countyCenters in enumerate(countyCentersList):
    ebirdJsonFileName = stateCodes[i].lower() + "CountyNameToRecords.json"
    countyNameToRecords = {}
    with open(ebirdJsonFileName, mode="r") as f:
        countyNameToRecords = json.load(f)
    print(f"Finished reading {ebirdJsonFileName}.")

    heatmapData =[]
    for countyName, countyCenter in countyCenters.items():
        if countyName in countyNameToRecords:
            heatmapData.append( [countyCenter[0],
                                 countyCenter[1],
                                 countyNameToRecords[countyName]["totalObsCount"] ])
            print("    ", stateCodes[i], countyName, countyNameToRecords[countyName]["totalObsCount"])
    print("    ", heatmapData)

    folium.plugins.HeatMap(
        data = heatmapData,
        radius = 30,
    ).add_to(maMap)
    # radius=,max_opacity=1,gradient={0.38: 'blue', 0.4: 'lime', 0.5:'yellow',0.75: 'orange', 0.9:'red'}


maMap.save("heatmap.html")



