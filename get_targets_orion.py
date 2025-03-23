from astroquery.simbad import Simbad
import csv

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


# Query Simbad for magnitudes using resolved identifiers
for i, name in enumerate(two_mass_names):
    resolved_id = resolve_to_simbad_id(name)
    if resolved_id:
        try:
            result_table = Simbad.query_object(resolved_id)
            if result_table is not None and len(result_table) > 0:
                G_mag = result_table['FLUX_G'][0]
                J_mag = result_table['FLUX_J'][0]
                H_mag = result_table['FLUX_H'][0]
                K_mag = result_table['FLUX_K'][0]
                G_mags.append(G_mag)
                J_mags.append(J_mag)
                H_mags.append(H_mag)
                K_mags.append(K_mag)
                
            else:
                print(f"No data found in Simbad for {resolved_id} (resolved from {name})")
                G_mags.append(None)
                J_mags.append(None)
                H_mags.append(None)
                K_mags.append(None)
        except Exception as e:
            print(f"Error retrieving data for {resolved_id} (resolved from {name}): {e}")
            G_mags.append(None)
            J_mags.append(None)
            H_mags.append(None)
            K_mags.append(None)
    else:
        print(f"Could not resolve {name} to a Simbad identifier")
        G_mags.append(None)
        J_mags.append(None)
        H_mags.append(None)
        K_mags.append(None)

print(two_mass_names)

# print(two_mass_names[2], G_mags[2], J_mags[2], H_mags[2], K_mags[2])

# # Check how many Nones
# print(G_mags.count(None))
# print(J_mags.count(None))
# print(H_mags.count(None))
# print(K_mags.count(None))

# From this list, save a new list of 2MASS names and magnitudes to a new file where the magnitudes are below a certain limit
# define limits
G_limit = 11
H_limit = 8

# Get new list of 2MASS names and magnitudes
new_list = []
for i in range(len(two_mass_names)):
    if G_mags[i] is not None and H_mags[i] is not None:
        if G_mags[i] < G_limit and H_mags[i] < H_limit:
            new_list.append((two_mass_names[i], G_mags[i], J_mags[i], H_mags[i], K_mags[i]))

# Write the new list to a file
with open(f'orion_sources_rev.txt', 'w') as file:
    for item in new_list:
        file.write(f"{item[0]} {item[1]} {item[2]} {item[3]} {item[4]}\n")
