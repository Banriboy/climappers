import folium, folium.plugins, csv
import datetime 
from pprint import pprint

inputFileName = "max_wbgt8.csv"
nyCenter = (40.7128, -74.0060)

daysCount = 4
wbgtData = [[] for _ in range(daysCount)]

with open(inputFileName) as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        lat = row[1]
        lon = row[2]
        for day_i in range(daysCount):
            wbgtData[day_i].append( [lat, lon, float(row[day_i+3])/100] )
#             print( [lat, lon, row[day_i+3]] )
# pprint(wbgtData)

timeStamps = [
    "2004-08-01",
    "2004-08-02",
    "2004-08-03",
    "2004-08-04",]

usMap = folium.Map(location = nyCenter, zoom_start = 7)

folium.plugins.HeatMapWithTime(
      wbgtData,
      index = timeStamps,
      auto_play = True,
      radius = 50,
      max_opacity = 0.3,
      gradient = {0.0: "green", 0.763:"yellow", 0.811:"orange", 0.842:"red", 0.862:"black"}
).add_to(usMap)

usMap.save("heatmap-withtime.html")


