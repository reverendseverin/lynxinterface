import csv
from io import StringIO

# Prompt the user for the input CSV file name
input_file_name = input("Enter the input CSV file name: ")

# Read the contents of the input file
with open(input_file_name, "r") as input_file:
    input_csv = input_file.read()

csv_reader = csv.DictReader(StringIO(input_csv))

current_event = None
current_heat = None
output_lines = []

# Loop through each row in the CSV file capturing the event informaiton, boat ID, row and club.
for row in csv_reader:
    event = row['Event']
    heat = row['Heat']
    description = row['Description']
    boat_id = row['Boat ID']
    lane = row['Lane']
    club = row['Boat Name']
    boat_label = row['Boat Labelbo']

    # If the event or heat has changed, add a new row with the event and heat information
    if event != current_event or heat != current_heat:
        current_event = event
        current_heat = heat
        output_lines.append(f'{event},1,{heat},"{description}",,')
        
    # Add a row for each boat with a 4-space indent before the boat_id
    output_lines.append(f'    ,{boat_id},{lane},,,{club}')

# Write the output to a file named 'lynx.evt' - Lynx requires the file be named lynx.evt
with open('lynx.evt', 'w') as output_file:
    output_file.write('\n'.join(output_lines))
