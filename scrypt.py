import sys


# linear congruential generator
def lcg(x_n):
    return (1103515245 * x_n + 12345) % 256


# sbdm hash
def sbdm(str):
    max = 18446744073709551615 + 1
    hash, c = 0, 0
    for char in str:
        c = ord(char)
        hash = c + (hash << 6) + (hash << 16) - hash
        # print("{}: {}".format(c, hash))

    # have to mod by max because I am using python
    return hash % max


def scrypt(password,var1,var2):
    start_file = open(var1, "r")
    end_file = open(var2, "w+")

    if not start_file:
        print("File does not exist")
        return -1

    seed = sbdm(password)
    key = lcg(seed)

    while True:
        m = start_file.read(1)
        if not m:
            break
        # xor = int.from_bytes(m, byteorder=sys.byteorder) ^ key
        xor = ord(m) ^ key
        #end_file.write(int.to_bytes(xor, byteorder=sys.byteorder, length=1))
        end_file.write(chr(xor))
        key = lcg(key)

    start_file.close()
    end_file.close()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Wrong number of arguments")
    password = sys.argv[1]
    var1 = sys.argv[2]
    var2 =sys.argv[3]
    scrypt(password,var1,var2)

