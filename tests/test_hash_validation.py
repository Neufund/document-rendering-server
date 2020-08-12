import unittest

from classes.exceptions import InvalidIPFSHashException
from classes.ipfs_document import IPFSDocument


class IPFSTestHashValidation(unittest.TestCase):
    @staticmethod
    def test_correct_hash():
        correct_hash = "QmQEGujQefenqt53Au82gPf5yjEbwzea5UJMxswJqmwtHF"
        IPFSDocument(correct_hash)

    def test_forbidden_hash(self):
        incorrect_hashes = [
            "../../etc/shadow",
            "QEGujQefenqt53Au82gPf5yjEbwzea5UJMxswJqmwtHF",
            1
        ]
        for h in incorrect_hashes:
            with self.assertRaises(InvalidIPFSHashException):
                IPFSDocument(h)


if __name__ == '__main__':
    unittest.main()