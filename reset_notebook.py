import os
import json

def reset_notebook(file_name):
    # Specify the full file path to the Jupyter notebook file
    notebook_file = os.path.join(os.getcwd(), file_name)

    # Read the JSON data from the notebook file
    with open(notebook_file, 'r', encoding='utf-8') as f:
        notebook_data = json.load(f)

    # Get the kernel ID from the notebook data
    for cell in notebook_data['cells']:
        if cell['cell_type'] == 'code':
            kernel_id = cell['metadata'].get('kernel')
            if kernel_id:
                break

    # Kill the kernel using the kernel ID
    os.system(f'jupyter-kernelspec stop {kernel_id}')

    os.system(f'jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace {notebook_file}')
    
    return print(f'{file_name} reseteado!')