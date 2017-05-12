#!/usr/bin/python
import re , json
import ipfsapi
from config import *
from classes.exceptions import *
import logging
import magic

class DocumentReplace:
    def __init__(self , doc):
        self.doc = doc

    def paragraph_replace(self, tags_dic):
        pattern = re.compile('|'.join(tags_dic.keys()))
        for paragraph in self.doc.paragraphs:
            if paragraph.text:
                paragraph.text = pattern.sub(lambda m:tags_dic[m.group(0)], paragraph.text)


class IPFS:
    def __init__(self, hash_key , replace_tags = None):
        self.ipfs = ipfsapi.connect(SERVER_IP, IPFS_PORT, timeout=(IPFS_TRANSMIT_CONNECT_TIMEOUT,IPFS_CONNECT_TIMEOUT))

        self.hash = hash_key
        self.check_valid_hash_key()

        self.replace_tags = replace_tags if replace_tags else {}
        self.encoded_hash = "%s_%s"%(hash_key,''.join(e for e in json.dumps(self.replace_tags , sort_keys=True) if e.isalnum()))

        self.downloaded_file_path = '%s/%s.%s' % (DOWNLOADS_DIR, self.encoded_hash, self.extension)
        self.converted_file_path = '%s/%s.%s' % (CONVERTED_DIR, self.encoded_hash, self.extension)
        self.pdf_file_path = '%s/%s.pdf' % (CONVERTED_DIR, self.encoded_hash)


    def check_valid_hash_key(self):
        if not isinstance(self.hash , str):
            raise UndefinedIPFSHashException('Invalid Ipfs Hash')


    def _is_document_pinned(self):
        pin_files = self.ipfs.pin_ls()
        return self.hash in list(pin_files['Keys'].keys())


    def download_ipfs_document(self):
        if not self._is_document_pinned(): raise AccessDeniedException('You don\'t have permission to access.')

        if os.path.isfile(self.downloaded_file_path):
            logging.info('File already exists in %s'%self.downloaded_file_path)
        else:
            content = self.ipfs.cat(self.hash)
            logging.debug('start Download IPFS document: %s' % self.encoded_hash)
            with open(self.downloaded_file_path, "wb") as file:
                logging.debug('Save IPFS document in file: %s' % self.downloaded_file_path)
                file.write(content)

            logging.info("finish saveing file")

        file_type = magic.from_file(self.downloaded_file_path)
        logging.debug("File type is %s"%file_type)
        if not file_type: raise UnKnownFileTypeException("Unknow file")

        supported = False
        cheched_file_extension = None
        for file in SUPPORTED_FILE.keys():
            if file in file_type.lower():
                supported = True
                cheched_file_extension = SUPPORTED_FILE[file]
                break

        if not supported:
            raise UnSupportedFileException("%s Unsupported file type"%file_type)

        if self.extension != cheched_file_extension:
            raise UnSupportedFileException("This document is %s and you assume it as %s" % (file_type, self.extension))



        return self.downloaded_file_path
