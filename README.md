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

- Run the server using uwisgi configuration.

# TODO: Docker installation
