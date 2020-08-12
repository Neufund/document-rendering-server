#!/usr/bin/python
import logging
import ipfshttpclient

from config import *


def ipfs_connect(func):
    def connection(self):
        logging.debug(
            "Start connection with IPFS Server :%s, Port:%s, Transmit connection timeout:%s, Connection timeout:%s",
            SERVER_IP,
            IPFS_PORT,
            IPFS_TRANSMIT_CONNECT_TIMEOUT,
            IPFS_CONNECT_TIMEOUT)

        if self.ipfs is None:
            self.ipfs = ipfshttpclient.connect(f"/dns/{SERVER_IP}/tcp/{IPFS_PORT}/http", timeout=(IPFS_CONNECT_TIMEOUT, IPFS_TRANSMIT_CONNECT_TIMEOUT))

        function_return = func(self)

        return function_return

    return connection
