#!/usr/bin/python
from classes.exceptions import *
from classes.utils import DocumentReplace
from docx import Document
from subprocess import call
from config import *
from classes.utils import *
import logging
import pdfkit


class PdfFactory(object):
    def factory(type ):
        if type =="html": return HtmlDocument
        if type =="docx": return WordDocument

    factory = staticmethod(factory)


class WordDocument(IPFS, PdfFactory):

    def __init__(self, hash_key , replace_tags = None):
        self.extension = "docx"
        super(WordDocument, self).__init__(hash_key=hash_key , replace_tags=replace_tags)


    def _replace_tags(self ):
        replace_tags = self.replace_tags
        if os.path.isfile(self.downloaded_file_path):
            logging.debug('start open the document: %s.docx'%self.downloaded_file_path)
            doc = Document(self.downloaded_file_path)
            replace = DocumentReplace(doc)
            if replace_tags:
                logging.debug('start replacing tags: %s.docx'%self.downloaded_file_path)

                # for key in replace_tags:
                replace.paragraph_replace(replace_tags)

            doc.save(self.converted_file_path)
            logging.debug('file has been saved in: %s/%s.docx'%(CONVERTED_DIR,self.encoded_hash))
        else:
            raise NotFoundException("Docx file %s.%s not found"%(self.extension,self.encoded_hash))

    def _doc_pdf(self):
        logging.info("start pdf:%s"%self.converted_file_path)

        if os.path.isfile(self.converted_file_path):
            script =  '../doc2pdf.sh %s %s'%(self.converted_file_path , CONVERTED_DIR)
            result = call(script, shell=True )
            if result == 0:
                logging.info("PDF file saved successfully")
                return self.encoded_hash
            else:
                err_message = "Bash script error in saving PDF file with hash %s"%self.encoded_hash
                logging.error(err_message)
                raise BashScriptException(err_message)
        else:
           raise NotFoundException("Docx File %s.%s not found"%(self.encoded_hash , self.extension))

    # This is the method that will called by the factory.
    def generate(self):
        self.download_ipfs_document()
        self._replace_tags()
        self._doc_pdf()

class HtmlDocument(IPFS,PdfFactory):
    def __init__(self, hash_key , replace_tags = None):
        self.extension = "html"
        super(HtmlDocument, self).__init__(hash_key=hash_key , replace_tags=replace_tags)

    def _replace_tags(self):

        with open(self.downloaded_file_path , "r") as file:
            data = file.read()

        if self.replace_tags:
            pattern = re.compile('|'.join(self.replace_tags.keys()))
            data = pattern.sub(lambda m:self.replace_tags[m.group(0)], data)

        with open(self.converted_file_path , "w") as file:
            file.write(data)

    # This is the method that will called by the factory.
    def generate(self):
        self.download_ipfs_document()
        self._replace_tags()

        pdfkit.from_file(self.converted_file_path, self.pdf_file_path)