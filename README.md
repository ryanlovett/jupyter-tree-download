[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ryanlovett/jupyter-tree-download/master)

# jupyter-tree-download
jupyter-tree-download contains:

 - a jupyter server extension that can bundle and compress a directory with zip or tar.
 - a notebook extension that provides a download button in the tree view

![demo](doc/notebook-button.png)

The download is streamed so that it doesn't occupy additional memory or disk
space in the server. Originally based on [nbzip](https://github.com/data-8/nbzip).

Requires either `zip` or `tar` executables. The latter can compress the
download if `gzip`, `bzip2`, or other compression utilities are available.

You can configure the compression type by setting `c.TreeDownload.compression`
in a jupyter_notebook_config.py in one of the config paths from `jupyter
--paths`. The default is "gzip" though you can specify "bzip2", "xz", or any
other compression supported by tar. Alternatively "zip" will create a zip
archive.

# Installation

```
pip install git+https://github.com/ryanlovett/jupyter-tree-download.git
```

The notebook and notebook server extensions are installed automatically.
