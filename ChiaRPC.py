import json
import urllib3
import os
import requests

class ChiaRPC:
    def __init__(self, url=None, cert=None):
        default_url = "https://localhost:9256/"
        default_cert = (
            os.path.expanduser('~\\.chia\\mainnet\\config\\ssl\\full_node\\private_full_node.crt'),
            os.path.expanduser('~\\.chia\\mainnet\\config\\ssl\\full_node\\private_full_node.key')
        )

        self.url = url or default_url
        self.cert = cert or default_cert
        self.headers = {"Content-Type": "application/json"}
        urllib3.disable_warnings()

    def submit(self, chia_call, data):
        """Submit data to the specified URL"""
        response = requests.post(self.url + chia_call, data=data, headers=self.headers, cert=self.cert, verify=False)
        response_text = response.text
        response_json = json.loads(response_text)
        return json.dumps(response_json, indent=4, sort_keys=True)

class CatWallet:
    def __init__(self, url=None, cert=None):
        self.url = url
        self.cert = cert
        self.chia_rpc = ChiaRPC(url, cert)
    
    def cancel_offers(self, batch_fee=0, secure=True, batch_size=5, cancel_all=False, asset_id="xch"):
        """Cancel offers category"""
        data = {
            "batch_fee": batch_fee,
            "secure": secure,
            "batch_size": batch_size,
            "cancel_all": cancel_all,
            "asset_id": asset_id.lower()
        }
        result =self.chia_rpc.submit("cancel_offers", json.dumps(data))
        return json.loads(result)

    def cat_asset_id_to_name(self, asset_id):
        """Retrieve asset name by asset ID"""
        data = {"asset_id": asset_id}
        result =self.chia_rpc.submit("cat_asset_id_to_name", json.dumps(data))
        return json.loads(result)

    def cancel_offer(self, offer_id):
        """Cancel a CAT Wallet offer by offer_id"""
        data = {"offer_id": offer_id}
        result =self.chia_rpc.submit("cancel_offer", json.dumps(data))
        return json.loads(result)
    
    def cat_get_asset_id(self, wallet_id):
        """Get the asset_id for a given asset_name in CAT Wallet"""
        data = {"wallet_id": wallet_id}
        result =self.chia_rpc.submit("cat_get_asset_id", json.dumps(data))
        return json.loads(result)
    
    def cat_get_name(self, wallet_id):
        """Get the asset_name for a given asset_id in CAT Wallet"""
        data = {"wallet_id": wallet_id}
        result =self.chia_rpc.submit("cat_get_name", json.dumps(data))
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
        result =self.chia_rpc.submit("cat_set_name", json.dumps(data))
        return json.loads(result)
    
    def cat_spend(self, wallet_id, coins, amount, fee, inner_address, memos, min_coin_amount, max_coin_amount, exclude_coin_amounts, exclude_coin_ids, reuse_puzhash):
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
        result =self.chia_rpc.submit("cat_spend", json.dumps(data))
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
        result =self.chia_rpc.submit("check_offer_validity", json.dumps(data))
        return json.loads(result)
    
    def create_offer_for_ids(self, offer, fee, validate_only, driver_dict, min_coin_amount, max_coin_amount, solver, reuse_puzhash):
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
        result =self.chia_rpc.submit("create_offer_for_ids", json.dumps(data))
        return json.loads(result)

    def get_all_offers(self, start, end, exclude_my_offers, exclude_taken_offers, include_completed, sort_key, reverse, file_contents):
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
        result =self.chia_rpc.submit("get_all_offers", json.dumps(data))
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
        result =self.chia_rpc.submit("get_offer", json.dumps(data))
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
        result =self.chia_rpc.submit("get_offer_summary", json.dumps(data))
        return json.loads(result)

    def get_offers_count(self):
        """Retrieves the count of all offers in CAT Wallet.

        Returns:
            dict: Response from the RPC
        """
        data = {}
        result =self.chia_rpc.submit("get_offers_count", json.dumps(data))
        return json.loads(result)

    def get_stray_cats(self):
        """Get a list of all unacknowledged CATs.

        Returns:
            dict: Response from the RPC call
        """
        data = {}
        result =self.chia_rpc.submit("get_stray_cats", json.dumps(data))
        return json.loads(result)
    
    def select_coins(self, wallet_id, amount, min_coin_amount, excluded_coins=None, max_coin_amount=None, exclude_coin_amounts=None):
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
        result =self.chia_rpc.submit("select_coins", json.dumps(data))
        return json.loads(result)

    def take_offer(self, offer, fee, min_coin_amount, max_coin_amount=None, solver=None, reuse_puzhash=True):
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
        result =self.chia_rpc.submit("take_offer", json.dumps(data))
        return json.loads(result)

#currently has functions from CatWallet
class DidWallet:
    def __init__(self, url=None, cert=None):
        self.url = url
        self.cert = cert
        self.chia_rpc = ChiaRPC(url, cert)
        
    def cancel_offers(self, batch_fee=0, secure=True, batch_size=5, cancel_all=False, asset_id="xch"):
        """Cancel offers category"""      
        data = {
            "batch_fee": batch_fee,
            "secure": secure,
            "batch_size": batch_size,
            "cancel_all": cancel_all,
            "asset_id": asset_id.lower()
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit("cancel_offers", json.dumps(data))

        # Parse the JSON response and return the result
        return json.loads(result)

    def cat_asset_id_to_name(self, asset_id):
        """Retrieve asset name by asset ID"""
        data = {"asset_id": asset_id}
        result =self.chia_rpc.submit("cat_asset_id_to_name", json.dumps(data))
        return json.loads(result)

    def cancel_offer(self, offer_id):
        """Cancel a CAT Wallet offer by offer_id"""
        data = {"offer_id": offer_id}
        result =self.chia_rpc.submit("cancel_offer", json.dumps(data))
        return json.loads(result)
    
    def cat_get_asset_id(self, wallet_id):
        """Get the asset_id for a given asset_name in CAT Wallet"""
        data = {"wallet_id": wallet_id}
        result =self.chia_rpc.submit("cat_get_asset_id", json.dumps(data))
        return json.loads(result)
    
    def cat_get_name(self, wallet_id):
        """Get the asset_name for a given asset_id in CAT Wallet"""
        data = {"wallet_id": wallet_id}
        result =self.chia_rpc.submit("cat_get_name", json.dumps(data))
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
        result =self.chia_rpc.submit("cat_set_name", json.dumps(data))
        return json.loads(result)
    
    def cat_spend(self, wallet_id, coins, amount, fee, inner_address, memos, min_coin_amount, max_coin_amount, exclude_coin_amounts, exclude_coin_ids, reuse_puzhash):
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
        result =self.chia_rpc.submit("cat_spend", json.dumps(data))
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
        result =self.chia_rpc.submit("check_offer_validity", json.dumps(data))
        return json.loads(result)
    
    def create_offer_for_ids(self, offer, fee, validate_only, driver_dict, min_coin_amount, max_coin_amount, solver, reuse_puzhash):
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
        result =self.chia_rpc.submit("create_offer_for_ids", json.dumps(data))
        return json.loads(result)

    def get_all_offers(self, start, end, exclude_my_offers, exclude_taken_offers, include_completed, sort_key, reverse, file_contents):
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
        result =self.chia_rpc.submit("get_all_offers", json.dumps(data))
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
        result =self.chia_rpc.submit("get_offer", json.dumps(data))
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
        result =self.chia_rpc.submit("get_offer_summary", json.dumps(data))
        return json.loads(result)

    def get_offers_count(self):
        """Retrieves the count of all offers in CAT Wallet.

        Returns:
            dict: Response from the RPC
        """
        data = {}
        result =self.chia_rpc.submit("get_offers_count", json.dumps(data))
        return json.loads(result)

    def get_stray_cats(self):
        """Get a list of all unacknowledged CATs.

        Returns:
            dict: Response from the RPC call
        """
        data = {}
        result =self.chia_rpc.submit("get_stray_cats", json.dumps(data))
        return json.loads(result)
    
    def select_coins(self, wallet_id, amount, min_coin_amount, excluded_coins=None, max_coin_amount=None, exclude_coin_amounts=None):
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
        result =self.chia_rpc.submit("select_coins", json.dumps(data))
        return json.loads(result)

    def take_offer(self, offer, fee, min_coin_amount, max_coin_amount=None, solver=None, reuse_puzhash=True):
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
        result =self.chia_rpc.submit("take_offer", json.dumps(data))
        return json.loads(result)

#currently has 1 functions from Wallet
class Wallet:
    def __init__(self, url=None, cert=None):
        self.url = url
        self.cert = cert
        self.chia_rpc = ChiaRPC(url, cert)
           
    def send_transaction_multi(self, wallet_id, additions, fee, coins, coin_announcements=None, puzzle_announcements=None):
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
        transaction = {
            'wallet_id': wallet_id,  # Required
            'additions': additions,  # Required
            'fee': fee,  # Required
            'coins': coins,  # Optional
            'coin_announcements': coin_announcements,  # Optional
            'puzzle_announcements': puzzle_announcements  # Optional
        }

        # Use the submit method of ChiaRPC instance to make the Chia RPC call
        result = self.chia_rpc.submit("send_transaction_multi", json.dumps(transaction))

        # Parse the JSON response and return the result
        return json.loads(result)



# # Create an instance of ChiaClient
# catwallet = CatWallet()
# for n in range(1, 100):
#     wallet_name = catwallet.cat_get_name(n)
#     print(wallet_name)
