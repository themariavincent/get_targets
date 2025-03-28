import pandas as pd
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz, SkyCoord
from astropy import units as u

# Load target data from the CSV
sourcelist = pd.read_csv('./disk_survey_data/S25B-Targets.csv')

# Convert RA and Declination columns into SkyCoord objects
sources = sourcelist['Target']
coords = [SkyCoord(ra * u.deg, dec * u.deg, frame='icrs') 
          for ra, dec in zip(sourcelist['RA'], sourcelist['Decl'])]

# Define the location of the site (example: Mauna Kea, Hawaii)
location = EarthLocation.of_site('Subaru')

# Define the range of dates
start_date = '2025-03-27'
end_date = '2025-03-28'

# Convert the dates to astropy Time objects
times = Time([start_date, end_date])

# Create an AltAz frame to calculate altitudes and azimuths
altaz_frame = AltAz(obstime=times, location=location)

# Loop over each object (target) and calculate its Altitude and Azimuth for the given times
for source, obj in zip(sources, coords):
    altaz = obj.transform_to(altaz_frame)
    
    print(f"Object: {source}")
    print(f"RA, Dec: {obj.to_string('hmsdms')}")
    # Ensure that altitude and azimuth are scalars
    altitude = altaz.alt[0].value  # Access the first value of the altitude
    azimuth = altaz.az[0].value   # Access the first value of the azimuth
    
    print(f"Altitude: {altitude:.2f} degrees, Azimuth: {azimuth:.2f} degrees")

    # Check if any of the altitudes are above the horizon (altitude > 0 degrees)
    if (altaz.alt > 0 * u.deg).any():
        print(f"Object {source} is visible.")
    else:
        print(f"Object {source} is not visible.")
    print()