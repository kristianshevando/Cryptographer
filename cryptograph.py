import os, random

from Crypto.Cipher import AES
from Crypto.Hash import SHA256

def encrypt(key, fileName):
    chunkSize = 64*1024
    outputFile = "(encrypted)" + fileName
    fileSize = str(os.path.getsize(fileName)).zfill(16)
    IV = ''

    for i in range(16):
        IV += chr(random.randint(0, 0xFF))

    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(fileName, 'rb') as inputFile:
        with open(outputFile, 'wb') as outputFile:
            outputFile.write(fileSize)
            outputFile.write(IV)

            while True:
                chunk = inputFile.read(chunkSize)

                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - (len(chunk) % 16))

                outputFile.write(encryptor.encrypt(chunk))

def decrypt(key, fileName):
    chunkSize = 64*1024
    outputFile = fileName[11:]

    with open(fileName, 'rb') as inputFile:
        fileSize = long(inputFile.read(16))
        IV = inputFile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(outputFile, 'wb') as outputFile:
            while True:
                chunk = inputFile.read(chunkSize)

                if len(chunk) == 0:
                    break

                outputFile.write(decryptor.decrypt(chunk))
            outputFile.truncate(fileSize)

def getKey(password):
    hasher = SHA256.new(password)
    return hasher.digest()

def mainFunction():
    choice = raw_input("Encrypt - E/e\n"
                        "Decrypt - D/d\n"
                        ">>> ")

    if choice == 'E' or choice == 'e':
        fileName = raw_input("File to encrypt: ")
        password = raw_input("Key: ")
        encrypt(getKey(password), fileName)
        print "Done."
    elif choice == 'D' or choice == 'd':
        fileName = raw_input("File to decrypt: ")
        password = raw_input("Key: ")
        decrypt(getKey(password), fileName)
        print "Done."
    else:
        print "No option selected, closing..."

if __name__ == '__main__':
    mainFunction()
