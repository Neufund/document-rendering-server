import unittest

from classes.documents import *
from config import CURRENT_DIRECTORY


class HtmlDocumentTest(unittest.TestCase):
    def setUp(self):
        self.hash = "QmQvrXFVTbPYHVLRSqPfnCPaVizhBomEKvFgAPB8Cd2B9x"
        self.replace_tags = {
            "{company}": "Fifth Force GmbH",
            "{country}": "Germany",
            "{hrb-clause}": "the commercial register of the local court of Berlin under HRB 179357 B",
            "{repo-url}": "git@github.com:Neufund/ESOP.git",
            "{commit-id}": "",
            "{court-city}": "Berlin"
        }

        self.html_factory = PdfFactory.factory('html', self.hash, self.replace_tags)

    def test_replace_tags(self):
        html_file_path = '%s/ESOPTerms&ConditionsDocument.html' % CURRENT_DIRECTORY
        data = self.html_factory._replace_tags(html_file_path)
        self.assertIsNot(data, None)

    def test_html_to_pdf(self):
        output_pdf_expected_file = "%s/converted/test.pdf"%CURRENT_DIRECTORY
        self.html_factory._html_pdf("<h1>Test Convert to pdf</h1>", output_pdf_expected_file)
        self.assertTrue(os.path.exists(output_pdf_expected_file))


if __name__ == '__main__':
    unittest.main()
