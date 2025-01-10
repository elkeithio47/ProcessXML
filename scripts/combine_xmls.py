import os
from lxml import etree  # Robust XML parser

# Directory to start the search
root_directory = "C:\\GIT\\automate\\qa\\Processes"
output_directory = "C:\GIT\\automate\\qa\\Processes\\000_output"
word_limit = 10000  # Word limit for each combined file

# Function to count words in an XML element
def count_words(element):
    return sum(len(el.text.split()) for el in element.iter() if el.text)

# Function to save a combined XML tree
def save_combined_file(root, file_count):
    output_file = os.path.join(output_directory, f"combined_output_{file_count}.txt")
    tree = etree.ElementTree(root)
    with open(output_file, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True, pretty_print=True)
    print(f"File saved: {output_file}")

# Function to clean invalid characters in XML content
def clean_xml(file_path):
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    # Replace known invalid characters or entities if needed
    content = content.replace("&", "&amp;")  # Example: Replace standalone '&'
    return content

# Create output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Initialize variables
file_count = 1
current_word_count = 0
current_root = etree.Element("Root")  # Change the tag name if needed

# Traverse all directories and subdirectories
for dirpath, dirnames, filenames in os.walk(root_directory):
    for file in filenames:
        if file.endswith(".xml"):  # Only process XML files
            file_path = os.path.join(dirpath, file)
            try:
                # Preprocess and clean the XML file
                content = clean_xml(file_path)
                root = etree.fromstring(content)
                
                # Count words in the current file
                file_word_count = count_words(root)
                
                # Check if adding this file exceeds the word limit
                if current_word_count + file_word_count > word_limit:
                    # Save the current combined file
                    save_combined_file(current_root, file_count)
                    # Reset variables for the next file
                    file_count += 1
                    current_word_count = 0
                    current_root = etree.Element("Root")
                
                # Add the current file's content to the combined root
                current_root.append(root)
                current_word_count += file_word_count
            
            except etree.XMLSyntaxError as e:
                print(f"Error parsing file {file_path}: {e}")
                continue  # Skip this file and move to the next

# Save the last combined file if any content remains
if len(current_root) > 0:
    save_combined_file(current_root, file_count)
