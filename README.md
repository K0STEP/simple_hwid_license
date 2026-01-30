# 🔐 Simple HWID License

**Simple HWID License** is a lightweight and easy-to-use library for protecting Python applications with hardware-bound licensing (HWID-based).  
It allows you to quickly add license protection to your software and sell activation keys to your customers.

> ⚠️ **Important**: This system provides **basic copy protection** against casual sharing. It is **not secure against reverse engineering or determined attackers**, but it’s perfect for indie projects, educational tools, small commercial apps, or internal utilities.

---

## 📦 Installation

Just copy the `hwid_license/` folder into your project root.  
No external dependencies are required — only Python’s standard library.

Project structure:
```
your_project/
├── hwid_license/
│   ├── __init__.py
│   ├── core.py
│   └── keygen.py
├── main.py          ← your application
└── ...              ← other files
```

---

## 🛠️ How to integrate into your app

1. **Import the `HWIDL` class** in your `main.py`:
   ```python
   from hwid_license.core import HWIDL
   ```

2. **Create an instance with your secret key**:
   ```python
   lic = HWIDL(secret=b"MY_SUPER_SECRET_123", license_file="myapp.lic")
   ```

   - `secret` — your **private secret key** (must be identical during key generation and validation).
   - `license_file` — filename to store the license (default: `"license.key"`).

3. **Call the license check before running your main logic**:
   ```python
   def main():
       # Your application code here
       pass

   if __name__ == "__main__":
       lic.check_valid()  # ← prompts for key if not activated
       main()
   ```

4. **(Optional) Build a standalone .exe** using PyInstaller:
   ```bash
   pip install pyinstaller
   pyinstaller --onefile main.py
   ```

---

## 🔑 License issuance workflow

### Step 1: User runs the program
- The app detects the device’s **HWID** (based on MAC address).
- If no valid license file exists, it shows:
  ```
  🔒 Program is not activated.
  Your HWID: A1B2C3D4E5F67890
  Send this HWID to the developer and obtain a license key.
  ```

### Step 2: User sends HWID to you (the developer)
- Via email, Telegram, web form, etc.

### Step 3: You generate a license key
Run the key generator from your project directory:
```bash
python hwid_license/keygen.py --hwid A1B2C3D4E5F67890 --secret "MY_SUPER_SECRET_123"
```

> 💡 The HWID must be **exactly 16 uppercase alphanumeric characters**.

Example output:
```
🔑 Generated license key:
A1B2C3D4E5F67890.8f3a1d...c9e2b7

Send this key to the client.
```

### Step 4: You send the key to the user
The user enters it on next launch → license is saved → app starts.

### Step 5: Validation on every launch
- Reads the saved license key.
- Compares the embedded HWID with the current device’s HWID.
- Verifies the HMAC-SHA256 signature using your secret.
- If everything matches — the app runs.

---

## 🔐 Protection algorithm

1. **HWID is generated as**:
   ```
   HWID = first 16 chars of SHA256(MAC address) in uppercase
   ```

2. **License key format**:
   ```
   <HWID>.<HMAC-SHA256(HWID, secret)>
   ```
   Example:
   ```
   A1B2C3D4E5F67890.8f3a1d5e9c0b7a2f4e6d8c9a1b3e5f7d0c2a4b6e8f0d2c4a6b8e0f2
   ```

3. **Validation**:
   - Splits the key into HWID and signature.
   - Recomputes the expected signature using your secret.
   - Uses `hmac.compare_digest()` for timing-safe comparison.

---

## 🧪 Usage example

File `main.py`:
```python
from hwid_license.core import HWIDL

def main():
    ...

if __name__ == "__main__":
    lic = HWIDL(secret=b'MY_KEY', license_file="license.key")
    lic.check_valid()
    main()
```

> Replace `b'MY_KEY'` with your own secret (as a byte string).  
> The default license file is `license.key`, but you can use any name.

---

## ❗ Limitations & recommendations

- **Never commit your `secret` to public repositories**.
- **HWID may change** if the user replaces their network card, uses WSL, Docker, or certain VMs.
- For stronger protection:
  - Use **code obfuscation** (e.g., `pyarmor`)
  - Add **online activation** via a simple web API
  - Combine with other anti-piracy measures
