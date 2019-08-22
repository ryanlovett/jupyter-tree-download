from notebook.utils import url_path_join as ujoin
from .handlers import TreeDownloadHandler


# Jupyter Extension points
def _jupyter_server_extension_paths():
    return [{
        'module': 'jupyter_tree_download',
    }]


def _jupyter_nbextension_paths():
    return [{
        "section": "tree",
        "dest": "jupyter_tree_download",
        "src": "static",
        "require": "jupyter_tree_download/tree"
    }]


def load_jupyter_server_extension(nbapp):
    web_app = nbapp.web_app
    base_url = web_app.settings['base_url']
    handlers = [
        (ujoin(base_url, 'tree-download'), TreeDownloadHandler),
    ]
    web_app.add_handlers('.*', handlers)
