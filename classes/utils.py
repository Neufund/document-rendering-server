#!/usr/bin/python
import json
import logging
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
            self.ipfs = ipfsapi.connect(SERVER_IP, IPFS_PORT,
                                        timeout=(IPFS_TRANSMIT_CONNECT_TIMEOUT, IPFS_CONNECT_TIMEOUT))

        function_return = func(self)

        return function_return

    return connection


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
            raise UndefinedIPFSHashException('%s is invalid IPFS Hash, should be string' % self.hash)

    # Check if the document is pinned in the ipfs server
    @ipfs_connect
    def _is_document_pinned(self):
        pin_files = self.ipfs.pin_ls()
        return self.hash in list(pin_files['Keys'].keys())

    @ipfs_connect
    def download_ipfs_document_into_cache(self):
        """
        - Download ipfs document into cache folder
        """
        if not self._is_document_pinned():
            logging.error("%s document is not pinned in the ipfs and the user had permission denied." % self.hash)
            raise AccessDeniedException('You don\'t have permission to access.')

        content = self.ipfs.cat(self.hash)
        logging.debug('start Download IPFS document: %s' % self.hash)
        temp = tempfile.NamedTemporaryFile(prefix='document_', dir=IPFS_CACHE_DIR, delete=False)

        with temp:
            temp.write(content)

        # Check if file extention is the same in requested
        self._check_file_extention(temp.name)

        # Rename the IPFS file to hash
        IPFS_file_path = '%s/%s' % (IPFS_CACHE_DIR, self.hash)

        # Rename the cached file to ipfs file name
        os.rename(temp.name, IPFS_file_path)

        return IPFS_file_path

    def _check_file_extention(self, file_path):
        file_type = magic.from_file(file_path)

        logging.debug("File type is %s" % file_type)

        if not file_type:
            os.remove(file_path)
            raise UnKnownFileTypeException("Unknown file")

        checked_file_extension = [file for file in SUPPORTED_FILE_TYPES if file in file_type.lower()]
        if len(checked_file_extension) == 0:
            os.remove(file_path)
            raise UnSupportedFileException("%s Unsupported file type" % file_type)

        if self.extension != checked_file_extension[0]:
            os.remove(file_path)
            raise UnSupportedFileException("This document is %s and you assume it as %s" % (file_type, self.extension))
