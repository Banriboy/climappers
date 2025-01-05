# Map tile choices: https://leaflet-extras.github.io/leaflet-providers/preview/
#   USGS.USTopo
#   OpenTopoMap
#   TopPlusOpen.Color
#   Stadia.StamenTerrainBackground
#   Thunderforest.Landscape
#   Jawg.Terrain
#   Esri.WorldStreetMap
#   Esri.WorldPhysical
#   NASAGIBS.ViirsEarthAtNight2012
#
# Font choices: https://fontawesome.com/
#
# Boundarires of WA counties (shepefiles/GeoJson):
#   https://geo.wa.gov/datasets/wadnr::wa-county-boundaries/
#
# Shapefiles -> GeoJson (and GeoJson -> GeoJson) conversion: 
#   https://mapshaper.org/
#     mapshaper -proj wgs84 -simplify dp 20% -o COUNTIES_POLYM.json
#   GDAL's ogr2ogr command:
#     ogr2ogr -f GeoJSON -t_srs crs:84 COUNTIES_POLYM.geojson COUNTIES_POLYM.shp
#
# Icon color choices: 'darkgreen', 'white', 'cadetblue', 'darkred', 'darkblue', 'orange',
#   'purple', 'green', 'lightblue', 'lightgray', 'red', 'black', 'blue', 'gray', 'darkpurple',
#   'lightred', 'lightgreen', 'pink', 'beige'
#
# US Drought Monitor (USDM)
#   https://droughtmonitor.unl.edu/DmData/GISData.aspx
# North American Drought Monitor (NADM) 
#   https://droughtmonitor.unl.edu/NADM/
#   https://www.ncei.noaa.gov/access/monitoring/nadm/
# Canadian Drount Monitor (CDM)
#   https://agriculture.canada.ca/en/agricultural-production/weather/canadian-drought-monitor
# Mexico Drougt Monitor (MDM)
#   https://smn.conagua.gob.mx/es/climatologia/monitor-de-sequia/monitor-de-sequia-en-mexico

import folium
from maputils import *
from usdm import *

# These are the 4 clusters that were made for Space Apps 23. 
# cluster0 = ["Seattle, WA", "Bellevue, WA", "Renton, WA"]
# cluster1 = ["Issaquah, WA", "North Bend, WA"]
# cluster2 = ["Easton, WA", "Cle Elum, WA"]
# cluster3 = ["Quincy, WA", "George, WA", "Ritzville, WA", "Ellensburg, WA", "Sprague, WA",
#             "Cheney, WA", "Spokane, WA", "Liberty Lake, WA"]

cluster1 = ['Seattle, WA',
     'Bellevue, WA',
     'Renton, WA',
     'Bremerton, WA',
     'Port Townsend, WA',
     'Glenwood, WA',
     'Everett, WA',
     'Mount Vernon, WA']

cluster2 = ['Tacoma, WA',
     'Olympia, WA',
     "Wa'atch, WA",
     'Forks, WA',
     'James Island, WA',
     'Abbey Island, WA',
     'Taholah, WA',
     'Aberdeen, WA',
     'Raymond, WA',
     'Long Beach, WA',
     'Centralia, WA',
     'Longview, WA',
     'Vancouver, WA',
     'Yale Park, WA',
     'Bellingham, WA',
     'Elma, WA',
     'Pe Ell, WA',
     'Cathlamet, WA',
     'Eatonville, WA',
     'Orting, WA',
     'Takamatsu, Japan',
     'Matsuyama, Japan',
     'Niihama, Japan',
     'Okayama, Japan',
     'Himeji, Japan',
     'Fukuyama, Japan',
     'Hiroshima, Japan',
     'Hofu, Japan']

cluster3 = ['Quincy, WA',
     'George, WA',
     'Ritzville, WA',
     'Moses Lake, WA',
     'Richland, WA',
     'Kennewick, WA',
     'Odessa, WA',
     'Coulee City, WA',
     'LaCrosse, WA',
     'Connell, WA',
     'Sixprong, WA',
     'Dayton, WA',
     'Sunnyside, WA']

cluster4 = ['Sacramento, CA', 'Fresno, CA']

cluster5 = ['Las Vegas, NV', 'Phoenix, AZ']

cluster6 = ['Sprague, WA',
     'Cheney, WA',
     'Spokane, WA',
     'Tire Junction, WA',
     'Carson, WA',
     'Peaceful Valley, WA',
     'Colfax, WA',
     'Pomeroy, WA',
     'Clarkston, WA']

cluster7 = ['Issaquah, WA',
     'North Bend, WA',
     'Union, WA',
     'Quilcene, WA',
     'Sequim, WA',
     'Port Angeles, WA',
     'Winston, WA',
     'Maple Valley, WA',
     'Monroe, WA',
     'Gold Bar, WA',
     'Darrington, WA',
     'Concrete, WA']

cluster8 = ['Easton, WA',
     'Cle Elum, WA',
     'Packwood, WA',
     'Scenic, WA',
     'Winthrop, WA',
     'Moore, WA']

cluster9 = ['Ellensburg, WA',
     'Liberty Lake, WA',
     'Goldendale, WA',
     'Omak, WA',
     'Brewster, WA',
     'Leavenworth, WA',
     'Wenatchee, WA',
     'Kittitas, WA',
     'Yakima, WA',
     'Mansfield, WA',
     'Trout Lake, WA',
     'Rockford, WA',
     'Parrott Crossing, WA',
     'Walla Walla, WA',
     'Republic, WA',
     'Colville, WA',
     'Ione, WA',
     'Entiat, WA',
     'Wilbur, WA',
     'Ford, WA',
     'Klickitat, WA',
     'Keller, WA']

clusters = [cluster1, cluster2, cluster3, cluster4, cluster5, cluster6, cluster7, cluster8, cluster9]
iconColors = ["purple", "green", "red", "lightblue", "darkpurple", "black", "lightgray", "darkblue", "pink", "darkgreen"]
# Icon color choices: 'darkgreen', 'white', 'cadetblue', 'darkred', 'darkblue', 'orange',
#   'purple', 'green', 'lightblue', 'lightgray', 'red', 'black', 'blue', 'gray', 'darkpurple',
#   'lightred', 'lightgreen', 'pink', 'beige'

usdmFileName = "usdm_current.json"
downloadUsdmDroughtSeverityGeoJson(usdmFileName)

cdmFilenames = ["CDM_2408_D0_LR.geojson",
                "CDM_2408_D1_LR.geojson",
                "CDM_2408_D2_LR.geojson",
                "CDM_2408_D3_LR.geojson"]

waCenter = (47.7511, -120.7401)
waMap = folium.Map(location = waCenter, zoom_start = 7, tiles="TopPlusOpen.Color")

makeBoundaryLayer("counties_wa.json", "WA Counties").add_to(waMap)
makeBoundaryLayer("us-states.json", "US States", show=False).add_to(waMap)

makeDroughtSeverityLayer(usdmFileName, "US Drought Severity").add_to(waMap)

canadaDroughtLayer = folium.FeatureGroup(name = "Canada Drought Severity").add_to(waMap)
for cdmFileName in cdmFilenames:
    makeDroughtSeverityLayer(cdmFileName, "Canada").add_to(canadaDroughtLayer)

makeKoppenClassificationLayer("climate-classification.json",
                              "Köppen-Geiger Climate Classification", show=False).add_to(waMap)

for clusterId, cluster in enumerate(clusters):
    makeClusterLayer(cluster, clusterId, iconColors[clusterId]).add_to(waMap)

folium.LayerControl().add_to(waMap)
waMap.save("wa-usstates-usdm-cdm-koppen.html")
