import os

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

CONVERTED_DIR = "%s/converted" % CURRENT_DIRECTORY

TEMP_DIR = '/tmp'

IPFS_NODE_URL = "https://ipfs.io/ipfs"

LOG_LEVEL = 'info'
LOG_FORMAT = '{asctime}#{levelname}#{filename}#{funcName}#{lineno}#{message}'
LOG_COLOR = True

IPFS_CONNECT_TIMEOUT = 10
IPFS_TRANSMIT_CONNECT_TIMEOUT = 10

SUPPORTED_FILE = {
    'word': 'docx',
    'html': 'html'
}
