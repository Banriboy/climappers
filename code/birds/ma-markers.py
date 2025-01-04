# Font choices: https://fontawesome.com/

import folium

maCenter = (42.4072, -71.3824)
logan = (42.365792221496, -71.00966724673485)
hanscom = (42.46495591784104, -71.2869683230597)

maMap = folium.Map(location = maCenter, zoom_start = 9)

folium.Marker(
    location = logan,
    popup = "<b><i>Logan Airport</i><b>",
    tooltip = "Click me!",
).add_to(maMap)

popupHanscom = folium.Popup("Here is Hanscom!",
                            show=True,)

folium.Marker(
    location = hanscom,
    popup = popupHanscom,
    tooltip = "Hi from Hanscom!",
    icon = folium.Icon(color="red", icon="plane")
).add_to(maMap)

maMap.save("ma-popups.html")



