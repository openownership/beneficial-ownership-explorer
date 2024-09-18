from geopy.geocoders import ArcGIS

geolocator_arcgis = ArcGIS()

def country_name(code):
    """Lookup country code"""
    try:
        if "-" in code:
            subdivision = pycountry.subdivisions.get(code=code)
            name = f"{subdivision.name}, {subdivision.country.name}"
        else:
            name = pycountry.countries.get(alpha_2=code).name
    except AttributeError:
        name = code
    return name

def build_address(entity):
    """Build full address (including country)"""
    for address in entity["addresses"]:
        if address["address"] and address["country"]:
            if len(address["country"]) == 2 or (len(address["country"]) == 5 and "-" in address["country"]):
                country = country_name(address["country"])
            else:
                country = address["country"]
            full_address = ', '.join([address["address"], address["country"]])
            return full_address
    return None

def geolocate_address(entity):
    """Get latitude and longitude from address"""
    address = build_address(entity)
    if address:
        location = geolocator_arcgis.geocode(address)
        return location[1], location[0]
    else:
        return None, None
