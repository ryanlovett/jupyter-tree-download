from glob import glob
import setuptools

setuptools.setup(
    name="jupyter-tree-download",
    version='1.0.1',
    url="https://github.com/ryanlovett/jupyter-tree-download",
    author="Ryan Lovett",
    author_email="rylo@berkeley.edu",
    description="Compresses and downloads all files in any of the user's directories.",
    packages=setuptools.find_packages(),
    install_requires=[
        'notebook'
    ],
    package_data={'jupyter-tree-download': ['static/*']},
    data_files=[
        ('share/jupyter/nbextensions/jupyter_tree_download',
            glob('jupyter_tree_download/static/*')),
        ('etc/jupyter/jupyter_notebook_config.d',
            ['jupyter_tree_download/etc/serverextension/jupyter-tree-download.json']),
        ('etc/jupyter/nbconfig/tree.d',
            ['jupyter_tree_download/etc/nbconfig/jupyter-tree-download.json'])
    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: Jupyter',
    ]
)

