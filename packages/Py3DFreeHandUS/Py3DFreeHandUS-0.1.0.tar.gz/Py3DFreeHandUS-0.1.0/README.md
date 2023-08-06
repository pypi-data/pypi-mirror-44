Py3DFreeHandUS
==============

**A Python library for 3D free-hand ultra-sound measurements**.

Folder *Py3DFreeHandUS* contains source code and doc.

HTML doc is in *doc/index.html* or *sphinx/_build/html/index.html*

After installing Anaconda/Miniconda (64-bit), do the following to create a
Conda sandboxed environment and install Py3DFreeHandUS:

*Windows*:

- create a .bat text file (\*) and insert the following content:

```
conda create -n 3dfus python=2.7 libpython msvc_runtime mingw spyder=3.1.4 pyqt --yes
call activate 3dfus
pip install Py3DFreeHandUS --no-cache-dir
call deactivate
pause
```

- double-click on the .bat file.

To run Spyder for the sandboxed environment, just create a .bat text file with
the following content:

```
call activate 3dfus
spyder
```

and double-click on it.

Data files and example scripts are tracked via [Git LFS](https://help.github.com/articles/configuring-git-large-file-storage/). To get the example data:

*Windows*:

- download and install [git](https://git-scm.com/). During installation, you can leave the default checkboxes as they are. Make sure that Git LFS is in the list of components to install.
- create a profile on [GitHub](https://github.com/), if you don't have it already.
- create an empty folder where you want data to be and inside right-click on **Git Bash here**. To download the sample data for the first time, type:

  ```
  git init
  git remote add origin https://github.com/u0078867/Py3DFreeHandUS.git
  git pull origin master
  pause
  ```

  When pulling, you may be requested username and password of your GitHub account. This operation will download both raw library code and samples data; the sample data is under to folder *samples*.

-  Every time you are notified for sample data updates, double-click on *download_sample_data.bat* (created when pulling) to update your local copy.


(\*): to create a .bat file in Windows, create first a .txt file, edit it with
the content indicated, save it and rename it with a .bat extension.


**IMPORTANT NOTE**: this library is under active development.
We do our best to try to maintain compatibility with previous versions.
