import json

def fetch_shipping_lanes():
    with open(r"assets/geojson/boundaries/Shipping_Lanes.geojson") as shipping:
        shipping_lanes_json = json.load(shipping)

    return shipping_lanes_json

def fetch_economic_zones():
    with open(r"assets/geojson/boundaries/EEZ_Boundaries.json") as eez:
        eez_boundaries_json = json.load(eez)

    return eez_boundaries_json

def fetch_ncs_fields():
    with open(r"assets/geojson/fields/myshpfile.geojson") as norway:
        norwegian_fields_json = json.load(norway)

    return norwegian_fields_json

def fetch_faults():
    with open(r"assets/geojson/geology/faults.json") as faults:
        faults_json = json.load(faults)

        return faults_json

def fetch_structures():
    with open(r"assets/geojson/geology/domer.json") as domer:
        domer_json = json.load(domer)

        return domer_json