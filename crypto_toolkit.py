import base64
from Crypto.Cipher import AES, DES, DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


# =========================
# SAFE INPUT
# =========================
def safe_input(prompt):
    while True:
        try:
            s = input(prompt)
            return s
        except KeyboardInterrupt:
            print("\n(Hủy - nhập 0 để quay lại)")
            return "0"


# =========================
# CONFIG ALGORITHMS
# =========================
ALGORITHMS = {
    "AES": {"cipher": AES, "block": 16, "keygen": lambda: get_random_bytes(16)},
    "DES": {"cipher": DES, "block": 8, "keygen": lambda: get_random_bytes(8)},
    "3DES": {
        "cipher": DES3,
        "block": 8,
        "keygen": lambda: DES3.adjust_key_parity(get_random_bytes(24)),
    },
}


# =========================
# CORE FUNCTIONS
# =========================
def encrypt(plaintext, key, algo):
    cipher = algo["cipher"].new(key, algo["cipher"].MODE_CBC)
    ct = cipher.encrypt(pad(plaintext.encode(), algo["block"]))
    return base64.b64encode(cipher.iv + ct).decode()


def decrypt(ciphertext, key, algo):
    data = base64.b64decode(ciphertext)
    iv = data[: algo["block"]]
    cipher = algo["cipher"].new(key, algo["cipher"].MODE_CBC, iv=iv)
    pt = unpad(cipher.decrypt(data[algo["block"] :]), algo["block"])
    return pt.decode()


def input_key():
    while True:
        k = safe_input("Enter key (Base64) (0 để quay lại): ")
        if k == "0":
            return None
        try:
            return base64.b64decode(k)
        except:
            print("Key không hợp lệ!")


def print_key(key):
    print("Key:", base64.b64encode(key).decode())


# =========================
# GENERIC MENU
# =========================
def crypto_menu(name, algo):
    while True:
        print(f"\n=== {name} MENU ===")
        print("1. Encrypt")
        print("2. Decrypt")
        print("0. Back")

        choice = safe_input("Choose: ")

        if choice == "1":
            text = safe_input("Plaintext (0 để hủy): ")
            if text == "0":
                continue

            opt = safe_input("1.Random key | 2.Enter key: ")

            if opt == "1":
                key = algo["keygen"]()
                print_key(key)
            else:
                key = input_key()
                if key is None:
                    continue

            print("Ciphertext:", encrypt(text, key, algo))

        elif choice == "2":
            ct = safe_input("Ciphertext (0 để hủy): ")
            if ct == "0":
                continue

            key = input_key()
            if key is None:
                continue

            try:
                print("Plaintext:", decrypt(ct, key, algo))
            except:
                print("❌ Decryption failed!")

        elif choice == "0":
            return


# =========================
# MAIN
# =========================
def main():
    while True:
        print("\n===== CRYPTO TOOLKIT =====")
        print("1. AES")
        print("2. DES")
        print("3. 3DES")
        print("0. Exit")

        choice = safe_input("Choose: ")

        if choice == "1":
            crypto_menu("AES", ALGORITHMS["AES"])
        elif choice == "2":
            crypto_menu("DES", ALGORITHMS["DES"])
        elif choice == "3":
            crypto_menu("3DES", ALGORITHMS["3DES"])
        elif choice == "0":
            print("Bye!")
            return


if __name__ == "__main__":
    main()
