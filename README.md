# Homomorphic Encryption Implementation

A comprehensive Python implementation of homomorphic encryption schemes with basic operations on encrypted data.

## Overview

This project implements three types of homomorphic encryption:

1. **Paillier Cryptosystem** - Additively Homomorphic
2. **RSA Cryptosystem** - Multiplicatively Homomorphic  
3. **BFV (Brakerski-Fan-Vercauteren)** - Somewhat Homomorphic

## Project Structure

```
homomorphic_encryption/
├── paillier/
│   ├── paillier.py          # Paillier implementation
│   └── example_paillier.py  # Usage examples
├── rsa/
│   ├── rsa.py               # RSA implementation
│   └── example_rsa.py       # Usage examples
├── bfv/
│   ├── bfv.py               # BFV implementation
│   └── example_bfv.py       # Usage examples
└── README.md                # This file
```

## What is Homomorphic Encryption?

Homomorphic encryption allows computations to be performed on encrypted data without decryption. The result, when decrypted, is the same as if the operations were performed on plaintext.

### Key Properties:

- **Additive Homomorphic**: E(m₁) ⊕ E(m₂) = E(m₁ + m₂)
- **Multiplicative Homomorphic**: E(m₁) ⊗ E(m₂) = E(m₁ × m₂)
- **Scalar Operations**: E(m)^k = E(k × m) or E(m)^k = E(m^k)

## 1. Paillier Cryptosystem

### Characteristics:
- **Type**: Partially Homomorphic (Additive)
- **Operations**: Addition, Scalar Multiplication
- **Plaintext Range**: 0 to n-1
- **Security**: Based on Computational Composite Residuosity Assumption

### Features:
- Homomorphic Addition: E(m₁) × E(m₂) = E(m₁ + m₂)
- Scalar Multiplication: E(m)^k = E(k × m)
- Probabilistic encryption (randomized)
- Semantically secure

### Usage Example:

```python
from paillier.paillier import generate_keys

# Generate keys
public_key, private_key = generate_keys(key_size=512)

# Encrypt
c1 = public_key.encrypt(42)
c2 = public_key.encrypt(58)

# Add encrypted values
c_sum = public_key.add_encrypted(c1, c2)

# Decrypt result
result = private_key.decrypt(c_sum)
print(result)  # Output: 100

# Scalar multiplication
c_scaled = public_key.multiply_encrypted_by_plaintext(c1, 5)
result = private_key.decrypt(c_scaled)
print(result)  # Output: 210
```

### Running the Example:

```bash
cd paillier
python example_paillier.py
```

## 2. RSA Cryptosystem

### Characteristics:
- **Type**: Partially Homomorphic (Multiplicative)
- **Operations**: Multiplication, Exponentiation
- **Plaintext Range**: 0 to n-1
- **Security**: Based on RSA Problem (Integer Factorization)

### Features:
- Homomorphic Multiplication: E(m₁) × E(m₂) = E(m₁ × m₂)
- Exponentiation: E(m)^k = E(m^k)
- Deterministic encryption
- Limited by plaintext size constraints

### Usage Example:

```python
from rsa.rsa import generate_keys

# Generate keys
public_key, private_key = generate_keys(key_size=512)

# Encrypt
c1 = public_key.encrypt(3)
c2 = public_key.encrypt(5)

# Multiply encrypted values
c_product = public_key.multiply_encrypted(c1, c2)

# Decrypt result
result = private_key.decrypt(c_product)
print(result)  # Output: 15 (mod n)

# Power operation
c_power = public_key.power_encrypted(c1, 3)
result = private_key.decrypt(c_power)
print(result)  # Output: 27 (mod n)
```

### Running the Example:

```bash
cd rsa
python example_rsa.py
```

## 3. BFV (Somewhat Homomorphic)

### Characteristics:
- **Type**: Somewhat Homomorphic (Both Addition and Multiplication)
- **Operations**: Addition, Multiplication (limited depth)
- **Polynomial Ring**: Cyclotomic polynomial Z[x]/(x^n + 1)
- **Security**: Based on Ring Learning With Errors (RLWE)

### Features:
- Supports both addition and multiplication
- Noise management (noise grows with operations)
- SIMD-like batch operations on vectors
- Limited by noise budget (operation depth)

### Usage Example:

```python
from bfv.bfv import generate_keys, BFVParameters

# Generate keys
params = BFVParameters(degree=256, plaintext_modulus=65537)
public_key, private_key, relin_key = generate_keys(params)

# Encrypt vectors
m1 = [10, 20, 30, 40]
m2 = [2, 3, 1, 2]

c1 = public_key.encrypt(m1)
c2 = public_key.encrypt(m2)

# Add encrypted vectors
c_sum = public_key.add_encrypted(c1, c2)
result = private_key.decrypt(c_sum)
print(result)  # Output: [12, 23, 31, 42]

# Multiply encrypted vectors
c_product = public_key.multiply_encrypted(c1, c2)
result = private_key.decrypt(c_product)
print(result)  # Approximate product
```

### Running the Example:

```bash
cd bfv
python example_bfv.py
```

## Comparison Table

| Feature | Paillier | RSA | BFV |
|---------|----------|-----|-----|
| Addition | ✓ | ✗ | ✓ |
| Multiplication | ✗ | ✓ | ✓ |
| Multiple Operations | ✓ | ✗ | Limited |
| Deterministic | ✗ | ✓ | ✗ |
| Key Size | Large | Large | Very Large |
| Noise Growth | None | N/A | Yes |
| Batch Processing | ✗ | ✗ | ✓ |

## Use Cases

### Paillier:
- Secure voting systems
- Privacy-preserving aggregation
- Encrypted data analytics (sum operations)
- Encrypted auctions

### RSA:
- Digital signatures (deterministic)
- Encrypted bit operations
- Authorization systems
- Small encrypted computations

### BFV:
- Complex encrypted computations
- Machine learning on encrypted data
- DNA sequence analysis (encrypted)
- Outsourced computation
- Privacy-preserving databases

## Installation Requirements

Python 3.6+

No external dependencies required for basic implementations.

For production use, consider using established libraries:
- `phe` - Python Homomorphic Encryption library
- `TenSEAL` - Homomorphic Encryption library for machine learning
- `SEAL` - Simple Encrypted Arithmetic Library

## Important Notes

### Security Considerations:
1. **Key Size**: Use at least 2048 bits for production use
2. **Random Number Generation**: Uses Python's `random` module (suitable for examples only; use `secrets` or `os.urandom` for cryptography)
3. **Noise Management**: In BFV, monitor noise budget to prevent decryption failures
4. **Moduli Selection**: Prime selection can impact security and performance

### Performance:
- Paillier: Moderate speed, suitable for practice
- RSA: Fast encryption but limited operations
- BFV: Slower, requires large key sizes; optimized for batch operations

### Limitations:
- **Paillier**: Only addition (no general multiplication)
- **RSA**: Only multiplication (no addition)
- **BFV**: Limited operation depth due to noise growth

## Examples Running Instructions

### Run all examples:

```bash
# Paillier
python paillier/example_paillier.py

# RSA
python rsa/example_rsa.py

# BFV
python bfv/example_bfv.py
```

### Expected Output Snippets:

**Paillier**: Demonstrates addition of encrypted numbers and scalar multiplication

**RSA**: Shows multiplication on encrypted data and power operations

**BFV**: Illustrates both addition and multiplication with vector processing

## Further Reading

- **Paillier**: "Public-Key Cryptosystems Based on Composite Degree Residuosity Classes" (Paillier, 1999)
- **RSA**: "A Method for Obtaining Digital Signatures and Public-Key Cryptosystems" (Rivest et al., 1978)
- **BFV**: "Encrypted Control for Cyber-Physical Systems" (Brakerski et al., 2014)

## License

Educational and demonstration purposes.

## Disclaimer

These implementations are for educational purposes. Do not use in production without professional security review. Use established cryptographic libraries for real-world applications.
