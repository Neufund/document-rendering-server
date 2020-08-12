import os

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

CONVERTED_DIR = "%s/converted" % CURRENT_DIRECTORY

LOG_LEVEL = 'DEBUG'
LOG_FORMAT = '{asctime}#{levelname}#{filename}#{funcName}#{lineno}#{message}'
LOG_COLOR = True

IPFS_CACHE_DIR = "%s/ipfs_cache" % CURRENT_DIRECTORY
SERVER_IP = os.environ.get('SERVER_IP')
IPFS_PORT = os.environ.get('IPFS_PORT')

IPFS_CONNECT_TIMEOUT = 10
IPFS_TRANSMIT_CONNECT_TIMEOUT = 10

SUPPORTED_FILE_TYPES = ['word', 'html']

DOCUMENT_RENDERING_OPTIONS = {
    'html': {'page-size': 'Letter', 'dpi': 300},
    'word': {}
}
