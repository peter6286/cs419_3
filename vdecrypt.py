import sys

def decrypt(key,cipher,plain):
    if len(sys.argv) != 4:
        print("Wrong number of arguments")
        return

    # define files
    key_file = open(key, "r")
    cipher_file = open(cipher, "rb")
    plain_file = open(plain, "w+")
    if not (plain_file and cipher_file):
        print("Error with opening files")
        return

    # decrypt
    while True:
        c = cipher_file.read(1)
        print(c)
        if not c:
            break

        if key_file:
            k = key_file.read(1)
            if not k:
                key_file.seek(0)
                k = key_file.read(1)
        else:
            k = 0

        #p = int.from_bytes(c, byteorder=sys.byteorder) - int.from_bytes(k, byteorder=sys.byteorder) + 256
        p = ord(c) - ord(k) + 256
        p %= 256
        plain_file.write(chr(p))

    key_file.close()
    plain_file.close()
    key_file.close()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Wrong number of arguments")
    # define files
    key = sys.argv[1]
    cipher = sys.argv[2]
    plain = sys.argv[3]
    decrypt(key,cipher,plain)