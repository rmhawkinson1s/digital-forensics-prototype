import json

def load_known_hashes():
    with open("known_hashes.json", "r") as f:
        return json.load(f)


def check_hash(hash_value):
    known_hashes = load_known_hashes()

    if hash_value in known_hashes:
        return f"Match Found: {known_hashes[hash_value]}"
    else:
        return "No Match Found"
