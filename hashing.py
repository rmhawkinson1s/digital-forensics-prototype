import hashlib
import json
import datetime

def compute_hash(file_path, algorithm="sha256"):
    hash_func = hashlib.new(algorithm)

    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            hash_func.update(chunk)

    return hash_func.hexdigest()


def create_manifest(file_path):
    manifest = {
        "file": file_path,
        "md5": compute_hash(file_path, "md5"),
        "sha1": compute_hash(file_path, "sha1"),
        "sha256": compute_hash(file_path, "sha256"),
        "timestamp": str(datetime.datetime.now())
    }

    with open("manifest.json", "w") as f:
        json.dump(manifest, f, indent=4)

    print("Manifest created.")


def verify_file(file_path):
    with open("manifest.json", "r") as f:
        manifest = json.load(f)

    current_sha256 = compute_hash(file_path, "sha256")

    if current_sha256 == manifest["sha256"]:
        result = "Integrity Verified"
    else:
        result = "File Modified - Integrity Compromised"

    log_verification(result)
    print(result)


def log_verification(status):
    with open("chain_of_custody.log", "a") as log:
        log.write(f"{datetime.datetime.now()} - {status}\n")
