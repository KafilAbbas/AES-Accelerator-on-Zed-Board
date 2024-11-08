from typing import List
import pandas as pd
import binascii
import zlib
import struct
# Implementation: S-Box
sbox = [
    # 0     1    2      3     4    5     6     7      8    9     A      B    C     D     E     F
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,  # 0
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,  # 1
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,  # 2
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,  # 3
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,  # 4
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,  # 5
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,  # 6
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,  # 7
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,  # 8
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,  # 9
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,  # A
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,  # B
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,  # C
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,  # D
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,  # E
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16   # F
]

rsbox = [
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
]

def get_sbox_value(num: int) -> int:
    return sbox[num]

def get_sbox_invert(num: int) -> int:
    return rsbox[num]

def rotate(word: List[int]) -> List[int]:
    return word[1:] + word[:1]

def get_rcon_value(num: int) -> int:
    rcon = [
        0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8,
        0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3,
        0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f,
        0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d,
        0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab,
        0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d,
        0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25,
        0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01,
        0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d,
        0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa,
        0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a,
        0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02,
        0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a,
        0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef,
        0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94,
        0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04,
        0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f,
        0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5,
        0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33,
        0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb
    ]

    return rcon[num]

def core(word: List[int], iteration: int) -> List[int]:
    word = rotate(word)
    word = [get_sbox_value(b) for b in word]
    word[0] ^= get_rcon_value(iteration)
    return word

def expand_key(key: List[int], size: int, expanded_key_size: int) -> List[int]:
    expanded_key = key[:]
    rcon_iteration = 1
    temp = [0] * 4

    while len(expanded_key) < expanded_key_size:
        temp = expanded_key[-4:]

        if len(expanded_key) % size == 0:
            temp = core(temp, rcon_iteration)
            rcon_iteration += 1

        if size == 32 and (len(expanded_key) % size) == 16:
            temp = [get_sbox_value(b) for b in temp]

        for i in range(4):
            expanded_key.append(expanded_key[-size] ^ temp[i])

    return expanded_key

def add_round_key(state: List[int], round_key: List[int]) -> List[int]:
    return [state[i] ^ round_key[i] for i in range(len(state))]

def sub_bytes(state: List[int]) -> List[int]:
    return [get_sbox_value(b) for b in state]

def shift_rows(state: List[int]) -> List[int]:
    state[1], state[5], state[9], state[13] = state[5], state[9], state[13], state[1]
    state[2], state[6], state[10], state[14] = state[10], state[14], state[2], state[6]
    state[3], state[7], state[11], state[15] = state[15], state[3], state[7], state[11]
    return state

def galois_multiplication(a: int, b: int) -> int:
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        hi_bit_set = a & 0x80
        a <<= 1
        if hi_bit_set:
            a ^= 0x1b
        b >>= 1
    return p % 256

def mix_columns(state: List[int]) -> List[int]:
    for i in range(4):
        t = state[i*4:(i+1)*4]
        state[i*4+0] = galois_multiplication(t[0], 2) ^ galois_multiplication(t[3], 1) ^ \
                       galois_multiplication(t[2], 1) ^ galois_multiplication(t[1], 3)
        state[i*4+1] = galois_multiplication(t[1], 2) ^ galois_multiplication(t[0], 1) ^ \
                       galois_multiplication(t[3], 1) ^ galois_multiplication(t[2], 3)
        state[i*4+2] = galois_multiplication(t[2], 2) ^ galois_multiplication(t[1], 1) ^ \
                       galois_multiplication(t[0], 1) ^ galois_multiplication(t[3], 3)
        state[i*4+3] = galois_multiplication(t[3], 2) ^ galois_multiplication(t[2], 1) ^ \
                       galois_multiplication(t[1], 1) ^ galois_multiplication(t[0], 3)
    return state

def aes_round(state: List[int], round_key: List[int]) -> List[int]:
    state = sub_bytes(state)
    state = shift_rows(state)
    state = mix_columns(state)
    state = add_round_key(state, round_key)
    return state

def aes_main(state: List[int], expanded_key: List[int], nbr_rounds: int) -> List[int]:
    state = add_round_key(state, expanded_key[:16])
    for i in range(1, nbr_rounds):
        state = aes_round(state, expanded_key[i*16:(i+1)*16])
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, expanded_key[nbr_rounds*16:(nbr_rounds+1)*16])
    return state

def aes_encrypt(input_bytes: List[int], key: List[int], size: int) -> List[int]:
    if size not in (16, 24, 32):
        raise ValueError("Invalid key size")

    nbr_rounds = {16: 10, 24: 12, 32: 14}[size]
    expanded_key_size = 16 * (nbr_rounds + 1)
    expanded_key = expand_key(key, size, expanded_key_size)
    state = input_bytes[:]
    state = aes_main(state, expanded_key, nbr_rounds)
    return state


def inv_sub_bytes(state: List[int]) -> List[int]:
    return [get_sbox_invert(b) for b in state]

def inv_shift_rows(state: List[int]) -> List[int]:
    state[1], state[5], state[9], state[13] = state[13], state[1], state[5], state[9]
    state[2], state[6], state[10], state[14] = state[10], state[14], state[2], state[6]
    state[3], state[7], state[11], state[15] = state[7], state[11], state[15], state[3]
    return state

def inv_mix_columns(state: List[int]) -> List[int]:
    for i in range(4):
        t = state[i*4:(i+1)*4]
        state[i*4+0] = galois_multiplication(t[0], 14) ^ galois_multiplication(t[3], 9) ^ \
                       galois_multiplication(t[2], 13) ^ galois_multiplication(t[1], 11)
        state[i*4+1] = galois_multiplication(t[1], 14) ^ galois_multiplication(t[0], 9) ^ \
                       galois_multiplication(t[3], 13) ^ galois_multiplication(t[2], 11)
        state[i*4+2] = galois_multiplication(t[2], 14) ^ galois_multiplication(t[1], 9) ^ \
                       galois_multiplication(t[0], 13) ^ galois_multiplication(t[3], 11)
        state[i*4+3] = galois_multiplication(t[3], 14) ^ galois_multiplication(t[2], 9) ^ \
                       galois_multiplication(t[1], 13) ^ galois_multiplication(t[0], 11)
    return state

def aes_inv_round(state: List[int], round_key: List[int]) -> List[int]:
    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    state = add_round_key(state, round_key)
    state = inv_mix_columns(state)
    return state



def aes_inv_main(state: List[int], expanded_key: List[int], nbr_rounds: int) -> List[int]:
    state = add_round_key(state, expanded_key[nbr_rounds * 16:(nbr_rounds + 1) * 16])
    for round in range(nbr_rounds - 1, 0, -1):
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        state = add_round_key(state, expanded_key[round * 16:(round + 1) * 16])
        state = inv_mix_columns(state)
    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    state = add_round_key(state, expanded_key[0:16])
    return state



def aes_decrypt(input_bytes: List[int], key: List[int], size: int) -> List[int]:
    if size not in (16, 24, 32):
        raise ValueError("Invalid key size")

    nbr_rounds = {16: 10, 24: 12, 32: 14}[size]
    expanded_key_size = 16 * (nbr_rounds + 1)
    expanded_key = expand_key(key, size, expanded_key_size)
    state = input_bytes[:]
    state = aes_inv_main(state, expanded_key, nbr_rounds)
    return state

# def main():
#     key_hex = '000102030405060708090a0b0c0d0e0f'
#     input_hex = '8299C7A9FA118E94814CB2B65A0B5D2C'

#     # Convert hex key and input to byte arrays
#     key = [int(key_hex[i:i+2], 16) for i in range(0, len(key_hex), 2)]
#     input_bytes = [int(input_hex[i:i+2], 16) for i in range(0, len(input_hex), 2)]

#     # Encrypt
#     cipher = aes_encrypt(input_bytes, key, 16)

#     # Decrypt
#     plain = aes_decrypt(cipher, key, 16)

#     # Print cipher and plain text in hexadecimal format
#     print("Cipher (HEX):", ''.join(format(x, '02x') for x in cipher))
#     print("Plain Text (HEX):", ''.join(format(x, '02x') for x in plain))



# def main2():
#     key_hex = '000102030405060708090a0b0c0d0e0f'
#     cipher_hex = '9bc13b3791cfc7c22fcf8162a1984c19'

#     # Convert hex key and ciphertext to byte arrays
#     key = [int(key_hex[i:i+2], 16) for i in range(0, len(key_hex), 2)]
#     cipher_bytes = [int(cipher_hex[i:i+2], 16) for i in range(0, len(cipher_hex), 2)]

#     # Decrypt
#     plain = aes_decrypt(cipher_bytes, key, 16)

#     # Print decrypted plaintext in hexadecimal format
#     print("Decrypted Plaintext (HEX):", ''.join(format(x, '02x') for x in plain))


# main()

# AES decryption function placeholder (You need to implement or import this)
# def aes_decrypt(cipher_bytes, key, block_size):
#     # Replace this with the actual decryption function code
#     raise NotImplementedError("Implement or import the AES decryption function here.")

def hex_to_bytes(hex_string):
    """Convert a hex string to bytes."""
    return binascii.unhexlify(hex_string)



def decrypt_and_concat_from_csv(csv_file_path):
    # AES key in hexadecimal format
    key_hex = '000102030405060708090a0b0c0d0e0f'
    key = [int(key_hex[i:i+2], 16) for i in range(0, len(key_hex), 2)]

    # Read the CSV file and sort by 'Sample in Buffer' column in ascending order
    df = pd.read_csv(csv_file_path)
    df_sorted = df.sort_values(by='Sample in Buffer')

    decrypted_chunks = []  # Store decrypted 640-bit chunks

    for hex_data in df_sorted['ila_data[639:0]']:
        decrypted_640_bit_chunk = ''

        for i in range(0, len(hex_data), 32):
            chunk_hex = hex_data[i:i+32]
            cipher_bytes = [int(chunk_hex[j:j+2], 16) for j in range(0, len(chunk_hex), 2)]
            plain = aes_decrypt(cipher_bytes, key,16)
            decrypted_640_bit_chunk += ''.join(format(x, '02x') for x in plain)

        decrypted_chunks.append(decrypted_640_bit_chunk)

    return decrypted_chunks


def add_decrypt_data(decrypted_chunks):
    # Join all hexadecimal strings into a single string
    hex_data = ''.join(decrypted_chunks)
    # Convert the hexadecimal string to bytes
    byte_data = binascii.unhexlify(hex_data)
    return byte_data



def save_decrypted_chunks_to_file(final_data, output_file_path):
    with open(output_file_path, 'wb') as output_file:
        output_file.write(final_data)
        trimmed_data_hex = final_data.hex()
        # print(trimmed_data_hex)
    


def decompress_data(data):
    """Extract original length from the data, and decompress."""
    original_length = struct.unpack('>I', data[:4])[0]  # Unpack the first 4 bytes for length
    compressed_data = data[4:]  # All the rest is compressed data
    # print("this is me ",data)
    decompressed_data = zlib.decompress(compressed_data)
    return decompressed_data[:original_length]  # Slice it to the original length


# Example usage
# csv_file_path = 'fourth_ila_readings.csv'
# output_file_path = 'output_file.txt'


# decrypted_chunks = decrypt_and_concat_from_csv(csv_file_path)

# data = add_decrypt_data(decrypted_chunks)
# final_data = decompress_data(data)
# print(final_data)
# save_decrypted_chunks_to_file(final_data,output_file_path)

def decrypt_and_save(csv_file_path,output_file_path):

    decrypted_chunks = decrypt_and_concat_from_csv(csv_file_path)
    data = add_decrypt_data(decrypted_chunks)
    final_data = decompress_data(data)
    # print(final_data)
    save_decrypted_chunks_to_file(final_data,output_file_path)
    print(" Data decrypted sucessful and saved in files as output_file.txt")
    return 1






















