import os
from IPython.display import display, HTML, Markdown

def get_notebook_links(notebook_dir='.', exclude_list=None, font_size='16px'):
    """
    Generate HTML links for Jupyter notebooks in the given directory.
    Args:
    notebook_dir (str): Directory containing the Jupyter notebooks.
    exclude_list (list): List of notebook filenames to exclude.
    font_size (str): Font size for the links.
    
    Returns:
    str: HTML string containing the list of notebook links.
    """
    # Default to an empty exclude list if none provided
    if exclude_list is None:
        exclude_list = []
    
    # List all Jupyter Notebooks and filter out the excluded ones
    notebooks = [f for f in os.listdir(notebook_dir) if f.endswith('.ipynb') and f not in exclude_list]
    
    # Create HTML list items for the links
    html_links = [f"<li><a href='{nb}' target='_blank' style='font-size: {font_size};'>{nb}</a></li>"
                  for nb in sorted(notebooks)]
    
    # Combine the list items into a single unordered list
    return f"<ul>{''.join(html_links)}</ul>"

def display_table_of_contents(notebook_dir='.', exclude_list=None, font_size='16px'):
    """
    Display the table of contents for Jupyter notebooks in the given directory.
    Args:
    notebook_dir (str): Directory containing the Jupyter notebooks.
    exclude_list (list): List of notebook filenames to exclude.
    font_size (str): Font size for the links.
    """
    # Generate the HTML for the notebook links
    html_list = get_notebook_links(notebook_dir, exclude_list, font_size)
    
    # Optional: Add additional styling for the display
    style = "<style>ul { list-style-type: circle; } body { font-family: 'Arial'; }</style>"
    
    # Display the Table of Contents title and the list of links
    toc_title = f"<h2 style='font-size: {font_size};'>Notebooks</h2>"
    display(HTML(style + toc_title + html_list))


def display_table_of_contents_markdown(notebook_dir='.', exclude_list=None):
    
    # Generate markdown links
    markdown_links = get_notebook_links(notebook_dir, exclude_list)

    # Display the ToC as markdown
    Markdown('\n'.join(markdown_links))