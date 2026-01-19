import os
import sys
import hashlib
import hmac
import uuid

class HWIDL:
    def __init__(self, secret: bytes, license_file: str = "license.key"):
        self.secret = secret
        self.license_file = license_file

    def get_hwid(self) -> str:
        mac = hex(uuid.getnode())[2:].upper()
        return mac

    def validate(self) -> bool:
        if not os.path.exists(self.license_file):
            return False
        with open(self.license_file, "r") as f:
            lic_key = f.read().strip()
        cur_hwid = self.get_hwid()
        hwid_from_key, signature = lic_key.rsplit(".", 1)
        if hwid_from_key != cur_hwid:
            return False
        expected_sig = hmac.new(self.secret, hwid_from_key.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(signature, expected_sig)

    def check_valid(self):
        if not self.validate():
            print("🔒 Program is not activated.")
            print(f"Your HWID: {self.get_hwid()}")
            print("Send this HWID to the developer and obtain a license key.\n")
            key = input("Enter license key: ").strip()
            with open(self.license_file, "w") as f:
                f.write(key)
            if not self.validate():
                print("❌ Ошибка: неверный ключ или лицензия привязана к другому устройству!")
                if os.path.exists(self.license_file):
                    os.remove(self.license_file)
                sys.exit(1)
            print("✅ Лицензия активирована!")



