#!/usr/bin/env python
from classes.exceptions import *
from docx import Document
from subprocess import call
from config import *
from classes.utils import *
import pdfkit


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
            return None

        return func(*args)

    return checker


class WordDocument(IPFSDocument):
    def __init__(self, hash_key, replace_tags=None):
        super(WordDocument, self).__init__(hash_key=hash_key, replace_tags=replace_tags, extension="word")
        self.temp_file = None

    def paragraph_replace(self, tags_dic):
        pattern = re.compile('|'.join(tags_dic.keys()))
        for paragraph in self.doc.paragraphs:
            if paragraph.text:
                paragraph.text = pattern.sub(lambda m: tags_dic[m.group(0)], paragraph.text)

    def _replace_tags(self):
        replace_tags = self.replace_tags
        print(self.IPFS_file)
        if os.path.exists(self.IPFS_file):
            logging.debug('start open the document: %s' % self.IPFS_file)

            self.doc = Document(self.IPFS_file)
            if replace_tags:
                logging.debug('start replacing tags: %s' % self.IPFS_file)
                # for key in replace_tags:
                self.paragraph_replace(replace_tags)

            temp = tempfile.NamedTemporaryFile(prefix='document_word_', dir=TEMP_DIR, delete=False)
            with temp as f:
                self.temp_file = f.name  # Temporary file name
            logging.debug('temporary file with tags replaces in %s' % self.temp_file)

            # Replace the downloaded temp file with the new document with tags.
            self.doc.save(self.temp_file)

            logging.debug('file has been saved in: %s/%s' % (CONVERTED_DIR, self.encoded_hash))
        else:
            raise NotFoundException("Docx file %s.%s not found" % (self.encoded_hash, self.extension))

    def _doc_pdf(self):
        logging.info("start pdf:%s" % self.temp_file)

        if os.path.isfile(self.temp_file):
            script = '%s/doc2pdf.sh %s %s' % (CURRENT_DIRECTORY, self.temp_file, CONVERTED_DIR)
            logging.debug("Execute script %s" % script)

            # execute bash script doc2pdf using `soffice` command
            result = call(script, shell=True)
            if result == 0:
                logging.info("PDF file saved successfully")
                return self.encoded_hash
            else:
                err_message = "Bash script error in saving PDF file with hash %s" % self.hash
                logging.error(err_message)
                os.remove(self.temp_file)
                raise BashScriptException(err_message)
        else:
            os.remove(self.temp_file)
            raise NotFoundException(".docx File %s.%s not found" % (self.encoded_hash, self.extension))

    # Rename the temp file and the converted file as well, to use as cache files.
    def _rename_files(self):

        # rename the replaced document into encoded hash name
        temp_file_name = os.path.basename(os.path.normpath(self.temp_file))
        # rename the pdf file into encoded hash
        os.rename('%s/%s.pdf' % (CONVERTED_DIR, temp_file_name), '%s/%s.pdf' % (CONVERTED_DIR, self.encoded_hash))

    @skip_file_exists
    def generate(self):

        # download ipfs document if not exists before in the temp folder
        self.download_ipfs_temp()

        # Replaced tags if exists, save replaced document in temp file
        self._replace_tags()

        # convert the replaced document file into pdf, then save it into converted folder
        self._doc_pdf()

        # rename the pdf file in converted folder into encoded hash to use in in cache
        self._rename_files()

        # Remove the temp file that replaced the tags
        os.remove(self.temp_file)


class HtmlDocument(IPFSDocument):
    def __init__(self, hash_key, replace_tags=None):
        super(HtmlDocument, self).__init__(hash_key=hash_key, replace_tags=replace_tags, extension="html")

    def _replace_tags(self):
        # open html file from temp folder
        with open(self.IPFS_file, "r") as file:
            data = file.read()

        # check if there's tags needs to replace
        if self.replace_tags:
            pattern = re.compile('|'.join(self.replace_tags.keys()))
            data = pattern.sub(lambda m: self.replace_tags[m.group(0)], str(data))

        return data

    def _doc_pdf(self, string_html, pdf_folder):
        pdfkit.from_string(string_html, pdf_folder)

    @skip_file_exists
    def generate(self):
        # download ipfs document if not exists before in the temp folder
        self.download_ipfs_temp()

        # Replaced tags if exists, return the results into data variable
        data = self._replace_tags()

        # convert the result in variable data into pdf file, save it into converted folder
        self._doc_pdf(str(data), self.pdf_file_path)
