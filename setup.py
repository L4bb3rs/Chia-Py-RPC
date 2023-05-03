from setuptools import setup
import wallet
import rpc_connect

setup(
    name="Chia-Py-RPC", 
    version="0.0.1", 
    description="Chia-Py-RPC is a Python library that provides a convenient way to interact with the Chia blockchain using the Chia RPC (Remote Procedure Call) protocol. It allows you to send transactions, check balances, and perform other Chia-related operations programmatically from Python.",
    packages=[wallet,rpc_connect],
    install_requires=["json","urllib3","os","requests"]
    )
