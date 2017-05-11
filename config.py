import os

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

DOWNLOADS_DIR = "/Users/mostafa/Documents/dev/neufund/replace_tags/downloads"
CONVERTED_DIR = "/Users/mostafa/Documents/dev/neufund/replace_tags/converted"


IPFS_NODE_URL = "https://ipfs.io/ipfs"

LOG_LEVEL='DEBUG'
LOG_FORMAT= '{asctime}#{levelname}#{filename}#{funcName}#{lineno}#{message}'
LOG_COLOR=True

SERVER_IP = "10.15.1.12"
IPFS_PORT = 5001
IPFS_CONNECT_TIMEOUT = 10

SUPPORTED_FILE= ['docx' , 'html']