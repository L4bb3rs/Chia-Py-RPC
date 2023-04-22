import os
import json
import requests
import urllib3

from typing import Optional, Tuple


class ChiaRPC:
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
                '~\\.chia\\mainnet\\config\\ssl\\full_node\\private_full_node.crt'),
            os.path.expanduser(
                '~\\.chia\\mainnet\\config\\ssl\\full_node\\private_full_node.key')
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


class SharedMethods:
    """Methods shared by all services."""

    def __init__(self, url=None, cert=None):
        self.url = url
        self.cert = cert
        self.chia_rpc = ChiaRPC(url, cert)

    def close_connection(self, node_id: str) -> dict:
        """
        Close a connection in a shared wallet.

        Args:
            node_id (str): Node ID of the connection to be closed.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'node_id': node_id
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit("close_connection", json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def get_connections(self) -> dict:
        """
        Retrieve the list of connections in a shared wallet.

        Returns:
            dict: A dictionary containing the list of connections.
        """

        # Prepare the payload as a dictionary
        payload = {}

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit("get_connections", json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def get_routes(self) -> dict:
        """
        Retrieve the list of routes/endpoints exposed by the shared wallet service.

        Returns:
            dict: A dictionary containing the list of routes/endpoints.
        """

        # Prepare the payload as a dictionary
        payload = {}

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        # without passing any parameters
        result = self.chia_rpc.submit("get_routes", json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def check_healthz(self) -> dict:
        """
        Check the health status of the shared wallet service.

        Returns:
            dict: Parsed JSON response from the shared wallet service.
        """

        # Prepare the payload as a dictionary
        payload = {}

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        # without passing any parameters
        result = self.chia_rpc.submit("healthz", json.dumps(payload))

        # Parse the JSON response and return it
        return json.loads(result)

    def open_connection(self, ip: str, port: int) -> dict:
        """
        Add a connection to another node.

        Args:
            ip (str): IP address of the node to connect to.
            port (int): Port number of the node to connect to.

        Returns:
            dict: Parsed JSON response from the shared wallet service.
        """
        # Prepare the payload as a dictionary
        payload = {
            "ip": ip,
            "port": port
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        # with the request data
        result = self.chia_rpc.submit("open_connection", json.dumps(payload))

        # Parse the JSON response and return it
        return json.loads(result)

    def stop_node(self) -> dict:
        """
        Stop the Chia node.

        Returns:
            dict: Parsed JSON response from the shared wallet service.
        """
        # Prepare the payload as a dictionary
        payload = {}

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        # with the request data
        result = self.chia_rpc.submit("stop_node", json.dumps(payload))

        # Parse the JSON response and return it
        return json.loads(result)


class CatWallet:
    # TODO Type Hints Doc Strings

    """CATs, trades, and offers."""

    def __init__(self, url: str = None, cert: str = None):
        """
        Initialize CatWallet instance.

        Args:
            url (str, optional): URL for ChiaRPC. Defaults to https://localhost:9256/ unless specified.
            cert (str, optional): Certificate for ChiaRPC. Default Ceritificates unless specified.
        """
        self.url = url
        self.cert = cert
        self.chia_rpc = ChiaRPC(url, cert)

    def cancel_offers(self, batch_fee: int = 0, secure: bool = True,
                      batch_size: int = 5, cancel_all: bool = False, asset_id: str = "xch") -> dict:
        """
        Cancel offers category.

        Args:
            batch_fee (int, optional): Batch fee. Defaults to 0.
            secure (bool, optional): Secure flag. Defaults to True.
            batch_size (int, optional): Batch size. Defaults to 5.
            cancel_all (bool, optional): Cancel all flag. Defaults to False.
            asset_id (str, optional): Asset ID. Defaults to "xch".

        Returns:
            dict: Response from the RPC.
        """
        data = {
            "batch_fee": batch_fee,
            "secure": secure,
            "batch_size": batch_size,
            "cancel_all": cancel_all,
            "asset_id": asset_id.lower()
        }
        result = self.chia_rpc.submit("cancel_offers", json.dumps(data))
        return json.loads(result)

    def cat_asset_id_to_name(self, asset_id: str) -> dict:
        """
        Retrieve asset name by asset ID

        Args:
            asset_id (str): Asset ID

        Returns:
            dict: Response from the RPC
        """
        data = {"asset_id": asset_id}
        result = self.chia_rpc.submit("cat_asset_id_to_name", json.dumps(data))
        return json.loads(result)

    def cancel_offer(self, offer_id):
        """Cancel a CAT Wallet offer by offer_id"""
        data = {"offer_id": offer_id}
        result = self.chia_rpc.submit("cancel_offer", json.dumps(data))
        return json.loads(result)

    def cat_get_asset_id(self, wallet_id):
        """Get the asset_id for a given asset_name in CAT Wallet"""
        data = {"wallet_id": wallet_id}
        result = self.chia_rpc.submit("cat_get_asset_id", json.dumps(data))
        return json.loads(result)

    def cat_get_name(self, wallet_id):
        """Get the asset_name for a given asset_id in CAT Wallet"""
        data = {"wallet_id": wallet_id}
        result = self.chia_rpc.submit("cat_get_name", json.dumps(data))
        return json.loads(result)

    def cat_set_name(self, wallet_id, name):
        """
        Set the name for a given asset_id in CAT Wallet

        Args:
            wallet_id (int): Wallet ID
            name (str): Asset name

        Returns:
            dict: Response from the RPC
        """
        data = {"wallet_id": wallet_id, "name": name}
        result = self.chia_rpc.submit("cat_set_name", json.dumps(data))
        return json.loads(result)

    def cat_spend(self, wallet_id, coins, amount, fee, inner_address, memos, min_coin_amount,
                  max_coin_amount, exclude_coin_amounts, exclude_coin_ids, reuse_puzhash):
        """
        Spends an amount from the given wallet

        Args:
            wallet_id (int): Wallet ID
            coins (list): List of coins to spend
            amount (int): Amount to spend
            fee (int): Fee to pay
            inner_address (str): Inner address to spend to
            memos (list): List of memos
            min_coin_amount (int): Minimum coin amount
            max_coin_amount (int): Maximum coin amount
            exclude_coin_amounts (list): List of coin amounts to exclude
            exclude_coin_ids (list): List of coin IDs to exclude
            reuse_puzhash (bool): Reuse puzzle hash

        Returns:
            dict: Response from the RPC
        """
        data = {
            "wallet_id": wallet_id,
            "coins": coins,
            "amount": amount,
            "fee": fee,
            "inner_address": inner_address,
            "memos": memos,
            "min_coin_amount": min_coin_amount,
            "max_coin_amount": max_coin_amount,
            "exclude_coin_amounts": exclude_coin_amounts,
            "exclude_coin_ids": exclude_coin_ids,
            "reuse_puzhash": reuse_puzhash
        }
        result = self.chia_rpc.submit("cat_spend", json.dumps(data))
        return json.loads(result)

    def check_offer_validity(self, offer):
        """
        Check the validity of an offer in CAT Wallet

        Args:
            offer (str): Offer string

        Returns:
            dict: Response from the RPC
        """
        data = {"offer": offer}
        result = self.chia_rpc.submit("check_offer_validity", json.dumps(data))
        return json.loads(result)

    def create_offer_for_ids(self, offer, fee, validate_only, driver_dict,
                             min_coin_amount, max_coin_amount, solver, reuse_puzhash):
        """
        Create an offer for a given set of wallet id and amount pairs in CAT Wallet

        Args:
            offer (dict): Offer dictionary
            fee (int): Fee amount
            validate_only (bool): Whether to only validate the offer or not
            driver_dict (dict): Driver dictionary
            min_coin_amount (int): Minimum coin amount
            max_coin_amount (int): Maximum coin amount
            solver (dict): Solver dictionary
            reuse_puzhash (bool): Whether to reuse the puzzle hash or not

        Returns:
            dict: Response from the RPC
        """
        data = {
            "offer": offer,
            "fee": fee,
            "validate_only": validate_only,
            "driver_dict": driver_dict,
            "min_coin_amount": min_coin_amount,
            "max_coin_amount": max_coin_amount,
            "solver": solver,
            "reuse_puzhash": reuse_puzhash
        }
        result = self.chia_rpc.submit("create_offer_for_ids", json.dumps(data))
        return json.loads(result)

    def get_all_offers(self, start, end, exclude_my_offers, exclude_taken_offers,
                       include_completed, sort_key, reverse, file_contents):
        """
       def cat_get_all_offers(self, start, end, exclude_my_offers, exclude_taken_offers, include_completed, sort_key, reverse, file_contents):

        Args:
            start (int): Start index for offers
            end (int): End index for offers
            exclude_my_offers (bool): Whether to exclude the user's own offers or not
            exclude_taken_offers (bool): Whether to exclude taken offers or not
            include_completed (bool): Whether to include completed offers or not
            sort_key (str): Sort key for offers
            reverse (bool): Whether to sort in reverse order or not
            file_contents (bool): Whether to include file contents or not

        Returns:
            dict: Response from the RPC
        """
        data = {
            "start": start,
            "end": end,
            "exclude_my_offers": exclude_my_offers,
            "exclude_taken_offers": exclude_taken_offers,
            "include_completed": include_completed,
            "sort_key": sort_key,
            "reverse": reverse,
            "file_contents": file_contents
        }
        result = self.chia_rpc.submit("get_all_offers", json.dumps(data))
        return json.loads(result)

    def get_offer(self, trade_id, file_contents=True):
        """Retrieves an offer by trade_id in CAT Wallet.

        Args:
            trade_id (str): Trade ID of the offer to retrieve
            file_contents (bool, optional): Whether to include file contents or not. Defaults to True.

        Returns:
            dict: Response from the RPC
        """
        data = {"trade_id": trade_id, "file_contents": file_contents}
        result = self.chia_rpc.submit("get_offer", json.dumps(data))
        return json.loads(result)

    def get_offer_summary(self, offer, advanced=False):
        """Retrieves a summary of an offer in CAT Wallet.

        Args:
            offer (str): Offer ID or Trade ID of the offer to retrieve
            advanced (bool, optional): Whether to include advanced details in the summary. Defaults to False.

        Returns:
            dict: Response from the RPC
        """
        data = {"offer": offer, "advanced": advanced}
        result = self.chia_rpc.submit("get_offer_summary", json.dumps(data))
        return json.loads(result)

    def get_offers_count(self):
        """Retrieves the count of all offers in CAT Wallet.

        Returns:
            dict: Response from the RPC
        """
        data = {}
        result = self.chia_rpc.submit("get_offers_count", json.dumps(data))
        return json.loads(result)

    def get_stray_cats(self):
        """Get a list of all unacknowledged CATs.

        Returns:
            dict: Response from the RPC call
        """
        data = {}
        result = self.chia_rpc.submit("get_stray_cats", json.dumps(data))
        return json.loads(result)

    def select_coins(self, wallet_id, amount, min_coin_amount,
                     excluded_coins=None, max_coin_amount=None, exclude_coin_amounts=None):
        """Selects coins in CAT Wallet for creating an offer using RPC.

        Args:
            wallet_id (int): ID of the wallet from which to select coins
            amount (int): Amount of coins to select
            min_coin_amount (int): Minimum amount of coins to select
            excluded_coins (list): List of dictionaries containing excluded coin details
            max_coin_amount (int): Maximum amount of coins to select (default: None)
            exclude_coin_amounts (list): List of coin amounts to exclude from selection (default: None)

        Returns:
            dict: Response from the RPC call
        """
        data = {
            "wallet_id": wallet_id,
            "amount": amount,
            "min_coin_amount": min_coin_amount,
            "excluded_coins": excluded_coins,
            "max_coin_amount": max_coin_amount,
            "exclude_coin_amounts": exclude_coin_amounts
        }
        result = self.chia_rpc.submit("select_coins", json.dumps(data))
        return json.loads(result)

    def take_offer(self, offer, fee, min_coin_amount,
                   max_coin_amount=None, solver=None, reuse_puzhash=True):
        """Takes an offer in CAT Wallet using RPC.

        Args:
            offer (str): Trade ID of the offer to take
            fee (int): Fee to offer in addition to the original offer
            min_coin_amount (int): Minimum amount of coins to use for solving the puzzle
            max_coin_amount (int): Maximum amount of coins to use for solving the puzzle (default: None)
            solver (dict): Dictionary containing solver options (default: None)
            reuse_puzhash (bool): Whether to reuse the puzzle hash from the original offer (default: True)

        Returns:
            dict: Response from the RPC call
        """
        data = {
            "offer": offer,
            "fee": fee,
            "min_coin_amount": min_coin_amount,
            "max_coin_amount": max_coin_amount,
            "solver": solver,
            "reuse_puzhash": reuse_puzhash
        }
        result = self.chia_rpc.submit("take_offer", json.dumps(data))
        return json.loads(result)


class DidWallet:
    # TODO Type Hints Doc Strings
    def __init__(self, url=None, cert=None):
        self.url = url
        self.cert = cert
        self.chia_rpc = ChiaRPC(url, cert)

    def did_create_attest(self, wallet_id, coin_name, pubkey, puzhash):
        """
        Create a DID attest for a specific DID wallet.

        Args:
            wallet_id (int): ID of the DID wallet to create the attest from.
            coin_name (str): Name of the coin to create the attest for.
            pubkey (str): Public key for the attest.
            puzhash (str): Puzhash for the attest.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'wallet_id': wallet_id,
            'coin_name': coin_name,
            'pubkey': pubkey,
            'puzhash': puzhash
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit("did_create_attest", json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def did_create_backup_file(self, wallet_id):
        """
        Create a backup file for a specific DID wallet.

        Args:
            wallet_id (int): ID of the DID wallet to create the backup file.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'wallet_id': wallet_id
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit(
            "did_create_backup_file",
            json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def did_find_lost_did(self, coin_id):
        """
        Find a lost DID for a specific coin ID.

        Args:
            coin_id (str): Coin ID to search for the lost DID.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'coin_id': coin_id
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit("did_find_lost_did", json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def did_get_current_coin_info(self, wallet_id):
        """
        Get the current coin info for a specific DID wallet.

        Args:
            wallet_id (int): ID of the DID wallet to retrieve coin info from.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'wallet_id': wallet_id
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit(
            "did_get_current_coin_info",
            json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def did_get_did(self, wallet_id):
        """
        Retrieve the distributed identity (DID) associated with a specific DID wallet.

        Args:
            wallet_id (int): ID of the DID wallet to retrieve the associated DID from.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'wallet_id': wallet_id
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit("did_get_did", json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def did_get_info(self, coin_id, latest=True):
        """
        Retrieve information about a specific distributed identity (DID) associated with a given coin ID.

        Args:
            coin_id (str): Coin ID of the DID to retrieve information for.
            latest (bool): Flag indicating whether to retrieve the latest information (default is True).

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'coin_id': coin_id,
            'latest': latest
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit("did_get_info", json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def did_get_information_needed_for_recovery(self, wallet_id):
        """
        Retrieve recovery information needed for a specific distributed identity (DID) wallet.

        Args:
            wallet_id (int): Wallet ID of the DID wallet to retrieve recovery information for.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'wallet_id': wallet_id
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit(
            "did_get_information_needed_for_recovery",
            json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def did_get_metadata(self, wallet_id):
        """
        Retrieve metadata of a specific distributed identity (DID) wallet.

        Args:
            wallet_id (int): Wallet ID of the DID wallet to retrieve metadata for.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'wallet_id': wallet_id
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit("did_get_metadata", json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def did_get_pubkey(self, wallet_id):
        """
        Retrieve the public key of a specific distributed identity (DID) wallet.

        Args:
            wallet_id (int): Wallet ID of the DID wallet to retrieve the public key for.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'wallet_id': wallet_id
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit("did_get_pubkey", json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def did_get_recovery_list(self, wallet_id):
        """
        Retrieve the recovery list for a specific distributed identity (DID) wallet.

        Args:
            wallet_id (int): Wallet ID of the DID wallet to retrieve the recovery list for.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'wallet_id': wallet_id
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit(
            "did_get_recovery_list", json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def did_get_wallet_name(self, wallet_id):
        """
        Retrieve the name of a specific distributed identity (DID) wallet.

        Args:
            wallet_id (int): Wallet ID of the DID wallet to retrieve the name for.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'wallet_id': wallet_id
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit(
            "did_get_wallet_name", json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def did_message_spend(
            self, wallet_id, coin_announcements, puzzle_announcements):
        """
        Spend a distributed identity (DID) message from a specific DID wallet.

        Args:
            wallet_id (int): Wallet ID of the DID wallet to spend the message from.
            coin_announcements (list): List of coin announcements as strings.
            puzzle_announcements (list): List of puzzle announcements as strings.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'wallet_id': wallet_id,
            'coin_announcements': coin_announcements,
            'puzzle_announcements': puzzle_announcements
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit("did_message_spend", json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def did_recovery_spend(self, wallet_id, attest_data, pubkey, puzhash):
        """
        Spend from a distributed identity (DID) wallet using recovery data.

        Args:
            wallet_id (int): Wallet ID of the DID wallet to spend from.
            attest_data (list): List of attest data as strings.
            pubkey (str): Public key associated with the DID wallet.
            puzhash (str): Puzzled hash associated with the DID wallet.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'wallet_id': wallet_id,
            'attest_data': attest_data,
            'pubkey': pubkey,
            'puzhash': puzhash
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit(
            "did_recovery_spend", json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def did_set_wallet_name(self, wallet_id, name):
        """
        Set the name of a distributed identity (DID) wallet.

        Args:
            wallet_id (int): Wallet ID of the DID wallet to set the name for.
            name (str): The new name for the DID wallet.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'wallet_id': wallet_id,
            'name': name
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit(
            "did_set_wallet_name", json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def did_transfer_did(self, wallet_id, inner_address,
                         fee, with_recovery_info, reuse_puzhash):
        """
        Transfer a distributed identity (DID) wallet to another owner.

        Args:
            wallet_id (int): Wallet ID of the DID wallet to transfer.
            inner_address (str): Inner address (Chia address) of the new owner.
            fee (float): Transaction fee to include in the transfer.
            with_recovery_info (bool): Whether to include recovery information in the transfer.
            reuse_puzhash (bool): Whether to reuse the puzzle hash of the DID wallet.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'wallet_id': wallet_id,
            'inner_address': inner_address,
            'fee': fee,
            'with_recovery_info': with_recovery_info,
            'reuse_puzhash': reuse_puzhash
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit("did_transfer_did", json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def did_update_metadata(self, wallet_id, metadata,
                            fee=0, reuse_puzhash=True):
        """
        Update the metadata of a distributed identity (DID) wallet.

        Args:
            wallet_id (int): Wallet ID of the DID wallet to update.
            metadata (dict): Dictionary containing the updated metadata.
            fee (int, optional): Fee to be paid for the update transaction (default: 0).
            reuse_puzhash (bool, optional): Whether to reuse the previous puzzle hash for the update transaction
                (default: True).

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'wallet_id': wallet_id,
            'metadata': metadata,
            'fee': fee,
            'reuse_puzhash': reuse_puzhash
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit(
            "did_update_metadata", json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def did_update_recovery_ids(
            self, wallet_id, new_list, num_verifications_required=0, reuse_puzhash=True):
        """
        Update the recovery IDs for a distributed identity (DID) wallet.

        Args:
            wallet_id (int): Wallet ID of the DID wallet to update.
            new_list (list): List of new recovery IDs to set.
            num_verifications_required (int, optional): Number of verifications required for recovery
                (default: 0).
            reuse_puzhash (bool, optional): Whether to reuse the previous puzzle hash for the update transaction
                (default: True).

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'wallet_id': wallet_id,
            'new_list': new_list,
            'num_verifications_required': num_verifications_required,
            'reuse_puzhash': reuse_puzhash
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit(
            "did_update_recovery_ids",
            json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)


class KeyManagement:
    # TODO Complete Functions
    def __init__(self, url=None, cert=None):
        self.url = url
        self.cert = cert
        self.chia_rpc = ChiaRPC(url, cert)


class PoolWallet:
    # TODO Complete Functions
    def __init__(self, url=None, cert=None):
        self.url = url
        self.cert = cert
        self.chia_rpc = ChiaRPC(url, cert)


class Notifications:
    # TODO Complete Functions
    def __init__(self, url=None, cert=None):
        self.url = url
        self.cert = cert
        self.chia_rpc = ChiaRPC(url, cert)


class Wallet:
    # TODO Type Hints Doc Strings
    def __init__(self, url=None, cert=None):
        self.url = url
        self.cert = cert
        self.chia_rpc = ChiaRPC(url, cert)

    def create_signed_transaction(self, wallet_id, additions, fee, coins, coin_announcements=None, puzzle_announcements=None,
                                  min_coin_amount=0, max_coin_amount=0, excluded_coins=None, excluded_coin_amounts=None):
        """
        Create a signed transaction for sending Chia coins.

        Args:
            wallet_id (int): ID of the wallet to use for creating the transaction.
            additions (list): List of dictionaries representing the recipients of the transaction.
                Each dictionary should contain the following keys:
                - 'amount' (int): The amount to send in mojos (1 XCH = 10^12 mojos).
                - 'puzzle_hash' (str): The puzzle hash of the recipient's address.
                - 'memos' (list): Optional list of memos to include in the transaction.
            fee (float): The transaction fee to be paid in XCH.
            coins (list): List of coin IDs to use for the transaction.
            coin_announcements (list): Coin announcements for the transaction. Optional.
            puzzle_announcements (list): Puzzle announcements for the transaction. Optional.
            min_coin_amount (int): Minimum coin amount for coin selection. Default is 0.
            max_coin_amount (int): Maximum coin amount for coin selection. Default is 0.
            excluded_coins (list): List of dictionaries representing coins to be excluded from coin selection.
                Each dictionary should contain the following keys:
                - 'parent_coin_info' (str): The parent coin ID.
                - 'puzzle_hash' (str): The puzzle hash of the coin.
                - 'amount' (int): The amount of the coin in mojos.
            excluded_coin_amounts (list): List of excluded coin amounts for coin selection.

        Returns:
            dict: A dictionary containing the signed transaction data.
        """
        # Construct the request payload
        payload = {
            'wallet_id': wallet_id,
            'additions': additions,
            'fee': fee,
            'coins': coins,
            'coin_announcements': coin_announcements,
            'puzzle_announcements': puzzle_announcements,
            'min_coin_amount': min_coin_amount,
            'max_coin_amount': max_coin_amount,
            'excluded_coins': excluded_coins,
            'excluded_coin_amounts': excluded_coin_amounts
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit(
            "create_signed_transaction",
            json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def delete_unconfirmed_transactions(self, wallet_id):
        """
        Delete unconfirmed transactions for a specific wallet.

        Args:
            wallet_id (int): ID of the wallet for which to delete unconfirmed transactions.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'wallet_id': wallet_id
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit(
            "delete_unconfirmed_transactions",
            json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def extend_derivation_index(self, index):
        """
        Extend the derivation index of a wallet.

        Args:
            index (int): The derivation index to extend.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'index': index
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit(
            "extend_derivation_index",
            json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def get_current_derivation_index(self):
        """
        Get the current derivation index for the default wallet.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit(
            "get_current_derivation_index", json.dumps({}))

        # Parse the JSON response and return the result
        return json.loads(result)

    def get_farmed_amount(self):
        """
        Get the total amount of Chia farmed by the default wallet.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit("get_farmed_amount", json.dumps({}))

        # Parse the JSON response and return the result
        return json.loads(result)

    def get_next_address(self, wallet_id, new_address=True):
        """
        Get the next address for receiving Chia payments for a specific wallet.

        Args:
            wallet_id (int): ID of the wallet for which to retrieve the next address.
            new_address (boolean):

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'wallet_id': wallet_id,
            'new_address': new_address
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit("get_next_address", json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def get_spendable_coins(self, wallet_id, min_coin_amount=0, max_coin_amount=0,
                            excluded_coin_amounts=None, excluded_coins=None, excluded_coin_ids=None):
        """
        Get the spendable coins for a specific wallet with optional filtering.

        Args:
            wallet_id (int): ID of the wallet for which to retrieve spendable coins.
            min_coin_amount (int, optional): Minimum amount of Chia coins to include in the result. Defaults to 0.
            max_coin_amount (int, optional): Maximum amount of Chia coins to include in the result. Defaults to 0.
            excluded_coin_amounts (list of int, optional): List of excluded coin amounts. Defaults to None.
            excluded_coins (list of dict, optional): List of excluded coins in the format
                [{'parent_coin_info': 'hex_string', 'puzzle_hash': 'hex_string', 'amount': int}, ...].
                Defaults to None.
            excluded_coin_ids (list of str, optional): List of excluded coin IDs. Defaults to None.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'wallet_id': wallet_id,
            'min_coin_amount': min_coin_amount,
            'max_coin_amount': max_coin_amount,
            'excluded_coin_amounts': excluded_coin_amounts if excluded_coin_amounts else [],
            'excluded_coins': excluded_coins if excluded_coins else [],
            'excluded_coin_ids': excluded_coin_ids if excluded_coin_ids else []
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit(
            "get_spendable_coins", json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def get_transaction(self, transaction_id):
        """
        Get information about a specific transaction.

        Args:
            transaction_id (str): ID of the transaction to retrieve.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'transaction_id': transaction_id
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit("get_transaction", json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def get_wallet_transaction_count(self, wallet_id):
        """
        Get the transaction count for a specific wallet ID.

        Args:
            wallet_id (int): ID of the wallet to retrieve transaction count for.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'wallet_id': wallet_id
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit(
            "get_transaction_count", json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def get_transaction_memo(self, transaction_id):
        """
        Get the memo of a specific transaction.

        Args:
            transaction_id (str): ID of the transaction to retrieve memo for.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'transaction_id': transaction_id
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit(
            "get_transaction_memo", json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def get_transactions(self, wallet_id, start, end, sort_key, reverse):
        """
        Get transactions for a specific wallet ID with pagination and sorting options.

        Args:
            wallet_id (int): ID of the wallet to retrieve transactions for.
            start (int): Starting index of the transactions to retrieve.
            end (int): Ending index of the transactions to retrieve.
            sort_key (str): Key to use for sorting the transactions.
            reverse (bool): Whether to sort the transactions in reverse order.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'wallet_id': wallet_id,
            'start': start,
            'end': end,
            'sort_key': sort_key,
            'reverse': reverse
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit("get_transactions", json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def get_wallet_balance(self, wallet_id):
        """
        Get the balance of a specific wallet ID.

        Args:
            wallet_id (int): ID of the wallet to retrieve balance for.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'wallet_id': wallet_id
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit(
            "get_wallet_balance", json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def send_transaction(self, wallet_id, amount, address, fee, memos=None, min_coin_amount=0, max_coin_amount=0,
                         exclude_coin_amounts=None, exclude_coin_ids=None, reuse_puzhash=True):
        """
        Send a transaction from a specific wallet ID.

        Args:
            wallet_id (int): ID of the wallet to send the transaction from.
            amount (int): Amount of Chia to send in mojo.
            address (str): Recipient address for the transaction.
            fee (int): Fee to include in the transaction in mojo.
            memos (list[str], optional): List of memos to include in the transaction. Defaults to None.
            min_coin_amount (int, optional): Minimum coin amount to use for the transaction. Defaults to 0.
            max_coin_amount (int, optional): Maximum coin amount to use for the transaction. Defaults to 0.
            exclude_coin_amounts (list[int], optional): List of coin amounts to exclude from the transaction.
                Defaults to None.
            exclude_coin_ids (list[str], optional): List of coin IDs to exclude from the transaction. Defaults to None.
            reuse_puzhash (bool, optional): Whether to reuse the puzhash of a previous transaction. Defaults to True.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        # Construct the request payload
        payload = {
            'wallet_id': wallet_id,
            'amount': amount,
            'address': address,
            'fee': fee,
            'memos': memos,
            'min_coin_amount': min_coin_amount,
            'max_coin_amount': max_coin_amount,
            'exclude_coin_amounts': exclude_coin_amounts,
            'exclude_coin_ids': exclude_coin_ids,
            'reuse_puzhash': reuse_puzhash
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit("send_transaction", json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(result)

    def send_transaction_multi(self, wallet_id, additions, fee,
                               coins, coin_announcements=None, puzzle_announcements=None):
        """
        Send transactions to multiple recipients in a single transaction.

        Args:
            wallet_id (int): ID of the wallet to use for sending the transaction.
            additions (list): List of dictionaries representing the recipients of the transaction.
                Each dictionary should contain the following keys:
                - 'amount' (int): The amount to send in mojos (1 XCH = 10^12 mojos).
                - 'puzzle_hash' (str): The puzzle hash of the recipient's address.
            fee (float): The transaction fee to be paid in XCH.
            coins (list): List of coin IDs to use for the transaction. Optional.
            coin_announcements (str): Coin announcements for the transaction. Optional.
            puzzle_announcements (str): Puzzle announcements for the transaction. Optional.

        Returns:
            dict: A dictionary containing the result of the transaction, including the transaction ID and status.
        """
        # Construct the transaction object for send_transaction_multi
        payload = {
            'wallet_id': wallet_id,  # Required
            'additions': additions,  # Required
            'fee': fee,  # Required
            'coins': coins,  # Optional
            'coin_announcements': coin_announcements,  # Optional
            'puzzle_announcements': puzzle_announcements  # Optional
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        response = self.chia_rpc.submit(
            "send_transaction_multi", json.dumps(payload))

        # Parse the JSON response and return the result
        return json.loads(response)


class WalletManagement:
    # TODO Complete Functions
    def __init__(self, url=None, cert=None):
        self.url = url
        self.cert = cert
        self.chia_rpc = ChiaRPC(url, cert)


class WalletNode:
    # TODO Complete Functions
    def __init__(self, url=None, cert=None):
        self.url = url
        self.cert = cert
        self.chia_rpc = ChiaRPC(url, cert)


class DataLayerWallet:
    # TODO Complete Functions
    def __init__(self, url=None, cert=None):
        self.url = url
        self.cert = cert
        self.chia_rpc = ChiaRPC(url, cert)


class NFTWallet:
    # TODO Complete Functions
    def __init__(self, url=None, cert=None):
        self.url = url
        self.cert = cert
        self.chia_rpc = ChiaRPC(url, cert)


class Coins:
    # TODO Complete Functions
    def __init__(self, url=None, cert=None):
        self.url = url
        self.cert = cert
        self.chia_rpc = ChiaRPC(url, cert)
