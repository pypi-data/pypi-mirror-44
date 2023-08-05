# Installing the extension manually


**Register the Jupyter server extension** which will communicate both with openBIS and the notebook:

```
jupyter serverextension enable --py jupyter-openbis-extension
```

**Register the notebook extension**, the client side of the Jupyter notebook, which will communicate with the server extension via AJAX calls:

```
 jupyter nbextension install --py jupyter-openbis-extension --user
```
If you are developing, you should consider creating a link to the JavaScript source instead:

```
 jupyter nbextension install --py jupyter-openbis-extension --user --symlink
```

Finally, activate the notebook extension.

```
jupyter nbextension enable jupyter-openbis-extension --user --py
``` 


## Manual installation (if above should fail)

### Install the Python module(s)
- clone the project: 
```
git clone git@sissource.ethz.ch:sispub/jupyter-openbis-extension.git
```
- cd into the extension `cd jupyter-openbis-extension`
- install the python module normally: `pip install .`
- or, for development, install just a symbolic link: `pip install -e .`
- this extension needs Jupyter and pyBIS 1.7.2 in order to run, so it will load / upgrade it if not yet present
- the jupyter-openbis-extension needs at least Python 3.3 in order to run. Therefore, your Jupyter notebook server (but not the kernel!) needs to run under at least Python 3.3 too.

### Register the Jupyter Notebook Server Extension (server-side, as the name suggests)
- in the terminal, enter the following:

``
jupyter serverextension enable --py jupyter-openbis-extension
``

- OR (1) register it manually:
- open the file `~/.jupyter/jupyter_notebook_config.py`
- add the following:

```
c.NotebookApp.server_extensions = [
    'jupyter-openbis-extension.server'
]
```

- OR (2) register it in `~/.jupyter/jupyter_notebook_config.json` manually, if the automatic registration fails for some reasons:
```
{
  "NotebookApp": {
    "nbserver_extensions": {
      "jupyter-openbis-extension.server": true
    }
  }
}
```

### Register the Jupyter Notebook Extension (client-side)

Inside the folder `~/Library/Jupyter/nbextension/` (Mac OS X) create a symbolic **link to the folder that contains the Java Script**:

```
ln -s /path/to/jupyter-openbis-extension/nbextension/dialog.js jupyter-openbis-extension
```
In the file `~/.jupyter/nbconfig/notebook.json` the JavaScript gets activated like this:

```
{
  "load_extensions": {
    "jupyter-openbis-extension/dialog": true
  }
}
```
**Check** that the nbextension has been installed and activated:

```
$ jupyter nbextension list
Known nbextensions:
  config dir: /Users/your-username/.jupyter/nbconfig
    notebook section
      jupyter-openbis-extension/dialog  enabled 
      - Validating: OK
```
