from hwid_license.core import HWIDL

def main():
    ...

if __name__ == "__main__":
    lic = HWIDL(secret=b'MY_KEY', license_file="license.key")
    lic.check_valid()
    main()
