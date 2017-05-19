import os

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

CONVERTED_DIR = "%s/converted" % CURRENT_DIRECTORY

IPFS_NODE_URL = "https://ipfs.io/ipfs"

LOG_LEVEL = 'DEBUG'
LOG_FORMAT = '{asctime}#{levelname}#{filename}#{funcName}#{lineno}#{message}'
LOG_COLOR = True

TEMP_DIR = "%s/ipfs_cache" % CURRENT_DIRECTORY
SERVER_IP = os.environ['SERVER_IP']
IPFS_PORT = os.environ['IPFS_PORT']

IPFS_CONNECT_TIMEOUT = 10
IPFS_TRANSMIT_CONNECT_TIMEOUT = 10

SUPPORTED_FILE = ['word', 'html']

OPTIONS = {
    'html': {'page-size': 'Letter', 'dpi': 300},
    'word': {}
}
