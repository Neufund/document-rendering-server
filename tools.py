#!/usr/bin/python
from exceptions import *
from docx import Document
import re
from subprocess import call
from config import *
import logging
import ipfsapi


class DocumentReplace:
    def __init__(self , doc):
        self.doc = doc

    def paragraph_replace(self, tags_dic):
        pattern = re.compile('|'.join(tags_dic.keys()))
        for paragraph in self.doc.paragraphs:
            if paragraph.text:
                paragraph.text = pattern.sub(lambda m:tags_dic[m.group(0)], paragraph.text)


class Manager:
    def __init__(self, hash):
        self.hash = hash
        self.ipfs = ipfsapi.connect(SERVER_IP, IPFS_PORT , timeout=IPFS_CONNECT_TIMEOUT)

    def replace(self , replace_tags = None):
        path = '%s/%s.docx'%(DOWNLOADS_DIR,self.hash)

        if os.path.isfile(path):
            logging.debug('start open the document: %s.docx'%path)
            doc = Document(path)
            replace = DocumentReplace(doc)
            if replace_tags:
                logging.debug('start replacing tags: %s.docx'%path)

                # for key in replace_tags:
                replace.paragraph_replace(replace_tags)

            doc.save('%s/%s.docx'%(CONVERTED_DIR,self.hash))
            logging.debug('file has been saved in: %s/%s.docx'%(CONVERTED_DIR,self.hash))
        else:
            raise NotFoundException("Docx file %s.docx not found"%self.hash)

    def doc_pdf(self):
        input_filename = '%s/%s.docx'%(CONVERTED_DIR,self.hash)

        if os.path.isfile(input_filename):
            result = call('./doc2pdf.sh %s'%(input_filename), shell=True )
            if result == 0:
                logging.info("PDF file saved successfully")
            else:
                err_message = "Bash script error in saving PDF file with hash %s"%self.hash
                logging.error(err_message)
                raise BashScriptException(err_message)
        else:
           raise NotFoundException("Docx File %s.docx not found"%self.hash)

    def _is_document_pinned(self):
        pin_files = self.ipfs.pin_ls()
        return self.hash in list(pin_files['Keys'].keys())

    def download_ipfs_document(self):
        if not self._is_document_pinned(): raise AccessDeniedException('You don\'t have permission to access.')

        content = self.ipfs.cat(self.hash)
        file_name = "%s/%s.docx"%(DOWNLOADS_DIR,self.hash)
        logging.debug('start Download IPFS document: %s'%self.hash)
        with open(file_name , "wb") as file:
            logging.debug('Save IPFS document in file: %s'%file_name)
            file.write(content)


