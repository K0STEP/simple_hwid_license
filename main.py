import os
import sys
import hashlib
import hmac
import subprocess
import uuid

SECRET = b"my_pizdatiy_key"
LICENSE_FILE = "license.key"

def get_cur_hwid() -> str:
    """
    :return: MAC-adress
    """
    mac = hex(uuid.getnode())[2:].upper()
    return mac
