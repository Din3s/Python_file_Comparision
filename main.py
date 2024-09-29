
import os
import pandas as pd

# Specify the folder path
folder_path = r'C:\repo\umf-models\01 UMF Models\01 WTG\CubePower\V2_CubePower_BV2023_26'  # Replace with the path to the folder

# Specify the file extensions to filter (e.g., .c, .cpp, .h)
extensions = ['.c', '.cpp', '.h', '.C']

# Get the list of file names in the folder
#file_names = [file for file in os.listdir(folder_path) if os.path.splitext(file)[1] in extensions]

# Get the list of file names in the folder, excluding files ending with '_inc.h'
file_names = [file for file in os.listdir(folder_path)
              if os.path.splitext(file)[1] in extensions and not file.endswith('_inc.h')]

# Create a DataFrame from the list of file names
df = pd.DataFrame(file_names, columns=['File Name'])

# Write the DataFrame to an Excel file
excel_path = r'C:\Users\dinra\OneDrive - Vestas Wind Systems A S\Documents\Test\file_list.xlsx'  # You can specify the desired path for the Excel file
df.to_excel(excel_path, index=False)

# Write the filtered file names to a text file
txt_path = r'C:\Users\dinra\OneDrive - Vestas Wind Systems A S\Documents\Test\filtered_file_list.txt'  # Specify the desired path for the text file
with open(txt_path, 'w') as f:
    for file_name in file_names:
        f.write(file_name + '\n')  # Write each file name on a new line

print(f"Filtered file names have been written to {excel_path} and {txt_path}")
