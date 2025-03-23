from astroquery.simbad import Simbad
import csv
import pandas as pd
import time
from astroquery.simbad import Simbad

# Configure Simbad to include J, H, and K magnitudes
Simbad.add_votable_fields('flux(G)', 'flux(J)', 'flux(H)', 'flux(K)')

# Read the file
with open(f'orion_sources.tsv', 'r') as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter='\t')
    data = list(tsvreader)[46:]

# Define empty lists
two_mass_names = [row[-1] for row in data if len(row) > 0]
G_mags = []
J_mags = []
H_mags = []
K_mags = []

print(two_mass_names)


# Function to resolve 2MASS identifiers to Simbad primary identifiers
def resolve_to_simbad_id(identifier):
    try:
        result = Simbad.query_objectids(identifier)
        if result is not None and len(result) > 0:
            return result[0][0]  # Return the first resolved identifier
        else:
            return None
    except Exception as e:
        print(f"Error resolving {identifier}: {e}")
        return None


# Increase timeout duration
Simbad.TIMEOUT = 300  # Set timeout to 5 minutes

# Configure Simbad to include G, J, H, and K magnitudes
Simbad.add_votable_fields('flux(G)', 'flux(J)', 'flux(H)', 'flux(K)')

# Batch query Simbad for magnitudes using all 2MASS names at once
try:
    result_table = Simbad.query_objects(two_mass_names)  # Batch query
    if result_table is not None:
        G_mags = result_table['FLUX_G'].filled(None).tolist()
        J_mags = result_table['FLUX_J'].filled(None).tolist()
        H_mags = result_table['FLUX_H'].filled(None).tolist()
        K_mags = result_table['FLUX_K'].filled(None).tolist()
    else:
        print("Batch query returned no results.")
        G_mags, J_mags, H_mags, K_mags = [None] * len(two_mass_names), [None] * len(two_mass_names), [None] * len(two_mass_names), [None] * len(two_mass_names)
except Exception as e:
    print(f"Batch query failed: {e}")
    G_mags, J_mags, H_mags, K_mags = [None] * len(two_mass_names), [None] * len(two_mass_names), [None] * len(two_mass_names), [None] * len(two_mass_names)

# print(two_mass_names[2], G_mags[2], J_mags[2], H_mags[2], K_mags[2])

# Check how many Nones
print(G_mags.count(None))
print(J_mags.count(None))
print(H_mags.count(None))
print(K_mags.count(None))

# From this list, save a new list of 2MASS names and magnitudes to a new file where the magnitudes are below a certain limit
# define limits
G_limit = 10
H_limit = 8

print(G_mags)

# Get new list of 2MASS names and magnitudes
new_list = []
for i in range(len(two_mass_names)):
    if G_mags[i] is not None and H_mags[i] is not None:
        if G_mags[i] > G_limit and H_mags[i] < H_limit:
            new_list.append((two_mass_names[i], G_mags[i], J_mags[i], H_mags[i], K_mags[i]))

# Write the new list to a file
with open(f'orion_sources_rev.txt', 'w') as file:
    for item in new_list:
        file.write(f"{item[0]} {item[1]} {item[2]} {item[3]} {item[4]}\n")
