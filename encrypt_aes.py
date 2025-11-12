import argparse
import sys
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def encrypt_file(input_file, output_file):
    """
    Encrypt files using AES-GCM mode and output key information.
    """
    try:
        # --- 1. Reading plaintext data ---
        with open(input_file, 'rb') as f_in:
            plaintext = f_in.read()

        # --- 2. Generating Keys and Nonce ---
        key = get_random_bytes(32)
        
        nonce = get_random_bytes(16)

        # --- 3. Create AES-GCM cipher ---
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

        # --- 4. Encrypt and generate an authentication tag (Tag) ---
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)

        # --- 5. Write encrypted data to a file ---
        with open(output_file, 'wb') as f_out:
            f_out.write(ciphertext)

        # --- 6. Print key information (hexadecimal) ---
        print("--- 🔒 File encrypted successfully ---")
        print(f"Input file: {input_file}")
        print(f"Output file: {output_file}")
        print("\n**Please ensure the following information is securely stored, as it will be required for decryption：**\n")
        print(f"Key:    {key.hex()}")
        print(f"Nonce (IV):  {nonce.hex()}")
        print(f"Tag: {tag.hex()}")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' Not Found。", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred during the encryption process: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    # --- Command-line argument parsing ---
    parser = argparse.ArgumentParser(description="Encrypt files using AES-GCM.")
    parser.add_argument("input_file", help="Source file to be encrypted")
    parser.add_argument("-o", "--output_file", required=True, help="encrypted output file")
    
    args = parser.parse_args()
    
    encrypt_file(args.input_file, args.output_file)
