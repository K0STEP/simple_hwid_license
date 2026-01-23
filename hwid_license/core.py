# core.py
import os
import sys
import hashlib
import hmac
import uuid
from datetime import datetime

class HWIDL:
    def __init__(self, secret: bytes, license_file: str = "license.key"):
        self.secret = secret
        self.license_file = license_file

    def get_hwid(self) -> str:
        mac = hex(uuid.getnode())[2:].upper()
        return hashlib.sha256(mac.encode()).hexdigest()[:16].upper()

    def validate(self) -> bool:
        if not os.path.exists(self.license_file):
            return False

        with open(self.license_file, "r") as f:
            lic_key = f.read().strip()

        parts = lic_key.split(".")
        if len(parts) != 3:
            return False

        hwid_from_key, expires_str, signature = parts

        # Проверка HWID
        current_hwid = self.get_hwid()
        if hwid_from_key != current_hwid:
            return False

        # Проверка срока действия
        try:
            expires_date = datetime.strptime(expires_str, "%Y%m%d").date()
            if datetime.now().date() > expires_date:
                return False
        except ValueError:
            return False  # Неверный формат даты

        # Проверка подписи
        payload = f"{hwid_from_key}.{expires_str}"
        expected_sig = hmac.new(self.secret, payload.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected_sig):
            return False

        return True

    def check_valid(self):
        if not self.validate():
            print("🔒 Program is not activated or license has expired.")
            print(f"Your HWID: {self.get_hwid()}")
            print("Send this HWID to the developer to get a new license key.\n")
            key = input("Enter license key: ").strip()
            with open(self.license_file, "w") as f:
                f.write(key)
            if not self.validate():
                print("❌ Error: invalid key, wrong device, or expired license!")
                if os.path.exists(self.license_file):
                    os.remove(self.license_file)
                sys.exit(1)
        print("✅ License is valid!")