import unittest, os
from classes.utils import *
from classes.documents import *


class WordDocumentTest(unittest.TestCase):
    def setUp(self):
        self.hash = "QmQEGujQefenqt53Au82gPf5yjEbwzea5UJMxswJqmwtHF"
        self.replace_tags = {
            "company": "Fifth Force GmbH",
            "country": "Germany",
            "hrb-clause": "the commercial register of the local court of Berlin under HRB 179357 B",
            "repo-url": "git@github.com:Neufund/ESOP.git",
            "commit-id": "",
            "court-city": "Berlin"
        }
        self.pdf_object = PdfFactory.factory('docx')

        self.doc_object = self.pdf_object(self.hash, self.replace_tags)

    def test_download_ipfs(self):
        self.doc_object.download_ipfs_document()
        assert os.path.isfile(self.doc_object.downloaded_file_path)

    def test_replace_tags(self):
        self.doc_object._replace_tags()
        assert os.path.isfile(self.doc_object.converted_file_path)

    def test_all_process(self):
        doc_object = self.pdf_object(self.hash, self.replace_tags)

        doc_object.generate()
        assert os.path.isfile(doc_object.pdf_file_path)


if __name__ == '__main__':
    unittest.main()
