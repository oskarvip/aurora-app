import streamlit as st
import json
from urllib.request import urlopen
from scipy import spatial
from os import environ
from mapbox import Geocoder
#import folium

# Declare constants
SCANDINAVIA_BBOX = (0.105400, 53.944367, 32.712822, 72.148786)
SCANDINAVIA_CENTER = (16.347656, 64.510643)
AURORA_DATA_URL = "https://services.swpc.noaa.gov/json/ovation_aurora_latest.json"
MAPBOX_ACCESS_TOKEN = environ.get("MAPBOX_ACCESS_TOKEN")
if not MAPBOX_ACCESS_TOKEN:
    raise ValueError("Missing MAPBOX_ACCESS_TOKEN")
geocoder = Geocoder()


st.title("Aurora Predictor app")
st.write("Predictions are performed using OVATION Prime auroral precipitation model")
# st.write("MAPBOX TOKEN IS: " + str(MAPBOX_ACCESS_TOKEN))


def forward_geocode(query):
    """
    Takes a query and returns the center coordinates as a tuple
    Args:
        query: str containing the name of a place
    """
    response = geocoder.forward(
        query, limit=3, types=["country", "place", "address"]
    ).json()
    features = response["features"]
    if len(features) == 0:
        return "Your search query yielded no results"
    return features[0]


def split_list(lst):
    coords = []
    ratings = []
    for row in lst:
        # Coordinates as tuple (lat, long)
        coords.append((row[1], row[0]))
        # Ratings as probability in percentage
        ratings.append(row[2])

    return coords, ratings


@st.cache(show_spinner=False, persist=False, suppress_st_warning=True)
def load_data(url):
    data = urlopen(url).read().decode()
    obj = json.loads(data)
    return obj


def find_closest(position):
    dist, index = tree.query(position)
    return dist, index


# Download the aurora predictions and prepare for search
with st.spinner(text='Getting data...'):
    aurora_data = load_data(AURORA_DATA_URL)
    aurora_coords, aurora_ratings = split_list(aurora_data["coordinates"])
    tree = spatial.KDTree(aurora_coords)

# Get the users location and convert to coordinates
st.header("Enter your location")
position_input = "Kiruna"
position_query = st.text_input("Enter a place (ex Kiruna)", "Kiruna")

position_properties = forward_geocode(position_query)
st.write(position_properties)

position_coordinates = tuple(reversed(position_properties["center"]))
st.write(position_coordinates)
#st.write(tuple(reversed(position_coordinates)))

dist, index = tree.query(position_coordinates)
ret = {
    "query": position_query,
    "query_result": position_properties["place_name"],
    "position": position_coordinates,
    "distance": dist,
    "aurora_coords": aurora_coords[index],
    "observation_time": aurora_data["Observation Time"],
    "forecast_time": aurora_data["Forecast Time"],
    "aurora_probability": str(aurora_ratings[index]) + "%",
}
st.write(
    "Forecasts should be interpreted as the probability of observing an aurora "
    "directly above you up to an hour in the future"
)
st.write(ret)
