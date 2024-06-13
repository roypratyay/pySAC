# pySAC
This script processes seismic event data from a CSV file using the obspy library and FDSN web services. Users can filter events by date and magnitude, select a specific event, and retrieve waveform data for a specified seismic phase at a given station. The retrieved waveform data is then saved in SAC (Seismic Analysis Code) format.


# README

## Seismic Data Extraction and Processing Script

This script is designed to extract seismic event data from a CSV file, filter events based on user-defined criteria, select a specific event, and retrieve waveform data for a given seismic phase at a specified station. The retrieved waveform data is then saved in SAC (Seismic Analysis Code) format. The script leverages the `obspy` library for seismic data processing and FDSN web services for data retrieval.

### Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.x
- `obspy` library
- Access to a jan76_dec20.csv file containing seismic event data

You can install the required libraries using pip:

```sh
pip install obspy
```

###  Global Centroid-Moment-Tensor (CMT) Catalog File

The jan76_dec20.csv is a small version of Global Centroid-Moment-Tensor (CMT) catalog file and contains the following columns in the specified order:

1. Event ID
2. Year
3. Month
4. Day
5. Hour
6. Minute
7. Second
8. Latitude
9. Longitude
10. Depth
11. Magnitude

### Script Usage

1. **Specify the Path to the CSV File:**

   Replace the placeholder path in the script with the actual path to your **jan76_dec20.csv** file:

   ```python
   csv_file = "path/to/your/jan76_dec20.csv"
   ```

2. **Run the Script:**

   Execute the script in your Python environment. You will be prompted to enter various inputs:

   - **Event Date Range:**
     - Start year, month, and day
     - End year, month, and day
   - **Magnitude Range:**
     - Minimum magnitude
     - Maximum magnitude
   - **Event Selection:**
     - Index number of the event you wish to select
   - **Phase, Network, and Station:**
     - Phase name (e.g., "P", "S")
     - Network name (e.g., "IU")
     - Station name (e.g., "ANMO")

3. **Retrieve and Save Waveform Data:**

   The script will retrieve the waveform data for the specified phase at the selected station and save it in SAC format. The filename will follow the convention:

   ```
   EventID.Network.Station.Component.SAC
   ```

### Example

Here's an example of how the script can be run and interacted with:

```sh
Enter start year: 2020
Enter start month: 1
Enter start day: 1
Enter end year: 2020
Enter end month: 12
Enter end day: 31
Enter minimum magnitude: 5.0
Enter maximum magnitude: 7.0
Events within the specified time period and magnitude range:
[0] Event: 1, Time: 2020-01-02T12:34:56, Magnitude: 5.5, Latitude: -10.0, Longitude: 110.0, Depth: 10.0
...
Enter the index number of the event you want to choose: 0
Selected Event: (1, UTCDateTime(2020, 1, 2, 12, 34, 56), 5.5, -10.0, 110.0, 10.0)
Enter phase name: P
Enter network name: IU
Enter station name: ANMO
```

### Important Notes

- Ensure that the CSV file path and the station/network details are correct.
- The script assumes that the CSV file does not contain a header row or that the header is skipped using `next(reader)`.
- Adjust the time window for waveform data retrieval (`start_time` and `end_time`) as needed.
- The script uses the `iasp91` model for travel time calculations. You can change this to another model if needed.

### License

This project is licensed under the MIT License. See the LICENSE file for details.

### Contributions

Contributions are welcome. Please open an issue or submit a pull request for any improvements or bug fixes.

### Acknowledgements

This script uses the `obspy` library, which is an open-source project for processing seismological data. Thank you to the developers and contributors of `obspy`!
