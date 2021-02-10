import streamlit as st
import json
from urllib.request import urlopen
from scipy import spatial


st.title("Aurora Predictor app")
st.write("Predictions are performed using OVATION Prime auroral precipitation model")


def split_list(lst):
    coords = []
    ratings = []
    for row in lst:
        coords.append((row[0], row[1]))






        ratings.append(row[2])
    return coords, ratings


@st.cache
def load_data():
    url = "https://services.swpc.noaa.gov/json/ovation_aurora_latest.json"
    data = urlopen(url).read().decode()
    obj = json.loads(data)
    return obj


def find_closest(my_pos):
    dist, index = tree.query(my_pos)
    return dist, index


aurora_data = load_data()

st.header("Enter your location")
my_pos_input = "(22.154751, 65.584160)"

my_pos = st.text_area(
    "Input coordinates on the form (long, lat)", my_pos_input, height=50
)
my_pos = eval(my_pos)

aurora_coords, aurora_ratings = split_list(aurora_data["coordinates"])

tree = spatial.KDTree(aurora_coords)
dist, index = tree.query(my_pos)

ret = {
    "my_position": my_pos,
    "distance": dist,
    "aurora_coords": aurora_coords[index],
    "aurora_ratings": aurora_ratings[index],
}

st.write(ret)
