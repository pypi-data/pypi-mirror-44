# nbprogress

Progressbar for Jupyter notebooks packaged as a pip package. (ref: https://github.com/kuk/log-progress)

Important to enable enable ipythonwidgets by running
```sh
jupyter nbextension enable --py widgetsnbextension
```

for jupyterlab
```sh
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

Use:
```sh
pip install nbprogress
```
```Python
import time
import nbprogress
for i in nbprogress.log(ranger(1,10), every=1):
    time.sleep(1)
```
![gifs/nbprogress1.gif](gifs/nbprogress1.gif)

```Python
import os
import glob
import time
import nbprogress

input_dir = os.getcwd()
files = glob.glob(os.path.join(input_dir, '*'))

for file in nbprogress.log(enumerate(files), every=1, size=len(files)):
    time.sleep(1)
```
![gifs/nbprogress12.gif](gifs/nbprogress2.gif)