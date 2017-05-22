#!/usr/bin/env python
import logging
import re
import tempfile
from subprocess import call

import pdfkit
from docx import Document

from classes.exceptions import *
from classes.utils import IPFSDocument
from config import *


class PdfFactory(object):
    def factory(type):
        if type == "html":
            return HtmlDocument
        elif type == "word":
            return WordDocument
        else:
            raise UnSupportedFileException("un supported extension")

    factory = staticmethod(factory)


# Decorator : If pdf file exist no need to execute the function.
def skip_file_exists(func):
    def checker(*args):
        file_path = args[0].pdf_file_path
        if os.path.exists(file_path):
            logging.info("The pdf file exists before in path %s" % file_path)
            return file_path

        return func(*args)

    return checker


class WordDocument(IPFSDocument):
    def __init__(self, hash_key, replace_tags=None):
        super(WordDocument, self).__init__(hash_key=hash_key, replace_tags=replace_tags, extension="word")
        self.temp_word_file_with_tags_replaced = None

    def _paragraph_replace(self, tags_dic):
        pattern = re.compile('|'.join(tags_dic.keys()))
        for paragraph in self.doc.paragraphs:
            if paragraph.text:
                paragraph.text = pattern.sub(lambda m: tags_dic[m.group(0)], paragraph.text)

    def _replace_tags(self, word_file_path):
        if os.path.exists(word_file_path):
            logging.debug('opening source word document: %s' % word_file_path)

            self.doc = Document(word_file_path)
            if self.replace_tags:
                logging.debug('start replacing tags: %s' % word_file_path)
                # for key in replace_tags:
                self._paragraph_replace(self.replace_tags)

            temp = tempfile.NamedTemporaryFile(prefix='document_word_', dir=IPFS_CACHE_DIR, delete=False)
            with temp:
                self.temp_word_file_with_tags_replaced = temp.name  # Temporary file name
            logging.debug('temporary file with tags replaces in %s' % self.temp_word_file_with_tags_replaced)

            # Replace the downloaded temp file with the new document with tags.
            self.doc.save(self.temp_word_file_with_tags_replaced)

            logging.debug('file has been saved in: %s/%s' % (CONVERTED_DIR, self.encoded_hash))

            return self.temp_word_file_with_tags_replaced
        else:
            raise NotFoundException("Docx file %s.%s not found" % (self.encoded_hash, self.extension))

    def _word_pdf(self, word_file_path):
        logging.info("start pdf:%s" % word_file_path)

        if os.path.isfile(word_file_path):
            script = '%s/doc2pdf.sh "%s" "%s"' % (CURRENT_DIRECTORY, word_file_path, CONVERTED_DIR)
            logging.debug("Execute script %s" % script)

            # execute bash script doc2pdf using `soffice` command
            result = call(script, shell=True)
            if result == 0:
                logging.info("PDF file saved successfully")
                return self.pdf_file_path
            else:
                err_message = "Bash script error in saving PDF file with hash %s" % self.hash
                raise BashScriptException(err_message)
        else:
            raise NotFoundException("%s File is not found" % (self.encoded_hash))

    # Rename the temp file and the converted file as well, to use as cache files.
    def _rename_files(self):
        # rename the replaced document into encoded hash name
        cached_file_name = os.path.basename(os.path.normpath(self.temp_word_file_with_tags_replaced))
        # rename the pdf file into encoded hash
        os.rename('%s/%s.pdf' % (CONVERTED_DIR, cached_file_name), '%s/%s.pdf' % (CONVERTED_DIR, self.encoded_hash))

    @skip_file_exists
    def generate(self):
        try:
            # download ipfs document if not exists in cache
            word_IPFS_file_path = self.download_ipfs_document_into_cache()

            # Replaced tags if exists, save replaced document in temp file
            word_tags_replaced_file_path = self._replace_tags(word_IPFS_file_path)

            # convert the replaced document file into pdf, then save it into converted folder
            self._word_pdf(word_tags_replaced_file_path)

            # rename the pdf file in converted folder into encoded hash to use in in cache
            self._rename_files()

        finally:
            # Remove the temp file that replaced the tags if exist
            if os.path.isfile(self.temp_word_file_with_tags_replaced):
                os.remove(self.temp_word_file_with_tags_replaced)

        return '%s/%s.pdf' % (CONVERTED_DIR, self.encoded_hash)


class HtmlDocument(IPFSDocument):
    def __init__(self, hash_key, replace_tags=None):
        super(HtmlDocument, self).__init__(hash_key=hash_key, replace_tags=replace_tags, extension="html")

    def _replace_tags(self, html_file_path):
        # open html file from temp folder
        # with open(self.IPFS_file, "r" , encoding='utf-8', ) as file:
        with open(html_file_path, "r") as file:
            data = file.read()

        # check if there's tags needs to replace
        if self.replace_tags:
            pattern = re.compile('|'.join(self.replace_tags.keys()))
            data = pattern.sub(lambda m: self.replace_tags[m.group(0)], str(data))

        return data

    def _html_pdf(self, string_html, pdf_folder):
        pdfkit.from_string(string_html, pdf_folder, options=DOCUMENT_RENDERING_OPTIONS[self.extension])

    @skip_file_exists
    def generate(self):
        # download ipfs document if not exists before in the temp folder
        html_IPFS_file_path = self.download_ipfs_document_into_cache()

        # Replaced tags if exists, return the results into data variable
        data = self._replace_tags(html_IPFS_file_path)

        # convert the result in variable data into pdf file, save it into converted folder
        self._html_pdf(str(data), self.pdf_file_path)

        return '%s/%s.pdf' % (CONVERTED_DIR, self.encoded_hash)
