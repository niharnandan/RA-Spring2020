import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

print('YAY')

notebook_filename = '.\Step1.ipynb'

with open(notebook_filename) as f:
	nb = nbformat.read(f, as_version=4)
	ep = ExecutePreprocessor(timeout=600, kernel_name='python')
	ep.preprocess(nb, {'metadata': {'path': '/'}})
with open('executed_notebook.ipynb', 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)