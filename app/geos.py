from geopy.geocoders import Nominatim 
from geopy.exc import GeocoderTimedOut
from geopy.distance import Distance
from geopy.distance import geodesic

# Function to obtain the coordinates of a list of places
def get_coordinates(places):
    geolocator = Nominatim(user_agent="Geopy Library")
    coordinates = []  # Use a list to store coordinate data
    
    for place in places:
        try:
            location = geolocator.geocode(place)
            if location:
                # Append the place and its coordinates as a list
                coordinates.append([place, location.latitude, location.longitude])
            else:
                # Append the place and a message indicating location was not found
                coordinates.append([place, "Location not found", "Location not found"])
        except Exception as e:
            # Append the place and the error occurred
            coordinates.append([place, f"Error occurred: {str(e)}", f"Error occurred: {str(e)}"])
    
    return coordinates