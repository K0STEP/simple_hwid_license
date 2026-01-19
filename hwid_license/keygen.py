import argparse
from hmac import new
from hashlib import sha256

SECRET = b"MY_KEY"

def generate_license(hwid: str, secret: bytes) -> str:
    """Генерирует лицензионный ключ для заданного HWID."""
    if not hwid or len(hwid) != 16:
        raise ValueError("HWID должен быть строкой из 16 символов")
    signature = new(secret, hwid.encode(), sha256).hexdigest()
    return f"{hwid}.{signature}"

def main():
    parser = argparse.ArgumentParser(description="License key generator for HWID-based protection")
    parser.add_argument("--hwid", required=True, help="Client HWID (16 characters)")
    parser.add_argument("--secret", required=True, help="Secret key (as a string)")
    args = parser.parse_args()
    if len(args.hwid) != 16:
        print("⚠️  HWID must be exactly 16 characters long")
        exit(1)
    try:
        key = generate_license(args.hwid, args.secret)
        print("\n🔑 Generated license key:")
        print(key)
        print("\nSend this key to the client.")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
