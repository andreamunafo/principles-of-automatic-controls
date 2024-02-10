"""
Jupyter Notebook Translation Script

This script is used to translate Jupyter Notebook (.ipynb) files from English to a specified language.
It keeps the code cells and HTML tags unaltered, only translating markdown cells.

Note: this script uses the `conda environment jupyter_translate`

Usage:
1. To translate a single notebook file:
   python jupyter_translate.py translate --fname="path/to/notebook.ipynb" --language="it"

2. To translate all notebooks in a directory:
   python jupyter_translate.py translate_all --directory="path/to/notebooks/folder" --language="it"

For example, if you run it inside the `principles-of-automatic-controls` folder:
   python jupyter_translate.py translate_all --directory='./nbs/' --language="it"



Parameters:
- fname: File path of the notebook to be translated (used for single file translation).
- directory: Path to the folder containing notebook files (used for translating all notebooks in the folder).
- language: Target language for translation, e.g., 'it' for Italian.

The translated notebooks are saved in a subfolder named after the language code (e.g., 'IT' for Italian) 
within the same directory as the original notebook. The filenames are appended with '_<language>'.
"""

import json, os, re, glob
from googletrans import Translator
from tqdm import tqdm

def update_image_paths_in_markdown(text):
    IMG_TAG_REGEX = r'(<img [^>]*src=")\./(pics/[^"]+")'
    return re.sub(IMG_TAG_REGEX, r'\1../\2', text)

def translate_markdown(text, dest_language='it'):
    HTML_TAG_REGEX = '<[^>]+>'
    translator = Translator()
    
    html_tags = re.findall(HTML_TAG_REGEX, text)
    text = re.sub(HTML_TAG_REGEX, 'xx_html_tag_xx', text)

    translated_text = translator.translate(text, dest=dest_language).text

    for tag in html_tags:
        translated_text = translated_text.replace('xx_html_tag_xx', tag, 1)

    return translated_text

def jupyter_translate(fname, language='it'):
    try:
        data = json.load(open(fname, 'r'))
        for cell in tqdm(data['cells'], desc=f"Translating {os.path.basename(fname)}", leave=False):
            if cell['cell_type'] == 'markdown':
                updated_text = update_image_paths_in_markdown(''.join(cell['source']))
                cell['source'] = translate_markdown(updated_text, dest_language=language)

        dest_folder = os.path.join(os.path.dirname(fname), language.upper())
        os.makedirs(dest_folder, exist_ok=True)
        base_name, ext = os.path.splitext(os.path.basename(fname))
        dest_fname = os.path.join(dest_folder, f"{base_name}_{language}{ext}")

        with open(dest_fname, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"The {language} translation has been saved as {dest_fname}")
    except Exception as e:
        print(f"Error translating file {fname}: {e}")
        return False

    return True

def translate_all_notebooks(directory, language='it'):
    files = glob.glob(os.path.join(directory, '**/*.ipynb'), recursive=True)
    for filepath in tqdm(files, desc="Translating Notebooks in Folder", leave=False):
        jupyter_translate(filepath, language)

if __name__ == '__main__':
    print('jupyter_translate')
    import fire
    fire.Fire({
        'translate': jupyter_translate,
        'translate_all': translate_all_notebooks
    })
