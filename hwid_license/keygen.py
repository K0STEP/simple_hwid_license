import argparse
from hmac import new
from hashlib import sha256

SECRET = b"MY_KEY"

def generate_license(hwid: str, secret: bytes) -> str:
    """Генерирует лицензионный ключ для заданного HWID."""
    signature = new(secret, hwid.encode(), sha256).hexdigest()
    return f"{hwid}.{signature}"

def main():
    parser = argparse.ArgumentParser(description="Генератор лицензионных ключей для HWID-защиты")
    parser.add_argument("--hwid", required=True, help="HWID клиента (16 символов)")
    parser.add_argument("--secret", required=True, help="Секретный ключ (в виде строки)")
    args = parser.parse_args()
    try:
        key = generate_license(args.hwid, args.secret.encode())
        print("\n🔑 Сгенерированный лицензионный ключ:")
        print(key)
        print("\nОтправьте этот ключ клиенту.")
    except Exception as e:
        print(f"Ошибка: {e}")
        exit(1)

if __name__ == "__main__":
    main()