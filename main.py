import os
import sys
import hashlib
import hmac
import subprocess
import uuid

SECRET = b"MY_KEY"
LICENSE_FILE = "license.key"


def get_cur_hwid() -> str:
    """
    :return: MAC-adress
    """
    mac = hex(uuid.getnode())[2:].upper()
    return mac


def validate_lic(lic_key: str, cur_hwid: str) -> bool:
    """
    check license key
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
    main body
    """
    cur_hwid = get_cur_hwid()
    if not os.path.exists(LICENSE_FILE):
        print("🔒 Программа не активирована.")
        print(f"Ваш HWID: {cur_hwid}")
        print("Отправьте этот HWID разработчику и получите лицензионный ключ.\n")
        key = input("Введите лицензионный ключ: ").strip()
        with open(LICENSE_FILE, "w") as f:
            f.write(key)
    else:
        with open(LICENSE_FILE, "r") as f:
            key = f.read().strip()

    if not validate_lic(key, cur_hwid):
        print("❌ Ошибка: неверный ключ или лицензия привязана к другому устройству!")

    print("✅ Лицензия активирована! Запуск программы...")
    input()

if __name__ == "__main__":
    main()
