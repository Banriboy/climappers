# Style choices in folium follows CSS style properties.
#   https://www.w3schools.com/cssref/index.php
#   Color choices: https://www.w3.org/wiki/CSS/Properties/color/keywords

from geopy.geocoders import Nominatim
import folium, branca

geolocator = Nominatim(user_agent="spaceapps24")

# Takes "cityName, stateCode" as cityState and returns its (lat, lon).
#
def cityStateToLatLon(cityState):
    cityName = cityState.split(",")[0].lstrip().rstrip()
    regionName = cityState.split(",")[1].lstrip().rstrip()
    if regionName == "Japan":
        queryParams = {"city" : cityName,
                       "country" : regionName }
    else:        
        queryParams = {"city" : cityName,
                       "state" : regionName,
                       "country" : "United States" }
    
    location = geolocator.geocode(query=queryParams, timeout=1000)
    if location != None:
        return (location.latitude, location.longitude)
    else:
        raise RuntimeError(f"Failed to find (lat, lon) for {cityState}.")

def makeBoundaryLayer(geoJsonFilename, layerName, show=True):
    layer = folium.GeoJson(
        geoJsonFilename,
        name = layerName,
        show = show,
        style_function = lambda feature: {
            "color": "darkblue",
            "weight": 2,
            "fillColor": "transparent"}
    )
    return layer

def makeDroughtSeverityLayer(geoJsonFilename, layerName, show=True):
    layer = folium.GeoJson(
        geoJsonFilename,
        name = layerName,
        show = show,
        style_function = lambda feature:{
            "color": "red",
            "weight": 1,
            "fillColor": "darkbrown"   if feature["properties"]["DM"] == 4 
                    else "red"         if feature["properties"]["DM"] == 3
                    else "darkorange"  if feature["properties"]["DM"] == 2
                    else "lightsalmon" if feature["properties"]["DM"] == 1  # USDM's official color: #FCD37F
                    else "yellow"      if feature["properties"]["DM"] == 0
                    else "transparent",
            "fillOpacity": 0.3},
    )
    return layer

koppenIdDescription = """
    <table class="table table-striped table-hover table-condensed table-responsive">
    <tr><th>ID</th><th>Köppen Climate Classification</th><tr>
    <tr><td>11</td><td>Af</td></tr>
    <tr><td>12</td><td>Am</td></tr>
    <tr><td>13</td><td>As</td></tr>
    <tr><td>14</td><td>Aw</td></tr>
    <tr><td>21</td><td>BWk... B: arid/dry, W: desert, k: cold</td></tr>
    <tr><td>22</td><td>BWh... B: arid/dry, W: desert, h: hot</td></tr>
    <tr><td>26</td><td>BSk... B: arid/dry, S: steppe, k: cold</td></tr>
    <tr><td>27</td><td>BSh... B: arid/dry, S; steppe, h: hot</td></tr>
    <tr><td>31</td><td>Cfa... C: warm temp, f: fully humid, a: hot summer</td></tr>
    <tr><td>32</td><td>Cfb... C: warm temp, f: fully humid, b: warm summer</td></tr>
    <tr><td>33</td><td>Cfc... C: warm temp, f: fully humid, c: cool summer</td></tr>
    <tr><td>34</td><td>Csa... C: warm temp, s: summer dry, a: hot summer</td></tr>
    <tr><td>35</td><td>Csb... C: warm temp, s: summer dry, b: warm summer</td></tr>
    <tr><td>36</td><td>Csc... C: warm temp, s: summer dry, c: cool summer</td></tr>
    <tr><td>37</td><td>Cwa... C: warm temp, w: winter dry, a: hot summer</td></tr>
    <tr><td>38</td><td>Cwb... C: warm temp, w: winter dry, b: warm summer</td></tr>
    <tr><td>39</td><td>Cwc... C: warm temp, w: winter dry, c: cool summer</td></tr>
    <tr><td>41</td><td>Dfa... D: continental/snow, f: fully humid, a: hot summer</td></tr>
    <tr><td>42</td><td>Dfb... D: continental/snow, f: fully humid, b: warm summer</td></tr>
    <tr><td>43</td><td>Dfc... D: continental/snow, f: fully humid, c: subarctic</td></tr>
    <tr><td>44</td><td>Dfd... D: continental/snow, f: fully humid, d: extremely cold subarctic</td></tr>
    <tr><td>45</td><td>Dsa... D: continental/snow, s: summer dry, a: hot summer</td></tr>
    <tr><td>46</td><td>Dsb... D: continental/snow, s: summer dry, b: warm summer</td></tr>
    <tr><td>47</td><td>Dsc... D: continental/snow, s: summer dry, c: subarctic</td></tr>
    <tr><td>48</td><td>Dsd... D: continental/snow, s: summer dry, d: extremely cold subarctic</td></tr>
    <tr><td>49</td><td>Dwa... D: continental/snow, w: winter dry, a: hot summer</td></tr>
    <tr><td>50</td><td>Dwb... D: continental/snow, w: winter dry, b: warm summer</td></tr>
    <tr><td>51</td><td>Dwc... D: continental/snow, w: winter dry, c: subarctic</td></tr>
    <tr><td>52</td><td>Dwd... D: continental/snow, w: winter dry, d: extremely cold subarctic</td></tr>
    <tr><td>61</td><td>EF</td></tr>
    <tr><td>62</td><td>ET</td></tr>
    </table>"""

# World Bank, Köppen-Geiger Climate Classification:
#   https://datacatalog.worldbank.org/search/dataset/0042325
#   http://koeppen-geiger.vu-wien.ac.at/shifts.htm
#   http://koeppen-geiger.vu-wien.ac.at/data/legend.txt
#
def makeKoppenClassificationLayer(geoJsonFilename, layerName, show=True):
    koppenIFrame = branca.element.IFrame(html=koppenIdDescription, width=500, height=300)
    layer = folium.GeoJson(
        geoJsonFilename,
        name = layerName,
        show = show,
        style_function=lambda feature: {
            "color": "darkgreen",
            "weight": 2,
            "fillColor": "brown"      if feature["properties"]["GRIDCODE"] == 21 # BWk
                    else "brown"      if feature["properties"]["GRIDCODE"] == 22 # BWh
                    else "orange"     if feature["properties"]["GRIDCODE"] == 26 # Bsk
                    else "orange"     if feature["properties"]["GRIDCODE"] == 27 # Bsh
                    else "green"      if feature["properties"]["GRIDCODE"] == 31 # Cfa
                    else "green"      if feature["properties"]["GRIDCODE"] == 32 # Cfb
                    else "green"      if feature["properties"]["GRIDCODE"] == 33 # Cfc
                    else "yellow"     if feature["properties"]["GRIDCODE"] == 34 # Csa
                    else "yellow"     if feature["properties"]["GRIDCODE"] == 35 # Csb
                    else "yellow"     if feature["properties"]["GRIDCODE"] == 36 # Csc        
                    else "lightgreen" if feature["properties"]["GRIDCODE"] == 37 # Cwa
                    else "lightgreen" if feature["properties"]["GRIDCODE"] == 38 # Cwb
                    else "lightgreen" if feature["properties"]["GRIDCODE"] == 39 # Cwc        
                    else "blue"       if feature["properties"]["GRIDCODE"] == 41 # Dfa
                    else "blue"       if feature["properties"]["GRIDCODE"] == 42 # Dfb
                    else "blue"       if feature["properties"]["GRIDCODE"] == 43 # Dfc
                    else "blue"       if feature["properties"]["GRIDCODE"] == 44 # Dfd
                    else "fuchsia"    if feature["properties"]["GRIDCODE"] == 45 # Dsa
                    else "fuchsia"    if feature["properties"]["GRIDCODE"] == 46 # Dsb
                    else "fuchsia"    if feature["properties"]["GRIDCODE"] == 47 # Dsc        
                    else "fuchsia"    if feature["properties"]["GRIDCODE"] == 48 # Dsd
                    else "transparent",
            "fillOpacity": 0.3},
        tooltip = folium.GeoJsonTooltip(fields = ["GRIDCODE"], aliases = ["Köppen Climate Classification ID"]),
        popup = folium.Popup(koppenIFrame) 
    )
    return layer



# cluster: a list of cities; e.g., ["Seattle, WA", "Bellevue, WA", "Renton, WA"]
# 
#
def makeClusterLayer(cluster:list, clusterId:int, clusterColor:str, layerName=None, show=True):
    featureGroup = folium.FeatureGroup( str(clusterId+1) )
    for cityState in cluster:
        cityName = cityState.split(",")[0].lower() # "Seattle, WA" -> "seattle"
        cityDescription = f"<b>{cityState}</b><br>" +\
                          f'<img width="400" src="{cityName}.png"">'        
        folium.Marker(
            cityStateToLatLon(cityState),
            popup = folium.Popup(html=cityDescription, max_width=500, lazy=True),
            icon=folium.Icon(
                prefix = "fa", icon = str(clusterId+1), 
                color = clusterColor),
        ).add_to(featureGroup)
    return featureGroup

if __name__ == "__main__":
    print( cityStateToLatLon("Boston, MA") )
    
    waCities = ["Seattle, WA", "Bellevue, WA", "Renton, WA", "Issaquah, WA", "North Bend, WA",
                "Easton, WA", "Cle Elum, WA", "Quincy, WA", "George, WA", "Ritzville, WA",
                "Ellensburg, WA", "Sprague, WA", "Cheney, WA", "Spokane, WA", "Liberty Cake, WA"]
    for city in waCities:
        print( city, cityStateToLatLon(city) )
    
