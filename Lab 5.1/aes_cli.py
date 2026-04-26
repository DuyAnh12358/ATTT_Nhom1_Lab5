from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import pyperclip

BLOCK_SIZE = 16

#====UTILS====
def pad(data):
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + chr(pad_len) * pad_len

def unpad(data):
    return data[:-ord(data[-1])]

def generate_key():
    return get_random_bytes(16)

def validate_key(key):
    return len(key) in [16, 24, 32]

def save_key_to_file(key):
    with open("aes_key.txt", "wb") as f:
        f.write(key)
    print("💾 Key saved to aes_key.txt")

#====AES====
def encypt(plaintext,key):
    cipher = AES.new(key,AES.MODE_CBC)
    ct = cipher.encrypt(pad(plaintext).encode())
    return base64.b64encode(cipher.iv + ct).decode()

def decrypt(ciphertext,key):
    data = base64.b64decode(ciphertext)
    iv = data[:16]
    ct = data[16:]
    cipher = AES.new(key,AES.MODE_CBC,iv)
    return unpad(cipher.decrypt(ct).decode())

#====FLOWS====
def aes_encrypt_flow():
    plaintext = input("Enter the plaintext: ")

    choice = input("1. Input Key\n2. Generate Key\nChoose: ")

    if choice == "1":
        key_input = input("Enter key (16/24/32 chars): ")
        key = key_input.encode()

        if not validate_key(key):
            print("❌ Invalid key length!")
            return
    else:
        key = generate_key()
        print("🔑 Key:", key)

        save = input("Save key? (y/n): ")
        if save == "y":
            save_key_to_file(key)

    try:
        cipher = encrypt(plaintext,key)
        print("✅ Ciphertext:", cipher)

        if input("Copy? (y/n): ") == "y":
            pyperclip.copy(cipher)
            print("📋 Copied!")

    except Exception as e:
        print("❌ Error:", e)

def aes_decrypt_flow():
    cipher = input("Enter ciphertext: ")
    key_input = input("Enter key: ")

    try:
        key = eval(key_input) if key_input.startswith("b'") else key_input.encode()

        if not validate_key(key):
            print("❌ Invalid key!")
            return

        text = decrypt(cipher,key)
        print("✅ Plaintext:", text)

    except:
        print("❌ Decryption failed")

#====Main====
def main():
    while True:
        print("\n=== AES CLI TOOLKIT ===")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Generate Key")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            aes_encrypt_flow()
        elif choice == "2":
            aes_decrypt_flow()
        elif choice == "3":
            print("🔑", generate_key())
        elif choice == "0":
            break
        else:
            print("❌ Invalid!")

if __name__ == "__main__":
    main()