import os
import csv
import obspy
import warnings
from obspy import UTCDateTime
from obspy.clients.fdsn import Client
from obspy.taup import TauPyModel
warnings.filterwarnings("ignore")

# define the CSV file path
csv_file = "\jan76_dec20.csv"  # replace with the path to your CSV file

# input for start event date (year, month, day)
start_year = int(input("Enter start year: "))
start_month = int(input("Enter start month: "))
start_day = int(input("Enter start day: "))

# input for end event date (year, month, day)
end_year = int(input("Enter end year: "))
end_month = int(input("Enter end month: "))
end_day = int(input("Enter end day: "))

# input for magnitude range (minimum and maximum magnitude)
min_magnitude = float(input("Enter minimum magnitude: "))
max_magnitude = float(input("Enter maximum magnitude: "))

# read the CSV file and extract required information
events_info = []
with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        evt = row[0]
        evtime = UTCDateTime(f"{row[1]}-{row[2]}-{row[3]}T{row[4]}:{row[5]}:{row[6]}")
        evmag = float(row[10])
        evlat = float(row[7])
        evlon = float(row[8])
        evdep = float(row[9])

        # Check if the event is within the specified time period and magnitude range
        if (start_year <= evtime.year <= end_year) and \
           (start_month <= evtime.month <= end_month) and \
           (start_day <= evtime.day <= end_day) and \
           (min_magnitude <= evmag <= max_magnitude):
            events_info.append((evt, evtime, evmag, evlat, evlon, evdep))

# print the events within the specified time period and magnitude range with index numbers
print("Events within the specified time period and magnitude range:")
for i, (evt, evtime, evmag, evlat, evlon, evdep) in enumerate(events_info):
    print(f"[{i}] Event: {evt}, Time: {evtime}, Magnitude: {evmag}, Latitude: {evlat}, Longitude: {evlon}, Depth: {evdep}")

# input for selecting an event by index number
selected_index = int(input("Enter the index number of the event you want to choose: "))

# check if the selected index is valid
if 0 <= selected_index < len(events_info):
    selected_event = events_info[selected_index]
    print(f"Selected Event: {selected_event}")
else:
    print("Invalid index number. Please choose a valid index.")



############################################################################################


# input for network and station names
phase_name = input("Enter phase name:")
network_name = input("Enter network name: ")
station_name = input("Enter station name: ")

# initialize the FDSN client (e.g., IRIS, USGS, RESIF)
client = Client("IRIS")

# create a TauPy model
model = TauPyModel(model="iasp91")

# calculate event time for the selected event
selected_event = events_info[selected_index]
evtime = selected_event[1]

# request station information (inventory)
inventory = client.get_stations(network=network_name, station=station_name, starttime=evtime - 31104000, endtime=evtime + 31104000)

# Initialize stla and stlo as None in case no matching station is found
stla = None
stlo = None

# extract station latitude and longitude if the station is found
for network_info in inventory:
    for station_info in network_info:
        stla = station_info.latitude
        stlo = station_info.longitude

# check if station information was found
if stla is not None and stlo is not None:
    print(f"Station: {station_name}, Network: {network_name}, Latitude: {stla}, Longitude: {stlo}")
else:
    print(f"No station information found for Station: {station_name}, Network: {network_name}")

# calculate phase arrival time for the selected event
selected_event = events_info[selected_index]
evtime = selected_event[1]
evmag = selected_event[2]
evlat = selected_event[3]
evlon = selected_event[4]
evdep = selected_event[5]

# calculate phase arrival time
dist0, az, baz = obspy.geodetics.base.gps2dist_azimuth(evlat, evlon, stla, stlo)
dist = obspy.geodetics.base.kilometers2degrees(dist0)
arrivals = model.get_travel_times(source_depth_in_km=evdep, distance_in_degree=dist, phase_list=[f"{phase_name}"])

if not arrivals:
    print(f"{phase_name} phase not found for the selected event.")
else:
    phase_time = evtime + arrivals[0].time.copy()
    print(f"{phase_name} phase arrival time: {phase_time}")

    # request waveform data for the selected phase
    start_time = phase_time - 100  # Adjust the time window as needed
    end_time = phase_time + 400    # Adjust the time window as needed

    # loop through the components and process each one
    for component in ["BHZ", "BHN", "BHE"]:  # Update with your desired components
        st = client.get_waveforms(network_name, station_name, "*", component, start_time, end_time)

        if st:
            # save the waveform data to a SAC file with the specified format
            sac_filename = f"{selected_event[0]}.{network_name}.{station_name}.{component}.SAC"
            st[0].stats.sac = {
                'o': evtime - start_time,
                'stla': stla,
                'stlo': stlo,
                'evla': evlat,
                'evlo': evlon,
                'evdp': evdep,
                'mag': evmag,
                'dist': dist0,
                'az': az,
                'baz': baz,
                'gcarc': dist0,
                'depmen': 0,
                'cmpaz': 0,
                'cmpinc': 0,
                'leven': 1,
                'khole': ' ' * 8,
                'nzyear': phase_time.year,
                'nzjday': phase_time.julday,
                #'nzday': evtime.day,
                'nzhour': phase_time.hour,
                'nzmin': phase_time.minute,
                'nzsec': phase_time.second,
                'nzmsec': phase_time.microsecond // 1000,
            }
            st.write(sac_filename, format="SAC")
            print(f"Waveform data and header saved to {sac_filename}")
        else:
            print(f"No waveform data found for {phase_name} phase at Station: {station_name}, Network: {network_name}, Component: {component}")