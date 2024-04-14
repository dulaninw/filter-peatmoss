import csv
import json
import os

# set the directory containing CSV files
csv_directory = ''
json_directory = ''

if not os.path.exists(json_directory):
    os.makedirs(json_directory)

# Loop through every file in the directory
for filename in os.listdir(csv_directory):
    if filename.endswith('.csv'):
        csv_file_path = os.path.join(csv_directory, filename)
        json_file_path = os.path.join(json_directory, filename[:-4] + '.json')

        # initialize a list to store CSV data as dictionary
        data = []
        
        try:
            # read the CSV and add data to a list of dictionaries
            with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    data.append(row)

            # write data to a JSON file
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, indent=4)

            print(f"{filename} converted to JSON.")

        except Exception as e:
            print(f"Failed to convert {filename}. Error: {str(e)}")

print("All files have been processed.")
