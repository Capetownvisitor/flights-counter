from opensky_api import OpenSkyApi, OpenSkyStates, StateVector
import sys

def get_aircraft_number_by_carrier(api: OpenSkyApi,carrier_code: str = "DLH") -> int:

    try:
        # Call the API and get all current States / Flights
        s: OpenSkyStates = api.get_states()
    except Exception as e:
        print("An error occurred while calling the API")
        print(e)
        return -1
    
    try:
        states_vector: list[StateVector] = s.states
    except Exception as e:
        print("Error reading the States")
        print(e)
        return -1

    num_carrier_planes = 0

    for state in states_vector:
        callsign: str = state.callsign
        # skip missing callsigns
        if callsign is None:
            continue
        onGround: bool = state.on_ground
        if callsign.startswith(carrier_code) and not onGround:
            #found callsign prefix
            num_carrier_planes += 1
    
    return num_carrier_planes

if __name__ == "__main__":
    # create API Object once and pass it over for every function call
    api = OpenSkyApi()

    print("Getting the Data from OpenSky...")
    if len(sys.argv) <= 1:
        # no argmuents supplied:
        print(f"Currently there are: {get_aircraft_number_by_carrier(api, 'DLH')} planes from LuftHansa in the air.")
    elif len(sys.argv[1]) == 3:
        # try to use comamnd line input as carrier_code:
        print(f"Currently there are: {get_aircraft_number_by_carrier(api, sys.argv[1].upper())} planes from your chosen carrier in the air.")
    else:
        print("Wrong Input Format!")
        print("Use: python script.py 'XXX' <-- 3 letter carrier code")
    