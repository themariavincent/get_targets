import csv
from astroquery.simbad import Simbad
import os

# Configure Simbad to include imp data fields
Simbad.add_votable_fields('ra', 'dec', 'G', 'J', 'H', 'K')

# first import the survey data
survey_dir = os.path.join(os.path.dirname(__file__))
taurus = os.path.join(survey_dir, 'Taurus_ClassII.tsv')


def read_tsv_ignore_comments(filepath):
    with open(filepath, 'r') as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter='\t')
        data = [row for row in tsvreader if row and not row[0].startswith('#')]  # Check if row is not empty
    return data


# read files in
data_taurus = read_tsv_ignore_comments(taurus)[3:]
hd_taurus = read_tsv_ignore_comments(taurus)[:3]

# Define empty lists
two_mass_names = ['2MASS '+row[1] for row in data_taurus]
ra = []
dec = []
G_mags = []
J_mags = []
H_mags = []
K_mags = []

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


# Query Simbad for magnitudes using resolved identifiers- individiual
for i, name in enumerate(two_mass_names):
    resolved_id = resolve_to_simbad_id(name)
    if resolved_id:
        try:
            result_table = Simbad.query_object(resolved_id)
            if result_table is not None and len(result_table) > 0:
                ra.append(result_table['ra'][0])
                dec.append(result_table['dec'][0])
                G_mags.append(result_table['G'][0])
                J_mags.append(result_table['J'][0])
                H_mags.append(result_table['H'][0])
                K_mags.append(result_table['K'][0])
            else:
                print(f"No data found in Simbad for {resolved_id} (resolved from {name})")
                ra.append(None)
                dec.append(None)
                G_mags.append(None)
                J_mags.append(None)
                H_mags.append(None)
                K_mags.append(None)
        except Exception as e:
            print(f"Error retrieving data for {resolved_id} (resolved from {name}): {e}")
            ra.append(None)
            dec.append(None)
            G_mags.append(None)
            J_mags.append(None)
            H_mags.append(None)
            K_mags.append(None)
    else:
        print(f"Could not resolve {name} to a Simbad identifier")
        ra.append(None)
        dec.append(None)
        G_mags.append(None)
        J_mags.append(None)
        H_mags.append(None)
        K_mags.append(None)

# # Uncomment lines 99-104 for checks
# print(two_mass_names[2], G_mags[2], J_mags[2], H_mags[2], K_mags[2])
# # Check how many Nones
# print(ra.count(None), dec.count(None), G_mags.count(None), J_mags.count(None), H_mags.count(None), K_mags.count(None))

# From this list, save a new list of 2MASS names and magnitudes to a new file where the magnitudes are below a certain limit
# define limits
G_limit = float(input("Enter the G magnitude limit: "))
H_limit = float(input("Enter the H magnitude limit: "))

# Get new list of 2MASS names and magnitudes
new_list = []
for i in range(len(two_mass_names)):
    if G_mags[i] is not None and H_mags[i] is not None:
        if G_mags[i] > G_limit and H_mags[i] < H_limit:
            new_list.append((two_mass_names[i], ra[i], dec[i], G_mags[i], J_mags[i], H_mags[i], K_mags[i]))

# Write the new list to a file
with open(os.path.join(survey_dir, 'taurus_sources_rev.txt'), 'w') as file:
    for item in new_list:
        file.write(f"{item[0]} {item[1]} {item[2]} {item[3]} {item[4]} {item[5]} {item[6]}\n")
print("New file 'taurus_sources_rev.txt' created successfully.")
# print(new_list)