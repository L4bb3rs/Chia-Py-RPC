# Chia-Py-RPC

Chia-Py-RPC is a Python library that provides a convenient way to interact with the Chia blockchain using the Chia RPC (Remote Procedure Call) protocol. It allows you to send transactions, check balances, and perform other Chia-related operations programmatically from Python.

## Features

- Send transactions to multiple recipients in a single transaction
- Check wallet balances and transaction history
- Get information about Chia blocks, coins, and transactions
- Create and manage Chia wallets
- Simple and easy-to-use
- Plus every RPC method avaliable in Chia Client 1.7.0 or previous.

## Installation

To install Chia-Py-RPC, you can use `pip`, the Python package manager. Open a terminal and run the following command:

```bash
pip install chia-py-rpc
```

## Usage
Here's an example of how you can use Chia-Py-RPC to send transactions to multiple recipients in a single transaction:

```
from chia_py_rpc.wallet import Wallet

# Create an instance of Wallet
chia_wallet = Wallet()

# Specify the wallet ID, additions (recipients), fee, and optional parameters
wallet_id = 1
additions = [
    {'amount': 1000000000000, 'puzzle_hash': '0x...'},  # Recipient 1
    {'amount': 500000000000, 'puzzle_hash': '0x...'},  # Recipient 2
]
fee = 0.00001
coins = None
coin_announcements = None
puzzle_announcements = None

# Call the send_transaction_multi method to send the transaction
result = chia_wallet.send_transaction_multi(wallet_id, additions, fee, coins, coin_announcements, puzzle_announcements)

# Parse the result and handle the transaction ID and status
transaction_id = result['transaction_id']
status = result['status']
print(f"Transaction ID: {transaction_id}")
print(f"Status: {status}")
```

For more examples and documentation, please refer to the official documentation.

## Contributing
If you would like to contribute to Chia-Py-RPC, please open an issue or submit a pull request on GitHub. We welcome any contributions, including bug fixes, feature enhancements, and documentation improvements.

## License
Chia-Py-RPC is open-source software licensed under the MIT License.

## Acknowledgements
Chia-Py-RPC is not affilated with the Chia Network in any way and it purely to provide a simple method of utlising Chia RPC in python.
