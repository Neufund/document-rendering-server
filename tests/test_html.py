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

    def test_ipfs(self):
        self.doc_object.ipfs.file_ls('QmQEGujQefenqt53Au82gPf5yjEbwzea5UJMxswJqmwtHF')

    def test_download_ipfs(self):
        self.doc_object.download_ipfs_document()
        assert os.path.isfile(self.doc_object.downloaded_file_path)

    def test_replace_tags(self):
        self.doc_object._replace_tags()
        assert os.path.isfile(self.doc_object.converted_file_path)

    def test_all_process(self):
        self.doc_object.generate()
        assert os.path.isfile(self.doc_object.pdf_file_path)

    def test_wrong_hash(self):
        hash = "QmQEGujQefenqt53Au82gPf5yjEbwzea5UJMxswJqmwtHF"  # html hash

        doc_object = self.pdf_object(hash, self.replace_tags)
        try:
            doc_object.generate()
        except UnSupportedFileException as e:
            pass
        else:
           self.fail('ExpectedException not raised')

if __name__ == '__main__':
    unittest.main()
