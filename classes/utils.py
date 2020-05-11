#!/usr/bin/python
import json
import logging
import re
import tempfile
from hashlib import sha1

import ipfsapi
import magic

from classes.exceptions import *
from config import *


def ipfs_connect(func):
    def connection(self):
        logging.debug(
            "Start connection with IPFS Server IP: %s, Port: %s, Transmit connection timeout: %s,"
            " Connection timeout: %s",
            SERVER_IP,
            IPFS_PORT,
            IPFS_TRANSMIT_CONNECT_TIMEOUT,
            IPFS_CONNECT_TIMEOUT)

        if self.ipfs is None:
            self.ipfs = ipfsapi.connect(SERVER_IP, IPFS_PORT)

        function_return = func(self)

        return function_return

    return connection


re_pattern_ipfs_hash = re.compile(r"^Qm[0-9a-zA-Z]+$")


class IPFSDocument:
    def __init__(self, hash_key, replace_tags=None, extension=None):
        self.ipfs = None
        self.extension = extension
        self.hash = hash_key
        self._check_valid_hash_key()

        self.replace_tags = replace_tags or {}
        self.encoded_hash = sha1((hash_key + json.dumps(self.replace_tags, sort_keys=True)).encode('utf-8')).hexdigest()

        self.converted_file_path = '%s/%s.%s' % (CONVERTED_DIR, self.encoded_hash, self.extension)
        self.pdf_file_path = '%s/%s.pdf' % (CONVERTED_DIR, self.encoded_hash)

    # Check if hash is valid
    def _check_valid_hash_key(self):
        if not isinstance(self.hash, str):
            raise InvalidIPFSHashException(self.hash)

        if re_pattern_ipfs_hash.fullmatch(self.hash) is None:
            raise InvalidIPFSHashException(self.hash)

    # Check if the document is pinned in the ipfs server
    @ipfs_connect
    def _is_document_pinned(self):
        pin_files = self.ipfs.pin.ls()
        return self.hash in list(pin_files['Keys'].keys())

    @ipfs_connect
    def download_pinned_ipfs_document_into_cache(self):
        """
        - Download ipfs document into cache folder
        """

        ipfs_cached_file_path = '%s/%s' % (IPFS_CACHE_DIR, self.hash)

        # If the original document exists in the cache, return the path.
        if os.path.exists(ipfs_cached_file_path):
            return ipfs_cached_file_path

        # If the is not pinned in the IPFS node raise access denied exception.
        if not self._is_document_pinned():
            logging.error("%s document is not pinned in the ipfs and the user had permission denied." % self.hash)
            raise AccessDeniedException('You don\'t have permission to access.')

        content = self.ipfs.cat(self.hash)
        logging.debug('Start downloading IPFS document: %s' % self.hash)

        temp_ipfs_cached_file_path = tempfile.NamedTemporaryFile(prefix='document_', dir=IPFS_CACHE_DIR, delete=False)

        # write the content of the downloaded file temporary
        with temp_ipfs_cached_file_path:
            temp_ipfs_cached_file_path.write(content)

        # Check if file extension is the same in requested
        self._check_file_extension(temp_ipfs_cached_file_path.name)

        # Rename the cached file to ipfs file name
        os.rename(temp_ipfs_cached_file_path.name, ipfs_cached_file_path)

        return ipfs_cached_file_path

    def _check_file_extension(self, file_path):
        file_type = magic.from_file(file_path)

        logging.debug("File type is %s" % file_type)

        if not file_type:
            os.remove(file_path)
            raise UnKnownFileTypeException(file_type)

        checked_file_extension = [file for file in SUPPORTED_FILE_TYPES if file in file_type.lower()]
        if len(checked_file_extension) == 0:
            os.remove(file_path)
            raise UnSupportedFileException(file_type)

        if self.extension != checked_file_extension[0]:
            os.remove(file_path)
            raise UnSupportedFileException(file_type)
