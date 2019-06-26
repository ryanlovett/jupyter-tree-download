# jupyter-tree-download
jupyter-tree-download provides a button to compress and download a jupyter server folder. The file is streamed so that it doesn't occupy additional memory or disk space on the server. Originally based on nbzip.

Requires executables for either `zip` or `tar`. The latter can compress the download if `gzip`, `bzip2`, or other compression utilities are available.
![demo](doc/demo.gif)

# Installation

```
pip install jupyter-tree-download
```

Then enable the jupyter server and notebook extensions.

```
jupyter serverextension enable --py jupyter-tree-download --sys-prefix
jupyter nbextension    install --py jupyter-tree-download --sys-prefix
jupyter nbextension     enable --py jupyter-tree-download
```
