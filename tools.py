#!/usr/bin/python

from docx import Document
from requests import get
import re
from subprocess import call
from config import *
import logging
class DocumentReplace:
    def __init__(self , doc):
        self.doc = doc

    def paragraph_replace(self, tags_dic):
        pattern = re.compile('|'.join(tags_dic.keys()))
        result = [pattern.sub(lambda m:tags_dic[m.group(0)], paragraph.text) if paragraph.text else None for paragraph in self.doc.paragraphs]

        for i in range(len(self.doc.paragraphs)):
            self.doc.paragraphs[i].text = result[i]

class Manager:
    def __init__(self, hash):
        self.hash = hash

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
            raise FileNotFoundError("Docx file %s.docx not found"%self.hash)

    def doc_pdf(self):
        input_filename = '%s/%s.docx'%(CONVERTED_DIR,self.hash)

        if os.path.isfile(input_filename):
            result = call('./doc2pdf.sh %s'%(input_filename), shell=True )
            if result == 0:
                logging.info("PDF file saved successfully")
            else:
                err_message = "Bash script error in saving PDF file with hash %s"%self.hash
                logging.error(err_message)
                raise IOError(err_message)
        else:
           raise FileNotFoundError("Docx File %s.docx not found"%self.hash)

    def _is_document_pinned(self):
        cmd = 'ssh %s docker exec -i %s ipfs pin ls %s'%(SSH_USER , DOCKRE_ID , self.hash)
        return call(cmd.split(" ")) == 0

    def download_ipfs_document(self):
        if not self._is_document_pinned(): raise FileExistsError('You don\'t have permission to access.')

        url = '%s/%s'%(IPFS_NODE_URL,self.hash)
        file_name = "%s/%s.docx"%(DOWNLOADS_DIR,self.hash)
        logging.debug('start Download IPFS document: %s'%self.hash)
        with open(file_name , "wb") as file:
            logging.debug('Save IPFS document in file: %s'%file_name)
            response = get(url)
            if response.status_code == 200:
                file.write(response.content)
            else:
                raise FileNotFoundError("Hash %s Not Found in ipfs"%self.hash)
