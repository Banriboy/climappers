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

cluster0 = ["Seattle, WA", "Bellevue, WA", "Renton, WA"]
cluster1 = ["Issaquah, WA", "North Bend, WA"]
cluster2 = ["Easton, WA", "Cle Elum, WA"]
cluster3 = ["Quincy, WA", "George, WA", "Ritzville, WA", "Ellensburg, WA", "Sprague, WA",
            "Cheney, WA", "Spokane, WA", "Liberty Lake, WA"]
clusters = [cluster0, cluster1, cluster2, cluster3]
iconColors = ["red", "blue", "darkpurple", "pink"]

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
    featureGroup = folium.FeatureGroup(
        name = "Cluster " + str(clusterId)
    ).add_to(waMap)
    for cityState in cluster:
#         cityName = cityState.split(",")[0] # "Seattle, WA" -> "Seattle"
        folium.Marker(
            cityStateToLatLon(cityState),
            popup = folium.Popup(
                f"<b>{cityState}</b><p>Cluster ID: {clusterId}</p>"),
            icon=folium.Icon(
                prefix = "fa", icon = str(clusterId), 
                color = iconColors[clusterId]),
        ).add_to(featureGroup)

folium.LayerControl().add_to(waMap)
waMap.save("wa-counties-cities-usdm-koppen.html")
