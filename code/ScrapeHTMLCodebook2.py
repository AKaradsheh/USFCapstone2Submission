import os
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import warnings

# Suppress the deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning)


# Function to append text to a file
def append_to_file(filename, text):
    with open(filename, 'a') as file:
        file.write(text + '\n')


# Specify the folder containing the HTML files
folder_path = '../data'  #'./NHANESData/NHANES/data_docs/2003-2004a' '../data/data_docs/2003-2004a'

# Create a list to store the data
all_data = []
os.makedirs('data', exist_ok=True)
# Define the output file to save a note
output_file = os.path.join('data', 'output_file')

# Iterate through all HTM files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.htm'):
        file_path = os.path.join(folder_path, filename)


        # Read the HTML file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Parse the HTML content
        soup = BeautifulSoup(content, 'html.parser')

        # Find the Codebook section
        codebook_section = soup.find('a', href='#Codebook')
        if codebook_section:
            codebook_links = codebook_section.find_next('div', id='CodebookLinks')
            if codebook_links:
                # Extract each item from the Codebook links
                for item in codebook_links.find_all('li'):

                    link = item.find('a')
                    if link:
                        all_data.append({
                            'File': filename,
                            'Variable': link['href'].lstrip('#'),
                            'Description': link.text.strip()

                        })
                        # print the file name to output
        append_to_file(output_file, f"File name that was parsed: {filename}")


# Create a DataFrame from the collected data
df = pd.DataFrame(all_data)
print(df.head())

# Save the DataFrame to an csv file
csv_path = '../data/justdemofile.csv'
df.to_csv(csv_path, index=False)

print(f"Data has been saved to {csv_path}")
print(f"Number of items extracted: {len(all_data)}")
# Append the results to the file
append_to_file(output_file, f"Number of items extracted from .htm files: {len(all_data)}")

