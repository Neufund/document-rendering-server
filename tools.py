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

    def paragraph_search(self, text_value):
        result = False
        para_regex = re.compile(text_value)
        for paragraph in self.doc.paragraphs:
            if paragraph.text:
                if para_regex.search(paragraph.text):
                    result = True
        return result


    def paragraph_replace(self, search, replace):
        searchre = re.compile(search)
        for paragraph in self.doc.paragraphs:
            paragraph_text = paragraph.text
            if paragraph_text:
                if searchre.search(paragraph_text):
                    self.clear_paragraph(paragraph)
                    paragraph.add_run(re.sub(search, replace, paragraph_text))
        return paragraph


    def clear_paragraph(self, paragraph):
        p_element = paragraph._p
        p_child_elements = [elm for elm in p_element.iterchildren()]
        for child_element in p_child_elements:
            p_element.remove(child_element)


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

                for key in replace_tags:
                    replace.paragraph_replace('{%s}'%key , replace_tags[key])

            doc.save('%s/%s.docx'%(CONVERTED_DIR,self.hash))
            logging.debug('file has been saved in: %s/%s.docx'%(CONVERTED_DIR,self.hash))
        else:
            raise FileNotFoundError("Docx file %s.docx not found"%self.hash)

    def doc_pdf(self):
        input_filename = '%s/%s.docx'%(CONVERTED_DIR,self.hash)

        if os.path.isfile(input_filename):
            call('./doc2pdf.sh %s'%(input_filename), shell=True )
        else:
           raise FileNotFoundError("Docx File %s.docx not found"%self.hash)

    def download_ipfs_document(self):
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
