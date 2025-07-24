import json
import requests
from flask import Flask

# API endpoint URL's and access keys
WMATA_API_KEY = "65c6bbbf1e0340249643af329a4a19b8"
INCIDENTS_URL = "https://api.wmata.com/Incidents.svc/json/ElevatorIncidents"
headers = {"api_key": WMATA_API_KEY, 'Accept': '*/*'}

################################################################################

app = Flask(__name__)

# get incidents by machine type (elevators/escalators)
# field is called "unit_type" in WMATA API response
@app.route("/incidents/<unit_type>", methods=["GET"])
def get_incidents(unit_type):
    # create an empty list called 'incidents'
    incidents = []
    
    # use 'requests' to do a GET request to the WMATA Incidents API
    response = requests.get(INCIDENTS_URL, headers=headers)
    
    # retrieve the JSON from the response
    json_data = response.json()
    
    # iterate through the JSON response and retrieve all incidents matching 'unit_type'
    for incident in json_data.get('ElevatorIncidents', []):
        # Check if the incident matches the requested unit_type
        incident_unit_type = incident.get('UnitType', '').upper()
        requested_type = unit_type.upper()
        
        if (requested_type == 'ELEVATORS' and incident_unit_type == 'ELEVATOR') or \
           (requested_type == 'ESCALATORS' and incident_unit_type == 'ESCALATOR'):
            # for each incident, create a dictionary containing the 4 fields from the Module 7 API definition
            #   -StationCode, StationName, UnitType, UnitName
            incident_dict = {
                'StationCode': incident.get('StationCode', ''),
                'StationName': incident.get('StationName', ''),
                'UnitType': incident.get('UnitType', ''),
                'UnitName': incident.get('UnitName', '')
            }
            # add each incident dictionary object to the 'incidents' list
            incidents.append(incident_dict)
    
    # return the list of incident dictionaries using json.dumps()
    return json.dumps(incidents)

if __name__ == '__main__':
    app.run(debug=True)
