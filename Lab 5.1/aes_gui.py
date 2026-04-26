from tkinter import *
from unittest import result

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import pyperclip

#====UTILS====
def pad(data):
    pad_len = 16 - (len(data) % 16)
    return data + chr(pad_len) * pad_len

def unpad(data):
    return data[:-ord(data[-1])]

def encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct = cipher.encrypt(pad(plaintext).encode())
    return base64.b64encode(cipher.iv + ct).decode()

def decrypt(ciphertext, key):
    data = base64.b64decode(ciphertext)
    iv = data[:16]
    ct = data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct).decode())

#====ACTIONS====
def generate_key():
    key = get_random_bytes(16)
    key_entry.delete(0, END)
    key_entry.insert(0, str(key))

def do_encrypt():
    try:
        key = eval(key_entry.get())
        result = encrypt(text_entry.get(), key)
        output.delete(0, END)
        output.insert(0, result)
    except:
        output.delete(0, END)
        output.insert(0, "❌ Error")

def do_decrypt():
    try:
        key = eval(key_entry.get())
        result = decrypt(text_entry.get(), key)
        output.delete(0, END)
        output.insert(0, result)
    except:
        output.delete(0, END)
        output.insert(0, "❌ Error")

def copy_result():
    pyperclip.copy(output.get())

#====GUI====
app = Tk()
app.title("AES Toolkit")

Label(app, text="Input").pack()
text_entry = Entry(app, width=50)
text_entry.pack()

Label(app, text="Key (b'...')").pack()
key_entry = Entry(app, width=50)
key_entry.pack()

Button(app, text="Generate Key", command=generate_key).pack()
Button(app, text="Encrypt", command=do_encrypt).pack()
Button(app, text="Decrypt", command=do_decrypt).pack()

Label(app, text="Output").pack()
output = Entry(app, width=50)
output.pack()

Button(app, text="Copy", command=copy_result).pack()

app.mainloop()
