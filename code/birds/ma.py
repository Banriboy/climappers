import folium
import folium.features

maCenter = (42.4072, -71.3824)

maMap = folium.Map(location = maCenter, zoom_start = 9)

maMap.save("ma.html")



