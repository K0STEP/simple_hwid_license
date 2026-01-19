from hmac import new
from hashlib import sha256

SECRET = b"MY_KEY"

def generate_license(hwid: str) -> str:
    if not hwid:
        raise ValueError("HWID cannot be empty")
    signature = new(SECRET, hwid.encode(), sha256).hexdigest()
    return f"{hwid}.{signature}"

if __name__ == "__main__":
    hwid = input("Enter client HWID: ").strip().upper()
    if len(hwid) != 16:
        print("⚠️  HWID must be exactly 16 characters long")
    else:
        key = generate_license(hwid)
        print("\n🔑 Generated license key:")
        print(key)
        print("\nSend this key to the client.")

