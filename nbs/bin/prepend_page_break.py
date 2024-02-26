import os
import json
import argparse

def prepend_page_break_to_notebook(notebook_path):
    """
    Prepends a Jupyter Notebook file with an HTML page break.

    This function opens a Jupyter Notebook, checks if the first cell is a page break,
    and if not, inserts a page break cell at the beginning of the notebook.

    Args:
    notebook_path (str): The file path of the Jupyter Notebook.
    """
    with open(notebook_path, 'r', encoding='utf-8') as file:
        notebook = json.load(file)

    # Define the HTML for the page break
    page_break_cell = {"cell_type": "markdown", "metadata": {}, "source": ["<div style=\"page-break-before: always;\"></div>"]}

    # Check if the first cell is already a page break
    if notebook['cells'] and notebook['cells'][0]['source'] != page_break_cell['source']:
        notebook['cells'].insert(0, page_break_cell)

        with open(notebook_path, 'w', encoding='utf-8') as file:
            json.dump(notebook, file, indent=2)

def process_all_notebooks(directory):
    """
    Processes all Jupyter Notebook files in a directory.

    This function walks through all files in the given directory (and its subdirectories),
    finds Jupyter Notebook files, and calls prepend_page_break_to_notebook on each.

    Args:
    directory (str): The directory path to search for Jupyter Notebook files.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.ipynb'):
                notebook_path = os.path.join(root, file)
                prepend_page_break_to_notebook(notebook_path)
                print(f"Processed {notebook_path}")

def main():
    """
    Main function to execute the script.

    This function parses command line arguments for the directory path and
    processes all Jupyter Notebooks in that directory to prepend a page break.
    """
    parser = argparse.ArgumentParser(description="Prepend a page break to each Jupyter Notebook in a specified directory.")
    parser.add_argument("directory", type=str, help="The directory containing Jupyter Notebooks.")
    args = parser.parse_args()

    process_all_notebooks(args.directory)

if __name__ == "__main__":
    main()
