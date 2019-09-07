import json

DOCTORS_HREF = '#doctors'
FLOAT_DECIMALS = 3

with open('facilityfilter.json') as json_file:
    facility_filter_json = json.load(json_file)
FACILITY_FILTER = set(facility_filter_json.get('Valid_Facility'))
