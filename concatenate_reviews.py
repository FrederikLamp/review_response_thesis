import pandas as pd
from pathlib import Path

# Specify the directory path
directory_path = "./Trustpilot_reviews/Annotated_data_csv/"

# Create a Path object for the directory
directory = Path(directory_path)

# Initialize an empty list to store DataFrames
list_of_dfs = []

# Iterate through each file in the directory
for file in directory.iterdir():
    # Check if the file is a CSV file
    if file.suffix == '.csv':
        # Read the CSV file and append its DataFrame to the list
        df = pd.read_csv(file, sep = ';')
        list_of_dfs.append(df)

# Concatenate all DataFrames into a single DataFrame
combined_df = pd.concat(list_of_dfs, ignore_index=True)

# Display or save the combined DataFrame
print(combined_df.head())

#duplicates = combined_df.duplicated(['reply'])

# Drop the 'Unnamed: 0' column if it exists
if 'Unnamed: 0' in combined_df.columns:
    combined_df = combined_df.drop('Unnamed: 0', axis=1)

# Save the combined DataFrame to a new CSV file
combined_df.to_csv('combined_reviews.csv', index=True)
