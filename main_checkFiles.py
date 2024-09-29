import os
from collections import Counter


# Function to compare the content of two files line by line
def compare_file_contents(file_A, file_B):
    try:
        with open(file_A, 'r', encoding='utf-8') as fA, open(file_B, 'r', encoding='utf-8') as fB:
            file_A_lines = fA.readlines()
            file_B_lines = fB.readlines()
            differences_count = 0
            result_file.write(f"{file_A}: **Comparing with** :{file_B}\n")
            if file_A_lines == file_B_lines:
                return True, None  # Files are identical
            else:
                differences = []
                for i, (line_A, line_B) in enumerate(zip(file_A_lines, file_B_lines), 1):
                    if line_A != line_B:
                        differences_count += 1
                        # differences.append(f"Line {i}: Folder_A: {line_A.strip()} | Folder_B: {line_B.strip()}")

                # Check for extra lines in file_A
                if len(file_A_lines) > len(file_B_lines):
                    for i in range(len(file_B_lines) + 1, len(file_A_lines) + 1):
                        differences_count += 1
                        # differences.append(f"Line {i}: Folder_A: {file_A_lines[i - 1].strip()} | Folder_B: (No line)")
                # Check for extra lines in file_B
                elif len(file_B_lines) > len(file_A_lines):
                    for i in range(len(file_A_lines) + 1, len(file_B_lines) + 1):
                        differences_count += 1
                        # differences.append(f"Line {i}: Folder_A: (No line) | Folder_B: {file_B_lines[i - 1].strip()}")

                return False, differences_count  # Files are different with detailed differences
    except Exception as e:
        return False, [f"Error comparing files: {str(e)}"]


# Function to get all file names in a directory including subdirectories

def get_all_files(directory):
    base_names = []  # List to store the base names (file names)
    full_paths = []  # List to store the full paths (directory + file name)

    for root, _, files in os.walk(directory):
        for file in files:
            base_names.append(os.path.basename(file))  # Append just the file name
            full_paths.append(os.path.join(root, file))  # Append the full path

    return base_names, full_paths


# Specify the main folder paths
folder_A = r'C:\Users\dinra\OneDrive - Vestas Wind Systems A S\Documents\EEM_202_softwareUpdate\converter_2024_12'  # Replace with the actual path to Folder_A
folder_B = r'C:\Users\dinra\OneDrive - Vestas Wind Systems A S\Documents\EEM_202_softwareUpdate\converter_2024_10'  # Replace with the actual path to Folder_B

# Path to the file list and results
file_list_path = r'C:\Users\dinra\OneDrive - Vestas Wind Systems A S\Documents\Test\filtered_file_list.txt'
results_path = r'C:\Users\dinra\OneDrive - Vestas Wind Systems A S\Documents\Test\V7vsV2_detailed_comparison_results.txt'

# Get base names and full paths for both directories
base_names_A, full_paths_A = get_all_files(folder_A)
base_names_B, full_paths_B = get_all_files(folder_B)

# Read the list of files from the .txt file
with open(file_list_path, 'r') as file_list:
    files = [line.strip() for line in file_list.readlines()]  # Strip newline characters

file_counter = Counter()
#num_element_A = len(base_names_A)
num = 0
# Create a new .txt file to store comparison results
with open(results_path, 'w') as result_file:
    for file_name in files:
        count_A = base_names_A.count(file_name)
        count_B = base_names_B.count(file_name)
        if file_name in base_names_A and file_name in base_names_B:
            # Compare the files if they exist in both folders
            # Get the index of the file in both base name lists to retrieve the full path
            index_A = base_names_A.index(file_name)
            index_B = base_names_B.index(file_name)
            # file_counter[file_name] += 1
            # Get the corresponding full paths
            path_A = full_paths_A[index_A]
            path_B = full_paths_B[index_B]
            paths_to_filter_A = []
            filtered_path_A=""
            paths_to_filter_B = []
            filtered_path_B = ""
            if count_A > 1:
                result_file.write(f"{count_A}: Files in Folder A\n")
                for i, name in enumerate(base_names_A):
                    if name == file_name:
                        index_A = base_names_A.index(name)
                        path_A = full_paths_A[i]
                        result_file.write(f"{path_A}: \n")
                        paths_to_filter_A.append(path_A)  # Append the full path
                        keywords = ["SharedLibs", "CubePower_Appl", "SharedBlocks"]
                        filtered_path_A = [path for path in paths_to_filter_A if any(keyword in path for keyword in keywords)]
                if filtered_path_A:
                    path_A = filtered_path_A[0]
            if count_B > 1:
                result_file.write(f"{count_B}: Files in Folder B\n")
                for i, name in enumerate(base_names_B):
                    if name == file_name:
                        index_B = base_names_B.index(name)
                        path_B = full_paths_B[i]
                        result_file.write(f"{path_B}: \n")
                        paths_to_filter_B.append(path_B)  # Append the full path
                        keywords = ["SharedLibs", "CubePower_Appl", "SharedBlocks"]
                        filtered_path_B = [path for path in paths_to_filter_B if any(keyword in path for keyword in keywords)]
                if filtered_path_B:
                    path_B = filtered_path_B[0]
            identical, differences = compare_file_contents(path_A, path_B)
            if identical:
                result_file.write(f"{file_name}: **** Identical contents ****\n")
            else:
                result_file.write(f"{file_name}: ---- Different contents ----\n")
                #result_file.write(f"    {differences} : Lines\n")
        else:
            # One or both files are missing
            if not file_name in base_names_A and not file_name in base_names_B:
                result_file.write(f"{file_name}: File not found in both Folders\n")
            else:
                if not file_name in base_names_B:
                    result_file.write(f"{file_name}: Missing in Folder_B\n")
                if not file_name in base_names_A:
                    result_file.write(f"{file_name}: Missing in Folder_A\n")
print(f"Detailed comparison results have been written to '{results_path}'")
