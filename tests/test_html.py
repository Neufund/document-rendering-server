import unittest , os
from classes.utils import *
from classes.documents import *

class HtmlDocumentTest(unittest.TestCase):
    def setUp(self):
        self.hash = "QmQvrXFVTbPYHVLRSqPfnCPaVizhBomEKvFgAPB8Cd2B9x"
        self.replace_tags = {
              "Fifth Force GmbH":"Company",
              "Germany":"Country"
        }
        self.pdf_object = PdfFactory.factory('html')

        self.doc_object = self.pdf_object(self.hash, self.replace_tags)

    def test_download_ipfs(self):
        self.doc_object.download_ipfs_document()
        assert os.path.isfile(self.doc_object.downloaded_file_path)

    def test_replace_tags(self):
        self.doc_object._replace_tags()
        assert os.path.isfile(self.doc_object.converted_file_path)

    def test_all_process(self):
        self.doc_object.generate()
        assert os.path.isfile(self.doc_object.pdf_file_path)



if __name__ == '__main__':
    unittest.main()
