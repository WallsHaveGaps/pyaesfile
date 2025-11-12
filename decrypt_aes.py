#!/usr/bin/env python3
import argparse
import sys
from Crypto.Cipher import AES
from binascii import unhexlify, Error as BinasciiError

KEY_LENGTH = 32
NONCE_LENGTH = 16 
TAG_LENGTH = 16

def decrypt_file(input_file, output_file, key_hex, nonce_hex, tag_hex):
    """
    Decrypt the file using AES-GCM mode and verify the authentication tag.
    """
    try:
        # 1. Converting a hexadecimal string to raw byte data
        key = unhexlify(key_hex)
        nonce = unhexlify(nonce_hex)
        tag = unhexlify(tag_hex)
    except BinasciiError as e:
        print(f"🚨 Error: Hexadecimal parameter conversion failed. Please check if Key/IV/Tag is a valid hexadecimal string. ({e})", file=sys.stderr)
        sys.exit(1)

    # 2. Check length
    if len(key) != KEY_LENGTH:
        print(f"🚨 Error: Incorrect key length. Expected {KEY_LENGTH} bytes (64 hexadecimal characters), received {len(key)} bytes.", file=sys.stderr)
        sys.exit(1)
    if len(nonce) != NONCE_LENGTH:
        print(f"🚨 Error: Incorrect IV (Nonce) length. Expected {NONCE_LENGTH} bytes (32 hexadecimal characters), received {len(nonce)} bytes.", file=sys.stderr)
        sys.exit(1)
    if len(tag) != TAG_LENGTH:
        print(f"🚨 Error: Incorrect tag length. Expected {TAG_LENGTH} bytes (32 hexadecimal characters), received {len(tag)} bytes.", file=sys.stderr)
        sys.exit(1)

    # 3. Reading ciphertext data
    try:
        with open(input_file, 'rb') as f_in:
            ciphertext = f_in.read()
    except IOError as e:
        print(f"🚨 Error: Unable to read input file '{input_file}'. ({e})", file=sys.stderr)
        sys.exit(1)
    
    print(f"💡 Decrypting file '{input_file}'...")
    
    # 4. Creating an AES-GCM decryption object
    try:
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    except ValueError as e:
        print(f"🚨 Error: Failed to create AES object. Please check if the key/IV is correct. ({e})", file=sys.stderr)
        sys.exit(1)

    # 5. Decrypt and verify the Tag (this is key for GCM mode)
    try:
        # decrypt_and_verify verifies the integrity of the ciphertext with the provided tag while decrypting.
        # If verification fails, it throws ValueError: mac check failed
        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    except ValueError:
        print("\n\n!!! 💥 Authentication failed (MAC Check Failed) 💥 !!!", file=sys.stderr)
        print("🚨 Error: The ciphertext has been tampered with, or the Key/IV/Tag is incorrect.", file=sys.stderr)
        sys.exit(1)
    
    # 6. Writing decrypted data
    try:
        with open(output_file, 'wb') as f_out:
            f_out.write(decrypted_data)
        
        print(f"✅ Decryption and verification successful. File saved to '{output_file}'")
    except IOError as e:
        print(f"🚨 Error: Unable to write to the output file '{output_file}'. ({e})", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Decrypt the file using AES-GCM mode and verify the authentication tag.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Positional arguments: input file and output file
    parser.add_argument('input_file', 
                        help="Encrypted file to be decrypted (e.g., result.dat)")
    
    parser.add_argument('-o', '--output', 
                        required=True,
                        dest='output_file',
                        help="Save path for decrypted files (e.g., compressed.7z)")

    # Required parameters: Key, IV (Nonce), Tag
    parser.add_argument('--key', 
                        required=True,
                        help="AES key for decryption, hexadecimal string")
    
    parser.add_argument('--iv', 
                        required=True,
                        help="GCM Nonce (Initialization Vector), hexadecimal string")
    
    parser.add_argument('--tag', 
                        required=True,
                        help="GCM authentication tag (Tag), hexadecimal string")

    args = parser.parse_args()

    # Execute Decryption
    decrypt_file(args.input_file, args.output_file, args.key, args.iv, args.tag)

if __name__ == "__main__":
    main()
