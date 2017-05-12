# Document Rendering Micro Service

- Download documents from Neufund IPFS node
- Replace some tags from the word document with json send by the api.
- export pdf file to the endpoint

# How to use:
- Install python3.4 or higher.
- install libreoffice librrary by the following command:
    Mac users: `brew cask install libreoffice`
- Specify the folder that you need to download the document into it from `config.py` DOWNLOADS_DIR
- Specify the folder that you need to put the replaced files into it from `config.py` CONVERTED_DIR

# Note: Make sure that you have installed all the dependencies.

# How to run
- `python -m server` or is case if uwisgi the configuration is uwisgi.ini 

# How to test
`python -m unittest`

# TODO: Docker installation

