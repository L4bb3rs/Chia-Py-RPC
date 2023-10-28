import os
import json
import requests
import urllib3
from typing import Optional, Tuple, Dict, Any

class WalletRPCConnect:
    """
    A class for connecting to a Chia Wallet RPC service.

    Attributes:
        url (str): URL of the Chia RPC service.
        cert (Tuple[str, str]): Paths to the SSL certificate and private key files.
    """

    DEFAULT_URL = "https://localhost:9256/"
    DEFAULT_CERT = (
        os.path.expanduser('~/.chia/mainnet/config/ssl/full_node/private_full_node.crt'),
        os.path.expanduser('~/.chia/mainnet/config/ssl/full_node/private_full_node.key')
    )

    def __init__(self, url: Optional[str] = None, cert: Optional[Tuple[str, str]] = None, disable_warnings: bool = False) -> None:
        """
        Initialize the WalletRPCConnect instance.

        Args:
            url (Optional[str]): URL of the Chia RPC service.
            cert (Optional[Tuple[str, str]]): Paths to the SSL certificate and private key files.
            disable_warnings (bool, optional): Disable SSL warnings. Defaults to False.
        """
        self.url = url or self.DEFAULT_URL
        self.cert = cert or self.DEFAULT_CERT
        self.headers = {"Content-Type": "application/json"}

        if disable_warnings:
            urllib3.disable_warnings()

    def submit(self, chia_call: str, data: str) -> Dict[str, Any]:
        """
        Submit a Chia RPC call.

        Args:
            chia_call (str): The Chia RPC call to be made.
            data (str): The data to be sent in the request.

        Returns:
            Dict[str, Any]: The JSON response.
        """
        try:
            response = requests.post(
                f"{self.url}{chia_call}",
                data=data,
                headers=self.headers,
                cert=self.cert,
                verify=True  # Enable SSL verification
            )
            response.raise_for_status()  # Raise HTTPError for bad responses
            return response.json()
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return {}
