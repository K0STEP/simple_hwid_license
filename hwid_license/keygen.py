import argparse
from hmac import new
from hashlib import sha256

SECRET = b"MY_KEY"

def generate_license(hwid: str, secret: bytes) -> str:
    """Generates a license key for the given HWID."""
    signature = new(secret, hwid.encode(), sha256).hexdigest()
    return f"{hwid}.{signature}"

def main():
    parser = argparse.ArgumentParser(description="License key generator for HWID-based protection")
    parser.add_argument("--hwid", required=True, help="Client HWID (16 characters)")
    parser.add_argument("--secret", required=True, help="Secret key (as a string)")
    args = parser.parse_args()
    try:
        key = generate_license(args.hwid, args.secret.encode())
        print("\n🔑 Generated license key:")
        print(key)
        print("\nSend this key to the client.")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()