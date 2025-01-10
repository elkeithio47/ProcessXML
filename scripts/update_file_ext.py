import os

def change_file_extensions(directory, old_extension, new_extension):
    """
    Change the extension of all files in the specified directory from old_extension to new_extension.

    :param directory: Directory containing the files to rename
    :param old_extension: Current file extension (e.g., '.XML')
    :param new_extension: Desired file extension (e.g., '.TXT')
    """
    # Ensure extensions start with a dot
    if not old_extension.startswith('.'):
        old_extension = '.' + old_extension
    if not new_extension.startswith('.'):
        new_extension = '.' + new_extension

    try:
        for filename in os.listdir(directory):
            if filename.endswith(old_extension):
                base_name = os.path.splitext(filename)[0]
                new_name = base_name + new_extension
                old_path = os.path.join(directory, filename)
                new_path = os.path.join(directory, new_name)
                os.rename(old_path, new_path)
                print(f'Renamed: {filename} -> {new_name}')
        print("All applicable files have been renamed.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Specify the directory containing the files
    target_directory = "C:\\GIT\\automate\\qa\\Processes\\000_output"

    # Change all .XML files to .TXT
    change_file_extensions(target_directory, '.xml', '.txt')
