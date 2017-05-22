import os
import unittest

from classes.utils import IPFSDocument


class IPFSTest(unittest.TestCase):
    def setUp(self):
        hash = "QmQEGujQefenqt53Au82gPf5yjEbwzea5UJMxswJqmwtHF"
        self.ipfs_document = IPFSDocument(hash, {
            'company': 'Fifth Forth'
        }, 'word')

    def test_check_IPFS_pinned_document(self):
        self.assertTrue(self.ipfs_document._is_document_pinned())

    def test_download_file_to_cache(self):
        downloaded_IPFS_file = self.ipfs_document.download_ipfs_document_into_cache()
        self.assertTrue(os.path.exists(downloaded_IPFS_file))
