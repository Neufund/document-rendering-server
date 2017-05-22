import unittest, os
from classes.utils import *
from classes.documents import *
from server import init_logging


# do not assume IPFS working, provide test document as file and skip IPFS download
class HtmlDocumentTest(unittest.TestCase):
    def setUp(self):
        self.hash = "QmQvrXFVTbPYHVLRSqPfnCPaVizhBomEKvFgAPB8Cd2B9x"
        self.replace_tags = {
            "Fifth Force GmbH": "Company",
            "Germany": "Country"
        }
        self.pdf_object = PdfFactory.factory('html')
        self.doc_object = self.pdf_object(self.hash, self.replace_tags)

        init_logging()

    def test_ipfs(self):
        self.doc_object.ipfs.file_ls('QmQEGujQefenqt53Au82gPf5yjEbwzea5UJMxswJqmwtHF')

    def test_download_ipfs(self):
        self.doc_object.download_ipfs_temp()
        assert self.doc_object.temp_file != None

    def test_replace_tags(self):
        self.doc_object.download_ipfs_temp()
        data = self.doc_object._replace_tags()
        assert data is not None

    def test_all_process(self):
        self.doc_object.generate()
        assert os.path.isfile(self.doc_object.pdf_file_path)

    def test_wrong_hash(self):
        hash = "QmQEGujQefenqt53Au82gPf5yjEbwzea5UJMxswJqmwtHF"  # html hash

        doc_object = self.pdf_object(hash, self.replace_tags)
        try:
            doc_object.generate()
        except UnSupportedFileException as e:
            # expected exception
            pass
        else:
            self.fail('ExpectedException not raised')


if __name__ == '__main__':
    unittest.main()
