import csv
from geopy.geocoders import Nominatim

input_file = 'hpn.csv'
# input_files = ['hpn.csv',
#                'jfk.csv']

output_file = 'max_wbgt.csv'

appName = "spaceapps24-wbgt"
geolocator = Nominatim(user_agent=appName)

airport_code = None
daily_max_wbgt = {}

with open(input_file, newline='') as csvfile:
    reader = csv.reader(csvfile)
    
    for i, row in enumerate(reader):
        if i == 0:
            continue 
        elif i == 1:            
            airport_code = row[0]
            location = geolocator.geocode(query=f"{airport_code}, United States", addressdetails=True)
            locationDataset = location.raw
            lat = round(float(locationDataset["lat"]), 2)
            lon = round(float(locationDataset["lon"]), 2)
            print(airport_code, lat, lon)
        else:            
            date = row[0]
            wbgt = float(row[2])             
            if date in daily_max_wbgt:
                daily_max_wbgt[date] = max(daily_max_wbgt[date], wbgt)
            else:
                daily_max_wbgt[date] = wbgt

max_wbgt_list = [airport_code, lat, lon] + [str(max_wbgt) for date, max_wbgt in sorted(daily_max_wbgt.items())]

with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(max_wbgt_list)
