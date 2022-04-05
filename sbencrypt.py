import sys

# Constants
BLOCK_SIZE = 16


def create_IV(seed):
    iv = []
    i = 0
    while i < BLOCK_SIZE:
        if i ==0:
            val = lcg(seed)
            iv.append(val)
            i+=1
        else:
            val = lcg(val)
            iv.append(val)
            i+=1
    return iv

def create_IV2(seed):
    iv = []
    val = lcg( seed )
    iv.append( val )
    for _ in range( BLOCK_SIZE - 1 ):
        val = lcg( val )
        iv.append( val )
        print(iv)
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
    rem = BLOCK_SIZE - len(m)
    temp_list = []
    if len(m) == 0:
        # return a whole block worth of padding
        #temp_list = []
        for i in range(BLOCK_SIZE):
            temp_list.append(BLOCK_SIZE)
            #print(temp_list)
        #m = bytes(temp_list)
    # return amount based on how many bytes left out of BLOCK_SIZE

    # add the curr values in m to a temp list that we are
    # then going to add the padding to
    # temp_list = []
    for val in m:
        temp_list.append(val)
        #print(temp_list)
    # tack on the remaining padding
    for idx in range(rem):
        temp_list.append(rem)
        #print(temp_list)

    return bytes(temp_list)


# byte shuffling
def bs(temp, key_stream):
    # convert to list to be able to swap
    temp = list(temp)

    for i in range(BLOCK_SIZE):
        first = key_stream[i] & (BLOCK_SIZE - 1)
        second = (key_stream[i] >> 4) & (BLOCK_SIZE - 1)
        # print('temp: {}'.format(temp))
        # print('keys: {}'.format(key_stream))
        # print('first: {}, second: {}'.format(first,second))
        temp[first], temp[second] = temp[second], temp[first]

    return bytes(temp)


def xor(plain, other):
    res = []
    for idx in range(len(plain)):
        res.append(plain[idx] ^ other[idx])
    return bytes(res)

def init(password,m):
    seed = sbdm(password)
    iv = create_IV(seed)
    temp = xor(m, iv)
    key_stream = create_IV(iv[-1])
    swap = bs(temp, key_stream)
    cipher = xor(swap, key_stream)
    return cipher,key_stream


def encrypt(password,var1,var2):

    # check the file
    start_file = open(var1, "rb")
    end_file = open(var2, "wb+")

    if not start_file:
        print("File does not exist")
        return -1
    run = True
    first = True
    cipher = []
    key_stream = []

    # read data block by block
    while run:
        # we want to read BLOCK_SIZE bytes
        m = start_file.read(BLOCK_SIZE)

        # check if at end
        if len(m) != BLOCK_SIZE:
            # pad
            m = pad(m)
            #print(m)
            run = False

        if first:
            first = False
            cipher,key_stream=init(password,m)
            end_file.write(cipher)
        else:
            temp = xor(m, cipher)
            key_stream = create_IV(key_stream[-1])
            swap = bs(temp, key_stream)
            cipher = xor(swap, key_stream)
            end_file.write(cipher)

    start_file.close()
    end_file.close()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Wrong number of arguments")
    password = sys.argv[1]
    var1 = sys.argv[2]
    var2 =sys.argv[3]
    encrypt(password,var1,var2)