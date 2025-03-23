import os
from astroquery.eso import Eso
from astroquery.gemini import Observations
from datetime import datetime

def query_sphere(object_names):
    """
    Query the VLT/SPHERE archive for given objects.
    :param object_names: List of astronomical object names.
    :return: Dictionary of query results.
    """
    results = {}
    for object_name in object_names:
        try:
            # Query ESO archive for SPHERE instrument
            result = Eso.query_instrument('sphere', target=object_name)
            
            if result is None or len(result) == 0:
                print(f"No data found for {object_name}")
                results[object_name] = None
            else:
                print(f"Found {len(result)} SPHERE results for {object_name}")
                results[object_name] = result
        
        except Exception as e:
            print(f"Error querying {object_name}: {e}")
            results[object_name] = None
    return results


def query_gpi(object_names):
    """
    Query the Gemini Planet Imager archive for given objects.
    :param object_names: List of astronomical object names.
    :return: Dictionary of query results.
    """
    results = {}
    for object_name in object_names:
        try:
            # Query Gemini archive for GPI instrument
            result = Observations.query_criteria(instrument='GPI', objectname=object_name)
            
            if result is None or len(result) == 0:
                print(f"No data found for {object_name}")
                results[object_name] = None
            else:
                print(f"Found {len(result)} GPI results for {object_name}")
                results[object_name] = result
        
        except Exception as e:
            print(f"Error querying {object_name}: {e}")
            results[object_name] = None
    return results


def main(file_path):
    """
    Main function to query the archives for objects listed in a file.
    :param file_path: Path to the file containing object names.
    """
    
    if not os.path.exists(file_path):
        print(f"File '{file_path}' not found!")
        return
    
    # Read object names from file
    with open(file_path, 'r') as file:
        rows = [line.strip() for line in file if line.strip()]
        object_names = [' '.join(row.split()[:2]) for row in rows]
    if not object_names:
        print("No object names found in the file.")
        return
    
    print("Querying archives for objects...")
    sphere_results = query_sphere(object_names)
    gpi_results = query_gpi(object_names)
    
    # Save the results in a text file
    now = datetime.now().strftime("%Y%m%d_%H%M%S") 
    with open(f"archive_query_results_{now}.txt", "w") as f:
        f.write("SPHERE Results:\n")
        for obj_name, result in sphere_results.items():
            f.write(f"{obj_name}:\n")
            if result:
                for row in result:
                    f.write(f"\t{row}\n")
            else:
                f.write("\tNo data found.\n")
        
        f.write("\n\nGPI Results:\n")
        for obj_name, result in gpi_results.items():
            f.write(f"{obj_name}:\n")
            if result:
                for row in result:
                    f.write(f"\t{row}\n")
            else:
                f.write("\tNo data found.\n")
    # Save the list of objects with no data found
    no_data_objects = [obj_name for obj_name, result in sphere_results.items() if result is None]
    no_data_objects += [obj_name for obj_name, result in gpi_results.items() if result is None]
    with open(f"no_data_objects_{now}.txt", "w") as f:
        for obj_name in no_data_objects:
            f.write(f"{obj_name}\n")

if __name__ == "__main__":
    main(file_path='taurus_sources_rev.txt')
