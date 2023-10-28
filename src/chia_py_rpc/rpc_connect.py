import json
import requests
import urllib3
import os

from typing import Optional, Tuple


class WalletRPCConnect:
    """
    This module provides a class for connecting to a Chia Wallet RPC service.

    The `WalletRPCConnect` class provides methods for submitting Chia RPC calls and
    receiving JSON responses.

    Usage:
        >>> wallet_rpc = WalletRPCConnect(url='https://localhost:9256/',
                                        cert=('path/to/cert', 'path/to/key'))
        >>> response = wallet_rpc.submit('get_wallet_balance', '{}')
        >>> print(response)

    Attributes:
        url (str): URL of the Chia RPC service.
        cert (tuple): Tuple containing paths to the SSL certificate and private key files.

    Methods:
        submit(chia_call: str, data: str) -> str:
            Submit a Chia RPC call to the specified URL with the given data.

            Args:
                chia_call (str): Name of the Chia RPC call to be made.
                data (str): Data to be sent in the request.

            Returns:
                str: JSON response as a string with indentation and sorted keys.
    """


    def __init__(self, url: Optional[str] = None,
                cert: Optional[Tuple[str, str]] = None):
        """
        Initialize ChiaRPC instance with the provided URL and certificate.

        Args:
            url (str, optional): URL of the Chia RPC service. Defaults to None.
            cert (tuple, optional): Tuple containing paths to the SSL certificate and private key files. Defaults to None.
        """
        default_url = "https://localhost:9256/"
        default_cert = (
            os.path.expanduser(
                '~/.chia/mainnet/config/ssl/full_node/private_full_node.crt'),
            os.path.expanduser(
                '~/.chia/mainnet/config/ssl/full_node/private_full_node.key')
        )

        self.url = url or default_url
        self.cert = cert or default_cert
        self.headers = {"Content-Type": "application/json"}
        urllib3.disable_warnings()


    def submit(self, chia_call: str, data: str):
        """
        Submit data to the specified URL.

        Args:
            chia_call (str): Chia RPC call to be made.
            data (str): Data to be sent in the request.

        Returns:
            str: JSON response as a string with indentation and sorted keys.
        """
        response = requests.post(
            self.url + chia_call,
            data=data,
            headers=self.headers,
            cert=self.cert,
            verify=False)
        response_text = response.text
        response_json = json.loads(response_text)
        return json.dumps(response_json, indent=4, sort_keys=True)