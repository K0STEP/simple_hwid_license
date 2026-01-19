import os
import hashlib
import hmac
import uuid

SECRET = b"MY_KEY"
LICENSE_FILE = "license.key"


def get_cur_hwid() -> str:
    """
    :return: MAC address
    """
    mac = hex(uuid.getnode())[2:].upper()
    return mac


def validate_lic(lic_key: str, cur_hwid: str) -> bool:
    """
    Check license key
    :param lic_key: license key from LICENSE_FILE
    :param cur_hwid: current hwid
    :return: TRUE if lic_key is correct
    """
    hwid_from_key, signature = lic_key.rsplit(".", 1)
    if hwid_from_key != cur_hwid:
        return False
    expected_sig = hmac.new(SECRET, hwid_from_key.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected_sig)


def main():
    """
    Main body
    """
    cur_hwid = get_cur_hwid()
    if not os.path.exists(LICENSE_FILE):
        print("🔒 Program is not activated.")
        print(f"Your HWID: {cur_hwid}")
        print("Send this HWID to the developer and obtain a license key.\n")
        key = input("Enter license key: ").strip()
        with open(LICENSE_FILE, "w") as f:
            f.write(key)
    else:
        with open(LICENSE_FILE, "r") as f:
            key = f.read().strip()

    if not validate_lic(key, cur_hwid):
        print("❌ Error: invalid key or license is bound to another device!")

    print("✅ License activated! Launching program...")
    input()


if __name__ == "__main__":
    main()