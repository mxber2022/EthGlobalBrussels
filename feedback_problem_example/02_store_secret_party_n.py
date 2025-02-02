import asyncio
import argparse
import py_nillion_client as nillion
import os
import pytest
import json
from web3 import Web3, EthereumTesterProvider
from py_nillion_client import NodeKey, UserKey
from dotenv import load_dotenv
from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

from config import CONFIG_N_PARTIES
from nillion_python_helpers import get_quote_and_pay, create_nillion_client, create_payments_config

home = os.getenv("HOME")
load_dotenv(f"{home}/.config/nillion/nillion-devnet.env")

# Bob and Charlie store their salaries in the network
async def main(args=None):
    parser = argparse.ArgumentParser(
        description="Create a secret on the Nillion network with set read/retrieve permissions"
    )
    parser.add_argument(
        "--user_id_1",
        required=True,
        type=str,
        help="User ID of the user who will compute with the secret being stored",
    )
    parser.add_argument(
        "--program_id",
        required=True,
        type=str,
        help="Program ID of the millionaires program",
    )

    args = parser.parse_args(args)

    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    grpc_endpoint = os.getenv("NILLION_NILCHAIN_GRPC")
    chain_id = os.getenv("NILLION_NILCHAIN_CHAIN_ID")
    # start a list of store ids to keep track of stored secrets
    store_ids = []
    party_ids = []

    for party_info in CONFIG_N_PARTIES:
        party_seed = party_info["party_name"] + "_seed"
        client_n = create_nillion_client(
            UserKey.from_seed(party_seed),
            NodeKey.from_seed(party_seed),
        )
        party_id_n = client_n.party_id
        user_id_n = client_n.user_id

        payments_config_n = create_payments_config(chain_id, grpc_endpoint)
        payments_client_n = LedgerClient(payments_config_n)
        payments_wallet_n = LocalWallet(
            PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))),
            prefix="nillion",
        )

        party_name = party_info["party_name"]
        secret_name = party_info["secret_name"]
        secret_value = party_info["secret_value"]

        # Create a secret for the current party
        stored_secret = nillion.NadaValues(
            {secret_name: nillion.SecretInteger(secret_value)}
        )

        # Create permissions object with default permissions for the current user
        permissions = nillion.Permissions.default_for_user(user_id_n)

        # Give compute permissions to Alice so she can use the secret in the specific millionionaires program by program id
        compute_permissions = {
            args.user_id_1: {args.program_id},
        }
        permissions.add_compute_permissions(compute_permissions)
        print(
            f"\n👍 {party_name} gives compute permissions on their secret to Alice's user_id: {args.user_id_1}"
        )

        receipt_store = await get_quote_and_pay(
            client_n,
            nillion.Operation.store_values(stored_secret, ttl_days=5),
            payments_wallet_n,
            payments_client_n,
            cluster_id,
        )
        # Store the permissioned secret
        store_id = await client_n.store_values(
            cluster_id, stored_secret, permissions, receipt_store
        )

        store_ids.append(store_id)
        party_ids.append(party_id_n)

        infura_url = 'https://sepolia.infura.io/v3/e96abcff2f494bcd81fadc53c8fd6ac9'
        # zircuit - https://zircuit1.p2pify.com/
        # base sepolia - https://sepolia.base.org
        web3 = Web3(Web3.HTTPProvider(infura_url))
        network_id = web3.net.version 
        print(f"Connected to network with ID: {network_id}")
        contract_address = '0xA7d8553FeF67Bcb187FCD6F76cf672a4e6B40262'
        contract_abi = json.loads('''
[
    {
        "inputs": [],
        "name": "getUUIDs",
        "outputs": [
            {
                "internalType": "string[]",
                "name": "",
                "type": "string[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "_uuid",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "_secretName",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "_partyName",
                "type": "string"
            }
        ],
        "name": "addRecord",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "_uuid",
                "type": "string"
            }
        ],
        "name": "getRecord",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "_uuid",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "_newSecretName",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "_newPartyName",
                "type": "string"
            }
        ],
        "name": "updateRecord",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]'''
)
        contract = web3.eth.contract(address=contract_address, abi=contract_abi)
        transaction = contract.functions.addRecord(store_id, secret_name, party_name).build_transaction({
        'from': "0x7199D548f1B30EA083Fe668202fd5E621241CC89",
        'nonce': web3.eth.get_transaction_count("0x7199D548f1B30EA083Fe668202fd5E621241CC89"),
        'gas': 2000000,
        'gasPrice': web3.to_wei('50', 'gwei')
        })
        signed_tx = web3.eth.account.sign_transaction(transaction, "d2ab6e77539c6d2ba90f19b217e26e4fad301e5066445514b4b63cba0fc80b6c")
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        web3.eth.wait_for_transaction_receipt(tx_hash)

        print(
            f"\n🎉 {party_name} stored {secret_name}: {secret_value} at store id: {store_id}"
        )

    party_ids_to_store_ids = " ".join(
        [f"{party_id}:{store_id}" for party_id, store_id in zip(party_ids, store_ids)]
    )

    print(
        "\n📋⬇️  Copy and run the following command to run multi party computation using the secrets"
    )
    print(
        f"\npython3 03_multi_party_compute.py --program_id {args.program_id} --party_ids_to_store_ids {party_ids_to_store_ids}"
    )
    return [args.program_id, party_ids_to_store_ids]


if __name__ == "__main__":
    asyncio.run(main())


@pytest.mark.asyncio
async def test_main():
    pass



