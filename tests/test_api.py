import os
from server import app
from classes.exceptions import *
import unittest

class ApiTest(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def test_wrong_endpoint(self):
        print("Wrong endpoint")
        response = self.tester.post('/api/document1' )
        self.assertEqual(response.status_code , 404)

    def test_missing_arguments(self):
        print("Missing arugment")
        response = self.tester.post('/api/document?hash=123')
        self.assertEqual(response.status_code , 400)

    def test_not_pinned_hash(self):
        print("Hash Not pinned")

        response = self.tester.post('/api/document?hash=123&type=html' )
        self.assertEqual(response.status_code , 403)

    def test_document_endpoint(self):
        hash = "QmQvrXFVTbPYHVLRSqPfnCPaVizhBomEKvFgAPB8Cd2B9x"
        type = 'html'
        response = self.tester.post('/api/document?hash=%s&type=%s'%(hash,type))
        self.assertEqual(response.status_code , 200)



if __name__ == '__main__':
    unittest.main()
