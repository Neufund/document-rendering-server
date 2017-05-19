#!/usr/bin/python
import re, json
import ipfsapi
from config import *
from classes.exceptions import *
import logging
import magic

from hashlib import sha1
import tempfile


def ipfs_connect(func):
    def connection(self):
        logging.debug("Start connection with IPFS")

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
        self.check_valid_hash_key()

        self.replace_tags = replace_tags if replace_tags else {}
        self.encoded_hash = sha1((hash_key + json.dumps(self.replace_tags, sort_keys=True)).encode('utf-8')).hexdigest()

        self.converted_file_path = '%s/%s.%s' % (CONVERTED_DIR, self.encoded_hash, self.extension)
        self.pdf_file_path = '%s/%s.pdf' % (CONVERTED_DIR, self.encoded_hash)

        self.IPFS_file = None

    # Check if hash is valid
    def check_valid_hash_key(self):
        if not isinstance(self.hash, str):
            raise UndefinedIPFSHashException('Invalid IPFS Hash')

    # Check if the document is pinned in the ipfs server
    @ipfs_connect
    def _is_document_pinned(self):
        pin_files = self.ipfs.pin_ls()
        return self.hash in list(pin_files['Keys'].keys())

    @ipfs_connect
    def download_ipfs_temp(self):
        """
        - Download ipfs document into temp folder
        - return the function if the file exists
        """

        # If the temp file exists no need to download file
        if os.path.exists('%s/%s' % (TEMP_DIR, self.hash)):
            self.IPFS_file = '%s/%s' % (TEMP_DIR, self.hash)
            logging.info("Skip installing from IPFS, file exists in cache as %s/%s" % (TEMP_DIR, self.IPFS_file))
            self.check_file_extention()
            return None

        if not self._is_document_pinned():
            raise AccessDeniedException('You don\'t have permission to access.')

        content = self.ipfs.cat(self.hash)
        logging.debug('start Download IPFS document: %s' % self.hash)
        temp = tempfile.NamedTemporaryFile(prefix='document_', dir=TEMP_DIR, delete=False)
        with temp as f:
            f.write(content)
            self.IPFS_file = f.name  # Temporary file name

        self.check_file_extention()
        # Rename the IPFS file to hash
        IPFS_file_name = '%s/%s' % (TEMP_DIR, self.hash)
        os.rename(self.IPFS_file, IPFS_file_name)
        self.IPFS_file = IPFS_file_name

    def check_file_extention(self):
        file_type = magic.from_file(self.IPFS_file)

        logging.debug("File type is %s" % file_type)

        if not file_type:
            os.remove(self.IPFS_file)
            raise UnKnownFileTypeException("Unknown file")

        checked_file_extension = [file for file in SUPPORTED_FILE if file in file_type.lower()]
        if len(checked_file_extension) == 0:
            os.remove(self.IPFS_file)
            raise UnSupportedFileException("%s Unsupported file type" % file_type)

        if self.extension != checked_file_extension[0]:
            os.remove(self.IPFS_file)
            raise UnSupportedFileException("This document is %s and you assume it as %s" % (file_type, self.extension))
