import sys


#def make_key_file():
#    with open("key-01", "wb") as fh:
#        fh.write(b"\x01")
#        fh.close


def encrypt(key,cipher,plain):

    key_file = open(key, "rb")

    plain_file = open(cipher, "rb")
    cipher_file = open(plain, "wb+")
    if not (plain_file and cipher_file):
        print("Error with opening files")
        return


    # encrypt
    while True:
        p = plain_file.read(1)
        #pp = bytes(p,'utf-8')
        if not p:
            break

        if key_file:
            k = key_file.read(1)
            #kk = bytes(k,'utf-8')
            if not k:
                key_file.seek(0)
                k = key_file.read(1)
             #   kk = bytes(k, 'utf-8')
        else:
            k = 0

        c = int.from_bytes(p, byteorder=sys.byteorder) + int.from_bytes(k, byteorder=sys.byteorder)
        c %= 256
        cipher_file.write(int.to_bytes(c, byteorder=sys.byteorder, length=1))

    key_file.close()
    plain_file.close()
    key_file.close()


if __name__ == "__main__":
    key = sys.argv[1]
    cipher = sys.argv[2]
    plain = sys.argv[3]
    encrypt(key, cipher, plain)