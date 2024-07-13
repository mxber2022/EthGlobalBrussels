import os

# Alice
CONFIG_PARTY_1 = {
    "userkey_file": os.getenv("NILLION_USERKEY_PATH_PARTY_1"),
    "nodekey_file": os.getenv("NILLION_NODEKEY_PATH_PARTY_1"),
    "nodekey_alternate_file": os.getenv("NILLION_NODEKEY_PATH_PARTY_4"),
    "party_name": "Alice",
    "secret_name": "alice_feedback",
    "secret_value": 9,
}

# Bob and Charlie
CONFIG_N_PARTIES = [
    {
        "userkey_file": os.getenv("NILLION_USERKEY_PATH_PARTY_2"),
        "nodekey_file": os.getenv("NILLION_NODEKEY_PATH_PARTY_2"),
        "party_name": "Bob",
        "secret_name": "bob_feedback",
        "secret_value": 8,
    },
    {
        "userkey_file": os.getenv("NILLION_USERKEY_PATH_PARTY_3"),
        "nodekey_file": os.getenv("NILLION_NODEKEY_PATH_PARTY_3"),
        "party_name": "Charlie",
        "secret_name": "charlie_feedback",
        "secret_value": 7,
    },
]
