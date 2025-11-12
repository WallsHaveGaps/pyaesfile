# 🛡️ Secure Cryptography Utility | AES-GCM File Encryption and Decryption Toolkit

![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)

---

### 📖 Project Overview

This project provides a robust command-line toolset for secure file encryption and decryption. At its core, it employs the industry-standard **AES-256-GCM (Galois/Counter Mode)** authenticated encryption algorithm.

In scenarios involving **cybersecurity** and **red team operations**, the tool serves as a foundational component for:
1. **Secure Storage**: During target environment operations or penetration testing phases, it securely encrypts and stores sensitive configurations, log files, or C2 (Command and Control) data.
2. **Data Integrity**: GCM mode provides authentication (Tag) to ensure that data remains untampered during encryption and transmission.

---

## ⚙️ Core Features and Tech Stack

* **Encryption Algorithm**: AES-256-GCM
* **Authentication Mechanism**: Automatically generates and verifies **Authentication Tag**.
* **Input/Output**: Command-line interface (CLI) handles file input, output, and key parameters.
* **Key Management**: Each encryption generates a random, secure **Key** and **Nonce**.

| FileName | Language | Description |
| :--- | :--- | :--- |
| `encrypt_aes.py` | Python 🐍 | File encryption tool outputs Key, Nonce, and Tag. |
| `decrypt_aes.py` | Python 🐍 | File decryption tool, requires Key, Nonce, and Tag as command line parameters. |

---

## 🚀 Quick Start (Python)

### 1. Environment Preparation

Ensure your environment has Python 3.8+ and the `pycryptodome` library installed.

```bash
python3 -m venv crypto

source crypto/bin/activate

pip install pycryptodome
````

### 2\. File Encryption (`encrypt_aes.py`)

Use this script to encrypt files. It will output the Key, IV (Nonce), and Tag—**ensure you securely store** this information.

**Command Format:**

```bash
python encrypt_aes.py <Source file path> -o <Output encrypted file path>
```

**Example:**

```bash
python encrypt_aes.py compressed.7z -o result.dat
```

**Example output:**

```
--- 🔒 File encrypted successfully ---
Input file: compressed.7z
Output file: result.dat

**Please ensure the following information is securely stored, as it will be required for decryption：**

Key:    3bd8190fe438136f464468d90716b02e2c75ecc16c9e05229e661da07d6a96d0
Nonce (IV):  a4f43ba00f6b44c1e635862a74c7c0d7
Tag: 50a7338fbf497346e5781d3d176d9abd
```

### 3\. File Decryption (`decrypt_aes.py`)

Decrypt the file using the **Key**, **IV (Nonce)**, and **Tag** obtained in the previous step.

**Command Format:**

```bash
python decrypt_aes.py <Encrypted file path> -o <Output file path> --key <KEY> --iv <NONCE> --tag <TAG>
```

**Example:**

```bash
python decrypt_aes.py result.dat \             
    -o compressed.7z \     
    --key 3bd8190fe438136f464468d90716b02e2c75ecc16c9e05229e661da07d6a96d0 \
    --iv a4f43ba00f6b44c1e635862a74c7c0d7 \
    --tag 50a7338fbf497346e5781d3d176d9abd
```

-----

## 🚨 Security and Key Management Instructions

Please note the following:

1.  **Authentication Failure**: If any of the Key/IV/Tag parameters used during decryption are incorrect, or if the contents of the `result.dat` file have been tampered with, the GCM authentication mechanism will raise a `ValueError: mac check failed` exception. Decryption will be aborted, and no output file will be generated. This is **GCM's data integrity guarantee**.
2.  **Production Environment**: This tool is intended for educational, testing, and red-team demonstration purposes. In real-world production systems, printing the Key and IV directly to the console or passing them via command-line arguments is **highly insecure**. Secure key management systems (KMS) or other confidential storage mechanisms should be used instead.
3.  **Key Length**: This tool uses AES-256 (32-byte Key, 16-byte Nonce/IV, 16-byte Tag), which complies with industry security standards.

-----

## 🤝 Contribution and Licensing

Welcome to submit bug reports and feature improvement suggestions.

This project is open-sourced under the MIT License. For details, please refer to the [LICENSE](https://github.com/WallsHaveGaps/pyaesfile/blob/main/LICENSE) file.
