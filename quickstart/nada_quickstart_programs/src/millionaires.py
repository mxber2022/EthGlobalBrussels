from nada_dsl import *


def nada_main():
    alice = Party(name="Alice")  # party 0
    bob = Party(name="Bob")  # party 1
    charlie = Party(name="Charlie")  # party 2

    alice_fed = SecretInteger(Input(name="alice_feedback", party=alice))
    bob_fed = SecretInteger(Input(name="bob_feedback", party=bob))
    charlie_fed = SecretInteger(Input(name="charlie_feedback", party=charlie))

    largest_position = (alice_fed + bob_fed + charlie_fed)

    out = Output(largest_position, "largest_position", alice)

    return [out]