import streamlit as st
import json
from urllib.request import urlopen
from scipy import spatial
from os import environ
from mapbox import Geocoder
from folium import Map, Marker
from folium.plugins import HeatMap
from streamlit_folium import folium_static

# import folium

# Declare constants
SCANDINAVIA_BBOX = (0.105400, 53.944367, 32.712822, 72.148786)
SCANDINAVIA_CENTER = (16.347656, 64.510643)
AURORA_DATA_URL = "https://services.swpc.noaa.gov/json/ovation_aurora_latest.json"
MAPBOX_ACCESS_TOKEN = environ.get("MAPBOX_ACCESS_TOKEN")
if not MAPBOX_ACCESS_TOKEN:
    raise ValueError("Missing MAPBOX_ACCESS_TOKEN")
geocoder = Geocoder()


st.title("Aurora Forecasting App")
st.write(
    "Short term forecasts are performed using OVATION Prime auroral precipitation "
    "model. Results should be interpreted as the probability of observing an aurora "
    "directly above a given location"
)
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


def generate_base_map(
    default_location=[64.9648751621697, 17.6754094331351], default_zoom_start=4
):
    base_map = Map(
        location=default_location, control_scale=True, zoom_start=default_zoom_start
    )
    return base_map


# Download the aurora predictions and prepare for search
with st.spinner(text="Getting data..."):
    aurora_data = load_data(AURORA_DATA_URL)
    aurora_coords, aurora_ratings = split_list(aurora_data["coordinates"])
    tree = spatial.KDTree(aurora_coords)

base_map = generate_base_map()
map_coords = [(row[1], row[0], row[2]) for row in aurora_data["coordinates"]]
HeatMap(data=map_coords, min_opacity=0, blur=50, radius=10).add_to(base_map)

# Get the users location and convert to coordinates
st.header("Enter your location")
position_query = st.text_input("Enter a place (ex Kiruna)")
ret = None
if position_query:
    position_properties = forward_geocode(position_query)
    # st.write(position_properties)

    position_coordinates = tuple(reversed(position_properties["center"]))

    dist, index = tree.query(position_coordinates)
    ret = {
        "query": position_query,
        "position_name": position_properties["place_name"],
        "position_coordinates": position_coordinates,
        "distance": dist,
        "aurora_coords": aurora_coords[index],
        "observation_time": aurora_data["Observation Time"],
        "forecast_time": aurora_data["Forecast Time"],
        "aurora_probability": str(aurora_ratings[index]) + "%",
    }

    popup = "Aurora Probability: {}".format(ret["aurora_probability"])
    Marker(position_coordinates, popup=popup, tooltip=ret["position_name"]).add_to(
        base_map
    )

    base_map.location = position_coordinates
    st.subheader("Aurora probability in {}".format(ret["position_name"]))
    st.write("Aurora Probability: {}".format(ret["aurora_probability"]))
    st.write("Forecast Time: {}".format(ret["forecast_time"]))
    st.write("Observation Time: {}".format(ret["observation_time"]))

folium_static(base_map)
# if ret:
# st.write(ret)
