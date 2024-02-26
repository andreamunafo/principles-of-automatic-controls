"""
This script automates the process of preparing a Jupyter Book for publishing by copying image resources, 
prepending page breaks to Jupyter Notebooks, and building the book with images.

The script performs the following tasks:
1. Copies an 'images' directory to a specified location in the Jupyter Book build directory.
2. Prepends each Jupyter Notebook in a specified directory with an HTML page break if not already present.
3. Builds the Jupyter Book using the 'jupyter-book build' command.

Functions:
- prepend_page_break_to_notebook: Adds a page break to the start of a Jupyter Notebook if needed.
- process_all_notebooks: Processes all notebooks in a given directory to add page breaks.
- main: The main function of the script, handling command-line arguments and executing the script's primary logic.

Usage:
Run the script from the command line, optionally passing the path to the directory containing Jupyter Notebooks:
    python <script_name.py> [notebooks_dir]

Where [notebooks_dir] is an optional argument specifying the directory containing the Jupyter Notebooks. 
If not provided, the script uses the project root directory by default.
"""

import os
import shutil
import subprocess
import argparse
import json

def prepend_page_break_to_notebook(notebook_path):
    """
    Prepends a Jupyter Notebook file with an HTML page break if it's not already present at the beginning.

    Args:
    notebook_path (str): The file path of the Jupyter Notebook.

    Returns:
    bool: True if the page break was added, False otherwise.
    """
    with open(notebook_path, 'r', encoding='utf-8') as file:
        notebook = json.load(file)

    page_break_cell = {"cell_type": "raw", "metadata": {}, "source": ["<div style=\"page-break-before: always;\"></div>"]}

    if notebook['cells'] and notebook['cells'][0]['source'] != page_break_cell['source']:
        notebook['cells'].insert(0, page_break_cell)

        with open(notebook_path, 'w', encoding='utf-8') as file:
            json.dump(notebook, file, indent=2)
        return True
    
    return False

def process_all_notebooks(directory):
    """
    Processes all Jupyter Notebook files in a directory to add a page break at the beginning if not present.

    Args:
    directory (str): The directory path to search for Jupyter Notebook files.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.ipynb'):
                notebook_path = os.path.join(root, file)
                if prepend_page_break_to_notebook(notebook_path):
                    print(f"Added page break to: {notebook_path}")

def main():
    parser = argparse.ArgumentParser(description='Copy images to Jupyter Book build directory, prepend page breaks, and build the book with images.')
    
    # Determine the script's current directory and project root
    script_dir = os.path.dirname(os.path.realpath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..'))

    # Make notebooks_dir argument optional and default to project_root
    parser.add_argument("notebooks_dir", nargs='?', default=project_root, type=str, help="The directory containing Jupyter Notebooks for processing page breaks. Defaults to the project root directory.")

    args = parser.parse_args()
 
    # Process notebooks for page breaks
    process_all_notebooks(args.notebooks_dir)

    
    images_src = os.path.join(project_root, 'images')
    images_dest = os.path.join(project_root, '_build', 'html', 'images')

    if not os.path.exists(images_src):
        print("Source 'images' folder not found.")
        return

    print(f"Images will be copied from \n SOURCE: '{images_src}' \n DESTINATION: '{images_dest}'.")
    confirm = input("Do you want to proceed? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Operation cancelled by the user.")
        return

    os.makedirs(images_dest, exist_ok=True)
    shutil.copytree(images_src, images_dest, dirs_exist_ok=True)
    print("Images copied successfully.")

    try:
        subprocess.run(['jupyter-book', 'build', os.path.join(project_root, ''), '--builder', 'pdfhtml'], check=True)
        print("Jupyter Book built successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error in building Jupyter Book: {e}")

if __name__ == "__main__":    
    main()
