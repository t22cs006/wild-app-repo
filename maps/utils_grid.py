# maps/utils_grid.py
from wildlife.constants import CENTER_LAT, CENTER_LON, GRID_SIZE, MIN_LAT, MAX_LAT, MIN_LON, MAX_LON
import math

def latlon_to_grid(lat, lon):
    gx = math.floor((lon - MIN_LON) / GRID_SIZE)
    gy = math.floor((lat - MIN_LAT) / GRID_SIZE)
    return gx, gy
