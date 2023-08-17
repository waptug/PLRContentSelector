import os
import random
import shutil
import logging
from chardet import detect

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to get the encoding type of a file
def get_encoding_type(file):
    with open(file, 'rb') as f:
        result = detect(f.read())
        return result['encoding']

# Function to convert a file to UTF-8 encoding
def convert_to_utf8(file):
    encoding_type = get_encoding_type(file)
    if encoding_type != 'utf-8':
        try:
            with open(file, 'rb') as f:
                content_bytes = f.read()
            content = content_bytes.decode(encoding_type)
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
        except UnicodeDecodeError:
            logging.warning(f"Unable to convert file {file} to UTF-8. Skipping.")

# Function to get all files from a directory recursively
def get_all_files(directory, extensions=None):
    files_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if extensions is None or file.endswith(tuple(extensions)):
                files_list.append(os.path.join(root, file))
    return files_list

# Ask user for inputs
source_folder = input("Enter the source folder path: ")

# Validate source folder
if not os.path.exists(source_folder):
    logging.error("Source folder does not exist.")
    exit()

extensions = input("Enter file extensions to include (comma-separated, leave blank for all): ").split(',')

num_files_to_pick = input("Enter the number of files to pick: ")

# Validate number of files to pick
try:
    num_files_to_pick = int(num_files_to_pick)
except ValueError:
    logging.error("Invalid number of files.")
    exit()

output_folder = input("Enter the output folder path: ")

# Get all files from the source folder
all_files = get_all_files(source_folder, extensions if extensions[0] else None)

# Validate number of files to pick
if num_files_to_pick > len(all_files):
    logging.error("Number of files to pick is greater than available files.")
    exit()

# Select random files without duplicates
selected_files = random.sample(all_files, num_files_to_pick)

# Create the output folder if it does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# HTML and Markdown content for index.html and readme.md
html_links = []  # List to store HTML links
md_content = "# List of Files\n"

# Copy files to the output folder and convert to UTF-8
for file in selected_files:
    file_name = os.path.basename(file)
    output_file_path = os.path.join(output_folder, file_name)
    shutil.copy(file, output_file_path)
    convert_to_utf8(output_file_path)
    html_links.append(f'<a href="{file_name}">{file_name}</a>')  # Add to HTML links list
    md_content += f"- {file_name}\n"
    logging.info(f"Processed file: {file_name}")

# Sort HTML links alphabetically
html_links.sort()

# Concatenate HTML links with line breaks
html_content = "<html><head><title>Index</title></head><body>" + "<br>".join(html_links) + "</body></html>"

# Write index.html
with open(os.path.join(output_folder, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html_content)

# Write readme.md
with open(os.path.join(output_folder, 'readme.md'), 'w', encoding='utf-8') as f:
    f.write(md_content)

logging.info("Files copied successfully!")