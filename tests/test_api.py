import unittest

from server import app


class ApiTest(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def test_wrong_endpoint(self):
        response = self.tester.post('/api/document1')
        self.assertEqual(response.status_code, 404)

    def test_missing_arguments(self):
        response = self.tester.post('/api/document?hash=123')
        self.assertEqual(response.status_code, 400)

    def test_not_pinned_hash(self):
        response = self.tester.post('/api/document?hash=123&type=html')
        self.assertEqual(response.status_code, 403)

    def test_document_endpoint(self):
        hash = "QmQEGujQefenqt53Au82gPf5yjEbwzea5UJMxswJqmwtHF"
        type = 'word'
        response = self.tester.post('/api/document?hash=%s&type=%s' % (hash, type))
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
