
import phonenumbers

import folium

from phonenum import number

from phonenumbers import geocoder

# ----------------------------------------------------------------
# Coded by: Abdullah Alqurashi.
# ----------------------------
# Git-Hub: https://github.com/Kaser2023
# Linked-In: https://www.linkedin.com/in/abdullah-alqurashi-a3777a224/
# Date: 18.Rabi'a Alakhir. 1446 -  2024.Oct.21
# ----------------------------------------------------------------



Key = 'm'

# get name of the country
k_number = phonenumbers.parse(number)
your_location = (geocoder.description_for_number(k_number, "en"))
print(your_location)

# get service provider (Sabafon, Yemenmobile, Turkcell ...etc)
from phonenumbers import carrier

service_number = phonenumbers.parse(number)
print(carrier.name_for_number(service_number, "en"))


# get latitude and longitude = الحصول على خطوط الطول والعرض

from opencage.geocoder import OpenCageGeocode

geocoder = OpenCageGeocode(Key)
query = str(your_location)
result = geocoder.geocode(query)

#print(result)

lat = result[0] ['geometry']['lat']
lng = result[0] ['geometry']['lng']

print(lat, lng)

myMap = folium.Map(loction=[lat, lng], zoom_start=9)
folium.Marker([lat, lng], popup=your_location).add_to(myMap)


## save map in html file

myMap.save("Kaser-Location.html")