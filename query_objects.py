import os
from astroquery.simbad import Simbad
from datetime import datetime


# Increase timeout duration
Simbad.TIMEOUT = 300  # Set timeout to 5 minutes

def get_info(identifiers, *fields, save_tsv=True):
    """
    Get information from Simbad for a list of identifiers.
    :param identifiers: List of identifiers to query
    :param fields: Fields to retrieve
    :param save_tsv: Save results to a TSV file. Default is True.
    :return: Dictionary of query results.
    """
    results = {}
    Simbad.add_votable_fields(*fields)  # Configure Simbad to include imp data fields

    # Batch query Simbad for magnitudes using all 2MASS names at once
    try:
        result_table = Simbad.query_objects(identifiers)  # Batch query
        if result_table is not None:
            for field in fields:
                results[field] = result_table[field].filled(None).tolist()
        else:
            print("Batch query returned no results.")
            for field in fields:
                results[field] = [None] * len(identifiers)
    except Exception as e:
        print(f"Batch query failed: {e}")
        for field in fields:
            results[field] = [None] * len(identifiers)

    if save_tsv:
        now = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_path = os.path.join(os.path.dirname(__file__), 'query_results', 'simple_query')
        os.makedirs(base_path, exist_ok=True)
        fname = os.path.join(base_path, f"simple_query_results_{now}.tsv")
        with open(fname, 'w') as file:
            file.write('Identifier\t' + '\t'.join(fields) + '\n')
            for i in range(len(identifiers)):
                file.write(identifiers[i] + '\t' + '\t'.join([str(results[field][i]) for field in fields]) + '\n')
            print(f"Results saved to '{fname}'")
    return results


# # Uncomment to test the function
# # Example 1: Query for a list of identifiers
# # import file to get identifiers
# with open('/Users/mariavincent/Documents/prelim_target_list.txt', 'r') as file:
#     identifiers = [line.strip() for line in file if line.strip()]
# # ignore these entries
# identifiers = [id for id in identifiers if id not in
#                [identifiers[0], identifiers[2], identifiers[3], identifiers[15], identifiers[21]]]
# fields = ['ra', 'dec', 'G', 'J', 'H', 'K']  # Fields to retrieve
# results = get_info(identifiers, *fields)
