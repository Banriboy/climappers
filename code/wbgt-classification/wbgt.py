from noaa_wbgt import getWbgt

lat = 42.490027972375344
lon = -71.28465073182961

currentWbgt, timeToWbgtDictToday, timeToWbgtDictTomorrow, timeToWbgtDictWeek = getWbgt(lat, lon)

print("Current WBGT (F): ", currentWbgt)
print(timeToWbgtDictToday)
