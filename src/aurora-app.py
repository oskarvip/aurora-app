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


# aurora_coords, aurora_ratings = split_list(data['coordinates'])


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

# sequence = st.sidebar.text_area("Sequence input", my_pos, height=250)
my_pos = st.text_area(
    "Input coordinates on the form (long, lat)", my_pos_input, height=250
)
my_pos = eval(my_pos)
# st.write(my_pos)


# st.write(aurora_data.keys())
aurora_coords, aurora_ratings = split_list(aurora_data["coordinates"])
# st.write(aurora_coords)
tree = spatial.KDTree(aurora_coords)


# my_pos = (coordinates["long"], coordinates["lat"])
dist, index = tree.query(my_pos)

# print(my_pos, aurora_coords[index], aurora_ratings[index])

# my_pos = {"lat": 65.584160, "long": 22.154751}
ret = {
    "my_position": my_pos,
    "distance": dist,
    "aurora_coords": aurora_coords[index],
    "aurora_ratings": aurora_ratings[index],
}

st.write(ret)
