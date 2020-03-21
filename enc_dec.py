from Crypto.Cipher import AES
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]
key = pad('my key')
iv = pad('my iv')
aes = AES.new(key, AES.MODE_CBC, iv)
data = pad('hello world ') # <- 16 bytes
encd = aes.encrypt(data)
print(encd)
