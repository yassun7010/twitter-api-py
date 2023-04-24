import base64
import hashlib
import os
import random
import re
import string
from time import time

UNICODE_ASCII_CHARACTER_SET = string.ascii_letters + string.digits


def generate_token(length=30, chars=UNICODE_ASCII_CHARACTER_SET) -> str:
    rand = random.SystemRandom()
    return "".join(rand.choice(chars) for _ in range(length))


def generate_timestamp() -> str:
    return str(int(time()))


def generate_code_verifier() -> str:
    code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
    return re.sub("[^a-zA-Z0-9]+", "", code_verifier)


def generate_code_challenge(code_verifier: str) -> str:
    """
    Create S256 code_challenge with the given code_verifier.
    """

    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")

    return code_challenge.replace("=", "")
