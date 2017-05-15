#!/usr/bin/python
from classes.exceptions import *
from classes.utils import DocumentReplace
from docx import Document
from subprocess import call
from config import *
from classes.utils import *
import pdfkit


class PdfFactory(object):
    def factory(type):
        if type == "html": return HtmlDocument
        if type == "docx": return WordDocument

    factory = staticmethod(factory)


# If pdf file exist no need to exiecute the funtion.
def skip_file_exists(func):
    def checker(*args):
        file_path = args[0].pdf_file_path
        if os.path.exists(file_path):
            logging.info("The pdf file exists before in path %s" % file_path)
            return None

        return func(*args)

    return checker


class WordDocument(IPFS):
    def __init__(self, hash_key, replace_tags=None):
        self.extension = "docx"
        super(WordDocument, self).__init__(hash_key=hash_key, replace_tags=replace_tags)

    def _replace_tags(self):
        replace_tags = self.replace_tags

        if os.path.exists(self.temp_file):
            logging.debug('start open the document: %s.docx' % self.temp_file)

            doc = Document(self.temp_file)
            replace = DocumentReplace(doc)
            if replace_tags:
                logging.debug('start replacing tags: %s.docx' % self.temp_file)
                # for key in replace_tags:
                replace.paragraph_replace(replace_tags)

            doc.save(self.temp_file)
            logging.debug('file has been saved in: %s/%s.docx' % (CONVERTED_DIR, self.encoded_hash))
        else:
            raise NotFoundException("Docx file %s.%s not found" % (self.extension, self.encoded_hash))

    def _doc_pdf(self):
        logging.info("start pdf:%s" % self.temp_file)

        if os.path.isfile(self.temp_file):
            script = './doc2pdf.sh %s %s' % (self.temp_file, CONVERTED_DIR)
            result = call(script, shell=True)
            if result == 0:
                logging.info("PDF file saved successfully")
                return self.encoded_hash
            else:
                err_message = "Bash script error in saving PDF file with hash %s" % self.encoded_hash
                logging.error(err_message)
                raise BashScriptException(err_message)
        else:
            raise NotFoundException("Docx File %s.%s not found" % (self.encoded_hash, self.extension))

    # Rename the temp file and the converted file as well, to use as cache files.
    def _rename_files(self):
        os.rename(self.temp_file, '%s/%s' % (TEMP_DIR, self.encoded_hash))
        temp_file_name = os.path.basename(os.path.normpath(self.temp_file))
        os.rename('%s/%s.pdf' % (CONVERTED_DIR, temp_file_name), '%s/%s.pdf' % (CONVERTED_DIR, self.encoded_hash))

    @skip_file_exists
    def generate(self):
        self.download_ipfs_temp()
        if self.extension != "docx":
            raise Exception("This file is not word document")

        self._replace_tags()
        self._doc_pdf()
        self._rename_files()


class HtmlDocument(IPFS):
    def __init__(self, hash_key, replace_tags=None):
        self.extension = "html"
        super(HtmlDocument, self).__init__(hash_key=hash_key, replace_tags=replace_tags)

    def _replace_tags(self):

        with open(self.temp_file, "r") as file:
            data = file.read()

        if self.replace_tags:
            pattern = re.compile('|'.join(self.replace_tags.keys()))
            data = pattern.sub(lambda m: self.replace_tags[m.group(0)], str(data))

        return data

    def _doc_pdf(self, string_html, pdf_folder):
        pdfkit.from_string(string_html, pdf_folder)

    # Rename the temp file to use as cache files.
    def _rename_files(self):
        os.rename(self.temp_file, '%s/%s' % (TEMP_DIR, self.encoded_hash))

    @skip_file_exists
    def generate(self):
        if self.extension != "html":
            raise UnKnownFileTypeException("This file is not html")

        self.download_ipfs_temp()
        data = self._replace_tags()
        self._doc_pdf(str(data), self.pdf_file_path)
        self._rename_files()
