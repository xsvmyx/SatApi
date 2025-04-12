import math

def quadkey_to_tile(quadkey):
    tile_x = tile_y = 0
    zoom = len(quadkey)
    
    for i in range(zoom):
        bit = zoom - i - 1
        mask = 1 << bit
        q = quadkey[i]
        if q == '1':
            tile_x |= mask
        elif q == '2':
            tile_y |= mask
        elif q == '3':
            tile_x |= mask
            tile_y |= mask
    return tile_x, tile_y, zoom

def tile_to_latlon(tile_x, tile_y, zoom):
    n = 2.0 ** zoom
    lon_deg = tile_x / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * tile_y / n)))
    lat_deg = math.degrees(lat_rad)
    return lat_deg, lon_deg

def quadkey_to_latlon(quadkey):
    tile_x, tile_y, zoom = quadkey_to_tile(quadkey)
    return tile_to_latlon(tile_x, tile_y, zoom)

def get_coordinates_from_filename(filename):
    quadkey = filename.split('.')[0][1:]  
    return quadkey_to_latlon(quadkey)

