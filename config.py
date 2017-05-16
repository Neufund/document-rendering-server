import os

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

CONVERTED_DIR = "%s/converted" % CURRENT_DIRECTORY
print("CONVERTED: %s" % CONVERTED_DIR)
IPFS_NODE_URL = "https://ipfs.io/ipfs"

LOG_LEVEL = 'DEBUG'
LOG_FORMAT = '{asctime}#{levelname}#{filename}#{funcName}#{lineno}#{message}'
LOG_COLOR = True

TEMP_DIR = '/develop/tmp'
SERVER_IP = os.environ['SERVER_IP']
IPFS_PORT = os.environ['IPFS_PORT']

IPFS_CONNECT_TIMEOUT = 10
IPFS_TRANSMIT_CONNECT_TIMEOUT = 10

SUPPORTED_FILE = {
    'word': 'docx',
    'html': 'html'
}
