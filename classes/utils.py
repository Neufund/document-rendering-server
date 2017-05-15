#!/usr/bin/python
import re, json
import ipfsapi
from config import *
from classes.exceptions import *
import logging
import magic

from hashlib import sha1
import tempfile



class DocumentReplace:
    def __init__(self, doc):
        self.doc = doc

    def paragraph_replace(self, tags_dic):
        pattern = re.compile('|'.join(tags_dic.keys()))
        for paragraph in self.doc.paragraphs:
            if paragraph.text:
                paragraph.text = pattern.sub(lambda m: tags_dic[m.group(0)], paragraph.text)



class IPFS:
    def __init__(self, hash_key, replace_tags=None):
        self.ipfs = ipfsapi.connect(SERVER_IP, IPFS_PORT, timeout=(IPFS_TRANSMIT_CONNECT_TIMEOUT, IPFS_CONNECT_TIMEOUT))

        self.hash = hash_key
        self.check_valid_hash_key()

        self.replace_tags = replace_tags if replace_tags else {}
        self.encoded_hash = "%s_%s" % (
            hash_key, ''.join(e for e in json.dumps(self.replace_tags, sort_keys=True) if e.isalnum()))

        self.encoded_hash = sha1(self.encoded_hash.encode('utf-8')).hexdigest()

        self.converted_file_path = '%s/%s.%s' % (CONVERTED_DIR, self.encoded_hash, self.extension)
        self.pdf_file_path = '%s/%s.pdf' % (CONVERTED_DIR, self.encoded_hash)

        self.temp_file = None

    def check_valid_hash_key(self):
        if not isinstance(self.hash, str):
            raise UndefinedIPFSHashException('Invalid Ipfs Hash')

    def _is_document_pinned(self):
        pin_files = self.ipfs.pin_ls()
        return self.hash in list(pin_files['Keys'].keys())

    def download_ipfs_temp(self):

        # IF the temp file exists no need to download file
        if os.path.exists('%s/%s' % (TEMP_DIR, self.encoded_hash)):
            self.temp_file = '%s/%s' % (TEMP_DIR, self.encoded_hash)
            logging.info("Skip installing from IPFS, file exists in cache as %s/%s"% (TEMP_DIR, self.encoded_hash))
            return None


        if not self._is_document_pinned():
            raise AccessDeniedException('You don\'t have permission to access.')

        content = self.ipfs.cat(self.hash)
        logging.debug('start Download IPFS document: %s' % self.encoded_hash)
        temp = tempfile.NamedTemporaryFile(prefix='document_', dir=TEMP_DIR, delete=False)
        try:
            with temp as f:
                f.write(content)
                self.temp_file = f.name
                file_type = magic.from_file(self.temp_file)
        finally:
            temp.close()

        logging.debug("File type is %s" % file_type)
        if not file_type:
            raise UnKnownFileTypeException("Unknown file")

        checked_file_extension = None
        for file in SUPPORTED_FILE.keys():
            if file in file_type.lower():
                checked_file_extension = SUPPORTED_FILE[file]
                break
        if checked_file_extension is None:
            raise UnSupportedFileException("%s Unsupported file type" % file_type)

        if self.extension != checked_file_extension:
            raise UnSupportedFileException("This document is %s and you assume it as %s" % (file_type, self.extension))

        return None


