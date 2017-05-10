import unittest
from tools import Manager


class ManagetTest(unittest.TestCase):
    def setUp(self):
        self.m = Manager('QmQEGujQefenqt53Au82gPf5yjEbwzea5UJMxswJqmwtHF')

    def test_download_ipfs_document(self):
        self.m.download_ipfs_document()

    def test_replace(self):
        self.m.replace({
          "{company}":"Fifth Force GmbH",
          "{country}":"Germany",
          "{hrb-clause}":"the commercial register of the local court of Berlin under HRB 179357 B",
          "{repo-url}":"git@github.com:Neufund/ESOP.git",
          "{commit-id}":"",
          "{court-city}":"Berlin",
        })


    # def test_doc_pdf(self):
    #     self.m.doc_pdf()

if __name__ == '__main__':
    unittest.main()
