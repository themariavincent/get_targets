import csv
from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
import astropy.units as u
import os

# Configure Simbad to include imp data fields
Simbad.add_votable_fields('main_id', 'ra', 'dec', 'G', 'J', 'H', 'K')

# first import the survey data
survey_dir = os.path.join(os.path.dirname(__file__))
ophiuchus = os.path.join(survey_dir, 'ODISEA_I.tsv')


def read_tsv_ignore_comments(filepath):
    with open(filepath, 'r') as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter='\t')
        data = [row for row in tsvreader if row and not row[0].startswith('#')]  # Check if row is not empty
    return data


# read files in
data_ophiuchus = read_tsv_ignore_comments(ophiuchus)[3:]
hd_ophiuchus = read_tsv_ignore_comments(ophiuchus)[:3]

# Define empty lists
names = []
ra = [row[0] for row in data_ophiuchus]
dec = [row[1] for row in data_ophiuchus]
G_mags = []
J_mags = []
H_mags = []
K_mags = []
print(len(ra))


# Function to get Simbad identifier from RA and Dec
failed_queries = []  # List to store failed RA/Dec queries


def resolve_to_simbad_id(ra, dec):
    try:
        result = Simbad.query_region(SkyCoord(ra=float(ra), dec=float(dec), unit=(u.deg, u.deg), frame='icrs'),
                                     radius=5 * u.arcsec)
        if result is not None and len(result) > 0:
            return result['main_id'][0]  # Return the first resolved identifier
        else:
            print(f"⚠️ No results found for RA={ra}, Dec={dec}")
            failed_queries.append((ra, dec))  # Store failed queries
            return None
    except Exception as e:
        print(f"Error resolving RA={ra}, Dec={dec}: {e}")
        failed_queries.append((ra, dec))  # Store failed queries
        return None


# Save all failed queries at the end for added verification
def save_failed_queries(filename=(os.path.join(survey_dir, "failed_queries_ODISEA.txt"))):
    with open(filename, "w") as f:
        for failed in failed_queries:
            f.write(f"{failed[0]} {failed[1]}\n")
    print(f"\nFailed queries saved to {filename}")


# # Uncomment to test the function
# print(resolve_to_simbad_id(ra[0], dec[0]))
# print(resolve_to_simbad_id(ra[1], dec[1]))


# Query Simbad for names and magnitudes using resolved identifiers in a batch
resolved_ids = [resolve_to_simbad_id(ra[i], dec[i]) for i in range(len(ra))]
names = resolved_ids

save_failed_queries()  # Save failed queries to a file

try:
    result_table = Simbad.query_objects(resolved_ids)  # Batch query
    if result_table is not None:
        G_mags = result_table['G'].filled(None).tolist()
        J_mags = result_table['J'].filled(None).tolist()
        H_mags = result_table['H'].filled(None).tolist()
        K_mags = result_table['K'].filled(None).tolist()
    else:
        print("Batch query returned no results.")
        G_mags, J_mags, H_mags, K_mags = [None] * len(ra), [None] * len(ra), [None] * len(ra), [None] * len(ra)
except Exception as e:
    print(f"Error querying Simbad: {e}")

# Uncomment to test the function
print(names[-1], G_mags[-1], J_mags[-1], H_mags[-1], K_mags[-1])


# From this list, save a new list of 2MASS names and magnitudes to a new file where the magnitudes are below a certain limit
# define limits
G_limit = float(input("Enter the G magnitude limit: "))
H_limit = float(input("Enter the H magnitude limit: "))

# Get new list of names and magnitudes
new_list = []
for i in range(len(names)):
    if H_mags[i] < H_limit:
        new_list.append((names[i], ra[i], dec[i], G_mags[i], J_mags[i], H_mags[i], K_mags[i]))

# Write the new list to a file
with open(os.path.join(survey_dir, 'ophiuchus_odisea_sources_rev.txt'), 'w') as file:
    for item in new_list:
        file.write(f"{item[0]} {item[1]} {item[2]} {item[3]} {item[4]} {item[5]} {item[6]}\n")
print("New file 'ophiuchus_odisea_sources_revs.txt' created successfully.")
# print(new_list)


# print(ra[0], dec[0])
# print(ra[1], dec[1])