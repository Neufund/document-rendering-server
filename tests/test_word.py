import unittest

from classes.documents import *


class WordDocumentTest(unittest.TestCase):
    def setUp(self):
        self.hash = "QmQEGujQefenqt53Au82gPf5yjEbwzea5UJMxswJqmwtHF"
        self.replace_tags = {
            "{company}": "Fifth Force GmbH",
            "{country}": "Germany",
            "{hrb-clause}": "the commercial register of the local court of Berlin under HRB 179357 B",
            "{repo-url}": "git@github.com:Neufund/ESOP.git",
            "{commit-id}": "",
            "{court-city}": "Berlin"
        }

        self.word_factory = PdfFactory.factory('word', self.hash, self.replace_tags)

    def test_replace_tags(self):
        word_file_path = '%s/ESOPTerms&ConditionsDocument.docx' % CURRENT_DIRECTORY
        word_document_tags_replaced_file_path = self.word_factory._replace_tags(word_file_path)

        self.assertTrue(os.path.exists(word_document_tags_replaced_file_path))
        os.remove(word_document_tags_replaced_file_path)

    def test_word_to_pdf(self):
        word_file_path = '%s/ESOPTerms&ConditionsDocument.docx' % CURRENT_DIRECTORY
        self.word_factory._word_pdf(word_file_path)
        output_pdf_expected_file = '%s/ESOPTerms&ConditionsDocument.pdf'%CONVERTED_DIR
        self.assertTrue(os.path.exists(output_pdf_expected_file))

    def test_wrong_word_path_to_pdf(self):
        try:
            word_file_path = '%s/ESOPTerms&ConditionsDocument.doc' % CURRENT_DIRECTORY
            self.word_factory._word_pdf(word_file_path)

        except NotFoundException:
            pass
        else:
            self.fail("NotFoundException supposed to be raised")

if __name__ == '__main__':
    unittest.main()
