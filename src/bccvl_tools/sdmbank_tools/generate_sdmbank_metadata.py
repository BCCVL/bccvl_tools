import os
import sys
import json
import csv
import swiftclient


def generate_csv(container, outfile):
    conn = swiftclient.Connection(
            user=os.environ.get('OS_USERNAME'),
            key=os.environ.get('OS_PASSWORD'),
            authurl=os.environ.get('OS_AUTH_URL'),
            tenant_name=os.environ.get('OS_TENANT_NAME'),
            auth_version=os.environ.get('OS_AUTH_VERSION', '2')
    )


    # Look for projection metatadata json file in the container for species.
    # Each metatadata record is read and insert as a data row in csv file.
    cols = None
    with open(outfile, mode='a') as csv_file:
        csv_writer = csv.writer(csv_file)
        for fdata in conn.get_container(container)[1]:
            if fdata['name'].endswith('proj_metadata.json'):
                obj_tuple = conn.get_object(container, fdata['name'])    
                data = json.loads(obj_tuple[1])

                # Insert column headings only the first time
                if cols is None:
                    cols = data.keys()
                    csv_writer.writerow(cols)
                csv_writer.writerow([data[col] for col in cols])


# Generate a csv file with projection metatadata for species found in the specified container.
def main():
    if len(sys.argv) < 3:
        print "Usage: {} <container_name> <output_csv_file>".format(sys.argv[0])
        exit(-1)
    generate_csv(container=sys.argv[1], outfile=sys.argv[2])

if __name__ == "__main__":
    main()
