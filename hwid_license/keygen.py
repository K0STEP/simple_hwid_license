# key_gen.py
import argparse
from datetime import datetime, timedelta
from hmac import new
from hashlib import sha256

def generate_license(hwid: str, secret: bytes, days: int = 30) -> str:
    """Generates a time-limited license key."""
    expires_at = (datetime.now() + timedelta(days=days)).strftime("%Y%m%d")
    payload = f"{hwid}.{expires_at}"
    signature = new(secret, payload.encode(), sha256).hexdigest()
    return f"{payload}.{signature}"

def main():
    parser = argparse.ArgumentParser(description="Time-limited license key generator")
    parser.add_argument("--hwid", required=True, help="Client HWID (16 characters)")
    parser.add_argument("--secret", required=True, help="Secret key (as string)")
    parser.add_argument("--days", type=int, default=30, help="License validity in days (default: 30)")
    args = parser.parse_args()
    try:
        key = generate_license(args.hwid, args.secret.encode(), args.days)
        print(f"\n🔑 Generated license (valid {args.days} days):")
        print(key)
        print("\nSend this key to the client.")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()