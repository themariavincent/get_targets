import csv
from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
import astropy.units as u
import os
import numpy as np

# first import the survey data
survey_dir = os.path.join(os.path.dirname(__file__), 'disk_survey_data')
orion1 = os.path.join(survey_dir, 'SODA_I.tsv')
taurus1 = os.path.join(survey_dir, 'Taurus_ClassII.tsv')


def read_tsv_ignore_comments(filepath):
    with open(filepath, 'r') as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter='\t')
        data = [row for row in tsvreader if row and not row[0].startswith('#')]  # Check if row is not empty
    return data


# read files in
data_orion1 = read_tsv_ignore_comments(orion1)[3:]
hd_orion1 = read_tsv_ignore_comments(orion1)[:3]
data_taurus1 = read_tsv_ignore_comments(taurus1)[3:]
hd_taurus1 = read_tsv_ignore_comments(taurus1)[:3]

# Get relevant columns
# Orion
ra_orion, dec_orion = [row[0] for row in data_orion1], [row[1] for row in data_orion1]
# Taurus
two_mass_names_taurus = [row[1] for row in data_taurus1]


# Function to compare this list with the lists we have

orion_file = os.path.join(os.path.dirname(__file__), 'data_lists', '20250324', 'no_data_objects_orion_20250324_234002.txt')
taurus_file = os.path.join(os.path.dirname(__file__), 'data_lists', '20250324', 'no_data_objects_taurus_20250324_234005.txt')
# Read the files
with open(orion_file, 'r') as file:
    orion_data = file.readlines()
with open(taurus_file, 'r') as file:
    taurus_data = file.readlines()

orion_data_names = [row.split()[1] for row in orion_data]
orion_ra = [row.split()[2] for row in orion_data]
orion_dec = [row.split()[3] for row in orion_data]
taurus_data_names = [row.split()[1] for row in taurus_data]

# Compare the lists
common_taurus = set(two_mass_names_taurus).intersection(taurus_data_names)
print(f"Common Taurus: {common_taurus}")
# Ensure RA values are in .3f format
ra_orion_formatted = [f"{float(ra):.3f}" for ra in ra_orion]
orion_ra_formatted = [f"{float(ra):.3f}" for ra in orion_ra]
# Find common elements
common_orion = set(ra_orion_formatted).intersection(orion_ra_formatted)
print(f"Common Orion: {common_orion}")

print(ra_orion_formatted)
print(orion_ra_formatted)
