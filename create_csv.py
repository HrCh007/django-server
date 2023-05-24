import csv

# Sample data
data = [
    ['source_pdf', 'digitized_pdf', 'model_file'],
    ['031.PDF', '031_digitized.PDF', '031.json'],
    
    # Add more rows as needed
]

# Define the CSV file path
csv_file = './master.csv'

# Write the data to the CSV file
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print(f"CSV file '{csv_file}' created successfully.")