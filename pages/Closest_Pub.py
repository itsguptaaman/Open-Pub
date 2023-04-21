import utils

lon, lat = utils.lat_lon_inputs()
try:
    if lon and lat != str:
        lon = float(lon)
        lat = float(lat)
        utils.display_locations(lon, lat)
except Exception as e:
    pass    