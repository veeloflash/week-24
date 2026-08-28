import hashlib
import hmac
import secrets

def hash_password(password: str):
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)
    return f"{salt.hex()}${digest.hex()}"

def verify_password(password: str, stored_hash: str):
    try:
        salt_hex, digest_hex = stored_hash.split("$", 1)
        expected = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), bytes.fromhex(salt_hex), 200_000
        ).hex()
    except (ValueError, TypeError):
        return False
    return hmac.compare_digest(expected, digest_hex)
