import sys
import os

# Constants
BLOCK_SIZE = 16


def create_IV(seed):
    iv = []
    val = lcg(seed)
    iv.append(val)
    for idx in range(BLOCK_SIZE - 1):
        val = lcg(val)
        iv.append(val)
    # print(iv)
    return iv


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


# padding
def pad(m):
    # check the last byte of
    last = m[-1]

    if not (last >= 0 and last <= BLOCK_SIZE):
        return m

    res = []
    for idx in range(BLOCK_SIZE - 1, -1, -1):
        # print('m: {}, bound: {}, idx: {}'.format(m[idx], BLOCK_SIZE - last, idx))
        if m[idx] != last or idx < BLOCK_SIZE - last:
            res.insert(0, m[idx])

    return bytes(res)


# byte shuffling
def bs(temp, key_stream):
    # convert to list to be able to swap
    temp = list(temp)

    for i in range(BLOCK_SIZE - 1, -1, -1):
        first = key_stream[i] & (BLOCK_SIZE - 1)
        second = (key_stream[i] >> 4) & (BLOCK_SIZE - 1)
        # print('{}: swapping ({},{}) = [ {} <> {} ]'.format(i,first,second,temp[first],temp[second]))
        temp[first], temp[second] = temp[second], temp[first]

    return bytes(temp)


def xor(plain, other):
    res = []
    for idx in range(len(plain)):
        res.append(plain[idx] ^ other[idx])
    return bytes(res)


def main():
    # check args
    if len(sys.argv) != 4:
        print("incorrect number of args")
        return -1

    password = sys.argv[1]

    # check the file
    start_file = open(sys.argv[2], "rb")
    end_file = open(sys.argv[3], "wb+")

    if not start_file:
        print("File does not exist")
        return -1

    # create the seed
    seed = sbdm(password)

    # create the iv
    iv = create_IV(seed)
    # print('iv: {}'.format(iv))

    run = True
    first = True
    cipher = []
    # calculate total num of bytes in file
    total_bytes = os.stat(sys.argv[2]).st_size
    bytes_read = 0
    prev_m = None

    # read data block by block
    while run:
        # we want to read BLOCK_SIZE bytes
        m = start_file.read(BLOCK_SIZE)
        bytes_read += len(m)
        # print('m: {}'.format(list(m)))
        # xor plain and iv / old cipher
        if first:
            # XOR
            # Gen new key_stream
            key_stream = create_IV(iv[-1])
            # print('keystream: {}'.format(key_stream))
            # xor plain and key stream
            temp = xor(m, key_stream)
        else:
            key_stream = create_IV(key_stream[-1])
            # print('keystream: {}'.format(key_stream))
            # XOR
            temp = xor(m, key_stream)

        # print('temp: {}'.format(list(temp)))
        # swap using key stream
        swap = bs(temp, key_stream)

        # print('swap: {}'.format(list(swap)))

        if first:
            first = False
            cipher = xor(swap, iv)
        else:
            cipher = xor(swap, prev_m)

        # print('cipher: {}'.format(list(cipher)))

        # check if at end
        if bytes_read == total_bytes:
            # print('after pad: {}'.format(list(cipher)))
            # pad
            cipher = pad(cipher)
            run = False

        # get prev text
        prev_m = m

        # print()

        # write cipher
        end_file.write(cipher)

    start_file.close()
    end_file.close()


if __name__ == "__main__":
    main()